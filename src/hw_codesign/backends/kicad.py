from __future__ import annotations

from pathlib import Path
import json
import shutil

from ..artifacts import deterministic_zip

from .command import run_tool, tool_report
from ..models import Failure, FailureCategory, GateReport, Status


class KiCadBackend:
    def run_erc(self, project: Path) -> GateReport:
        schematic = next((project / "electronics" / "generated" / "kicad").glob("*.kicad_sch"), None)
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
        board = next((project / "electronics" / "generated" / "kicad").glob("*.kicad_pcb"), None)
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
        board = next((project / "electronics" / "generated" / "kicad").glob("*.kicad_pcb"), None)
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
        step = release / "mechanical" / "board.step"
        step.parent.mkdir(parents=True, exist_ok=True)
        step_result = run_tool("kicad-cli", ["pcb", "export", "step", "--subst-models", "--output", str(step), str(board)], project)
        if step_result.returncode != 0:
            return tool_report("fabrication_export", step_result)
        gerbers = [(item, item.name) for item in native.iterdir() if item.suffix.lower() not in {".drl", ".xln", ".pdf"}]
        drills = [(item, item.name) for item in native.iterdir() if item.suffix.lower() in {".drl", ".xln", ".pdf"}]
        deterministic_zip(fabrication / "gerbers.zip", gerbers)
        deterministic_zip(fabrication / "drill.zip", drills)
        artifacts = [str(fabrication / "gerbers.zip"), str(fabrication / "drill.zip"), str(step)]
        return GateReport("fabrication_export", Status.PASS, metrics={"gerber_files": len(gerbers), "drill_files": len(drills)}, artifacts=artifacts, backend={"name": "kicad-cli", "deterministic_archive": True})
