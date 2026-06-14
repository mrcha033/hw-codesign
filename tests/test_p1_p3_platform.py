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
