from __future__ import annotations

from pathlib import Path
import json
import re
import shutil
import xml.etree.ElementTree as ET
from typing import Any

from ..artifacts import deterministic_zip

from .command import resolve_tool, run_tool, tool_report, tool_version
from ..models import Failure, FailureCategory, GateReport, Status
from ..io import write_json
from ..provenance import artifact_provenance
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
            "source_release_eligible": bool(files),
            "sources": self.source_entries(target, [Path(path) for path in files]),
            "contract_gates": list(self.gate_names),
            "release_blocking_gates": list(self.gate_names),
            "provenance": artifact_provenance(spec, self.platform_root / "parts", self.name, compiler_version=tool_version("kicad-cli"), command=["kicad-cli", "sch", "export", "netlist"], release_eligible=bool(files)),
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
            return GateReport("erc", Status.FAIL, [Failure(FailureCategory.EDA_ERROR, "missing_design_source", "No generated KiCad schematic exists")])
        output = project / "validation" / "reports" / "kicad_erc.json"
        result = run_tool("kicad-cli", ["sch", "erc", "--format", "json", "--output", str(output), str(schematic)], project)
        report = tool_report("erc", result, [str(output)] if output.exists() else [])
        if report.status == Status.PASS and output.exists():
            data = json.loads(output.read_text(encoding="utf-8"))
            violations = [item for sheet in data.get("sheets", []) for item in sheet.get("violations", [])]
            if violations:
                report.status = Status.FAIL
                report.failures = [Failure(FailureCategory.EDA_ERROR, "erc_violation", item.get("description", "KiCad ERC violation"), details=item) for item in violations]
            report.metrics = {"violations": len(violations)}
        return report

    def run_drc(self, project: Path) -> GateReport:
        board = self._design_file(project, "*.kicad_pcb")
        if board is None:
            return GateReport("drc", Status.FAIL, [Failure(FailureCategory.EDA_ERROR, "missing_design_source", "No generated KiCad PCB exists")])
        output = project / "validation" / "reports" / "kicad_drc.json"
        result = run_tool("kicad-cli", ["pcb", "drc", "--format", "json", "--refill-zones", "--save-board", "--output", str(output), str(board)], project)
        report = tool_report("drc", result, [str(output)] if output.exists() else [])
        if report.status == Status.PASS and output.exists():
            data = json.loads(output.read_text(encoding="utf-8"))
            violations = [*data.get("violations", []), *data.get("unconnected_items", []), *data.get("schematic_parity", [])]
            if violations:
                report.status = Status.FAIL
                report.failures = [Failure(FailureCategory.EDA_ERROR, "drc_violation", item.get("description", "KiCad DRC violation"), details=item) for item in violations]
            report.metrics = {"violations": len(violations)}
        return report

    def export_manufacturing(self, project: Path, release: Path) -> GateReport:
        board = self._design_file(project, "*.kicad_pcb")
        if board is None:
            return GateReport("fabrication_export", Status.FAIL, [Failure(FailureCategory.EDA_ERROR, "missing_design_source", "No generated KiCad PCB exists")])
        fabrication = release / "fabrication"
        native = fabrication / "native_kicad"
        shutil.rmtree(native, ignore_errors=True)
        native.mkdir(parents=True)
        gerber = run_tool("kicad-cli", ["pcb", "export", "gerbers", "--output", str(native), "--layers", "F.Cu,In1.Cu,In2.Cu,B.Cu,F.Mask,B.Mask,F.Silkscreen,B.Silkscreen,Edge.Cuts", str(board)], project)
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
        step = release / "mechanical" / "board.step"
        step.parent.mkdir(parents=True, exist_ok=True)
        step_result = run_tool("kicad-cli", ["pcb", "export", "step", "--subst-models", "--output", str(step), str(board)], project)
        if step_result.returncode != 0:
            return tool_report("fabrication_export", step_result)
        gerbers = [(item, item.name) for item in native.iterdir() if item.suffix.lower() not in {".drl", ".xln", ".pdf"}]
        drills = [(item, item.name) for item in native.iterdir() if item.suffix.lower() in {".drl", ".xln", ".pdf"}]
        gerbers = [(item, name) for item, name in gerbers if item != position]
        if not gerbers or not drills:
            return GateReport("fabrication_export", Status.FAIL, [Failure(FailureCategory.EDA_ERROR, "manufacturing_files_missing", "KiCad export did not produce both Gerber and drill artifacts")])
        deterministic_zip(fabrication / "gerbers.zip", gerbers)
        deterministic_zip(fabrication / "drill.zip", drills)
        shutil.copy2(position, fabrication / "pick_and_place.csv")
        bom_source = project / "electronics" / "generated" / "bom.csv"
        if not bom_source.is_file():
            return GateReport("fabrication_export", Status.FAIL, [Failure(FailureCategory.EDA_ERROR, "bom_export_missing", "Resolved BOM must exist before manufacturing export")])
        shutil.copy2(bom_source, fabrication / "bom.csv")
        artifacts = [str(fabrication / "gerbers.zip"), str(fabrication / "drill.zip"), str(fabrication / "pick_and_place.csv"), str(fabrication / "bom.csv"), str(step)]
        return GateReport("fabrication_export", Status.PASS, metrics={"gerber_files": len(gerbers), "drill_files": len(drills), "position_file": True, "bom": True}, artifacts=artifacts, backend={"name": "kicad-cli", "deterministic_archive": True})

    @staticmethod
    def _design_file(project: Path, pattern: str) -> Path | None:
        source = project / "electronics" / "source" / "kicad"
        generated = project / "electronics" / "generated" / "kicad"
        source_match = next(source.glob(pattern), None) if source.is_dir() else None
        return source_match or next(generated.glob(pattern), None)
