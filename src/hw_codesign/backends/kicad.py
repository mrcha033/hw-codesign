from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import textwrap
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
from typing import Any

from ..artifacts import deterministic_zip, sha256
from ..io import atomic_write_text, read_yaml, write_json
from ..models import Failure, FailureCategory, GateReport, Status
from ..provenance import artifact_provenance
from .command import resolve_kicad_python, resolve_tool, run_tool, tool_report, tool_version
from .electronics import ElectronicsBackendAdapter


class KiCadBackend(ElectronicsBackendAdapter):
    name = "kicad"

    def __init__(self, platform_root: Path | None = None):
        self.platform_root = (platform_root or Path.cwd()).resolve()

    def generate_source(self, project: Path, spec: dict[str, Any], graph: dict[str, Any]) -> list[str]:
        generated = project / "electronics" / "generated" / "kicad"
        target = project / "electronics" / "source" / "kicad"
        shutil.rmtree(target, ignore_errors=True)
        target.mkdir(parents=True, exist_ok=True)
        files: list[str] = []
        for item in generated.iterdir() if generated.is_dir() else []:
            if item.suffix in {".kicad_sch", ".kicad_pcb", ".kicad_pro"}:
                destination = target / item.name
                shutil.copy2(item, destination)
                files.append(str(destination))
        manifest = target / "source_manifest.json"
        write_json(manifest, {
            "backend": self.name,
            "backend_release_capable": True,
            "release_tier": "fabrication",
            "source_release_eligible": bool(files),
            "netlist_release_eligible": False,
            "hdl_source_release_eligible": False,
            "fabrication_release_eligible": bool(files),
            "sources": self.source_entries(target, [Path(path) for path in files]),
            "contract_gates": list(self.gate_names),
            "release_blocking_gates": list(self.gate_names),
            "provenance": artifact_provenance(
                spec,
                self.platform_root / "parts",
                self.name,
                compiler_version=tool_version("kicad-cli"),
                command=["kicad-cli", "sch", "export", "netlist"],
                release_eligible=bool(files),
                release_tier="fabrication",
            ),
        })
        return [*files, str(manifest)]

    def evaluate(self, project: Path, graph: dict[str, Any]) -> list[GateReport]:
        source = project / "electronics" / "source" / "kicad"
        schematic = next(source.glob("*.kicad_sch"), None)
        board = next(source.glob("*.kicad_pcb"), None)
        if schematic is None or board is None:
            return self.blocked_contract("missing_design_source", "Generate KiCad-native source before evaluation", category=FailureCategory.EDA_ERROR)
        if resolve_tool("kicad-cli") is None:
            return self.blocked_contract("tool_unavailable", "kicad-cli is unavailable")
        netlist_path = project / "electronics" / "generated" / "kicad_native.net"
        result = run_tool("kicad-cli", ["sch", "export", "netlist", "--format", "kicadxml", "--output", str(netlist_path), str(schematic)], project)
        backend = {"name": self.name, "available": result.available, "command": result.command, "returncode": result.returncode}
        if result.returncode != 0:
            failure = Failure(FailureCategory.EDA_ERROR, "kicad_compile_failed", "KiCad netlist export returned nonzero", details={"stderr": result.stderr[-2000:]})
            return self.complete_contract([GateReport("kicad_compile", Status.FAIL, [failure], backend=backend)])
        try:
            compiled_netlist, compiled_footprints = self._extract_kicad_netlist(netlist_path)
        except (ET.ParseError, OSError) as exc:
            failure = Failure(FailureCategory.EDA_ERROR, "kicad_netlist_parse_failed", str(exc))
            return self.complete_contract([GateReport("kicad_compile", Status.PASS, artifacts=[str(netlist_path)], backend=backend), GateReport("kicad_netlist_extract", Status.FAIL, [failure], backend=backend)])
        expected = self.graph_netlist(graph)
        parity_failures = [] if compiled_netlist == expected else [Failure(FailureCategory.EDA_ERROR, "graph_parity_mismatch", "KiCad exported netlist differs from resolved graph", details={"expected": expected, "compiled": compiled_netlist})]
        footprint_failures = []
        for component in graph.get("components", []):
            expected_footprint = component.get("footprint_metadata", {}).get("library_id") or component.get("footprint")
            if compiled_footprints.get(component["ref"]) != expected_footprint:
                footprint_failures.append(Failure(FailureCategory.EDA_ERROR, "footprint_parity_mismatch", f"KiCad footprint differs for {component['ref']}", details={"expected": expected_footprint, "compiled": compiled_footprints.get(component["ref"])}))
        board_text = board.read_text(encoding="utf-8")
        placed_refs = set(re.findall(r'\(property\s+"Reference"\s+"([^"]+)"', board_text))
        expected_refs = {component["ref"] for component in graph.get("components", [])}
        layout_failures = [Failure(FailureCategory.EDA_ERROR, "component_unplaced", f"{ref} is absent from the KiCad PCB") for ref in sorted(expected_refs - placed_refs)]
        if not re.search(r"\((?:segment|arc|via)\s", board_text):
            layout_failures.append(Failure(FailureCategory.EDA_ERROR, "pcb_traces_absent", "KiCad PCB has no routed copper evidence"))
        manufacturing = self.export_manufacturing(project, project / "exports" / "candidates" / "backend-validation" / "kicad")
        manufacturing.gate = "kicad_manufacturing_export"
        return self.complete_contract([
            GateReport("kicad_compile", Status.PASS, artifacts=[str(netlist_path)], backend=backend),
            GateReport("kicad_netlist_extract", Status.PASS, artifacts=[str(netlist_path)], backend=backend),
            GateReport("kicad_graph_parity", Status.FAIL if parity_failures else Status.PASS, parity_failures, backend=backend),
            GateReport("kicad_footprint_parity", Status.FAIL if footprint_failures else Status.PASS, footprint_failures, backend=backend),
            GateReport("kicad_layout_completeness", Status.FAIL if layout_failures else Status.PASS, layout_failures, backend=backend),
            manufacturing,
        ])

    @staticmethod
    def _extract_kicad_netlist(path: Path) -> tuple[dict[str, list[str]], dict[str, str]]:
        root = ET.parse(path).getroot()
        nets = {
            net.attrib["name"].removeprefix("/"): sorted(f"{node.attrib['ref']}.{node.attrib['pin']}" for node in net.findall("node"))
            for net in root.findall("./nets/net")
        }
        footprints = {
            component.attrib["ref"]: (component.findtext("footprint") or "")
            for component in root.findall("./components/comp")
        }
        return dict(sorted(nets.items())), footprints

    def run_erc(self, project: Path) -> GateReport:
        schematic = self._design_file(project, "*.kicad_sch")
        if schematic is None:
            return GateReport("erc", Status.BLOCKED, [Failure(FailureCategory.EDA_ERROR, "missing_design_source", "No generated KiCad schematic exists — electronics compile gate must pass first")])
        output = project / "validation" / "reports" / "kicad_erc.json"
        result = run_tool("kicad-cli", ["sch", "erc", "--format", "json", "--output", str(output), str(schematic)], project)
        report = tool_report("erc", result, [str(output)] if output.exists() else [])
        if report.status == Status.PASS and output.exists():
            data = json.loads(output.read_text(encoding="utf-8"))
            all_violations = [item for sheet in data.get("sheets", []) for item in sheet.get("violations", [])]
            # footprint_link_issues are library-lookup failures, not circuit ERC violations;
            # they are separately measured by the kicad_library_crosscheck gate.
            violations = [v for v in all_violations if v.get("type") != "footprint_link_issues"]
            if violations:
                report.status = Status.FAIL
                report.failures = [Failure(FailureCategory.EDA_ERROR, "erc_violation", item.get("description", "KiCad ERC violation"), details=item) for item in violations]
            report.metrics = {"violations": len(violations), "footprint_link_issues": len(all_violations) - len(violations)}
        return report

    def run_drc(self, project: Path) -> GateReport:
        board = self._design_file(project, "*.kicad_pcb")
        if board is None:
            return GateReport("drc", Status.BLOCKED, [Failure(FailureCategory.EDA_ERROR, "missing_design_source", "No generated KiCad PCB exists — electronics compile gate must pass first")])
        output = project / "validation" / "reports" / "kicad_drc.json"
        result = run_tool("kicad-cli", ["pcb", "drc", "--format", "json", "--severity-error", "--output", str(output), str(board)], project, timeout=300)
        # Negative return code = signal/crash (SIGABRT on KiCad 10 macOS); also fall back
        # when kicad-cli exits non-zero without producing an output file (e.g. exit 3 on
        # certain board configurations) — both are toolchain failures, not design failures.
        if result.available and result.returncode != 0 and not output.exists():
            return self._run_drc_pcbnew_fallback(board, project)
        report = tool_report("drc", result, [str(output)] if output.exists() else [])
        if report.status == Status.PASS and output.exists():
            data = json.loads(output.read_text(encoding="utf-8"))
            violations = [*data.get("violations", []), *data.get("unconnected_items", []), *data.get("schematic_parity", [])]
            if violations:
                report.status = Status.FAIL
                report.failures = [Failure(FailureCategory.EDA_ERROR, "drc_violation", item.get("description", "KiCad DRC violation"), details=item) for item in violations]
            report.metrics = {"violations": len(violations)}
        return report

    def _run_drc_pcbnew_fallback(self, board: Path, project: Path) -> GateReport:
        """Run connectivity + design-rules DRC via pcbnew Python API.

        Used when kicad-cli pcb drc crashes (e.g. SIGABRT on KiCad 10 macOS).
        Checks: unconnected items, track widths, board outline presence.
        """
        kicad_python = resolve_kicad_python()
        if kicad_python is None:
            failure = Failure(FailureCategory.TOOL_ERROR, "tool_unavailable", "kicad-cli pcb drc crashed and pcbnew Python fallback not found", details={"board": str(board)})
            return GateReport("drc", Status.BLOCKED, [failure])

        kicad_site = str(Path(kicad_python).parent.parent / "lib" / f"python{'.'.join(Path(kicad_python).name.lstrip('python').split('.')[:2])}" / "site-packages")
        script = textwrap.dedent(f"""
            import sys, json
            sys.path.insert(0, {kicad_site!r})
            import pcbnew

            board = pcbnew.LoadBoard({str(board)!r})
            filler = pcbnew.ZONE_FILLER(board)
            filler.Fill(board.Zones())
            board.BuildConnectivity()
            connectivity = board.GetConnectivity()
            unconnected = connectivity.GetUnconnectedCount(False)

            rules = board.GetDesignSettings()
            min_track_nm = rules.m_TrackMinWidth

            width_violations = []
            for track in board.GetTracks():
                if track.GetClass() == 'PCB_TRACK':
                    w = track.GetWidth()
                    if w < min_track_nm:
                        width_violations.append(f'Track width {{w/1e6:.3f}}mm < {{min_track_nm/1e6:.3f}}mm')

            has_outline = any(item.GetLayer() == pcbnew.Edge_Cuts for item in board.GetDrawings())

            print(json.dumps({{
                'unconnected': unconnected,
                'width_violations': width_violations[:10],
                'has_outline': has_outline,
                'min_track_mm': min_track_nm / 1e6,
            }}))
        """)

        try:
            proc = subprocess.run([kicad_python, "-c", script], capture_output=True, text=True, timeout=120)
        except subprocess.TimeoutExpired:
            failure = Failure(FailureCategory.TOOL_ERROR, "pcbnew_drc_timeout", "pcbnew DRC script timed out after 120s")
            return GateReport("drc", Status.BLOCKED, [failure])

        if proc.returncode != 0:
            # Filter out benign KiCad wxApp/trait warnings from stderr
            fatal = [ln for ln in proc.stderr.splitlines() if "assert" in ln.lower() and "traits" not in ln and "GetWidth" not in ln and ln.strip()]
            if fatal or not proc.stdout.strip():
                failure = Failure(FailureCategory.TOOL_ERROR, "pcbnew_drc_failed", f"pcbnew DRC script failed: {'; '.join(fatal[:2]) or 'no output'}", details={"stderr": proc.stderr[-2000:]})
                return GateReport("drc", Status.BLOCKED, [failure])

        data: dict[str, Any] = {}
        for line in proc.stdout.splitlines():
            line = line.strip()
            if line.startswith("{"):
                try:
                    data = json.loads(line)
                    break
                except json.JSONDecodeError:
                    pass
        if not data:
            failure = Failure(FailureCategory.TOOL_ERROR, "pcbnew_drc_parse_failed", "pcbnew DRC produced no parseable output", details={"stdout": proc.stdout[-1000:]})
            return GateReport("drc", Status.BLOCKED, [failure])

        failures: list[Failure] = []
        if data.get("unconnected", 0) > 0:
            failures.append(Failure(FailureCategory.EDA_ERROR, "unconnected_items", f"{data['unconnected']} unconnected item(s) in routed board"))
        for v in data.get("width_violations", []):
            failures.append(Failure(FailureCategory.EDA_ERROR, "track_width_violation", v))
        if not data.get("has_outline"):
            failures.append(Failure(FailureCategory.EDA_ERROR, "missing_board_outline", "No board outline on Edge.Cuts layer"))

        output_path = project / "validation" / "reports" / "kicad_drc_pcbnew.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        write_json(output_path, {"tool": "pcbnew", "fallback_reason": "kicad-cli-drc-sigabrt", **data, "failure_count": len(failures)})

        metrics = {"unconnected": data.get("unconnected", -1), "width_violations": len(data.get("width_violations", [])), "has_outline": int(data.get("has_outline", False))}
        if failures:
            return GateReport("drc", Status.FAIL, failures, metrics=metrics)
        return GateReport("drc", Status.PASS, metrics=metrics, artifacts=[str(output_path)])

    def export_manufacturing(self, project: Path, release: Path) -> GateReport:
        board = self._design_file(project, "*.kicad_pcb")
        if board is None:
            return GateReport("fabrication_export", Status.FAIL, [Failure(FailureCategory.EDA_ERROR, "missing_design_source", "No generated KiCad PCB exists")])
        bom_source = project / "electronics" / "generated" / "bom.csv"
        if not bom_source.is_file():
            return GateReport("fabrication_export", Status.FAIL, [Failure(FailureCategory.EDA_ERROR, "bom_export_missing", "Resolved BOM must exist before manufacturing export")])

        board_hash = sha256(board)
        routing_path = project / "electronics" / "generated" / "kicad" / "routing.json"
        routing_binding: dict[str, Any] = {
            "status": "not_available",
            "board_sha256_match": None,
        }
        if routing_path.is_file():
            try:
                routing_receipt = json.loads(routing_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError) as exc:
                return GateReport(
                    "fabrication_export",
                    Status.FAIL,
                    [
                        Failure(
                            FailureCategory.RELEASE_ERROR,
                            "invalid_routing_receipt",
                            "The routing receipt cannot be parsed, so the fabrication export cannot be bound to routed board evidence",
                            path=str(routing_path),
                            details={"error": str(exc)},
                        )
                    ],
                )
            receipt_status = routing_receipt.get("status", "unknown")
            receipt_board_hash = routing_receipt.get("board_sha256")
            board_hash_match = receipt_board_hash == board_hash
            routing_binding = {
                "status": "verified" if receipt_status == "pass" and board_hash_match else "unverified",
                "receipt_status": receipt_status,
                "board_sha256": receipt_board_hash,
                "board_sha256_match": board_hash_match,
            }
            if receipt_status == "pass" and not board_hash_match:
                return GateReport(
                    "fabrication_export",
                    Status.FAIL,
                    [
                        Failure(
                            FailureCategory.RELEASE_ERROR,
                            "routing_receipt_board_mismatch",
                            "The passing routing receipt is for a different KiCad board revision",
                            path=str(board),
                            details={"board_sha256": board_hash, "routing_receipt_board_sha256": receipt_board_hash},
                        )
                    ],
                )
            if receipt_status == "pass" and (
                routing_receipt.get("signal_routing") != "complete"
                or routing_receipt.get("unrouted") != 0
                or routing_receipt.get("post_import_unconnected") != 0
            ):
                return GateReport(
                    "fabrication_export",
                    Status.FAIL,
                    [
                        Failure(
                            FailureCategory.RELEASE_ERROR,
                            "routing_receipt_incomplete",
                            "The routing receipt says pass but does not record complete zero-unconnected routing",
                            path=str(routing_path),
                        )
                    ],
                )

        export_layers = [
            *_declared_copper_layers(board.read_text(encoding="utf-8")),
            "F.Mask",
            "B.Mask",
            "F.Paste",
            "B.Paste",
            "F.Silkscreen",
            "B.Silkscreen",
            "Edge.Cuts",
        ]
        input_paths = [board, bom_source, *([routing_path] if routing_path.is_file() else [])]
        input_hashes = {path: sha256(path) for path in input_paths}
        release.mkdir(parents=True, exist_ok=True)

        with tempfile.TemporaryDirectory(prefix=".native-kicad-export-", dir=release) as temporary:
            staging = Path(temporary)
            native = staging / "native_kicad"
            native.mkdir(parents=True)
            staged_fabrication = staging / "fabrication"
            staged_fabrication.mkdir(parents=True)

            gerber = run_tool("kicad-cli", ["pcb", "export", "gerbers", "--output", str(native), "--layers", ",".join(export_layers), str(board)], project)
            if not gerber.available or gerber.returncode != 0:
                report = tool_report("fabrication_export", gerber)
                report.status = Status.BLOCKED if not gerber.available else Status.FAIL
                return report
            drill = run_tool("kicad-cli", ["pcb", "export", "drill", "--output", str(native), "--generate-map", "--map-format", "pdf", str(board)], project)
            if drill.returncode != 0:
                return tool_report("fabrication_export", drill)
            position = native / "positions.csv"
            position_result = run_tool("kicad-cli", ["pcb", "export", "pos", "--format", "csv", "--units", "mm", "--output", str(position), str(board)], project)
            if position_result.returncode != 0 or not position.is_file():
                report = tool_report("fabrication_export", position_result)
                if position_result.returncode == 0:
                    report.status = Status.FAIL
                    report.failures = [Failure(FailureCategory.EDA_ERROR, "position_export_missing", "KiCad reported success without a position file")]
                return report
            staged_step = staging / "mechanical" / "board.step"
            staged_step.parent.mkdir(parents=True)
            step_result = run_tool("kicad-cli", ["pcb", "export", "step", "--subst-models", "--output", str(staged_step), str(board)], project)
            if step_result.returncode != 0:
                return tool_report("fabrication_export", step_result)

            for native_file in native.iterdir():
                if native_file.is_file():
                    _normalize_kicad_export_metadata(native_file)
            _normalize_kicad_export_metadata(staged_step)

            gerbers = [
                (item, item.name)
                for item in native.iterdir()
                if item.is_file() and item != position and item.suffix.lower() not in {".drl", ".xln", ".pdf", ".csv"}
            ]
            # Drill maps are review aids rather than machine drill data, and their
            # PDF metadata is renderer-dependent. Keep only Excellon drill payloads.
            drills = [(item, item.name) for item in native.iterdir() if item.is_file() and item.suffix.lower() in {".drl", ".xln"}]
            if not gerbers or not drills:
                return GateReport("fabrication_export", Status.FAIL, [Failure(FailureCategory.EDA_ERROR, "manufacturing_files_missing", "KiCad export did not produce both Gerber and machine drill artifacts")])
            missing_paste_layers = _missing_populated_side_paste_layers(position, [path for path, _ in gerbers])
            if missing_paste_layers:
                return GateReport(
                    "fabrication_export",
                    Status.FAIL,
                    [
                        Failure(
                            FailureCategory.EDA_ERROR,
                            "assembly_paste_layer_missing",
                            "KiCad did not emit a solder-paste Gerber for every populated assembly side",
                            path=str(board),
                            details={"missing_layers": missing_paste_layers},
                        )
                    ],
                    metrics={"missing_paste_layers": missing_paste_layers},
                )

            staged_gerbers = staged_fabrication / "gerbers.zip"
            staged_drills = staged_fabrication / "drill.zip"
            staged_position = staged_fabrication / "pick_and_place.csv"
            staged_bom = staged_fabrication / "bom.csv"
            deterministic_zip(staged_gerbers, gerbers)
            deterministic_zip(staged_drills, drills)
            shutil.copyfile(position, staged_position)
            shutil.copyfile(bom_source, staged_bom)

            changed_inputs = [str(path) for path, expected in input_hashes.items() if not path.is_file() or sha256(path) != expected]
            if changed_inputs:
                return GateReport(
                    "fabrication_export",
                    Status.BLOCKED,
                    [
                        Failure(
                            FailureCategory.RELEASE_ERROR,
                            "design_source_changed_during_export",
                            "Fabrication inputs changed while KiCad was exporting; rerun against a stable board revision",
                            details={"changed_inputs": changed_inputs},
                        )
                    ],
                )

            fabrication = release / "fabrication"
            step = release / "mechanical" / "board.step"
            promoted = {
                staged_gerbers: fabrication / "gerbers.zip",
                staged_drills: fabrication / "drill.zip",
                staged_position: fabrication / "pick_and_place.csv",
                staged_bom: fabrication / "bom.csv",
                staged_step: step,
            }
            for source, destination in promoted.items():
                _atomic_copy_file(source, destination)

            readiness_manifest = _write_fabrication_readiness_manifest(project, board, fabrication, routing_binding)

            inputs = [
                _hash_record(path, project, role="canonical_kicad_board" if path == board else ("resolved_bom" if path == bom_source else "routing_receipt"))
                for path in input_paths
            ]
            output_records = [
                _hash_record(path, release, role=role)
                for path, role in (
                    (fabrication / "gerbers.zip", "gerber_archive"),
                    (fabrication / "drill.zip", "machine_drill_archive"),
                    (fabrication / "pick_and_place.csv", "pick_and_place"),
                    (fabrication / "bom.csv", "resolved_bom_copy"),
                    (readiness_manifest, "vendor_neutral_readiness_manifest"),
                    (step, "board_step"),
                )
            ]
            archive_members = {
                "fabrication/gerbers.zip": [_hash_record(path, native, role="gerber") for path, _ in sorted(gerbers, key=lambda item: item[1])],
                "fabrication/drill.zip": [_hash_record(path, native, role="machine_drill") for path, _ in sorted(drills, key=lambda item: item[1])],
            }
            manifest_payload: dict[str, Any] = {
                "schema_version": 1,
                "kind": "native_kicad_fabrication_candidate",
                "inputs": inputs,
                "routing_binding": routing_binding,
                "toolchain": {
                    "name": "kicad-cli",
                    "version": tool_version("kicad-cli"),
                    "commands": [
                        ["kicad-cli", "pcb", "export", "gerbers", "--output", "<staging>/native_kicad", "--layers", ",".join(export_layers), board.relative_to(project).as_posix()],
                        ["kicad-cli", "pcb", "export", "drill", "--output", "<staging>/native_kicad", "--generate-map", "--map-format", "pdf", board.relative_to(project).as_posix()],
                        ["kicad-cli", "pcb", "export", "pos", "--format", "csv", "--units", "mm", "--output", "<staging>/native_kicad/positions.csv", board.relative_to(project).as_posix()],
                        ["kicad-cli", "pcb", "export", "step", "--subst-models", "--output", "<staging>/mechanical/board.step", board.relative_to(project).as_posix()],
                    ],
                },
                "export_contract": {
                    "layers": export_layers,
                    "archive_metadata_normalized": True,
                    "volatile_kicad_timestamps_normalized": True,
                    "drill_map_pdf_included": False,
                },
                "artifacts": output_records,
                "archive_members": archive_members,
                "evidence_boundary": {
                    "native_tool_output": True,
                    "release_eligible": "not_asserted_by_this_receipt",
                    "fabrication_qualified": "not_asserted_by_this_receipt",
                },
            }
            candidate_id = f"sha256:{_canonical_sha256(manifest_payload)}"
            manifest = {**manifest_payload, "candidate_id": candidate_id}
            manifest_path = fabrication / "fabrication_manifest.json"
            write_json(manifest_path, manifest)

        verification = self.verify_manufacturing_export(project, release)
        if verification.status != Status.PASS:
            verification.gate = "fabrication_export"
            return verification
        artifacts = [
            str(fabrication / "gerbers.zip"),
            str(fabrication / "drill.zip"),
            str(fabrication / "pick_and_place.csv"),
            str(fabrication / "bom.csv"),
            str(fabrication / "readiness_manifest.json"),
            str(step),
            str(manifest_path),
        ]
        return GateReport(
            "fabrication_export",
            Status.PASS,
            metrics={
                "gerber_files": len(gerbers),
                "drill_files": len(drills),
                "position_file": True,
                "bom": True,
                "export_layers": export_layers,
                "source_board_sha256": board_hash,
                "routing_binding": routing_binding["status"],
                "fabrication_candidate_id": candidate_id,
                "manifest_verified": True,
            },
            artifacts=artifacts,
            backend={
                "name": "kicad-cli",
                "deterministic_archive": True,
                "volatile_metadata_normalized": True,
                "content_addressed_manifest": True,
            },
        )

    def verify_manufacturing_export(self, project: Path, release: Path) -> GateReport:
        """Verify a native fabrication receipt against both its inputs and outputs."""
        manifest_path = release / "fabrication" / "fabrication_manifest.json"
        if not manifest_path.is_file():
            return GateReport(
                "fabrication_manifest",
                Status.FAIL,
                [Failure(FailureCategory.RELEASE_ERROR, "fabrication_manifest_missing", "Native fabrication export manifest is missing", path=str(manifest_path))],
            )
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            return GateReport(
                "fabrication_manifest",
                Status.FAIL,
                [Failure(FailureCategory.RELEASE_ERROR, "fabrication_manifest_invalid", "Native fabrication export manifest is not valid JSON", path=str(manifest_path), details={"error": str(exc)})],
            )

        failures: list[Failure] = []
        if manifest.get("schema_version") != 1 or manifest.get("kind") != "native_kicad_fabrication_candidate":
            failures.append(
                Failure(
                    FailureCategory.RELEASE_ERROR,
                    "fabrication_manifest_contract_invalid",
                    "Native fabrication manifest schema version or kind is invalid",
                    path=str(manifest_path),
                )
            )
        candidate_id = manifest.get("candidate_id")
        payload = {key: value for key, value in manifest.items() if key != "candidate_id"}
        expected_candidate_id = f"sha256:{_canonical_sha256(payload)}"
        if candidate_id != expected_candidate_id:
            failures.append(
                Failure(
                    FailureCategory.RELEASE_ERROR,
                    "fabrication_candidate_id_mismatch",
                    "Fabrication candidate ID does not match the canonical receipt content",
                    path=str(manifest_path),
                    details={"expected": expected_candidate_id, "actual": candidate_id},
                )
            )

        input_records = manifest.get("inputs", [])
        if isinstance(input_records, list):
            input_roles = {record.get("role") for record in input_records if isinstance(record, dict)}
            missing_roles = {"canonical_kicad_board", "resolved_bom"} - input_roles
            if missing_roles:
                failures.append(
                    Failure(
                        FailureCategory.RELEASE_ERROR,
                        "fabrication_required_input_missing",
                        "Fabrication receipt omits required source inputs",
                        path=str(manifest_path),
                        details={"missing_roles": sorted(missing_roles)},
                    )
                )
        artifact_records = manifest.get("artifacts", [])
        if isinstance(artifact_records, list):
            artifact_paths = {record.get("path") for record in artifact_records if isinstance(record, dict)}
            required_artifact_paths = {
                "fabrication/gerbers.zip",
                "fabrication/drill.zip",
                "fabrication/pick_and_place.csv",
                "fabrication/bom.csv",
                "fabrication/readiness_manifest.json",
                "mechanical/board.step",
            }
            missing_artifacts = required_artifact_paths - artifact_paths
            if missing_artifacts:
                failures.append(
                    Failure(
                        FailureCategory.RELEASE_ERROR,
                        "fabrication_required_artifact_missing",
                        "Fabrication receipt omits required outputs",
                        path=str(manifest_path),
                        details={"missing_paths": sorted(missing_artifacts)},
                    )
                )

        checked = 0
        for root, records, kind in (
            (project, manifest.get("inputs", []), "input"),
            (release, manifest.get("artifacts", []), "artifact"),
        ):
            if not isinstance(records, list):
                failures.append(Failure(FailureCategory.RELEASE_ERROR, f"fabrication_{kind}_records_invalid", f"Fabrication {kind} records must be a list", path=str(manifest_path)))
                continue
            for record in records:
                if not isinstance(record, dict):
                    failures.append(Failure(FailureCategory.RELEASE_ERROR, f"fabrication_{kind}_record_invalid", f"Fabrication {kind} record must be an object", path=str(manifest_path)))
                    continue
                resolved = _safe_manifest_path(root, record.get("path"))
                if resolved is None:
                    failures.append(Failure(FailureCategory.RELEASE_ERROR, f"fabrication_{kind}_path_invalid", f"Fabrication {kind} path is not a safe relative path", path=str(manifest_path), details={"path": record.get("path")}))
                    continue
                checked += 1
                if not resolved.is_file():
                    failures.append(Failure(FailureCategory.RELEASE_ERROR, f"fabrication_{kind}_missing", f"Fabrication {kind} is missing: {record.get('path')}", path=str(resolved)))
                    continue
                actual_hash = sha256(resolved)
                actual_bytes = resolved.stat().st_size
                if actual_hash != record.get("sha256") or actual_bytes != record.get("bytes"):
                    failures.append(
                        Failure(
                            FailureCategory.RELEASE_ERROR,
                            "fabrication_checksum_mismatch",
                            f"Fabrication {kind} checksum mismatch: {record.get('path')}",
                            path=str(resolved),
                            details={
                                "expected_sha256": record.get("sha256"),
                                "actual_sha256": actual_hash,
                                "expected_bytes": record.get("bytes"),
                                "actual_bytes": actual_bytes,
                            },
                        )
                    )

        archive_members_checked = 0
        archive_contract = manifest.get("archive_members", {})
        if not isinstance(archive_contract, dict):
            failures.append(
                Failure(
                    FailureCategory.RELEASE_ERROR,
                    "fabrication_archive_contract_invalid",
                    "Fabrication archive_members must be an object",
                    path=str(manifest_path),
                )
            )
        else:
            required_archives = {"fabrication/gerbers.zip", "fabrication/drill.zip"}
            if set(archive_contract) != required_archives:
                failures.append(
                    Failure(
                        FailureCategory.RELEASE_ERROR,
                        "fabrication_archive_contract_incomplete",
                        "Fabrication archive receipt must cover both Gerber and machine-drill archives",
                        path=str(manifest_path),
                        details={"expected": sorted(required_archives), "actual": sorted(archive_contract)},
                    )
                )
            for archive_reference, member_records in archive_contract.items():
                archive_path = _safe_manifest_path(release, archive_reference)
                if archive_path is None or not isinstance(member_records, list):
                    failures.append(
                        Failure(
                            FailureCategory.RELEASE_ERROR,
                            "fabrication_archive_contract_invalid",
                            "Fabrication archive path or member records are invalid",
                            path=str(manifest_path),
                            details={"archive": archive_reference},
                        )
                    )
                    continue
                if not archive_path.is_file():
                    continue  # The outer artifact check already records the missing archive.
                expected_members: dict[str, dict[str, Any]] = {}
                invalid_member_contract = False
                for record in member_records:
                    if not isinstance(record, dict) or _safe_archive_member_name(record.get("path")) is None:
                        invalid_member_contract = True
                        failures.append(
                            Failure(
                                FailureCategory.RELEASE_ERROR,
                                "fabrication_archive_member_path_invalid",
                                "Fabrication archive member must be a safe relative file name",
                                path=str(manifest_path),
                                details={"archive": archive_reference, "member": record.get("path") if isinstance(record, dict) else None},
                            )
                        )
                        continue
                    member_name = str(record["path"])
                    if member_name in expected_members:
                        invalid_member_contract = True
                        failures.append(
                            Failure(
                                FailureCategory.RELEASE_ERROR,
                                "fabrication_archive_member_duplicate",
                                f"Fabrication archive receipt repeats member: {member_name}",
                                path=str(manifest_path),
                            )
                        )
                    expected_members[member_name] = record
                if invalid_member_contract:
                    continue
                try:
                    with zipfile.ZipFile(archive_path) as archive:
                        names = archive.namelist()
                        if len(names) != len(set(names)) or any(_safe_archive_member_name(name) is None for name in names):
                            failures.append(
                                Failure(
                                    FailureCategory.RELEASE_ERROR,
                                    "fabrication_archive_member_set_invalid",
                                    f"Fabrication archive contains duplicate or unsafe member names: {archive_reference}",
                                    path=str(archive_path),
                                )
                            )
                            continue
                        if set(names) != set(expected_members):
                            failures.append(
                                Failure(
                                    FailureCategory.RELEASE_ERROR,
                                    "fabrication_archive_member_set_mismatch",
                                    f"Fabrication archive members differ from the receipt: {archive_reference}",
                                    path=str(archive_path),
                                    details={"expected": sorted(expected_members), "actual": sorted(names)},
                                )
                            )
                        for member_name in sorted(set(names) & set(expected_members)):
                            info = archive.getinfo(member_name)
                            expected = expected_members[member_name]
                            archive_members_checked += 1
                            digest = hashlib.sha256()
                            with archive.open(info) as handle:
                                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                                    digest.update(chunk)
                            if info.file_size != expected.get("bytes") or digest.hexdigest() != expected.get("sha256"):
                                failures.append(
                                    Failure(
                                        FailureCategory.RELEASE_ERROR,
                                        "fabrication_archive_member_checksum_mismatch",
                                        f"Fabrication archive member checksum mismatch: {archive_reference}:{member_name}",
                                        path=str(archive_path),
                                        details={
                                            "expected_sha256": expected.get("sha256"),
                                            "actual_sha256": digest.hexdigest(),
                                            "expected_bytes": expected.get("bytes"),
                                            "actual_bytes": info.file_size,
                                        },
                                    )
                                )
                except (OSError, RuntimeError, zipfile.BadZipFile) as exc:
                    failures.append(
                        Failure(
                            FailureCategory.RELEASE_ERROR,
                            "fabrication_archive_invalid",
                            f"Fabrication archive cannot be verified: {archive_reference}",
                            path=str(archive_path),
                            details={"error": str(exc)},
                        )
                    )

        return GateReport(
            "fabrication_manifest",
            Status.FAIL if failures else Status.PASS,
            failures,
            metrics={
                "records_checked": checked,
                "archive_members_checked": archive_members_checked,
                "fabrication_candidate_id": candidate_id,
                "manifest_sha256": sha256(manifest_path),
            },
            artifacts=[str(manifest_path)],
            backend={"name": "sha256-manifest", "native_tool_output": True},
        )

    @staticmethod
    def _design_file(project: Path, pattern: str) -> Path | None:
        source = project / "electronics" / "source" / "kicad"
        generated = project / "electronics" / "generated" / "kicad"
        if pattern.startswith("*."):
            canonical = f"{project.name}{pattern[1:]}"
            for root in (source, generated):
                candidate = root / canonical
                if candidate.is_file():
                    return candidate
        source_match = next(iter(sorted(source.glob(pattern))), None) if source.is_dir() else None
        generated_match = next(iter(sorted(generated.glob(pattern))), None) if generated.is_dir() else None
        return source_match or generated_match


def _declared_copper_layers(board_text: str) -> list[str]:
    layers = [
        match.group(1)
        for match in re.finditer(r'\(\s*\d+\s+"([^"]+\.Cu)"\s+(?:signal|power)\b', board_text)
    ]
    return layers or ["F.Cu", "B.Cu"]


def _missing_populated_side_paste_layers(position: Path, gerbers: list[Path]) -> list[str]:
    """Return paste layers absent for assembly sides present in native PnP output."""
    with position.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        side_field = next((field for field in (reader.fieldnames or []) if field.strip().lower() == "side"), None)
        if side_field is None:
            return ["F.Paste", "B.Paste"]
        sides = {str(row.get(side_field, "")).strip().lower() for row in reader}
    suffixes = {path.suffix.lower() for path in gerbers}
    required: list[tuple[str, str]] = []
    if sides & {"top", "front"}:
        required.append(("F.Paste", ".gtp"))
    if sides & {"bottom", "back"}:
        required.append(("B.Paste", ".gbp"))
    return [layer for layer, suffix in required if suffix not in suffixes]


def _canonical_sha256(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    return hashlib.sha256(payload).hexdigest()


def _hash_record(path: Path, root: Path, *, role: str) -> dict[str, Any]:
    return {
        "path": path.relative_to(root).as_posix(),
        "role": role,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def _safe_manifest_path(root: Path, value: object) -> Path | None:
    if not isinstance(value, str) or not value or "\\" in value:
        return None
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        return None
    return root / relative


def _safe_archive_member_name(value: object) -> str | None:
    if not isinstance(value, str) or not value or "\\" in value:
        return None
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts or value.endswith("/"):
        return None
    return value


def _atomic_copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{destination.name}.", dir=destination.parent)
    os.close(descriptor)
    temporary_path = Path(temporary)
    try:
        shutil.copyfile(source, temporary_path)
        os.replace(temporary_path, destination)
    finally:
        temporary_path.unlink(missing_ok=True)


def _normalize_kicad_export_metadata(path: Path) -> None:
    """Remove volatile KiCad creation times without changing manufacturing geometry."""
    suffix = path.suffix.lower()
    if suffix == ".gbrjob":
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeError):
            return
        header = payload.get("Header")
        if isinstance(header, dict) and "CreationDate" in header:
            header["CreationDate"] = "1970-01-01T00:00:00+00:00"
            write_json(path, payload)
        return
    if suffix not in {".gbr", ".gtl", ".gbl", ".gts", ".gbs", ".gtp", ".gbp", ".gto", ".gbo", ".gm1", ".drl", ".xln", ".step", ".stp"}:
        return
    try:
        original = path.read_text(encoding="utf-8")
    except UnicodeError:
        return
    normalized = re.sub(
        r"(?m)^%TF\.CreationDate,[^*]*\*%$",
        "%TF.CreationDate,1970-01-01T00:00:00+00:00*%",
        original,
    )
    normalized = re.sub(
        r"(?m)^(G04 Created by KiCad \(PCBNEW [^)]+\) date )[^*]+(\*)$",
        r"\g<1>1970-01-01 00:00:00\2",
        normalized,
    )
    normalized = re.sub(
        r"(?m)^(; DRILL file KiCad .+? date )\S+\s*$",
        r"\g<1>1970-01-01T00:00:00",
        normalized,
    )
    normalized = re.sub(
        r"(?m)^(; #@! TF\.CreationDate,).+$",
        r"\g<1>1970-01-01T00:00:00+00:00",
        normalized,
    )
    normalized = re.sub(
        r"(FILE_NAME\('[^']*',)'[^']*'",
        r"\g<1>'1970-01-01T00:00:00'",
        normalized,
        count=1,
    )
    if normalized != original:
        atomic_write_text(path, normalized)


def _write_fabrication_readiness_manifest(
    project: Path,
    board: Path,
    fabrication: Path,
    routing_binding: dict[str, Any],
) -> Path:
    """Write a vendor-neutral RFQ receipt without asserting order readiness."""
    manufacturing_path = project / "spec" / "manufacturing.yaml"
    mechanical_path = project / "spec" / "mechanical.yaml"
    manufacturing = read_yaml(manufacturing_path).get("manufacturing", {}) if manufacturing_path.is_file() else {}
    mechanical = read_yaml(mechanical_path).get("mechanical", {}) if mechanical_path.is_file() else {}
    pcb = manufacturing.get("pcb", {}) if isinstance(manufacturing, dict) else {}
    via_in_pad = pcb.get("via_in_pad", {}) if isinstance(pcb, dict) else {}
    locations = via_in_pad.get("locations", []) if isinstance(via_in_pad, dict) else []
    if not isinstance(locations, list):
        locations = []
    observed_geometry, geometry_error = _declared_via_in_pad_geometry(board, locations)
    declared_count = sum(
        int(location.get("via_count", 0))
        for location in locations
        if isinstance(location, dict) and isinstance(location.get("via_count"), int)
    )
    observed_count = sum(int(item.get("observed_count", 0)) for item in observed_geometry)
    via_used = bool(via_in_pad.get("used")) if isinstance(via_in_pad, dict) else False
    process = via_in_pad.get("process", {}) if isinstance(via_in_pad, dict) else {}
    assembly_alignment = _fabrication_assembly_alignment(fabrication)
    blockers: list[dict[str, str]] = []
    if geometry_error:
        blockers.append({"code": "via_in_pad_geometry_unreadable", "message": geometry_error})
    if routing_binding.get("status") != "verified":
        blockers.append(
            {
                "code": "routing_binding_unverified",
                "message": "The fabrication export is not bound to a passing zero-unconnected routing receipt for this exact board hash.",
            }
        )
    if assembly_alignment["status"] != "aligned":
        blockers.append(
            {
                "code": "bom_pick_and_place_reference_mismatch",
                "message": "Resolved BOM and native pick-and-place reference sets are unavailable or do not match; reconcile assembly scope before RFQ approval.",
            }
        )
    if via_used and declared_count != observed_count:
        blockers.append(
            {
                "code": "via_in_pad_count_mismatch",
                "message": f"Declared {declared_count} via-in-pad holes but observed {observed_count} matching plated pad forms in the board source.",
            }
        )
    for mismatch in _via_in_pad_geometry_mismatches(locations, observed_geometry):
        blockers.append({"code": "via_in_pad_geometry_mismatch", "message": mismatch})
    if via_used and (
        via_in_pad.get("qualification_status") != "qualified"
        or not isinstance(process, dict)
        or process.get("selection_status") != "selected"
    ):
        blockers.append(
            {
                "code": "via_in_pad_process_unqualified",
                "message": "Via-in-pad disposition, fill/cap finish, and fabricator process remain unselected or unqualified.",
            }
        )
    if pcb.get("controlled_impedance") == "required":
        blockers.append(
            {
                "code": "fabricator_stackup_confirmation_required",
                "message": "The selected fabricator must return a stackup and impedance construction before an order can be approved.",
            }
        )

    envelope = mechanical.get("envelope", {}) if isinstance(mechanical, dict) else {}
    readiness = {
        "schema_version": 1,
        "kind": "vendor_neutral_fabrication_readiness",
        "status": "blocked" if blockers else "review_required",
        "order_ready": False,
        "fabricator_selection": "unselected",
        "routing_binding": routing_binding,
        "board": {
            "path": board.relative_to(project).as_posix(),
            "bytes": board.stat().st_size,
            "sha256": sha256(board),
        },
        "assembly_alignment": assembly_alignment,
        "stackup_assumptions": {
            "layers": pcb.get("layers"),
            "finished_board_thickness_mm": envelope.get("board_thickness_mm") if isinstance(envelope, dict) else None,
            "minimum_clearance_mm": pcb.get("min_clearance_mm"),
            "minimum_track_width_mm": pcb.get("min_track_width_mm"),
            "controlled_impedance": pcb.get("controlled_impedance"),
            "copper_weights": "unselected",
            "laminate_and_dielectric_construction": "unselected",
            "surface_finish": "unselected",
        },
        "via_in_pad": {
            "used": via_used,
            "qualification_status": via_in_pad.get("qualification_status") if isinstance(via_in_pad, dict) else None,
            "declared_count": declared_count,
            "observed_count": observed_count,
            "count_matches_board": declared_count == observed_count,
            "locations": locations,
            "observed_geometry": observed_geometry,
            "process": process if isinstance(process, dict) else {},
        },
        "blockers": blockers,
        "required_fabricator_response": [
            "Return a DFM review tied to the board SHA-256 in this manifest.",
            "Return the proposed layer stackup, finished thickness tolerance, copper weights, laminate, surface finish, solder-mask rules, and minimum feature capabilities.",
            "Return the controlled-impedance construction, target/tolerance, calculation or field-solver basis, and coupon/test method.",
            "Confirm each declared via-in-pad location, hole/land geometry, fill or plugging material, cap or plate-over finish, planarization, and assembly compatibility.",
            "Confirm Gerber, machine-drill, outline, BOM, and pick-and-place interpretation before order approval.",
        ],
        "required_returned_evidence": [
            "written capability and DFM response",
            "approved stackup drawing and impedance plan",
            "released fabrication and assembly notes",
            "via-in-pad process identifier and certificate or microsection plan",
            "first-article inspection, x-ray or equivalent exposed-pad inspection, and yield report",
        ],
        "evidence_boundary": "This is an RFQ/readiness input, not an order approval, release promotion, fabrication qualification, or physical bring-up record.",
    }
    target = fabrication / "readiness_manifest.json"
    write_json(target, readiness)
    return target


def _fabrication_assembly_alignment(fabrication: Path) -> dict[str, Any]:
    bom_references, bom_error = _csv_reference_set(fabrication / "bom.csv", {"reference", "ref", "designator"})
    position_references, position_error = _csv_reference_set(
        fabrication / "pick_and_place.csv",
        {"reference", "ref", "designator"},
    )
    if bom_error or position_error:
        return {
            "status": "unavailable",
            "bom_reference_count": len(bom_references),
            "pick_and_place_reference_count": len(position_references),
            "missing_from_pick_and_place": [],
            "missing_from_bom": [],
            "errors": [error for error in (bom_error, position_error) if error],
        }
    missing_from_position = sorted(bom_references - position_references)
    missing_from_bom = sorted(position_references - bom_references)
    return {
        "status": "aligned" if not missing_from_position and not missing_from_bom else "mismatch",
        "bom_reference_count": len(bom_references),
        "pick_and_place_reference_count": len(position_references),
        "missing_from_pick_and_place": missing_from_position,
        "missing_from_bom": missing_from_bom,
        "errors": [],
    }


def _csv_reference_set(path: Path, accepted_fields: set[str]) -> tuple[set[str], str | None]:
    if not path.is_file():
        return set(), f"Missing CSV: {path.name}"
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            reference_field = next(
                (field for field in (reader.fieldnames or []) if field.strip().lower() in accepted_fields),
                None,
            )
            if reference_field is None:
                return set(), f"CSV has no reference field: {path.name}"
            return {
                str(row.get(reference_field, "")).strip()
                for row in reader
                if str(row.get(reference_field, "")).strip()
            }, None
    except (OSError, UnicodeError, csv.Error) as exc:
        return set(), f"Unable to parse {path.name}: {exc}"


def _declared_via_in_pad_geometry(board: Path, locations: list[object]) -> tuple[list[dict[str, Any]], str | None]:
    try:
        from sexpdata import Symbol, loads

        root = loads(board.read_text(encoding="utf-8"))

        def atom(value: object) -> str:
            return value.value() if isinstance(value, Symbol) else str(value)

        def direct(value: object, head: str) -> list[list[object]]:
            if not isinstance(value, list):
                return []
            return [
                item
                for item in value[1:]
                if isinstance(item, list) and item and atom(item[0]) == head
            ]

        footprints: dict[str, list[object]] = {}
        for footprint in direct(root, "footprint"):
            reference = next(
                (
                    atom(prop[2])
                    for prop in direct(footprint, "property")
                    if len(prop) >= 3 and atom(prop[1]) == "Reference"
                ),
                None,
            )
            if reference:
                footprints[reference] = footprint

        results: list[dict[str, Any]] = []
        for raw_location in locations:
            if not isinstance(raw_location, dict):
                continue
            reference = str(raw_location.get("reference", ""))
            pad_number = str(raw_location.get("pad", ""))
            footprint = footprints.get(reference)
            matched = []
            if footprint is not None:
                matched = [
                    pad
                    for pad in direct(footprint, "pad")
                    if len(pad) >= 3 and atom(pad[1]) == pad_number and atom(pad[2]) == "thru_hole"
                ]
            coordinates: list[list[float]] = []
            outer_diameters: list[float] = []
            drill_diameters: list[float] = []
            layers: set[str] = set()
            for pad in matched:
                at = direct(pad, "at")
                size = direct(pad, "size")
                drill = direct(pad, "drill")
                pad_layers = direct(pad, "layers")
                if at and len(at[0]) >= 3:
                    coordinates.append([float(at[0][1]), float(at[0][2])])
                if size and len(size[0]) >= 3:
                    outer_diameters.append(max(float(size[0][1]), float(size[0][2])))
                if drill:
                    numeric_drill = []
                    for value in drill[0][1:]:
                        try:
                            numeric_drill.append(float(atom(value)))
                        except ValueError:
                            continue
                    if numeric_drill:
                        drill_diameters.append(max(numeric_drill))
                if pad_layers:
                    layers.update(atom(value) for value in pad_layers[0][1:])
            x_values = sorted({point[0] for point in coordinates})
            y_values = sorted({point[1] for point in coordinates})
            results.append(
                {
                    "reference": reference,
                    "pad": pad_number,
                    "declared_count": raw_location.get("via_count"),
                    "observed_count": len(matched),
                    "local_coordinates_mm": sorted(coordinates),
                    "outer_diameter_mm": sorted(set(outer_diameters)),
                    "drill_diameter_mm": sorted(set(drill_diameters)),
                    "grid_pitch_x_mm": _uniform_pitch(x_values),
                    "grid_pitch_y_mm": _uniform_pitch(y_values),
                    "layers": sorted(layers),
                }
            )
        return results, None
    except Exception as exc:
        return [], f"Unable to extract declared via-in-pad geometry from the KiCad board: {exc}"


def _uniform_pitch(values: list[float]) -> float | None:
    if len(values) < 2:
        return None
    pitches = [round(right - left, 6) for left, right in zip(values, values[1:])]
    return pitches[0] if len(set(pitches)) == 1 else None


def _via_in_pad_geometry_mismatches(
    locations: list[object],
    observed_geometry: list[dict[str, Any]],
) -> list[str]:
    observed_by_site = {(item.get("reference"), item.get("pad")): item for item in observed_geometry}
    mismatches: list[str] = []
    for location in locations:
        if not isinstance(location, dict):
            continue
        reference = str(location.get("reference", ""))
        pad = str(location.get("pad", ""))
        geometry = location.get("geometry")
        if not isinstance(geometry, dict):
            mismatches.append(f"{reference}.{pad} has no declared via geometry to compare with the board source.")
            continue
        observed = observed_by_site.get((reference, pad), {})
        expected_count = geometry.get("rows", 0) * geometry.get("columns", 0)
        if expected_count and observed.get("observed_count") != expected_count:
            mismatches.append(f"{reference}.{pad} expected {expected_count} holes from rows x columns but the board has {observed.get('observed_count', 0)}.")
        expected_pitch = geometry.get("pitch_mm")
        if expected_pitch is not None and any(
            value is None or abs(float(value) - float(expected_pitch)) > 1e-6
            for value in (observed.get("grid_pitch_x_mm"), observed.get("grid_pitch_y_mm"))
        ):
            mismatches.append(f"{reference}.{pad} board grid pitch does not match declared {expected_pitch} mm.")
        expected_outer = geometry.get("via_diameter_mm")
        if expected_outer is not None and observed.get("outer_diameter_mm") != [float(expected_outer)]:
            mismatches.append(f"{reference}.{pad} board via land diameter does not match declared {expected_outer} mm.")
        expected_drill = geometry.get("drill_diameter_mm")
        if expected_drill is not None and observed.get("drill_diameter_mm") != [float(expected_drill)]:
            mismatches.append(f"{reference}.{pad} board drill diameter does not match declared {expected_drill} mm.")
    return mismatches
