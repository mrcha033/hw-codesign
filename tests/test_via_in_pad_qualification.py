from __future__ import annotations

from copy import deepcopy


def test_rp2040_template_declares_unselected_unqualified_via_in_pad(service):
    project = "rp2040_via_in_pad_declaration"
    service.create_project(project, template="rp2040_usb_device")
    spec = service.read_spec(project)

    declaration = spec["manufacturing"]["pcb"]["via_in_pad"]
    assert declaration == {
        "used": True,
        "qualification_status": "unqualified",
        "process": {
            "selection_status": "unselected",
            "via_disposition": "unselected",
            "cap_finish": "unselected",
            "fabricator_process_id": None,
        },
        "locations": [
            {
                "reference": "U2",
                "pad": "57",
                "via_count": 9,
                "purpose": "exposed_pad_ground_via_array",
                "geometry": {
                    "pattern": "square_grid",
                    "rows": 3,
                    "columns": 3,
                    "pitch_mm": 1.275,
                    "via_diameter_mm": 0.6,
                    "drill_diameter_mm": 0.35,
                },
            }
        ],
    }
    assert service.validator.validate_spec(spec).status.value == "pass"


def test_unqualified_via_in_pad_requires_process_and_yield_evidence(service):
    project = "rp2040_via_in_pad_plan"
    service.create_project(project, template="rp2040_usb_device")

    result = service.generate_physical_qualification_plan(project)

    test = next(item for item in result["plan"]["tests"] if item["id"] == "via_in_pad_process_qualification")
    assert test["required_for_release"] is True
    assert test["conditions"]["qualification_status"] == "unqualified"
    assert test["conditions"]["process_selection_status"] == "unselected"
    assert test["conditions"]["declared_via_disposition"] == "unselected"
    assert test["conditions"]["declared_cap_finish"] == "unselected"
    assert test["conditions"]["declared_locations"] == [
        {
            "reference": "U2",
            "pad": "57",
            "via_count": 9,
            "purpose": "exposed_pad_ground_via_array",
            "geometry": {
                "pattern": "square_grid",
                "rows": 3,
                "columns": 3,
                "pitch_mm": 1.275,
                "via_diameter_mm": 0.6,
                "drill_diameter_mm": 0.35,
            },
        }
    ]
    assert {
        "fabricator_via_in_pad_capability_statement",
        "microsection_or_certificate_of_conformance",
        "xray_or_equivalent_joint_inspection",
        "first_article_yield_report",
    } <= set(test["evidence_required"])
    acceptance = " ".join(test["acceptance_criteria"]).lower()
    assert all(term in acceptance for term in ("tented", "filled", "capped", "first-pass yield"))
    assert any("do not select or qualify" in boundary for boundary in result["plan"]["oracle_boundary"])

    report = service._physical_qualification_report(service.workspace.require_project(project))
    assert report.status.value == "blocked"
    assert any(
        failure.code == "physical_evidence_missing"
        and failure.path == "validation.physical_evidence.via_in_pad_process_qualification"
        for failure in report.failures
    )


def test_via_array_geometry_must_match_count_and_preserve_an_annulus(service):
    project = "rp2040_via_in_pad_geometry"
    service.create_project(project, template="rp2040_usb_device")
    spec = deepcopy(service.read_spec(project))
    geometry = spec["manufacturing"]["pcb"]["via_in_pad"]["locations"][0]["geometry"]

    geometry["rows"] = 2
    count_report = service.validator.validate_spec(spec)
    assert count_report.status.value == "fail"
    assert "via_array_count_mismatch" in {
        failure.code for failure in count_report.failures
    }

    geometry["rows"] = 3
    geometry["drill_diameter_mm"] = geometry["via_diameter_mm"]
    annulus_report = service.validator.validate_spec(spec)
    assert annulus_report.status.value == "fail"
    assert "via_annulus_invalid" in {
        failure.code for failure in annulus_report.failures
    }


def test_qualified_via_in_pad_requires_a_selected_process_and_omits_open_test(service):
    project = "rp2040_via_in_pad_qualified"
    service.create_project(project, template="rp2040_usb_device")
    spec = deepcopy(service.read_spec(project))
    declaration = spec["manufacturing"]["pcb"]["via_in_pad"]
    declaration["qualification_status"] = "qualified"

    invalid = service.validator.validate_spec(spec)
    assert invalid.status.value == "fail"
    assert any(failure.path.endswith("process.selection_status") for failure in invalid.failures)

    declaration["process"]["selection_status"] = "selected"
    incomplete_process = service.validator.validate_spec(spec)
    assert incomplete_process.status.value == "fail"
    assert {
        "manufacturing.pcb.via_in_pad.process.via_disposition",
        "manufacturing.pcb.via_in_pad.process.cap_finish",
        "manufacturing.pcb.via_in_pad.process.fabricator_process_id",
    } <= {failure.path for failure in incomplete_process.failures}

    declaration["process"] = {
        "selection_status": "selected",
        "via_disposition": "filled_and_capped",
        "cap_finish": "copper_capped",
        "fabricator_process_id": "example-qualified-process",
    }
    assert service.validator.validate_spec(spec).status.value == "pass"
    tests = service._physical_qualification_tests(spec, {"components": [], "nets": []})
    assert "via_in_pad_process_qualification" not in {item["id"] for item in tests}


def test_projects_without_via_in_pad_do_not_gain_process_test(service):
    project = "robot_without_via_in_pad"
    service.create_project(project, template="robotics_controller_full")

    result = service.generate_physical_qualification_plan(project)

    assert "via_in_pad_process_qualification" not in set(result["required_tests"])
