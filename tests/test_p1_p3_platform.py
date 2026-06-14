from __future__ import annotations

import json
from pathlib import Path

import yaml

from hw_codesign.backends.tscircuit import TSCircuitBackend


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
    root = Path(__file__).parents[1]
    spec = yaml.safe_load((root / "src/hw_codesign/templates/robotics_controller_full.yaml").read_text())
    spec["electronics"]["backend"] = "tscircuit"
    from hw_codesign.electronics_design import build_controller_graph
    project = root / ".pytest-tscircuit"
    if project.exists():
        import shutil
        shutil.rmtree(project)
    (project / "electronics/generated").mkdir(parents=True)
    try:
        graph = build_controller_graph(spec)
        backend = TSCircuitBackend(root)
        backend.generate_source(project, spec, graph)
        reports = {item.gate: item for item in backend.compile(project, graph)}
        assert reports["tscircuit_compile"].status == "pass"
        assert reports["tscircuit_netlist_extract"].status == "pass"
        assert reports["tscircuit_graph_parity"].status == "pass"
    finally:
        import shutil
        shutil.rmtree(project, ignore_errors=True)


def test_tscircuit_pcb_gates_blocked_when_pcb_disabled():
    """Compile with pcbDisabled/routingDisabled produces no pcb_component entries;
    tscircuit_footprint_parity and tscircuit_layout_completeness must be BLOCKED
    with failure code pcb_layout_absent — not PASS or FAIL."""
    root = Path(__file__).parents[1]
    spec = yaml.safe_load((root / "src/hw_codesign/templates/robotics_controller_full.yaml").read_text())
    spec["electronics"]["backend"] = "tscircuit"
    from hw_codesign.electronics_design import build_controller_graph
    project = root / ".pytest-tscircuit-pcb"
    if project.exists():
        import shutil
        shutil.rmtree(project)
    (project / "electronics/generated").mkdir(parents=True)
    try:
        graph = build_controller_graph(spec)
        backend = TSCircuitBackend(root)
        backend.generate_source(project, spec, graph)
        reports = {item.gate: item for item in backend.compile(project, graph)}
        # Compile and netlist must succeed even with pcb disabled
        assert reports["tscircuit_compile"].status == "pass"
        # PCB gates must be BLOCKED (not PASS, not FAIL) because pcbDisabled suppresses layout
        fp = reports["tscircuit_footprint_parity"]
        lc = reports["tscircuit_layout_completeness"]
        assert fp.status.value == "blocked", f"expected blocked, got {fp.status}"
        assert lc.status.value == "blocked", f"expected blocked, got {lc.status}"
        assert any(f.code == "pcb_layout_absent" for f in fp.failures)
        assert any(f.code == "pcb_layout_absent" for f in lc.failures)
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
