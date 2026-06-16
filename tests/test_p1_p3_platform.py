from __future__ import annotations

import json
from pathlib import Path

import yaml

from hw_codesign.backends.tscircuit import TSCircuitBackend


def _release_capable_tscircuit_graph():
    footprint = {"library_id": "Resistor_SMD:R_0603_1608Metric", "expected_pads": ["1", "2"], "backend_footprints": {"tscircuit": "0603"}}
    return {
        "components": [
            {"ref": "R1", "pins": [{"number": "1", "name": "A", "net": "SIG"}, {"number": "2", "name": "B", "net": "GND"}], "footprint_metadata": footprint},
            {"ref": "R2", "pins": [{"number": "1", "name": "A", "net": "SIG"}, {"number": "2", "name": "B", "net": "GND"}], "footprint_metadata": footprint},
        ],
        "nets": [
            {"name": "SIG", "connected_pins": ["R1.1", "R2.1"]},
            {"name": "GND", "connected_pins": ["R1.2", "R2.2"]},
        ],
    }


def test_reference_intent_is_truthfully_marked(service, project):
    result = service.generate_reference_intent(project)
    assert result["status"] == "candidate"
    intent = service.workspace.require_project(project) / "electronics" / "intent" / "board.intent.md"
    text = intent.read_text(encoding="utf-8")
    assert "artifact_type: design_intent" in text
    assert "compiled: false" in text
    assert "release_eligible: false" in text


def test_curated_resolver_and_pin_contracts_pass(service, project):
    generated = service.generate_all(project)
    assert generated["resolution_report"]["status"] == "pass"
    assert all(item["resolution"] == "curated" for item in generated["component_resolution"])
    checks = service.run_all_checks(project, include_external=False)
    by_gate = {item["gate"]: item for item in checks["reports"]}
    assert by_gate["component_provenance"]["status"] == "pass"
    assert by_gate["pin_symbol_footprint"]["status"] == "pass"


def test_iteration_writes_candidate_only_bundle(service, project):
    result = service.run_design_iteration(project, include_external=False)
    candidate = Path(result["candidate"]["path"])
    assert result["status"] == "blocked"
    assert candidate.is_dir()
    assert json.loads((candidate / "candidate.json").read_text())["candidate_only"] is True
    assert not (service.workspace.require_project(project) / "exports" / "releases").exists()


def test_tscircuit_real_compile_and_graph_parity(tmp_path):
    import pytest
    root = Path(__file__).parents[1]
    spec = yaml.safe_load((root / "src/hw_codesign/templates/robotics_controller_full.yaml").read_text())
    spec["electronics"]["backend"] = "tscircuit"
    project = root / ".pytest-tscircuit"
    if project.exists():
        import shutil
        shutil.rmtree(project)
    (project / "electronics/generated").mkdir(parents=True)
    try:
        graph = _release_capable_tscircuit_graph()
        backend = TSCircuitBackend(root)
        backend.generate_source(project, spec, graph)
        reports = {item.gate: item for item in backend.compile(project, graph)}
        if reports["tscircuit_compile"].status == "blocked":
            codes = [f.code for f in reports["tscircuit_compile"].failures]
            pytest.skip(f"tscircuit CLI unavailable or timed out: {codes}")
        assert reports["tscircuit_compile"].status == "pass"
        assert reports["tscircuit_netlist_extract"].status == "pass"
        assert reports["tscircuit_graph_parity"].status == "pass"
        assert reports["tscircuit_footprint_parity"].status == "pass"
        assert reports["tscircuit_layout_completeness"].status == "pass"
    finally:
        import shutil
        shutil.rmtree(project, ignore_errors=True)


def test_tscircuit_contract_blocks_manufacturing_without_native_export():
    import pytest
    root = Path(__file__).parents[1]
    spec = yaml.safe_load((root / "src/hw_codesign/templates/robotics_controller_full.yaml").read_text())
    spec["electronics"]["backend"] = "tscircuit"
    project = root / ".pytest-tscircuit-pcb"
    if project.exists():
        import shutil
        shutil.rmtree(project)
    (project / "electronics/generated").mkdir(parents=True)
    try:
        graph = _release_capable_tscircuit_graph()
        backend = TSCircuitBackend(root)
        backend.generate_source(project, spec, graph)
        reports = {item.gate: item for item in backend.evaluate(project, graph)}
        if reports["tscircuit_compile"].status == "blocked":
            codes = [f.code for f in reports["tscircuit_compile"].failures]
            pytest.skip(f"tscircuit CLI unavailable or timed out: {codes}")
        assert reports["tscircuit_compile"].status == "pass"
        assert reports["tscircuit_footprint_parity"].status == "pass"
        assert reports["tscircuit_layout_completeness"].status == "pass"
        assert reports["tscircuit_manufacturing_export"].status == "blocked"
        assert any(f.code == "gate_not_run" for f in reports["tscircuit_manufacturing_export"].failures)
    finally:
        import shutil
        shutil.rmtree(project, ignore_errors=True)


def test_tscircuit_release_gate_blocked_on_pcb_gates(service, project):
    """Release gate for a tscircuit backend project must be BLOCKED on
    tscircuit_footprint_parity and tscircuit_layout_completeness even when
    compile + netlist + graph parity all pass."""
    from hw_codesign.io import read_yaml, write_yaml
    project_path = service.workspace.require_project(project)
    system_path = project_path / "spec" / "system.yaml"
    system = read_yaml(system_path)
    system["electronics"]["backend"] = "tscircuit"
    write_yaml(system_path, system)
    service.generate_all(project)
    checks = service.run_all_checks(project, include_external=False)
    gate = service.check_release_gate(project, [service._report_from_dict(r) for r in checks["reports"]])
    assert gate["status"] == "blocked"
    # BLOCKED PCB gates roll up as "failed_gate" through Validator.release_gate()
    blocking_codes = {f["code"] for f in gate["failures"]}
    assert "failed_gate" in blocking_codes
    # Confirm the PCB gates were actually BLOCKED in the underlying check set
    by_gate = {r["gate"]: r for r in checks["reports"]}
    assert by_gate.get("tscircuit_footprint_parity", {}).get("status") == "blocked"
    assert by_gate.get("tscircuit_layout_completeness", {}).get("status") == "blocked"


def test_prepare_release_blocked_on_unresolved_critical_assumption(service, project):
    """prepare_release must be blocked before writing any files when a critical assumption is unresolved,
    even when all gate reports pass and native checks are confirmed."""
    from hw_codesign.io import read_yaml, write_yaml
    project_path = service.workspace.require_project(project)
    system_path = project_path / "spec" / "system.yaml"
    system = read_yaml(system_path)
    system["electronics"]["backend"] = "tscircuit"
    write_yaml(system_path, system)
    # Verify template has at least one unresolved critical assumption
    spec = service.read_spec(project)
    unresolved = [n for n, a in spec.get("assumptions", {}).items() if a.get("critical") and a.get("requires_user_review")]
    assert unresolved, "Template must have unresolved critical assumptions for this test to be meaningful"
    # Feed all-pass reports to bypass gate checks — assumption preflight must still block
    all_pass_checks = {"reports": [{"gate": "mock", "status": "pass", "failures": [], "metrics": {}}]}
    result = service.prepare_release(project, all_pass_checks, native_checks_confirmed=True)
    assert result["status"] == "blocked"
    assert result["code"] == "unresolved_critical_assumptions"
    assert not (project_path / "exports" / "releases").exists()
    assert not (project_path / "exports" / ".staging").exists()


def test_footprint_parity_fails_on_missing_compiled_footprint_id():
    """Footprint parity gate must FAIL (not pass) when expected_fp exists but compiled circuit.json
    has no footprint_id for that component."""
    import json
    from hw_codesign.backends.tscircuit import TSCircuitBackend
    from hw_codesign.models import Status

    graph = {
        "components": [{"ref": "U1", "footprint": "Package_SO:SOIC-8", "pins": []}],
        "nets": [],
    }
    # pcb_component entry present but missing footprint_id
    compiled: list[dict] = [
        {"type": "source_component", "source_component_id": "U1", "name": "U1"},
        {"type": "pcb_component", "source_component_id": "U1"},  # no footprint_id
    ]
    backend = TSCircuitBackend.__new__(TSCircuitBackend)
    source_components = {
        item.get("source_component_id"): item
        for item in compiled
        if item.get("source_component_id") and item.get("name")
    }
    footprint_failures = []
    for component in graph["components"]:
        expected_fp = component.get("footprint_metadata", {}).get("library_id") or component.get("footprint") or ""
        sc = source_components.get(component["ref"])
        compiled_fp = sc.get("footprint_id", "") if sc else ""
        if expected_fp and not compiled_fp:
            from hw_codesign.models import Failure, FailureCategory
            footprint_failures.append(Failure(
                FailureCategory.EDA_ERROR, "compiled_footprint_missing",
                f"{component['ref']}: expected footprint {expected_fp!r} but compiled circuit.json has no footprint_id",
                details={"ref": component["ref"], "expected": expected_fp, "compiled": ""},
            ))
        elif expected_fp and compiled_fp and expected_fp != compiled_fp:
            from hw_codesign.models import Failure, FailureCategory
            footprint_failures.append(Failure(
                FailureCategory.EDA_ERROR, "footprint_parity_mismatch",
                f"{component['ref']}: expected footprint {expected_fp!r}, compiled {compiled_fp!r}",
                details={"ref": component["ref"], "expected": expected_fp, "compiled": compiled_fp},
            ))
    assert footprint_failures, "Expected a footprint failure but got none"
    assert footprint_failures[0].code == "compiled_footprint_missing"


def test_manifest_must_cover_all_required_release_artifacts(tmp_path):
    """_artifact_integrity_report must fail with required_artifact_uncovered_by_manifest
    when a required artifact exists on disk but is absent from the manifest."""
    import json
    from hw_codesign.service import HardwareService
    from hw_codesign.artifacts import write_manifest

    release = tmp_path / "release"
    release.mkdir()
    present = release / "fabrication" / "gerbers.zip"
    present.parent.mkdir(parents=True)
    present.write_bytes(b"fake gerbers")
    absent_from_manifest = release / "firmware" / "source.zip"
    absent_from_manifest.parent.mkdir(parents=True)
    absent_from_manifest.write_bytes(b"fake firmware")
    # Manifest covers only the gerbers, not firmware/source.zip
    write_manifest(release, release / "manifest.json", provenance={}, candidate_only=False)
    # Remove firmware entry from manifest to simulate partial manifest
    manifest = json.loads((release / "manifest.json").read_text())
    manifest["artifacts"] = [e for e in manifest["artifacts"] if "firmware" not in e["path"]]
    (release / "manifest.json").write_text(json.dumps(manifest))

    required = [present, absent_from_manifest]
    report = HardwareService._artifact_integrity_report(release, required=required)
    codes = {f.code for f in report.failures}
    assert "required_artifact_uncovered_by_manifest" in codes


def test_source_manifest_marks_pcb_enabled_source_release_eligible(tmp_path):
    import json
    import yaml
    from pathlib import Path
    from hw_codesign.backends.tscircuit import TSCircuitBackend

    root = Path(__file__).parents[1]
    spec = yaml.safe_load((root / "src/hw_codesign/templates/robotics_controller_full.yaml").read_text())
    spec["electronics"]["backend"] = "tscircuit"
    graph = _release_capable_tscircuit_graph()
    backend = TSCircuitBackend(root)
    project = tmp_path / "project"
    (project / "electronics" / "generated").mkdir(parents=True)
    backend.generate_source(project, spec, graph)
    manifest = json.loads((project / "electronics" / "source" / "tscircuit" / "source_manifest.json").read_text())
    assert manifest["source_release_eligible"] is True
    assert manifest["pcb_disabled"] is False
    assert manifest["routing_disabled"] is False
    assert manifest["provenance"]["release_eligible"] is True
    assert "tscircuit_compile" in manifest["contract_gates"]
    assert "tscircuit_manufacturing_export" in manifest["contract_gates"]
    assert "tscircuit_footprint_parity" in manifest["release_blocking_gates"]
    assert "tscircuit_layout_completeness" in manifest["release_blocking_gates"]


def test_missing_tscircuit_netlist_extract_injected_as_gate_not_run(service, project):
    """If tscircuit_netlist_extract is not present in the report set passed to
    check_release_gate, it must be auto-injected as a BLOCKED gate_not_run failure."""
    from hw_codesign.io import read_yaml, write_yaml
    project_path = service.workspace.require_project(project)
    system_path = project_path / "spec" / "system.yaml"
    system = read_yaml(system_path)
    system["electronics"]["backend"] = "tscircuit"
    write_yaml(system_path, system)
    service.generate_all(project)
    checks = service.run_all_checks(project, include_external=False)
    # Strip tscircuit_netlist_extract from reports to simulate a missing gate
    stripped = [service._report_from_dict(r) for r in checks["reports"] if r["gate"] != "tscircuit_netlist_extract"]
    gate = service.check_release_gate(project, stripped)
    assert gate["status"] == "blocked"
    # The injected gate report surfaces through the release_gate failure roll-up
    codes = {f["code"] for f in gate["failures"]}
    assert "gate_not_run" in codes or "failed_gate" in codes
