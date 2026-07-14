from __future__ import annotations

import json


def _registration(component_id: str = "project_pca9685") -> dict:
    return {
        "id": component_id,
        "role": "servo_pwm_controller",
        "rationale": "Project-owned PWM module with reviewed pin and footprint contract",
        "mpn": "PCA9685PW-MODULE",
        "manufacturer": "Project approved module vendor",
        "package": "MODULE-4PIN",
        "symbol": {"library_id": "Project:PCA9685_Module", "verified": True, "expected_pins": ["1", "2", "3", "4"]},
        "footprint": {"library_id": "Project:PCA9685_Module_4Pin", "verified": True, "expected_pads": ["1", "2", "3", "4"]},
        "pins": [
            {"number": "1", "name": "VCC", "electrical_type": "power_in", "voltage_domain": "V3V3", "current_limit_a": 0.1},
            {"number": "2", "name": "GND", "electrical_type": "power_in", "voltage_domain": "GND", "current_limit_a": 2.0},
            {"number": "3", "name": "SCL", "electrical_type": "input", "voltage_domain": "V3V3", "current_limit_a": 0.01},
            {"number": "4", "name": "SDA", "electrical_type": "bidirectional", "voltage_domain": "V3V3", "current_limit_a": 0.01},
        ],
        "electrical_ratings": {
            "supply_voltage_min_v": 2.3,
            "supply_voltage_max_v": 5.5,
            "current_continuous_a": 0.1,
            "current_peak_a": 0.2,
        },
        "mechanical": {"body_mm": [25.0, 15.0], "height_mm": 8.0, "model": None, "mounting_holes": []},
        "validation": {
            "status": "approved",
            "reviewer": "project_owner",
            "reviewed_at": "2026-07-14",
            "rules": [
                {"id": "pins", "kind": "pin_contract", "status": "pass", "constraint": "Pins match reviewed module header", "evidence": ["module drawing"]},
                {"id": "rating", "kind": "electrical_rating", "status": "pass", "constraint": "Logic supply remains within 2.3-5.5 V", "evidence": ["datasheet"]},
                {"id": "footprint", "kind": "footprint", "status": "pass", "constraint": "Pad numbering matches header", "evidence": ["footprint review"]},
                {"id": "body", "kind": "mechanical", "status": "pass", "constraint": "Body envelope fits keepout", "evidence": ["module drawing"]},
            ],
        },
        "lifecycle": "active",
        "sourcing": {
            "status": "waived",
            "supplier_skus": [],
            "waiver": {
                "reason": "Project-owned module purchase",
                "risk": "Vendor stock is not tracked by the central catalog",
                "mitigation": "Verify module identity at receiving inspection",
                "approved_by": "project_owner",
                "approved_at": "2026-07-14",
                "required_reviews": ["incoming_inspection"],
            },
        },
        "constraints": ["project_owned_module"],
        "review_status": "approved",
    }


def test_register_project_part_persists_formal_contract(service, project):
    result = service.register_project_part(project, _registration())
    listing = service.list_project_parts(project)

    assert result["status"] == "generated"
    assert listing["status"] == "pass"
    assert listing["roles"]["servo_pwm_controller"]["resolution"] == "project_owned"
    assert listing["components"][0]["electrical_ratings"]["current_peak_a"] == 0.2
    assert listing["components"][0]["mechanical"]["body_mm"] == [25.0, 15.0]
    assert listing["components"][0]["validation"]["status"] == "approved"


def test_project_owned_part_resolves_without_central_catalog_edit(service, project):
    service.register_project_part(project, _registration())
    service.add_circuit_block(project, {
        "ref": "U20",
        "role": "servo_pwm_controller",
        "category": "servo_pwm_controller",
        "connections": {"VCC": "V3V3", "GND": "GND", "SCL": "I2C_SCL", "SDA": "I2C_SDA"},
    })

    result = service.generate_electronics_only(project)
    graph_path = service.workspace.require_project(project) / "electronics" / "generated" / "electrical_graph.json"
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    local = next(item for item in graph["components"] if item["ref"] == "U20")

    assert result["resolution_report"]["status"] == "pass"
    assert local["resolution"] == "project_owned"
    assert local["component_id"] == "project_pca9685"
    assert local["resolution_provenance"]["ownership"] == "project"
    assert graph["component_resolution_report"]["metrics"]["project_owned"] == 1


def test_invalid_project_part_is_rejected_before_file_write(service, project):
    invalid = _registration("bad_part")
    invalid["validation"]["rules"] = []

    try:
        service.register_project_part(project, invalid)
    except ValueError as exc:
        assert "Invalid project part registration" in str(exc)
    else:
        raise AssertionError("invalid registration should fail")

    assert not (service.workspace.require_project(project) / "parts.local.yaml").exists()
