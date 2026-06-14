from __future__ import annotations

import json
import re
import zipfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .backends.kicad import KiCadBackend
from .backends.freerouting import FreeroutingBackend
from .backends.mechanical import OpenCascadeMechanicalBackend
from .backends.zephyr import ZephyrBackend
from .artifacts import deterministic_zip, sha256, simple_pdf, write_manifest
from .generators import generate_bom, generate_electronics, generate_firmware, generate_mechanical
from .io import atomic_write_text, read_yaml, write_json, write_yaml
from .models import Failure, FailureCategory, GateReport, Status
from .policy import ChangePolicy
from .reference_backend import build_firmware_reference, export_fabrication, export_mechanical, internal_drc, internal_erc
from .validation import Validator, persist_report
from .workspace import Workspace


class HardwareService:
    def __init__(self, root: Path | str):
        self.root = Path(root).resolve()
        self.workspace = Workspace(self.root)
        self.validator = Validator(self.root / "schemas")
        self.kicad = KiCadBackend()
        self.freerouting = FreeroutingBackend(self.root)
        self.mechanical = OpenCascadeMechanicalBackend()
        self.zephyr = ZephyrBackend()

    def create_project(self, name: str, template: str = "robotics_controller_full") -> dict[str, Any]:
        return self.workspace.create_project(name, template)

    def read_spec(self, project: str) -> dict[str, Any]:
        return self.workspace.read_spec(project)

    def update_spec(self, project: str, section: str, value: dict[str, Any], user_approved: bool = False) -> dict[str, Any]:
        if section == "safety" and not user_approved:
            ChangePolicy().check_spec_paths(["safety.requirements"])
        if section == "manufacturing" and "limits" in value and not user_approved:
            ChangePolicy().check_spec_paths(["manufacturing.limits.change"])
        changed = self.workspace.update_spec(project, section, value)
        return {"status": "updated", "changed_files": [changed], "user_approved": user_approved}

    def update_requirements(self, project: str, requirements_text: str) -> dict[str, Any]:
        """Deterministically lower common natural-language requirements into the typed spec."""
        spec = self.read_spec(project)
        system_path = self.workspace.require_project(project) / "spec" / "system.yaml"
        firmware_path = self.workspace.require_project(project) / "spec" / "firmware.yaml"
        manufacturing_path = self.workspace.require_project(project) / "spec" / "manufacturing.yaml"
        system_file = read_yaml(system_path); firmware_file = read_yaml(firmware_path); manufacturing_file = read_yaml(manufacturing_path)
        changed = []
        patterns = [
            (r"(\d+)\s*(?:채널|channel)", lambda value: (system_file["actuation"].__setitem__("motor_channels", int(value)), "actuation.motor_channels")),
            (r"(?:각\s*채널\s*)?(?:피크\s*)?(\d+(?:\.\d+)?)\s*A", lambda value: (system_file["actuation"].__setitem__("motor_channel_peak_current_a", float(value)), "actuation.motor_channel_peak_current_a")),
            (r"(\d+(?:\.\d+)?)\s*V\s*(?:배터리|battery)", lambda value: (system_file["system"]["supply"]["battery"].__setitem__("pack_voltage_nominal", float(value)), "system.supply.battery.pack_voltage_nominal")),
            (r"(STM32H7\w*|ESP32S3|RP2040)", lambda value: (system_file["compute"]["mcu"].__setitem__("family", value.upper()), "compute.mcu.family")),
            (r"(\d+)\s*[- ]?layer", lambda value: (manufacturing_file["manufacturing"]["pcb"].__setitem__("layers", int(value)), "manufacturing.pcb.layers")),
        ]
        for pattern, setter in patterns:
            match = re.search(pattern, requirements_text, flags=re.IGNORECASE)
            if match:
                _, path = setter(match.group(1)); changed.append(path)
        lowered = requirements_text.lower()
        if "zephyr" in lowered:
            firmware_file["firmware"]["framework"] = "zephyr"; changed.append("firmware.framework")
        features = {"imu": "imu", "emergency stop": "e_stop", "e-stop": "e_stop", "비상 정지": "e_stop"}
        for token, key in features.items():
            if token in lowered:
                system_file["sensing"][key] = "required"; changed.append(f"sensing.{key}")
        write_yaml(system_path, system_file); write_yaml(firmware_path, firmware_file); write_yaml(manufacturing_path, manufacturing_file)
        unresolved = []
        if not re.search(r"(?:external|onboard|외장|온보드).*(?:driver|드라이버)", requirements_text, re.IGNORECASE):
            unresolved.append("motor driver topology retained from documented assumption")
        if not re.search(r"(?:forced|passive|팬|자연 냉각)", requirements_text, re.IGNORECASE):
            unresolved.append("cooling condition retained from documented assumption")
        return {"status": "updated", "changed_paths": sorted(set(changed)), "changed_files": [str(system_path), str(firmware_path), str(manufacturing_path)], "unresolved_requirements": unresolved}

    def validate_spec(self, project: str) -> dict[str, Any]:
        path = self.workspace.require_project(project)
        report = self.validator.validate_spec(self.read_spec(project))
        persist_report(path, report)
        return report.to_dict()

    def generate_all(self, project: str) -> dict[str, Any]:
        path = self.workspace.require_project(project)
        spec = self.read_spec(project)
        files = {
            "electronics": generate_electronics(path, spec),
            "mechanical": generate_mechanical(path, spec),
            "firmware": generate_firmware(path, spec),
        }
        files["bom"] = [generate_bom(path)]
        return {"status": "generated", "files": files}

    def generate_electronics_only(self, project: str) -> dict[str, Any]:
        path = self.workspace.require_project(project)
        spec = self.read_spec(project)
        files = generate_electronics(path, spec)
        return {"status": "generated", "files": files}

    def generate_mechanical_only(self, project: str) -> dict[str, Any]:
        path = self.workspace.require_project(project)
        spec = self.read_spec(project)
        files = generate_mechanical(path, spec)
        return {"status": "generated", "files": files}

    def generate_firmware_only(self, project: str) -> dict[str, Any]:
        path = self.workspace.require_project(project)
        spec = self.read_spec(project)
        files = generate_firmware(path, spec)
        return {"status": "generated", "files": files}

    def run_all_checks(self, project: str, include_external: bool = True) -> dict[str, Any]:
        path = self.workspace.require_project(project)
        spec = self.read_spec(project)
        reports = [
            self.validator.validate_spec(spec),
            self.validator.check_electrical_semantics(spec),
            self.validator.check_mechanical(spec),
        ]
        pinmap_path = path / "firmware" / "generated" / "pinmap.json"
        pinmap = json.loads(pinmap_path.read_text(encoding="utf-8")) if pinmap_path.exists() else []
        if pinmap:
            reports.append(self.validator.check_pinmap(pinmap))
        else:
            reports.append(GateReport("firmware_pinmap", Status.FAIL, [Failure(FailureCategory.FIRMWARE_ERROR, "missing_pinmap", "Generate firmware before checking the pinmap")]))
        graph_path = path / "electronics" / "generated" / "electrical_graph.json"
        graph = json.loads(graph_path.read_text(encoding="utf-8")) if graph_path.exists() else {"components": []}
        if graph_path.exists():
            reports.append(self.validator.check_bom(graph["components"]))
            reports.append(self.validator.check_sourcing(graph["components"]))
            reports.append(self.validator.check_hw_sw_parity(graph, pinmap))
        else:
            reports.append(GateReport("bom", Status.FAIL, [Failure(FailureCategory.BOM_ERROR, "missing_bom_source", "Generate electronics before checking the BOM")]))
        autoroute = self.freerouting.route(path) if include_external else None
        reports.extend([internal_erc(graph), internal_drc(path, spec, graph), self._geometry_report(path, spec), build_firmware_reference(path)])
        if include_external:
            native = [self.kicad.run_erc(path), self.kicad.run_drc(path), self.zephyr.build(path, spec.get("firmware", {}).get("target", "unknown"))]
            for report in native:
                report.gate = f"native_{report.gate}"
            reports.extend([autoroute, *native])
        for report in reports:
            persist_report(path, report)
        return self._report_set(reports)

    def prepare_release(self, project: str, checks: dict[str, Any], require_native: bool = False) -> dict[str, Any]:
        path = self.workspace.require_project(project)
        spec = self.read_spec(project)
        graph = json.loads((path / "electronics" / "generated" / "electrical_graph.json").read_text(encoding="utf-8"))
        release = path / "exports" / spec["project"]["revision"]
        files = export_fabrication(path, spec, graph, release)
        ref_mech = export_mechanical(path, spec, release)
        if require_native:
            mechanical_report = self.mechanical.generate(spec, release)
            if mechanical_report.status == Status.PASS:
                files.extend(mechanical_report.artifacts)
            # BLOCKED or FAIL: keep status as-is; reference files above are still on disk
        else:
            files.extend(ref_mech)
            mechanical_report = GateReport("mechanical_export", Status.PASS, metrics={"mode": "reference"}, artifacts=ref_mech, backend={"name": "reference-faceted"})
        persist_report(path, mechanical_report)
        fabrication_report = self.kicad.export_manufacturing(path, release) if require_native else GateReport("fabrication_export", Status.PASS, metrics={"mode": "reference"}, artifacts=files, backend={"name": "reference-fabrication"})
        if fabrication_report.status == Status.PASS:
            files.extend(fabrication_report.artifacts)
        # BLOCKED: keep status as-is; do not promote to PASS
        persist_report(path, fabrication_report)
        firmware = release / "firmware"; firmware.mkdir(parents=True, exist_ok=True)
        firmware_sources = [(item, item.relative_to(path / "firmware").as_posix()) for item in sorted((path / "firmware").rglob("*")) if item.is_file() and "build" not in item.parts]
        deterministic_zip(firmware / "source.zip", firmware_sources)
        for name in ("pinmap.h", "devicetree.overlay"):
            source = path / "firmware" / "generated" / name
            (firmware / name).write_bytes(source.read_bytes())
        atomic_write_text(firmware / "build_instructions.md", "# Firmware Build\n\nReference verification: `cmake -S firmware/reference -B build -G Ninja && cmake --build build && ctest --test-dir build`.\n\nZephyr target: `west build -b robot_controller firmware/zephyr/app`.\n")
        docs = release / "docs"; docs.mkdir(parents=True, exist_ok=True)
        statuses = [f"{item['gate']}: {item['status']}" for item in checks["reports"]]
        atomic_write_text(docs / "design_report.md", "# Design Report\n\n" + "\n".join(f"- {line}" for line in statuses) + "\n")
        write_json(docs / "validation_report.json", checks)
        atomic_write_text(docs / "bringup_guide.md", "# Bring-up Guide\n\n1. Inspect assembly and verify no shorts with power removed.\n2. Current-limit the bench supply below 0.5 A and apply 24 V through the protected input.\n3. Verify 5 V and 3.3 V rails before fitting the MCU.\n4. Keep motor enable disabled; flash the Zephyr image over SWD.\n5. Verify console, IMU identity, CAN loopback, E-stop latch, then each PWM/encoder/current channel.\n6. Increase load only under instrumented thermal and transient monitoring.\n")
        atomic_write_text(docs / "known_risks.md", "# Known Risks\n\n- EMI/EMC, full-load thermal behavior, vibration life, battery abuse, motor transients, ingress protection, and connector fatigue require physical qualification.\n- The reference design controls external motor drivers; it does not route 8 A motor phase current through the controller PCB.\n")
        simple_pdf("Robot Controller Schematic", [f"Components: {len(graph['components'])}", f"Nets: {len(graph['nets'])}", "See KiCad project for editable source."], docs / "schematic.pdf")
        simple_pdf("Assembly Drawing", ["Top-side placement is provided in fabrication/pick_and_place.csv.", "Verify connector orientation before assembly."], docs / "assembly_drawing.pdf")
        simple_pdf("Validation Report", statuses, docs / "validation_report.pdf")
        simple_pdf("Design Report", statuses + ["Physical qualification risks are listed in known_risks.md."], docs / "design_report.pdf")
        simple_pdf("Layout Preview", [f"Board envelope: {spec['mechanical']['envelope']['board_width_mm']} x {spec['mechanical']['envelope']['board_height_mm']} mm", f"Placement entries: {len(graph['components'])}"], docs / "layout_preview.pdf")
        simple_pdf("Bring-up Guide", ["Current-limit initial power-up.", "Verify rails before MCU operation.", "Test E-stop before motor enable.", "Run each channel with motor power isolated."], docs / "bringup_guide.pdf")
        (release / "fabrication" / "assembly_drawing.pdf").write_bytes((docs / "assembly_drawing.pdf").read_bytes())
        manifest = write_manifest(release, release / "manifest.json")
        reports = [fabrication_report.to_dict(), mechanical_report.to_dict()]
        return {"status": "generated" if all(item["status"] == "pass" for item in reports) else "failed", "release_path": str(release), "files": files + [str(firmware / "source.zip"), manifest], "reports": reports}

    def check_release_gate(self, project: str, reports: list[GateReport] | None = None, include_external: bool = False) -> dict[str, Any]:
        path = self.workspace.require_project(project)
        spec = self.read_spec(project)
        if reports is None:
            report_data = self.run_all_checks(project, include_external=include_external)
            reports = [self._report_from_dict(item) for item in report_data["reports"]]
        revision = spec["project"]["revision"]
        release = path / "exports" / revision
        required = [
            release / "fabrication" / "gerbers.zip", release / "fabrication" / "drill.zip",
            release / "fabrication" / "bom.csv", release / "fabrication" / "pick_and_place.csv",
            release / "fabrication" / "assembly_drawing.pdf",
            release / "mechanical" / "enclosure.step", release / "mechanical" / "enclosure.stl", release / "mechanical" / "assembly.step",
            release / "firmware" / "source.zip", release / "docs" / "design_report.md",
            release / "firmware" / "pinmap.h", release / "firmware" / "devicetree.overlay", release / "firmware" / "build_instructions.md",
            release / "docs" / "validation_report.json", release / "docs" / "bringup_guide.md", release / "docs" / "known_risks.md",
            release / "docs" / "schematic.pdf", release / "docs" / "layout_preview.pdf", release / "docs" / "design_report.pdf",
            release / "docs" / "validation_report.pdf", release / "docs" / "bringup_guide.pdf", release / "manifest.json",
        ]
        reports = [*reports, self._artifact_integrity_report(release)]
        report = self.validator.release_gate(reports, spec.get("assumptions", {}), required)
        persist_report(path, report)
        return report.to_dict()

    def generate_repair_plan(self, project: str, check_result: dict[str, Any] | None = None) -> dict[str, Any]:
        check_result = check_result or self.run_all_checks(project)
        actions: list[dict[str, Any]] = []
        requires_user_decision = False
        mapping = {
            "current_budget_exceeded": "Add power-domain concurrency limits or increase an explicitly approved battery/current-path rating.",
            "tool_unavailable": "Run the deterministic toolchain in the pinned Docker image or install the missing backend.",
            "missing_mpn": "Resolve an approved MPN and substitute before release.",
            "insufficient_clearance": "Increase enclosure dimensions or reduce the constrained envelope.",
            "pin_conflict": "Reassign the conflicting MCU peripheral pin in the firmware/electrical source.",
        }
        for report in check_result["reports"]:
            for failure in report["failures"]:
                action = mapping.get(failure["code"], f"Resolve {failure['code']}: {failure['message']}")
                requires = failure.get("requires_user_decision", False) or failure["code"] in {"current_budget_exceeded", "unsafe_assumption"}
                requires_user_decision |= requires
                actions.append({"gate": report["gate"], "failure_code": failure["code"], "action": action, "requires_user_decision": requires})
        return {"project": project, "requires_user_decision": requires_user_decision, "actions": actions}

    def resolve_assumption(self, project: str, name: str, resolution: Any, approved: bool) -> dict[str, Any]:
        path = self.workspace.require_project(project) / "spec" / "system.yaml"
        value = self.workspace.read_spec(project)
        assumptions = value.get("assumptions", {})
        if name not in assumptions:
            raise ValueError(f"Unknown assumption: {name}")
        if not approved:
            return {"status": "blocked", "assumption": name, "message": "Explicit approval is required to resolve an assumption"}
        assumptions[name]["resolved_value"] = resolution
        assumptions[name]["requires_user_review"] = False
        system_file = read_yaml(path)
        system_file["assumptions"] = assumptions
        write_yaml(path, system_file)
        return {"status": "resolved", "assumption": name, "resolution": resolution}

    def export_release_bundle(self, project: str) -> dict[str, Any]:
        gate = self.check_release_gate(project)
        if gate["status"] != "pass":
            return {"status": "blocked", "release_gate": gate, "message": "Release bundle cannot be exported until all required gates pass"}
        path = self.workspace.require_project(project)
        revision = self.read_spec(project)["project"]["revision"]
        release = path / "exports" / revision
        bundle = path / "exports" / f"{project}-{revision}.zip"
        deterministic_zip(bundle, [(artifact, artifact.relative_to(release).as_posix()) for artifact in release.rglob("*") if artifact.is_file()])
        with zipfile.ZipFile(bundle) as archive:
            bad = archive.testzip()
        if bad:
            return {"status": "failed", "bundle": str(bundle), "corrupt_entry": bad}
        return {"status": "exported", "bundle": str(bundle), "sha256": sha256(bundle), "bytes": bundle.stat().st_size}

    def run_design_iteration(self, project: str, include_external: bool = True) -> dict[str, Any]:
        generated = self.generate_all(project)
        checks = self.run_all_checks(project, include_external=include_external)
        repair_plan = self.generate_repair_plan(project, checks)
        # Release artifacts are written only when all checks pass (in design_until_release),
        # not speculatively on every iteration.
        all_pass = all(item["status"] == "pass" for item in checks["reports"])
        iteration_id = self.workspace.snapshot(project, {"goal": "make all release gates pass"})
        result = {
            "status": "passed" if all_pass else ("blocked" if repair_plan["requires_user_decision"] else "failed"),
            "iteration_id": iteration_id,
            "generated": generated,
            "passed_gates": [item["gate"] for item in checks["reports"] if item["status"] == "pass"],
            "failed_gates": [item["gate"] for item in checks["reports"] if item["status"] != "pass"],
            "repair_plan": repair_plan,
            "release_gate": {"status": "pass" if all_pass else "failed"},
        }
        write_json(self.workspace.require_project(project) / "history" / "iterations" / iteration_id / "result.json", result)
        self._append_failures(project, iteration_id, checks)
        return result

    def apply_repair_plan(self, project: str, check_result: dict[str, Any] | None = None) -> dict[str, Any]:
        checks = check_result or self.run_all_checks(project, include_external=False)
        path = self.workspace.require_project(project) / "spec" / "system.yaml"
        system_file = read_yaml(path)
        changes = []
        codes = {failure["code"] for report in checks["reports"] for failure in report["failures"]}
        if "current_budget_exceeded" in codes:
            battery = system_file["system"]["supply"]["battery"]["pack_current_peak_a"]
            current = system_file["actuation"]["motor_channel_peak_current_a"]
            limit = max(1, int(battery // current))
            system_file["actuation"]["max_simultaneous_peak_channels"] = limit
            changes.append({"path": "actuation.max_simultaneous_peak_channels", "value": limit, "reason": "Keep concurrent peak demand within the unchanged battery safety limit"})
        if changes:
            write_yaml(path, system_file)
        return {"status": "applied" if changes else "no_changes", "changes": changes}

    def design_until_release(self, project: str, max_iterations: int = 8, include_external: bool = False) -> dict[str, Any]:
        iterations = []
        for _ in range(max_iterations):
            result = self.run_design_iteration(project, include_external=include_external)
            iterations.append({"iteration_id": result["iteration_id"], "status": result["status"], "failed_gates": result["failed_gates"]})
            if result["release_gate"]["status"] == "pass":
                checks = self.run_all_checks(project, include_external=include_external)
                self.prepare_release(project, checks, require_native=include_external)
                bundle = self.export_release_bundle(project)
                if bundle.get("status") == "exported":
                    return {"status": "released", "iterations": iterations, "release": bundle}
                return {"status": "blocked", "iterations": iterations, "release_gate": self.check_release_gate(project)}
            applied = self.apply_repair_plan(project, self.run_all_checks(project, include_external=False))
            if applied["status"] == "no_changes":
                return {"status": "blocked", "iterations": iterations, "repair": applied, "release_gate": result["release_gate"]}
        return {"status": "max_iterations_exceeded", "iterations": iterations}

    @staticmethod
    def _geometry_report(path: Path, spec: dict[str, Any]) -> GateReport:
        stl = path / "exports" / spec["project"]["revision"] / "mechanical" / "enclosure.stl"
        # Geometry is generated after checks on the first iteration; spec-level fit remains authoritative there.
        failures = []
        if stl.exists():
            text = stl.read_text(encoding="utf-8")
            if text.count("facet normal") < 12 or not text.rstrip().endswith(("endsolid", "endsolid enclosure")):
                failures.append(Failure(FailureCategory.MECHANICAL_ERROR, "non_manifold_stl", "Generated STL is incomplete"))
        return GateReport("geometry", Status.FAIL if failures else Status.PASS, failures, metrics={"enclosure_dimensions_mm": spec["mechanical"]["enclosure_internal_mm"]}, backend={"name": "reference-geometry", "deterministic": True})

    @staticmethod
    def _artifact_integrity_report(release: Path) -> GateReport:
        manifest_path = release / "manifest.json"
        failures = []
        checked = 0
        if not manifest_path.is_file():
            failures.append(Failure(FailureCategory.RELEASE_ERROR, "missing_manifest", "Release manifest is missing"))
        else:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            for entry in manifest.get("artifacts", []):
                artifact = release / entry["path"]
                checked += 1
                if not artifact.is_file():
                    failures.append(Failure(FailureCategory.RELEASE_ERROR, "manifest_file_missing", f"Manifest artifact is missing: {entry['path']}"))
                elif artifact.stat().st_size != entry["bytes"] or sha256(artifact) != entry["sha256"]:
                    failures.append(Failure(FailureCategory.RELEASE_ERROR, "checksum_mismatch", f"Artifact checksum mismatch: {entry['path']}"))
        return GateReport("artifact_integrity", Status.FAIL if failures else Status.PASS, failures, metrics={"checked_artifacts": checked}, artifacts=[str(manifest_path)] if manifest_path.exists() else [])

    def generate_design_report(self, project: str) -> dict[str, Any]:
        path = self.workspace.require_project(project)
        spec = self.read_spec(project)
        reports_dir = path / "validation" / "reports"
        reports = [json.loads(item.read_text(encoding="utf-8")) for item in sorted(reports_dir.glob("*.json"))]
        lines = [f"# Design Report: {project}", "", f"Generated: {datetime.now(UTC).isoformat()}", "", "## Scope", "", f"Target: {spec['project']['target_use']}; revision: {spec['project']['revision']}.", "", "## Validation", ""]
        lines.extend(f"- {item['gate']}: {item['status']} ({len(item.get('failures', []))} findings)" for item in reports)
        lines.extend(["", "## Known Physical Validation Gaps", "", "- Load current and thermal behavior require instrumented hardware testing.", "- EMI/EMC, vibration, abuse safety, transients, ingress, and connector fatigue are not certified by digital checks.", ""])
        output = path / "exports" / "working" / "documentation" / "design_report.md"
        atomic_write_text(output, "\n".join(lines))
        return {"status": "generated", "file": str(output)}

    @staticmethod
    def _report_set(reports: list[GateReport]) -> dict[str, Any]:
        return {"status": "pass" if all(item.passed for item in reports) else "failed", "reports": [item.to_dict() for item in reports]}

    @staticmethod
    def _report_from_dict(value: dict[str, Any]) -> GateReport:
        failures = [Failure(FailureCategory(item["category"]), item["code"], item["message"], item.get("severity", "error"), item.get("path"), item.get("details", {}), item.get("requires_user_decision", False)) for item in value.get("failures", [])]
        return GateReport(value["gate"], Status(value["status"]), failures, value.get("metrics", {}), value.get("artifacts", []), value.get("backend", {}))

    def _append_failures(self, project: str, iteration_id: str, checks: dict[str, Any]) -> None:
        path = self.workspace.require_project(project) / "history" / "failure_log.jsonl"
        existing = path.read_text(encoding="utf-8").strip()
        if existing == "[]":
            existing = ""
        entries = []
        for report in checks["reports"]:
            for failure in report["failures"]:
                entries.append(json.dumps({"iteration_id": iteration_id, "gate": report["gate"], **failure}, sort_keys=True))
        atomic_write_text(path, (existing + ("\n" if existing and entries else "") + "\n".join(entries) + ("\n" if entries else "")))
