from __future__ import annotations

from hw_codesign.models import Failure, FailureCategory, GateReport, Status


# ── Fix 1: BLOCKED → PASS masquerade ─────────────────────────────────────────

def test_blocked_native_mechanical_stays_blocked_in_prepare_release(service, project, monkeypatch):
    """When native mechanical backend returns BLOCKED and require_native=True, that status must
    not be promoted to PASS."""
    service.generate_all(project)
    checks = service.run_all_checks(project, include_external=False)
    monkeypatch.setattr(
        service.mechanical,
        "generate",
        lambda spec, release: GateReport(
            "mechanical_export",
            Status.BLOCKED,
            [Failure(FailureCategory.TOOL_ERROR, "tool_unavailable", "cadquery-ocp not installed")],
        ),
    )
    result = service.prepare_release(project, checks, require_native=True)
    reports_by_gate = {r["gate"]: r for r in result["reports"]}
    assert reports_by_gate["mechanical_export"]["status"] == "blocked"


def test_blocked_native_fabrication_stays_blocked_in_prepare_release(service, project, monkeypatch):
    """When KiCad export_manufacturing is BLOCKED and require_native=True, fabrication must
    not be promoted to PASS."""
    service.generate_all(project)
    checks = service.run_all_checks(project, include_external=False)
    monkeypatch.setattr(
        service.kicad,
        "export_manufacturing",
        lambda path, release: GateReport(
            "fabrication_export",
            Status.BLOCKED,
            [Failure(FailureCategory.TOOL_ERROR, "tool_unavailable", "KiCad not installed")],
        ),
    )
    result = service.prepare_release(project, checks, require_native=True)
    reports_by_gate = {r["gate"]: r for r in result["reports"]}
    assert reports_by_gate["fabrication_export"]["status"] == "blocked"


def test_reference_mode_prepare_release_passes_without_native_tools(service, project):
    """When require_native=False (reference mode), prepare_release must return PASS for both
    mechanical and fabrication even when no native tools are installed."""
    service.generate_all(project)
    checks = service.run_all_checks(project, include_external=False)
    result = service.prepare_release(project, checks, require_native=False)
    reports_by_gate = {r["gate"]: r for r in result["reports"]}
    assert reports_by_gate["mechanical_export"]["status"] == "pass"
    assert reports_by_gate["fabrication_export"]["status"] == "pass"


# ── Fix 2: Critical assumption auto-resolve ───────────────────────────────────

def test_apply_repair_plan_does_not_resolve_user_review_assumptions(service, project):
    """apply_repair_plan must not auto-resolve assumptions flagged requires_user_review=True."""
    service.generate_all(project)
    checks = service.run_all_checks(project, include_external=False)
    spec_before = service.read_spec(project)
    needs_review = {
        name
        for name, val in spec_before.get("assumptions", {}).items()
        if val.get("requires_user_review")
    }
    assert needs_review, "Template must have critical assumptions for this test to be meaningful"

    service.apply_repair_plan(project, checks)

    spec_after = service.read_spec(project)
    for name in needs_review:
        assert spec_after["assumptions"][name].get("requires_user_review") is True, (
            f"apply_repair_plan silently resolved assumption '{name}' without user approval"
        )


# ── Fix 3: Candidate artifacts in release path ───────────────────────────────

def test_failed_design_iteration_does_not_write_to_release_directory(service, project):
    """A design iteration that does not pass all gates must not write to exports/<revision>/."""
    spec = service.read_spec(project)
    revision = spec["project"]["revision"]
    release_path = service.workspace.require_project(project) / "exports" / revision

    result = service.run_design_iteration(project, include_external=False)

    assert result["status"] != "passed", "First iteration should not pass"
    assert not release_path.exists(), (
        f"Release directory {release_path} was populated during a failed iteration"
    )


# ── Fix 4: Gate name disambiguation ──────────────────────────────────────────

def test_reference_host_firmware_build_has_distinct_gate_name(service, project):
    """Reference host CMake firmware build must be named 'host_firmware_build', not
    the ambiguous 'firmware_build' shared with the Zephyr native gate."""
    service.generate_all(project)
    checks = service.run_all_checks(project, include_external=False)
    gate_names = {r["gate"] for r in checks["reports"]}

    assert "host_firmware_build" in gate_names
    assert "firmware_build" not in gate_names


# ── Fix 5: Domain generate side effects ──────────────────────────────────────

def test_generate_electronics_only_does_not_touch_firmware_files(service, project):
    """generate_electronics_only must not regenerate firmware files as a side effect."""
    service.generate_all(project)
    pinmap = service.workspace.require_project(project) / "firmware" / "generated" / "pinmap.h"
    sentinel = "/* sentinel — must not be overwritten */\n"
    pinmap.write_text(sentinel, encoding="utf-8")

    service.generate_electronics_only(project)

    assert pinmap.read_text(encoding="utf-8") == sentinel


def test_generate_firmware_only_does_not_touch_electronics_files(service, project):
    """generate_firmware_only must not regenerate electronics files as a side effect."""
    service.generate_all(project)
    graph = (
        service.workspace.require_project(project)
        / "electronics"
        / "generated"
        / "electrical_graph.json"
    )
    sentinel = '{"sentinel": true}\n'
    graph.write_text(sentinel, encoding="utf-8")

    service.generate_firmware_only(project)

    assert graph.read_text(encoding="utf-8") == sentinel


def test_generate_mechanical_only_does_not_touch_electronics_or_firmware(service, project):
    """generate_mechanical_only must not regenerate electronics or firmware files."""
    service.generate_all(project)
    graph = (
        service.workspace.require_project(project)
        / "electronics"
        / "generated"
        / "electrical_graph.json"
    )
    pinmap = service.workspace.require_project(project) / "firmware" / "generated" / "pinmap.h"
    graph.write_text('{"sentinel": true}\n', encoding="utf-8")
    pinmap.write_text("/* sentinel */\n", encoding="utf-8")

    service.generate_mechanical_only(project)

    assert graph.read_text(encoding="utf-8") == '{"sentinel": true}\n'
    assert pinmap.read_text(encoding="utf-8") == "/* sentinel */\n"
