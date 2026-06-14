from __future__ import annotations


def test_template_schema_is_valid_but_semantic_budget_fails(service, project):
    spec = service.read_spec(project)
    schema = service.validator.validate_spec(spec)
    semantic = service.validator.check_electrical_semantics(spec)
    assert schema.status == "pass"
    assert semantic.status == "fail"
    assert {item.code for item in semantic.failures} == {"current_budget_exceeded"}


def test_mechanical_clearance_passes_template(service, project):
    report = service.validator.check_mechanical(service.read_spec(project))
    assert report.status == "pass"


def test_pin_conflicts_and_net_mismatches_are_reported(service):
    report = service.validator.check_pinmap([
        {"signal": "I2C_SCL", "mcu_pin": "GPIO9", "net_name": "I2C_SCL"},
        {"signal": "MOTOR3_PWM", "mcu_pin": "GPIO9", "net_name": "PWM_WRONG"},
    ])
    assert report.status == "fail"
    assert {item.code for item in report.failures} == {"pin_conflict", "peripheral_mismatch"}


def test_release_rejects_unresolved_assumptions_and_missing_exports(service, project):
    service.generate_all(project)
    checks = service.run_all_checks(project, include_external=False)
    release = service.check_release_gate(project, [service._report_from_dict(item) for item in checks["reports"]])
    codes = {item["code"] for item in release["failures"]}
    assert release["status"] == "blocked"
    assert "unresolved_critical_assumption" in codes
    assert "missing_export" in codes


def test_bom_requires_approved_mpns(service):
    report = service.validator.check_bom([{"ref": "U1", "mpn": None}, {"ref": "R1", "mpn": "RC0603FR-0710KL"}])
    assert report.status == "fail"
    assert [item.code for item in report.failures] == ["missing_mpn"]
