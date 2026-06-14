from __future__ import annotations

import json
from pathlib import Path

import pytest

from hw_codesign.errors import UnsafeChangeError
from hw_codesign.backends.freerouting import FreeroutingBackend


def test_generation_is_deterministic_and_cross_domain(service, project):
    first = service.generate_all(project)
    second = service.generate_all(project)
    assert first == second
    path = service.workspace.require_project(project)
    assert (path / "electronics" / "source" / "board.ato").is_file()
    assert (path / "mechanical" / "source" / "enclosure.py").is_file()
    assert (path / "firmware" / "generated" / "pinmap.h").is_file()
    assert (path / "exports" / "working" / "fabrication" / "bom.csv").is_file()
    routing = json.loads((path / "electronics" / "generated" / "kicad" / "routing.json").read_text())
    assert routing["mode"] == "plane_preseeded"
    assert routing["signal_routing"] == "deferred_to_freerouting"


def test_freerouting_log_parser_distinguishes_complete_and_incomplete():
    assert FreeroutingBackend._final_unrouted("final score: 988.64 (1 unrouted)\n") == 1
    assert FreeroutingBackend._final_unrouted("final score: 992.25\nSaving board\n") == 0


def test_iteration_records_reports_history_and_repair_plan(service, project):
    result = service.run_design_iteration(project, include_external=False)
    path = service.workspace.require_project(project)
    assert result["iteration_id"] == "0001"
    assert result["status"] == "blocked"
    assert "semantic_electrical" in result["failed_gates"]
    assert result["repair_plan"]["requires_user_decision"] is True
    assert (path / "history" / "iterations" / "0001" / "result.json").is_file()
    assert (path / "history" / "iterations" / "0001" / "electronics" / "source" / "board.ato").is_file()
    assert (path / "history" / "iterations" / "0001" / "firmware" / "generated" / "pinmap.h").is_file()
    log = (path / "history" / "failure_log.jsonl").read_text(encoding="utf-8")
    assert "current_budget_exceeded" in log


def test_external_backends_report_real_availability_and_violations(service, project, monkeypatch):
    service.generate_all(project)
    monkeypatch.setattr("shutil.which", lambda _: None)
    checks = service.run_all_checks(project, include_external=True)
    external = [item for item in checks["reports"] if item["gate"] in {"native_erc", "native_drc", "native_firmware_build"}]
    firmware = next(item for item in external if item["gate"] == "native_firmware_build")
    assert firmware["status"] == "blocked"
    assert firmware["failures"][0]["code"] == "tool_unavailable"
    for item in (entry for entry in external if entry["gate"] in {"native_erc", "native_drc"} and entry["status"] == "pass"):
        assert item["metrics"]["violations"] == 0
        assert item["backend"]["available"] is True


def test_design_report_states_physical_gaps(service, project):
    service.generate_all(project)
    service.run_all_checks(project, include_external=False)
    output = Path(service.generate_design_report(project)["file"])
    text = output.read_text(encoding="utf-8")
    assert "EMI/EMC" in text
    assert "instrumented hardware testing" in text


def test_safety_spec_changes_require_explicit_approval(service, project):
    with pytest.raises(UnsafeChangeError):
        service.update_spec(project, "safety", {"emergency_stop": {"required": False}})
    result = service.update_spec(project, "safety", {"emergency_stop": {"required": True}}, user_approved=True)
    assert result["user_approved"] is True


def test_design_until_release_closes_reference_pipeline(service, project):
    result = service.design_until_release(project, max_iterations=4, include_external=False)
    assert result["status"] == "released"
    bundle = Path(result["release"]["bundle"])
    assert bundle.is_file()
    release = service.workspace.require_project(project) / "exports" / "r1"
    required = [
        "fabrication/gerbers.zip", "fabrication/drill.zip", "fabrication/bom.csv",
        "fabrication/pick_and_place.csv", "mechanical/enclosure.step",
        "mechanical/enclosure.stl", "mechanical/assembly.step", "firmware/source.zip",
        "docs/schematic.pdf", "docs/validation_report.json", "docs/bringup_guide.md", "manifest.json",
    ]
    assert all((release / item).is_file() for item in required)
    assert result["iterations"][-1]["status"] == "passed"


def test_natural_language_requirements_update_structured_spec(service, project):
    result = service.update_requirements(project, "16 channel 24V battery, peak 6A, STM32H7, IMU, emergency stop, Zephyr, 6-layer")
    spec = service.read_spec(project)
    assert result["status"] == "updated"
    assert spec["actuation"]["motor_channels"] == 16
    assert spec["actuation"]["motor_channel_peak_current_a"] == 6.0
    assert spec["system"]["supply"]["battery"]["pack_voltage_nominal"] == 24.0
    assert spec["manufacturing"]["pcb"]["layers"] == 6
    assert spec["firmware"]["framework"] == "zephyr"
