from __future__ import annotations

import json


def test_mini_servo_robot_template_is_discoverable_and_copies_local_parts(service):
    assert "mini_servo_robot" in service.get_capabilities()["templates"]
    service.create_project("mini_servo_template", template="mini_servo_robot")
    path = service.workspace.require_project("mini_servo_template")

    assert (path / "parts.local.yaml").is_file()
    spec = service.read_spec("mini_servo_template")
    assert spec["actuation"]["motor_channels"] == 6
    assert spec["system"]["supply"]["battery"]["pack_voltage_nominal"] == 7.4
    assert {rail["name"] for rail in spec["system"]["supply"]["rails"]} == {"USB_VBUS", "V3V3", "SERVO_V5"}
    assert len(spec["placement"]["constraints"]) == 4


def test_mini_servo_robot_generates_power_pwm_imu_and_six_distinct_headers(service):
    project = "mini_servo_graph"
    service.create_project(project, template="mini_servo_robot")
    result = service.generate_electronics_only(project)
    path = service.workspace.require_project(project)
    graph = json.loads((path / "electronics" / "generated" / "electrical_graph.json").read_text(encoding="utf-8"))
    by_ref = {item["ref"]: item for item in graph["components"]}
    nets = {item["name"]: set(item["connected_pins"]) for item in graph["nets"]}

    assert result["resolution_report"]["status"] == "pass"
    assert graph["design_basis"]["servo_channels"] == 6
    assert graph["design_basis"]["logic_servo_power_domains_separated"] is True
    assert by_ref["U21"]["component_id"] == "project_pca9685pw"
    assert by_ref["U3"]["category"] == "imu"
    assert {"J20.1", "F20.1"} <= nets["VBAT_RAW"]
    assert {"F20.2", "U20.1"} <= nets["VBAT_FUSED"]
    assert {"U20.3", "C20.1", "J21.2", "J26.2"} <= nets["SERVO_V5"]
    assert {"U21.2", "U20.2", "J21.3", "J26.3", "U3.7"} <= nets["GND"]

    headers = [by_ref[f"J{index}"] for index in range(21, 27)]
    positions = {tuple(item["pcb_position_mm"]) for item in headers}
    assert len(positions) == 6
    assert all(item["resolution"] == "project_owned" for item in headers)
    assert not graph["placement"].get("failures")


def test_mini_servo_robot_contract_includes_current_budget_decoupling_and_fail_safe(service):
    project = "mini_servo_contract"
    service.create_project(project, template="mini_servo_robot")
    service.generate_all(project)
    spec = service.read_spec(project)
    path = service.workspace.require_project(project)
    graph = json.loads((path / "electronics" / "generated" / "electrical_graph.json").read_text(encoding="utf-8"))
    by_ref = {item["ref"]: item for item in graph["components"]}

    declared_peak = spec["actuation"]["motor_channel_peak_current_a"] * spec["actuation"]["max_simultaneous_peak_channels"]
    servo_rail = next(rail for rail in spec["system"]["supply"]["rails"] if rail["name"] == "SERVO_V5")
    assert declared_peak == 6.0
    assert servo_rail["current_peak_a"] >= declared_peak
    assert by_ref["C20"]["value"].startswith("1000uF")
    assert by_ref["C21"]["value"].startswith("100nF")
    assert {module["id"] for module in spec["firmware"]["modules"]} >= {"pca9685_servo_pwm", "servo_safety_watchdog", "lsm6dsox_driver"}
    assert spec["safety"]["emergency_stop"]["fail_safe_hardware_path"] is True
    assert {constraint["relationship"] for constraint in spec["placement"]["constraints"]} == {"adjacent_to", "thermal_separation"}
