from __future__ import annotations

from pathlib import Path

from hw_codesign.service import _BENCHMARK_SPECS, HardwareService

# ---------------------------------------------------------------------------
# Benchmark spec catalogue integrity
# ---------------------------------------------------------------------------

def test_benchmark_specs_non_empty():
    assert len(_BENCHMARK_SPECS) >= 3, "Benchmark suite must have at least 3 reference designs"


def test_benchmark_specs_all_have_required_keys():
    for spec in _BENCHMARK_SPECS:
        assert "id" in spec and "template" in spec and "intent" in spec, f"Spec missing required key: {spec}"


def test_benchmark_spec_ids_unique():
    ids = [s["id"] for s in _BENCHMARK_SPECS]
    assert len(ids) == len(set(ids)), "Benchmark spec IDs must be unique"


def test_benchmark_spec_ids_valid_project_name_stem():
    import re
    # After prefixing with "bench_" + suffix each must match the workspace regex
    stem_re = re.compile(r"^[a-z][a-z0-9_]+$")
    for spec in _BENCHMARK_SPECS:
        assert stem_re.fullmatch(spec["id"]), f"Spec id {spec['id']!r} is not a valid name stem"


def test_benchmark_spec_intents_non_empty():
    for spec in _BENCHMARK_SPECS:
        assert spec["intent"].strip(), f"Intent must not be empty for spec {spec['id']!r}"


def test_benchmark_templates_are_supported(service: HardwareService):
    from hw_codesign.workspace import SUPPORTED_TEMPLATES
    for spec in _BENCHMARK_SPECS:
        assert spec["template"] in SUPPORTED_TEMPLATES, (
            f"Spec {spec['id']!r} references unsupported template {spec['template']!r}"
        )


# ---------------------------------------------------------------------------
# run_design_benchmark structural contract
# ---------------------------------------------------------------------------

def test_run_design_benchmark_returns_required_keys(service: HardwareService):
    result = service.run_design_benchmark(include_external=False)
    assert "status" in result
    assert "benchmark" in result
    assert "summary" in result
    assert "specs" in result
    assert result["benchmark"] == "design_benchmark_v0"


def test_run_design_benchmark_status_is_valid_enum(service: HardwareService):
    result = service.run_design_benchmark(include_external=False)
    assert result["status"] in {"pass", "fail", "partial"}


def test_run_design_benchmark_summary_counts_consistent(service: HardwareService):
    result = service.run_design_benchmark(include_external=False)
    summary = result["summary"]
    assert summary["total"] == len(_BENCHMARK_SPECS)
    assert summary["passed"] + summary["failed"] == summary["total"]
    assert 0.0 <= summary["pass_rate"] <= 1.0


def test_run_design_benchmark_specs_count_matches_suite(service: HardwareService):
    result = service.run_design_benchmark(include_external=False)
    assert len(result["specs"]) == len(_BENCHMARK_SPECS)


def test_run_design_benchmark_spec_results_have_required_keys(service: HardwareService):
    result = service.run_design_benchmark(include_external=False)
    for spec_result in result["specs"]:
        assert "id" in spec_result
        assert "template" in spec_result
        assert "intent" in spec_result
        assert "status" in spec_result
        assert "iterations" in spec_result
        assert "gate_summary" in spec_result


def test_run_design_benchmark_spec_ids_match_suite(service: HardwareService):
    result = service.run_design_benchmark(include_external=False)
    expected_ids = {s["id"] for s in _BENCHMARK_SPECS}
    result_ids = {r["id"] for r in result["specs"]}
    assert result_ids == expected_ids


def test_run_design_benchmark_saves_artifact(service: HardwareService):
    result = service.run_design_benchmark(include_external=False)
    assert "artifact" in result
    artifact_path = Path(result["artifact"])
    assert artifact_path.is_file(), f"Benchmark artifact must exist at {artifact_path}"


def test_run_design_benchmark_artifact_is_json(service: HardwareService):
    import json
    result = service.run_design_benchmark(include_external=False)
    artifact_path = Path(result["artifact"])
    data = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert data["benchmark"] == "design_benchmark_v0"
    assert "summary" in data


def test_run_design_benchmark_cleans_up_projects_by_default(service: HardwareService):
    service.run_design_benchmark(include_external=False)
    # After benchmark with keep_projects=False, no bench_ projects should remain
    projects = service.workspace.list_projects()
    bench_projects = [p for p in projects if p.startswith("bench_")]
    assert bench_projects == [], f"Benchmark left behind projects: {bench_projects}"


def test_run_design_benchmark_keep_projects_preserves_them(service: HardwareService):
    service.run_design_benchmark(include_external=False, keep_projects=True)
    projects = service.workspace.list_projects()
    bench_projects = [p for p in projects if p.startswith("bench_")]
    assert len(bench_projects) == len(_BENCHMARK_SPECS), (
        f"Expected {len(_BENCHMARK_SPECS)} bench projects, got {bench_projects}"
    )


def test_run_design_benchmark_multiple_runs_produce_separate_artifacts(service: HardwareService):
    r1 = service.run_design_benchmark(include_external=False)
    r2 = service.run_design_benchmark(include_external=False)
    assert r1["artifact"] != r2["artifact"], "Each benchmark run must produce a distinct artifact file"


def test_run_design_benchmark_mean_iterations_non_negative(service: HardwareService):
    result = service.run_design_benchmark(include_external=False)
    assert result["summary"]["mean_iterations"] >= 0


def test_run_design_benchmark_each_spec_has_non_negative_iterations(service: HardwareService):
    result = service.run_design_benchmark(include_external=False)
    for spec_result in result["specs"]:
        assert spec_result["iterations"] >= 0, f"Iterations must be >= 0 for {spec_result['id']!r}"


def test_run_design_benchmark_status_reflects_pass_rate(service: HardwareService):
    result = service.run_design_benchmark(include_external=False)
    summary = result["summary"]
    if summary["passed"] == summary["total"]:
        assert result["status"] == "pass"
    elif summary["passed"] == 0:
        assert result["status"] == "fail"
    else:
        assert result["status"] == "partial"


def test_run_design_benchmark_software_gate_pass_rate_in_summary(service: HardwareService):
    result = service.run_design_benchmark(include_external=False)
    summary = result["summary"]
    assert "software_gate_pass_rate" in summary
    assert 0.0 <= summary["software_gate_pass_rate"] <= 1.0


def test_run_design_benchmark_software_gate_pass_rate_per_spec(service: HardwareService):
    result = service.run_design_benchmark(include_external=False)
    for spec_result in result["specs"]:
        if spec_result["status"] != "error":
            assert "software_gate_pass_rate" in spec_result
            assert 0.0 <= spec_result["software_gate_pass_rate"] <= 1.0


def test_run_design_benchmark_software_gate_pass_rate_non_zero_for_valid_templates(service: HardwareService):
    # Valid templates should pass most software gates; rate must be > 0
    result = service.run_design_benchmark(include_external=False)
    summary = result["summary"]
    assert summary["software_gate_pass_rate"] > 0.0, (
        f"Software gate pass rate should be > 0 for valid templates; got {summary['software_gate_pass_rate']}"
    )


def test_run_design_benchmark_software_gates_ready_in_summary(service: HardwareService):
    result = service.run_design_benchmark(include_external=False)
    summary = result["summary"]
    assert "software_gates_ready" in summary
    assert "software_gates_ready_rate" in summary
    assert 0 <= summary["software_gates_ready"] <= summary["total"]
    assert 0.0 <= summary["software_gates_ready_rate"] <= 1.0


def test_design_until_release_never_releases_without_native_gates(service: HardwareService):
    # Without include_external=True, design_until_release must never claim "released"
    service.create_project("bench_no_release_test")
    service.update_requirements("bench_no_release_test", "STM32H7 motor controller 12 channels 24V")
    result = service.design_until_release("bench_no_release_test", include_external=False)
    assert result["status"] != "released", (
        "design_until_release must not claim released without native gates (include_external=False)"
    )


def test_design_until_release_software_gates_ready_contract(service: HardwareService):
    # If design_until_release returns software_gates_ready, it must carry the required fields
    service.create_project("bench_sw_ready_test")
    result = service.design_until_release("bench_sw_ready_test", include_external=False)
    if result["status"] == "software_gates_ready":
        assert "pending_external_gates" in result, "software_gates_ready must carry pending_external_gates"
        assert "message" in result, "software_gates_ready must carry a message"
        assert isinstance(result["pending_external_gates"], list)
        assert len(result["pending_external_gates"]) > 0, "Must name at least one pending external gate"


def test_run_design_benchmark_native_gate_pass_rate_in_summary(service: HardwareService):
    result = service.run_design_benchmark(include_external=False)
    summary = result["summary"]
    assert "native_gate_pass_rate" in summary, "Summary must include native_gate_pass_rate"
    assert 0.0 <= summary["native_gate_pass_rate"] <= 1.0


def test_run_design_benchmark_native_gate_pass_rate_per_spec(service: HardwareService):
    result = service.run_design_benchmark(include_external=False)
    for spec_result in result["specs"]:
        if spec_result["status"] != "error":
            assert "native_gate_pass_rate" in spec_result, f"Spec {spec_result.get('id')!r} missing native_gate_pass_rate"
            assert 0.0 <= spec_result["native_gate_pass_rate"] <= 1.0


def test_run_design_benchmark_gate_counts_per_spec(service: HardwareService):
    result = service.run_design_benchmark(include_external=False)
    for spec_result in result["specs"]:
        if spec_result["status"] != "error":
            assert "gates_passed_count" in spec_result
            assert "gates_failed_count" in spec_result
            assert spec_result["gates_passed_count"] >= 0
            assert spec_result["gates_failed_count"] >= 0


def test_run_design_benchmark_tracks_physical_qualification_gaps(service: HardwareService):
    result = service.run_design_benchmark(include_external=False)
    summary = result["summary"]

    assert summary["physical_qualification_required_tests"] >= len(_BENCHMARK_SPECS)
    assert summary["physical_qualification_missing_or_unapproved"] >= len(_BENCHMARK_SPECS)
    assert summary["physical_qualification_ready"] == 0
    assert summary["physical_qualification_ready_rate"] == 0.0
    assert summary["physical_qualification_gap_categories"]


def test_run_design_benchmark_physical_summary_per_spec(service: HardwareService):
    result = service.run_design_benchmark(include_external=False)
    for spec_result in result["specs"]:
        if spec_result["status"] == "error":
            continue
        physical = spec_result["physical_qualification_summary"]
        assert physical["status"] == "blocked"
        assert physical["required_tests"] > 0
        assert physical["missing_or_unapproved"] > 0
        assert "gate" in physical
        assert physical["gate"]["gate"] == "physical_qualification"
