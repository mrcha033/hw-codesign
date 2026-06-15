from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from .service import HardwareService


def create_server(root: Path | str | None = None):
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:
        raise RuntimeError("Install the MCP extra with: pip install -e '.[mcp]'") from exc

    service = HardwareService(root or os.environ.get("HW_PLATFORM_ROOT", Path.cwd()))
    server = FastMCP("hw-codesign-platform")

    @server.tool(name="hw_create_project")
    def create_project(name: str, template: str = "robotics_controller_full", target: str = "manufacturable_pcb_with_enclosure_and_firmware") -> dict[str, Any]:
        result = service.create_project(name, template)
        result["target"] = target
        return result

    @server.tool(name="hw_open_project")
    def open_project(project: str) -> dict[str, Any]:
        return {"status": "pass", "project": project, "project_path": str(service.workspace.require_project(project)), "spec": service.read_spec(project)}

    @server.tool(name="hw_snapshot_project")
    def snapshot_project(project: str) -> dict[str, Any]:
        return {"project": project, "iteration_id": service.workspace.snapshot(project), "status": "generated"}

    @server.tool(name="hw_compare_iterations")
    def compare_iterations(project: str, before: str, after: str) -> dict[str, Any]:
        base = service.workspace.require_project(project) / "history" / "iterations"
        before_files = {item.relative_to(base / before).as_posix(): item.read_text(encoding="utf-8", errors="replace") for item in (base / before).rglob("*") if item.is_file()}
        after_files = {item.relative_to(base / after).as_posix(): item.read_text(encoding="utf-8", errors="replace") for item in (base / after).rglob("*") if item.is_file()}
        names = sorted(set(before_files) | set(after_files))
        return {"status": "pass", "project": project, "before": before, "after": after, "added": [name for name in names if name not in before_files], "removed": [name for name in names if name not in after_files], "changed": [name for name in names if name in before_files and name in after_files and before_files[name] != after_files[name]]}

    @server.tool(name="hw_read_spec")
    def read_spec(project: str) -> dict[str, Any]:
        return {"status": "pass", "spec": service.read_spec(project)}

    @server.tool(name="hw_validate_spec")
    def validate_spec(project: str) -> dict[str, Any]:
        return service.validate_spec(project)

    @server.tool(name="hw_update_spec")
    def update_spec(project: str, section: str, value: dict[str, Any], user_approved: bool = False) -> dict[str, Any]:
        return service.update_spec(project, section, value, user_approved)

    @server.tool(name="hw_update_requirements")
    def update_requirements(project: str, requirements_text: str) -> dict[str, Any]:
        return service.update_requirements(project, requirements_text)

    @server.tool(name="hw_list_assumptions")
    def list_assumptions(project: str) -> dict[str, Any]:
        return {"status": "pass", "project": project, "assumptions": service.read_spec(project).get("assumptions", {})}

    @server.tool(name="hw_resolve_assumption")
    def resolve_assumption(project: str, name: str, resolution: str, approved: bool = False) -> dict[str, Any]:
        return service.resolve_assumption(project, name, resolution, approved)

    @server.tool(name="hw_generate_all")
    def generate_all(project: str) -> dict[str, Any]:
        return service.generate_all(project)

    @server.tool(name="hw_generate_reference_intent")
    def generate_reference_intent(project: str) -> dict[str, Any]:
        return service.generate_reference_intent(project)

    @server.tool(name="hw_generate_electronics_source")
    def generate_electronics_tool(project: str) -> dict[str, Any]:
        return service.generate_electronics_source(project)

    @server.tool(name="hw_generate_mechanical")
    def generate_mechanical_tool(project: str, backend: str = "build123d") -> dict[str, Any]:
        result = service.generate_mechanical_source(project)
        return {"status": result["status"], "backend": backend, "files": result["files"]}

    @server.tool(name="hw_generate_firmware")
    def generate_firmware_tool(project: str, framework: str = "zephyr") -> dict[str, Any]:
        result = service.generate_firmware_source(project)
        return {"status": result["status"], "framework": framework, "files": result["files"]}

    @server.tool(name="hw_run_erc")
    def run_erc(project: str) -> dict[str, Any]:
        report = service.kicad.run_erc(service.workspace.require_project(project))
        return report.to_dict()

    @server.tool(name="hw_run_drc")
    def run_drc(project: str, profile: str = "jlcpcb_4layer") -> dict[str, Any]:
        report = service.kicad.run_drc(service.workspace.require_project(project))
        value = report.to_dict()
        value["profile"] = profile
        return value

    @server.tool(name="hw_check_electrical_semantics")
    def check_electrical_semantics(project: str) -> dict[str, Any]:
        return service.validator.check_electrical_semantics(service.read_spec(project)).to_dict()

    @server.tool(name="hw_extract_electrical_graph")
    def extract_electrical_graph(project: str) -> dict[str, Any]:
        import json
        path = service.workspace.require_project(project) / "electronics" / "generated" / "electrical_graph.json"
        return {"status": "generated" if path.exists() else "blocked", "graph": json.loads(path.read_text(encoding="utf-8")) if path.exists() else None}

    @server.tool(name="hw_export_pcb_fabrication")
    def export_pcb_fabrication(project: str) -> dict[str, Any]:
        return {"status": "blocked", "project": project, "code": "native_kicad_export_required", "message": "Fabrication export requires a generated KiCad board that passes ERC and DRC"}

    @server.tool(name="hw_check_mechanical_fit")
    def check_mechanical_fit(project: str) -> dict[str, Any]:
        return service.validator.check_mechanical(service.read_spec(project)).to_dict()

    @server.tool(name="hw_import_board_step")
    def import_board_step(project: str, source: str) -> dict[str, Any]:
        return {"status": "blocked", "project": project, "source": source, "code": "validated_step_import_not_implemented"}

    @server.tool(name="hw_export_mechanical")
    def export_mechanical(project: str) -> dict[str, Any]:
        return {"status": "blocked", "project": project, "code": "native_cad_export_required", "message": "STEP/STL export requires the pinned build123d backend and geometry validation"}

    @server.tool(name="hw_check_pinmap")
    def check_pinmap(project: str) -> dict[str, Any]:
        return next(item for item in service.run_all_checks(project, include_external=False)["reports"] if item["gate"] == "firmware_pinmap")

    @server.tool(name="hw_build_firmware")
    def build_firmware(project: str) -> dict[str, Any]:
        spec = service.read_spec(project)
        return service.zephyr.build(service.workspace.require_project(project), spec["firmware"]["target"]).to_dict()

    @server.tool(name="hw_generate_bringup_tests")
    def generate_bringup_tests(project: str) -> dict[str, Any]:
        files = service.generate_firmware_only(project)["files"]
        return {"status": "generated", "files": [item for item in files if "test" in item]}

    @server.tool(name="hw_run_all_checks")
    def run_all_checks(project: str, include_external: bool = True) -> dict[str, Any]:
        return service.run_all_checks(project, include_external)

    @server.tool(name="hw_generate_repair_plan")
    def generate_repair_plan(project: str) -> dict[str, Any]:
        return service.generate_repair_plan(project)

    @server.tool(name="hw_get_failure_report")
    def get_failure_report(project: str, gate: str | None = None) -> dict[str, Any]:
        import json
        directory = service.workspace.require_project(project) / "validation" / "reports"
        reports = [json.loads(item.read_text(encoding="utf-8")) for item in sorted(directory.glob("*.json")) if gate is None or item.stem == gate]
        return {"status": "pass", "project": project, "reports": reports}

    @server.tool(name="hw_apply_repair_plan")
    def apply_repair_plan(project: str, approved: bool = False) -> dict[str, Any]:
        return service.apply_repair_plan(project, approved=approved)

    @server.tool(name="hw_run_design_iteration")
    def run_design_iteration(project: str, goal: str = "make all release gates pass", include_external: bool = True) -> dict[str, Any]:
        result = service.run_design_iteration(project, include_external)
        result["goal"] = goal
        return result

    @server.tool(name="hw_design_until_release")
    def design_until_release(project: str, max_iterations: int = 8, include_external: bool = False) -> dict[str, Any]:
        return service.design_until_release(project, max_iterations, include_external)

    @server.tool(name="hw_check_release_gate")
    def check_release_gate(project: str) -> dict[str, Any]:
        return service.check_release_gate(project)

    @server.tool(name="hw_generate_design_report")
    def generate_design_report(project: str) -> dict[str, Any]:
        return service.generate_design_report(project)

    @server.tool(name="hw_export_release_bundle")
    def export_release_bundle(project: str) -> dict[str, Any]:
        return service.export_release_bundle(project)

    @server.tool(name="hw_verify_release")
    def verify_release(project: str) -> dict[str, Any]:
        spec = service.read_spec(project)
        release = service.workspace.require_project(project) / "exports" / "releases" / spec["project"]["revision"]
        return service._artifact_integrity_report(release).to_dict()

    return server


def main() -> None:
    create_server().run()


if __name__ == "__main__":
    main()
