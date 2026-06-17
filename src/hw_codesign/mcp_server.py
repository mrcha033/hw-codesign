from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from .contracts import TOOL_REGISTRY as _TR
from .service import HardwareService


def _enrich(result: dict[str, Any], **extra: Any) -> dict[str, Any]:
    """Merge envelope fields into a tool result, always overriding for safety-critical contract fields."""
    return {**result, **extra}


def create_server(root: Path | str | None = None):
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:
        raise RuntimeError("Install the MCP extra with: pip install -e '.[mcp]'") from exc

    service = HardwareService(root or os.environ.get("HW_PLATFORM_ROOT", Path.cwd()))
    server = FastMCP("hw-codesign-platform")

    # ------------------------------------------------------------------
    # Project management
    # ------------------------------------------------------------------

    @server.tool(name=_TR["hw_create_project"].name)
    def create_project(name: str, template: str = "robotics_controller_full", target: str = "manufacturable_pcb_with_enclosure_and_firmware") -> dict[str, Any]:
        result = service.create_project(name, template)
        result["target"] = target
        return _enrich(result, release_eligible=False, candidate_only=True, release_blocking_failures=["project created — run generate and hw_check_release_gate before release"])

    @server.tool(name=_TR["hw_open_project"].name)
    def open_project(project: str) -> dict[str, Any]:
        return {"status": "pass", "project": project, "project_path": str(service.workspace.require_project(project)), "spec": service.read_spec(project)}

    @server.tool(name=_TR["hw_snapshot_project"].name)
    def snapshot_project(project: str) -> dict[str, Any]:
        return _enrich({"project": project, "iteration_id": service.workspace.snapshot(project), "status": "generated"},
            release_eligible=False, candidate_only=True, release_blocking_failures=["snapshot is a candidate artifact — hw_check_release_gate must pass before release"])

    @server.tool(name=_TR["hw_compare_iterations"].name)
    def compare_iterations(project: str, before: str, after: str) -> dict[str, Any]:
        base = service.workspace.require_project(project) / "history" / "iterations"
        before_files = {item.relative_to(base / before).as_posix(): item.read_text(encoding="utf-8", errors="replace") for item in (base / before).rglob("*") if item.is_file()}
        after_files = {item.relative_to(base / after).as_posix(): item.read_text(encoding="utf-8", errors="replace") for item in (base / after).rglob("*") if item.is_file()}
        names = sorted(set(before_files) | set(after_files))
        return {"status": "pass", "project": project, "before": before, "after": after, "added": [name for name in names if name not in before_files], "removed": [name for name in names if name not in after_files], "changed": [name for name in names if name in before_files and name in after_files and before_files[name] != after_files[name]]}

    # ------------------------------------------------------------------
    # Spec read/write
    # ------------------------------------------------------------------

    @server.tool(name=_TR["hw_read_spec"].name)
    def read_spec(project: str) -> dict[str, Any]:
        return {"status": "pass", "spec": service.read_spec(project)}

    @server.tool(name=_TR["hw_validate_spec"].name)
    def validate_spec(project: str) -> dict[str, Any]:
        return service.validate_spec(project)

    @server.tool(name=_TR["hw_update_spec"].name)
    def update_spec(project: str, section: str, value: dict[str, Any], user_approved: bool = False) -> dict[str, Any]:
        return service.update_spec(project, section, value, user_approved)

    @server.tool(name=_TR["hw_update_requirements"].name)
    def update_requirements(project: str, requirements_text: str) -> dict[str, Any]:
        result = service.update_requirements(project, requirements_text)
        unsupported = result.get("unsupported_constraints") or []
        existing = result.get("release_blocking_failures") or []
        combined = list(dict.fromkeys(existing + unsupported))
        return _enrich(result, release_blocking_failures=combined)

    @server.tool(name=_TR["hw_list_assumptions"].name)
    def list_assumptions(project: str) -> dict[str, Any]:
        return {"status": "pass", "project": project, "assumptions": service.read_spec(project).get("assumptions", {})}

    @server.tool(name=_TR["hw_resolve_assumption"].name)
    def resolve_assumption(project: str, name: str, resolution: str, approved: bool = False) -> dict[str, Any]:
        return service.resolve_assumption(project, name, resolution, approved)

    # ------------------------------------------------------------------
    # Generation (all generation tools emit candidate_only/release_eligible/release_blocking_failures)
    # ------------------------------------------------------------------

    @server.tool(name=_TR["hw_generate_all"].name)
    def generate_all(project: str) -> dict[str, Any]:
        result = service.generate_all(project)
        backend = result.get("backend", "reference")
        from .service import _RELEASE_ELIGIBLE_BACKENDS
        is_release_eligible_backend = backend in _RELEASE_ELIGIBLE_BACKENDS
        return _enrich(result,
            release_eligible=False,
            candidate_only=True,
            release_blocking_failures=[f"backend '{backend}' is candidate-only — run hw_check_release_gate to evaluate release eligibility"] if not is_release_eligible_backend else ["hw_check_release_gate must pass before release"],
        )

    @server.tool(name=_TR["hw_generate_reference_intent"].name)
    def generate_reference_intent(project: str) -> dict[str, Any]:
        result = service.generate_reference_intent(project)
        return _enrich(result,
            release_eligible=False,
            candidate_only=True,
            release_blocking_failures=["reference backend is candidate-only — switch to tscircuit, kicad, or python_netlist for a release-eligible backend"],
        )

    @server.tool(name=_TR["hw_generate_electronics_source"].name)
    def generate_electronics_tool(project: str) -> dict[str, Any]:
        result = service.generate_electronics_source(project)
        spec = service.read_spec(project)
        backend = spec.get("electronics", {}).get("backend", "reference")
        from .service import _RELEASE_ELIGIBLE_BACKENDS
        is_release_eligible_backend = backend in _RELEASE_ELIGIBLE_BACKENDS
        return _enrich(result,
            release_eligible=False,
            candidate_only=True,
            release_blocking_failures=[f"backend '{backend}' is candidate-only"] if not is_release_eligible_backend else ["hw_check_release_gate must pass before release"],
        )

    @server.tool(name=_TR["hw_generate_mechanical"].name)
    def generate_mechanical_tool(project: str, backend: str = "build123d") -> dict[str, Any]:
        result = service.generate_mechanical_source(project)
        return _enrich({"status": result["status"], "backend": backend, "files": result["files"]},
            release_eligible=False,
            candidate_only=True,
            release_blocking_failures=["hw_check_release_gate must pass before release"],
        )

    @server.tool(name=_TR["hw_generate_firmware"].name)
    def generate_firmware_tool(project: str, framework: str = "zephyr") -> dict[str, Any]:
        result = service.generate_firmware_source(project)
        return _enrich({"status": result["status"], "framework": framework, "files": result["files"]},
            release_eligible=False,
            candidate_only=True,
            release_blocking_failures=result.get("release_blocking_failures") or ["hw_check_release_gate must pass before release"],
        )

    # ------------------------------------------------------------------
    # ERC / DRC / electrical checks
    # ------------------------------------------------------------------

    @server.tool(name=_TR["hw_run_erc"].name)
    def run_erc(project: str) -> dict[str, Any]:
        report = service.kicad.run_erc(service.workspace.require_project(project))
        return report.to_dict()

    @server.tool(name=_TR["hw_run_drc"].name)
    def run_drc(project: str, profile: str = "jlcpcb_4layer") -> dict[str, Any]:
        report = service.kicad.run_drc(service.workspace.require_project(project))
        value = report.to_dict()
        value["profile"] = profile
        return value

    @server.tool(name=_TR["hw_check_electrical_semantics"].name)
    def check_electrical_semantics(project: str) -> dict[str, Any]:
        return service.validator.check_electrical_semantics(service.read_spec(project)).to_dict()

    @server.tool(name=_TR["hw_extract_electrical_graph"].name)
    def extract_electrical_graph(project: str) -> dict[str, Any]:
        path = service.workspace.require_project(project) / "electronics" / "generated" / "electrical_graph.json"
        return {"status": "generated" if path.exists() else "blocked", "graph": json.loads(path.read_text(encoding="utf-8")) if path.exists() else None}

    # ------------------------------------------------------------------
    # Fabrication exports (currently blocked — require native KiCad/CAD)
    # ------------------------------------------------------------------

    @server.tool(name=_TR["hw_export_pcb_fabrication"].name)
    def export_pcb_fabrication(project: str) -> dict[str, Any]:
        return {"status": "blocked", "project": project, "code": "native_kicad_export_required", "message": "Fabrication export requires a generated KiCad board that passes ERC and DRC"}

    # ------------------------------------------------------------------
    # Mechanical checks and exports
    # ------------------------------------------------------------------

    @server.tool(name=_TR["hw_check_mechanical_fit"].name)
    def check_mechanical_fit(project: str) -> dict[str, Any]:
        return service.validator.check_mechanical(service.read_spec(project)).to_dict()

    @server.tool(name=_TR["hw_import_board_step"].name)
    def import_board_step(project: str, source: str) -> dict[str, Any]:
        return {"status": "blocked", "project": project, "source": source, "code": "validated_step_import_not_implemented"}

    @server.tool(name=_TR["hw_export_mechanical"].name)
    def export_mechanical(project: str) -> dict[str, Any]:
        return {"status": "blocked", "project": project, "code": "native_cad_export_required", "message": "STEP/STL export requires the pinned build123d backend and geometry validation"}

    # ------------------------------------------------------------------
    # Firmware checks and build
    # ------------------------------------------------------------------

    @server.tool(name=_TR["hw_check_pinmap"].name)
    def check_pinmap(project: str) -> dict[str, Any]:
        return next(item for item in service.run_all_checks(project, include_external=False)["reports"] if item["gate"] == "firmware_pinmap")

    @server.tool(name=_TR["hw_build_firmware"].name)
    def build_firmware(project: str) -> dict[str, Any]:
        spec = service.read_spec(project)
        return service.zephyr.build(service.workspace.require_project(project), spec["firmware"]["target"]).to_dict()

    @server.tool(name=_TR["hw_generate_bringup_tests"].name)
    def generate_bringup_tests(project: str) -> dict[str, Any]:
        files = service.generate_firmware_only(project)["files"]
        return {"status": "generated", "files": [item for item in files if "test" in item]}

    # ------------------------------------------------------------------
    # Validation / repair loop
    # ------------------------------------------------------------------

    @server.tool(name=_TR["hw_run_all_checks"].name)
    def run_all_checks(project: str, include_external: bool = True) -> dict[str, Any]:
        result = service.run_all_checks(project, include_external)
        failing = [r["gate"] for r in result.get("reports", []) if r["status"] != "pass"]
        return _enrich(result, release_eligible=False, candidate_only=True,
            release_blocking_failures=failing or ["hw_check_release_gate must pass before release"])

    @server.tool(name=_TR["hw_generate_repair_plan"].name)
    def generate_repair_plan(project: str) -> dict[str, Any]:
        return service.generate_repair_plan(project)

    @server.tool(name=_TR["hw_get_failure_report"].name)
    def get_failure_report(project: str, gate: str | None = None) -> dict[str, Any]:
        directory = service.workspace.require_project(project) / "validation" / "reports"
        reports = [json.loads(item.read_text(encoding="utf-8")) for item in sorted(directory.glob("*.json")) if gate is None or item.stem == gate]
        return {"status": "pass", "project": project, "reports": reports}

    @server.tool(name=_TR["hw_apply_repair_plan"].name)
    def apply_repair_plan(project: str, approved: bool = False) -> dict[str, Any]:
        return service.apply_repair_plan(project, approved=approved)

    # ------------------------------------------------------------------
    # Design iteration
    # ------------------------------------------------------------------

    @server.tool(name=_TR["hw_run_design_iteration"].name)
    def run_design_iteration(project: str, goal: str = "make all release gates pass", include_external: bool = True) -> dict[str, Any]:
        result = service.run_design_iteration(project, include_external)
        result["goal"] = goal
        return result

    @server.tool(name=_TR["hw_design_until_release"].name)
    def design_until_release(
        project: str,
        max_iterations: int = 8,
        include_external: bool = False,
        user_approved_autonomous_iteration: bool = False,
    ) -> dict[str, Any]:
        if not user_approved_autonomous_iteration:
            return {
                "status": "blocked",
                "code": "autonomous_iteration_not_approved",
                "message": (
                    f"hw_design_until_release will run up to {max_iterations} generate→check→repair cycles "
                    "autonomously without user review of intermediate states. "
                    "Set user_approved_autonomous_iteration=true to proceed. "
                    "Use hw_run_design_iteration for a single supervised iteration instead."
                ),
                "release_eligible": False,
                "candidate_only": True,
                "release_blocking_failures": ["user_approved_autonomous_iteration must be true"],
                "iterations": [],
            }
        return service.design_until_release(project, max_iterations, include_external)

    # ------------------------------------------------------------------
    # Release gate and exports
    # ------------------------------------------------------------------

    @server.tool(name=_TR["hw_check_release_gate"].name)
    def check_release_gate(project: str) -> dict[str, Any]:
        result = service.check_release_gate(project)
        passed = result.get("status") == "pass"
        blocking = [f["message"] for f in result.get("failures", [])] if not passed else []
        return _enrich(result,
            release_eligible=passed,
            candidate_only=not passed,
            release_blocking_failures=blocking,
        )

    @server.tool(name=_TR["hw_generate_design_report"].name)
    def generate_design_report(project: str) -> dict[str, Any]:
        return service.generate_design_report(project)

    @server.tool(name=_TR["hw_export_candidate_bundle"].name)
    def export_candidate_bundle(project: str) -> dict[str, Any]:
        """Export a candidate bundle. Always candidate_only=true, release_eligible=false."""
        return service.export_candidate_bundle(project)

    # ------------------------------------------------------------------
    # Candidate lifecycle
    # ------------------------------------------------------------------

    @server.tool(name=_TR["hw_list_candidates"].name)
    def list_candidates(project: str) -> dict[str, Any]:
        return service.list_candidates(project)

    @server.tool(name=_TR["hw_get_candidate"].name)
    def get_candidate(project: str, candidate_id: str) -> dict[str, Any]:
        return service.get_candidate(project, candidate_id)

    @server.tool(name=_TR["hw_review_candidate"].name)
    def review_candidate(project: str, candidate_id: str) -> dict[str, Any]:
        return service.review_candidate(project, candidate_id)

    @server.tool(name=_TR["hw_compare_candidates"].name)
    def compare_candidates(project: str, candidate_a: str, candidate_b: str) -> dict[str, Any]:
        return service.compare_candidates(project, candidate_a, candidate_b)

    # ------------------------------------------------------------------
    # Fabrication review preparation
    # ------------------------------------------------------------------

    @server.tool(name=_TR["hw_prepare_fabrication_review"].name)
    def prepare_fabrication_review(project: str, candidate_id: str | None = None) -> dict[str, Any]:
        return service.prepare_fabrication_review(project, candidate_id)

    # ------------------------------------------------------------------
    # Environment diagnosis
    # ------------------------------------------------------------------

    @server.tool(name=_TR["hw_diagnose_environment"].name)
    def diagnose_environment(target: str = "fabrication_release", backend: str | None = None) -> dict[str, Any]:
        return service.diagnose_environment(target, backend)

    @server.tool(name=_TR["hw_export_release_bundle"].name)
    def export_release_bundle(project: str) -> dict[str, Any]:
        """Export the release bundle. Requires all gates to pass. Distinct from candidate bundles."""
        result = service.export_release_bundle(project)
        released = result.get("status") == "released"
        return _enrich(result,
            release_eligible=released,
            candidate_only=not released,
            release_blocking_failures=[] if released else ["release gate did not pass — hw_check_release_gate must pass before hw_export_release_bundle"],
        )

    @server.tool(name=_TR["hw_verify_release"].name)
    def verify_release(project: str) -> dict[str, Any]:
        spec = service.read_spec(project)
        release = service.workspace.require_project(project) / "exports" / "releases" / spec["project"]["revision"]
        result = service._artifact_integrity_report(release).to_dict()
        passed = result.get("status") == "pass"
        return _enrich(result,
            release_eligible=False,
            candidate_only=not passed,
            release_blocking_failures=[] if passed else ["artifact integrity check failed — release bundle may be incomplete or corrupt"],
        )

    # ------------------------------------------------------------------
    # Mechanical part design (agent-authored CAD)
    # ------------------------------------------------------------------

    @server.tool(name=_TR["hw_design_part"].name)
    def design_part(project: str, part_name: str, part_type: str, intent: dict) -> dict[str, Any]:
        """Design a parametric 3D-printable part from agent intent. Returns STEP/STL + printability gate."""
        return service.design_part(project, part_name, part_type, intent)

    @server.tool(name=_TR["hw_list_parts"].name)
    def list_parts(project: str) -> dict[str, Any]:
        """List all designed mechanical parts for a project."""
        return service.list_parts(project)

    @server.tool(name=_TR["hw_get_part_types"].name)
    def get_part_types() -> dict[str, Any]:
        """Return available part types and their full intent schemas."""
        return service.get_part_types()

    # ------------------------------------------------------------------
    # Platform introspection
    # ------------------------------------------------------------------

    @server.tool(name=_TR["hw_get_capabilities"].name)
    def get_capabilities() -> dict[str, Any]:
        """Return available backends, external tools, and gate enablement. Call before generating."""
        return service.get_capabilities()

    @server.tool(name=_TR["hw_review_release_readiness"].name)
    def review_release_readiness(project: str) -> dict[str, Any]:
        """Summarise release readiness from persisted reports without re-running checks."""
        return service.review_release_readiness(project)

    # ------------------------------------------------------------------
    # MCP resources — structured reads without tool invocations
    # ------------------------------------------------------------------

    @server.resource(
        "hw://project/{project}/release-gate",
        name="release-gate",
        description="Current release gate status for a project (from persisted reports).",
        mime_type="application/json",
    )
    def resource_release_gate(project: str) -> str:
        result = service.review_release_readiness(project)
        return json.dumps(result, indent=2)

    @server.resource(
        "hw://project/{project}/spec",
        name="spec",
        description="Full merged project spec.",
        mime_type="application/json",
    )
    def resource_spec(project: str) -> str:
        return json.dumps(service.read_spec(project), indent=2)

    @server.resource(
        "hw://project/{project}/requirements",
        name="requirements",
        description="Active requirements: lowered and unresolved constraints.",
        mime_type="application/json",
    )
    def resource_requirements(project: str) -> str:
        from .io import read_yaml
        req_path = service.workspace.require_project(project) / "spec" / "requirements.yaml"
        data = read_yaml(req_path) if req_path.is_file() else {}
        return json.dumps(data, indent=2)

    return server


def main() -> None:
    create_server().run()


if __name__ == "__main__":
    main()
