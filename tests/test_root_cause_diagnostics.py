from __future__ import annotations

from hw_codesign.diagnostics import analyze_root_causes
from hw_codesign.review_report import render_html


def _report(gate: str, status: str, code: str, message: str, details: dict | None = None) -> dict:
    return {
        "gate": gate,
        "status": status,
        "failures": [{
            "category": "BOM_ERROR",
            "code": code,
            "message": message,
            "severity": "error",
            "details": details or {},
            "requires_user_decision": False,
        }],
        "metrics": {},
        "artifacts": [],
        "backend": {},
    }


def test_root_cause_analysis_folds_dependency_cascade():
    reports = [
        _report("component_resolution", "fail", "component_missing", "PCA9685 metadata is missing"),
        _report("component_provenance", "blocked", "compile_prerequisite_failed", "prerequisite component_resolution", {"prerequisite": "component_resolution"}),
        _report("pin_symbol_footprint", "blocked", "compile_prerequisite_failed", "prerequisite component_provenance", {"prerequisite": "component_provenance"}),
        _report("placement_constraints", "blocked", "compile_prerequisite_failed", "prerequisite pin_symbol_footprint", {"prerequisite": "pin_symbol_footprint"}),
        _report("ir_pcb_sanity", "blocked", "compile_prerequisite_failed", "prerequisite placement_constraints", {"prerequisite": "placement_constraints"}),
        _report("release", "blocked", "failed_gate", "Required gate did not pass: ir_pcb_sanity"),
    ]

    analysis = analyze_root_causes(reports)

    assert analysis["repair_order"] == ["component_resolution"]
    assert analysis["root_cause_count"] == 1
    assert analysis["folded_gate_count"] == 5
    assert analysis["top_root_causes"][0]["failure_codes"] == ["component_missing"]
    assert {"component_provenance", "pin_symbol_footprint", "placement_constraints", "ir_pcb_sanity"} <= set(analysis["top_root_causes"][0]["affected_gates"])


def test_review_first_actions_show_top_root_causes_not_downstream_noise():
    reports = [
        _report("component_resolution", "fail", "component_missing", "PCA9685 metadata is missing"),
        _report("placement_constraints", "blocked", "compile_prerequisite_failed", "prerequisite component_resolution", {"prerequisite": "component_resolution"}),
        _report("release", "blocked", "failed_gate", "Required gate did not pass: placement_constraints"),
    ]
    analysis = analyze_root_causes(reports)
    bundle = {
        "bundle_hash": "abc123",
        "generated_at": "2026-07-14T00:00:00+00:00",
        "project": {"name": "robot", "revision": "r1", "target_use": "candidate", "backend": "reference"},
        "gate_reports": reports,
        "root_cause_analysis": analysis,
        "summary": {"total": 3, "pass": 0, "fail": 1, "blocked": 2, "other": 0},
    }

    html = render_html(bundle)
    action_list = html.split('<div id="action-list" class="action-list">', 1)[1].split("</div>", 1)[0]

    assert "Root cause #1" in action_list
    assert 'data-title="component resolution"' in action_list
    assert 'data-title="placement constraints"' not in action_list
    assert 'data-title="release"' not in action_list
    assert "affects 2 downstream gates" in action_list
