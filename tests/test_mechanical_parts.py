"""Tests for Phase A: agent-authored mechanical part design."""
from __future__ import annotations

import json
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# hw_get_part_types
# ---------------------------------------------------------------------------

def test_get_part_types_returns_all_five(service, project):
    result = service.get_part_types()
    assert result["status"] == "pass"
    assert result["count"] == 5
    types = result["part_types"]
    assert "pcb_mount_bracket" in types
    assert "standoff_tower" in types
    assert "cable_clip" in types
    assert "din_rail_adapter" in types
    assert "custom_enclosure_variant" in types


def test_get_part_types_includes_intent_schema(service, project):
    result = service.get_part_types()
    for pt_name, pt_data in result["part_types"].items():
        assert "description" in pt_data, f"{pt_name} missing description"
        assert "intent_schema" in pt_data, f"{pt_name} missing intent_schema"
        schema = pt_data["intent_schema"]
        assert schema.get("type") == "object", f"{pt_name} intent_schema must be object type"


# ---------------------------------------------------------------------------
# hw_list_parts — empty before any design calls
# ---------------------------------------------------------------------------

def test_list_parts_empty_before_any_design(service, project):
    result = service.list_parts(project)
    assert result["status"] == "pass"
    assert result["parts"] == []
    assert result["count"] == 0


# ---------------------------------------------------------------------------
# Unknown part type returns blocked
# ---------------------------------------------------------------------------

def test_design_part_unknown_type_returns_blocked(service, project):
    result = service.design_part(project, "test_part", "not_a_real_type", {})
    assert result["status"] == "blocked"
    assert result["code"] == "unknown_part_type"
    assert "available_part_types" in result


# ---------------------------------------------------------------------------
# OCP-blocked graceful degradation
# ---------------------------------------------------------------------------

def test_design_part_blocked_when_ocp_unavailable(service, project, monkeypatch):
    """When cadquery-ocp is not installed every part type must return status=blocked."""
    import builtins
    real_import = builtins.__import__

    def mock_import(name, *args, **kwargs):
        if name.startswith("OCP"):
            raise ImportError("cadquery-ocp not installed (mocked)")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", mock_import)
    result = service.design_part(project, "test_bracket", "pcb_mount_bracket", {
        "bracket_width_mm": 60, "bracket_height_mm": 40,
    })
    assert result["status"] == "blocked"
    assert result["code"] == "tool_unavailable"


# ---------------------------------------------------------------------------
# OCP-available tests (skipped if OCP not installed)
# ---------------------------------------------------------------------------

ocp_available = pytest.mark.skipif(
    not __import__("importlib").util.find_spec("OCP"),
    reason="cadquery-ocp not installed",
)


@ocp_available
def test_pcb_mount_bracket_generates_artifacts(service, project):
    result = service.design_part(project, "frame_mount_left", "pcb_mount_bracket", {
        "bracket_width_mm": 60,
        "bracket_height_mm": 40,
        "leg_depth_mm": 15,
        "thickness_mm": 3.0,
        "fastener": "M3",
        "interface": "2020_extrusion_slot_6",
    })
    assert result["status"] in ("generated", "fail")
    assert result["part_type"] == "pcb_mount_bracket"
    assert len(result["artifacts"]) >= 2
    for path in result["artifacts"]:
        assert Path(path).is_file(), f"Artifact not found: {path}"
    assert "printability" in result
    assert "gate_report" in result
    assert result["gate_report"]["gate"] == "part_design"


@ocp_available
def test_standoff_tower_generates_artifacts(service, project):
    result = service.design_part(project, "pcb_standoff_m3_12mm", "standoff_tower", {
        "height_mm": 12.0,
        "outer_diameter_mm": 8.0,
        "fastener": "M3",
        "through_bore": True,
        "base_style": "flanged",
        "flange_diameter_mm": 12.0,
    })
    assert result["status"] in ("generated", "fail")
    assert "printability" in result
    assert Path(result["artifacts"][0]).suffix in (".step", ".stl")


@ocp_available
def test_cable_clip_generates_artifacts(service, project):
    result = service.design_part(project, "power_cable_clip", "cable_clip", {
        "cable_diameter_mm": 8.0,
        "wall_mm": 2.0,
        "mount_type": "screw",
        "fastener": "M3",
    })
    assert result["status"] in ("generated", "fail")
    assert result["part_type"] == "cable_clip"
    for path in result["artifacts"]:
        assert Path(path).is_file()


@ocp_available
def test_din_rail_adapter_generates_artifacts(service, project):
    result = service.design_part(project, "controller_din_mount", "din_rail_adapter", {
        "plate_width_mm": 100.0,
        "plate_height_mm": 80.0,
        "plate_thickness_mm": 3.0,
        "clip_position": "both",
        "fastener": "M3",
    })
    assert result["status"] in ("generated", "fail")
    assert result["part_type"] == "din_rail_adapter"
    for path in result["artifacts"]:
        assert Path(path).is_file()


@ocp_available
def test_custom_enclosure_variant_generates_assembly(service, project):
    result = service.design_part(project, "sensor_enclosure", "custom_enclosure_variant", {
        "internal_mm": [80, 60, 30],
        "wall_thickness_mm": 2.5,
        "lid": True,
        "panel_cutouts": [
            {"side": "front", "width_mm": 12, "height_mm": 8, "center_x_mm": 40, "center_z_mm": 15, "label": "USB"},
        ],
        "gland_holes": [
            {"side": "rear", "diameter_mm": 12, "center_x_mm": 20, "center_z_mm": 15, "label": "power"},
        ],
    })
    assert result["status"] in ("generated", "fail")
    assert result["part_type"] == "custom_enclosure_variant"
    names = [Path(a).name for a in result["artifacts"]]
    assert any("assembly" in n for n in names), "Assembly STEP must be produced"
    assert any("_base" in n for n in names), "Base STEP must be produced"
    assert any("_lid" in n for n in names), "Lid STEP must be produced"


@ocp_available
def test_list_parts_after_design(service, project):
    service.design_part(project, "bracket_a", "pcb_mount_bracket", {
        "bracket_width_mm": 50, "bracket_height_mm": 35,
    })
    service.design_part(project, "standoff_b", "standoff_tower", {
        "height_mm": 10.0, "fastener": "M3",
    })
    result = service.list_parts(project)
    assert result["count"] == 2
    names = {p["part_name"] for p in result["parts"]}
    assert "bracket_a" in names
    assert "standoff_b" in names
    for p in result["parts"]:
        assert "gate_status" in p
        assert "part_type" in p


@ocp_available
def test_part_intent_persisted_to_disk(service, project):
    """intent.json must be written before geometry so it survives a failed design attempt."""
    intent = {"bracket_width_mm": 70, "bracket_height_mm": 50, "fastener": "M4"}
    service.design_part(project, "intent_test_bracket", "pcb_mount_bracket", intent)
    path = service.workspace.require_project(project)
    intent_file = path / "mechanical" / "parts" / "intent_test_bracket" / "intent.json"
    assert intent_file.is_file()
    saved = json.loads(intent_file.read_text(encoding="utf-8"))
    assert saved["intent"]["fastener"] == "M4"


@ocp_available
def test_printability_report_structure(service, project):
    result = service.design_part(project, "printability_check", "standoff_tower", {
        "height_mm": 15.0, "outer_diameter_mm": 8.0, "fastener": "M3",
    })
    p = result["printability"]
    assert "printable" in p
    assert "max_overhang_deg" in p
    assert "min_wall_mm" in p
    assert "stl_manifold" in p
    assert "recommended_orientation" in p
    assert isinstance(p["violations"], list)


@ocp_available
def test_thin_wall_triggers_printability_violation(service, project):
    """A 0.5mm wall thickness should fail the FDM minimum wall check."""
    result = service.design_part(project, "thin_bracket", "pcb_mount_bracket", {
        "bracket_width_mm": 40,
        "bracket_height_mm": 30,
        "thickness_mm": 0.5,  # below 1.2mm FDM minimum
    })
    assert result["printability"]["printable"] is False
    violations = result["printability"]["violations"]
    assert any("wall" in v.lower() for v in violations)
