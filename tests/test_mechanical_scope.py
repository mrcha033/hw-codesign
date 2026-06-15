from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

from hw_codesign.artifacts import sha256
from hw_codesign.backends.mechanical import OpenCascadeMechanicalBackend
from hw_codesign.mechanical_contract import build_mechanical_contract
from hw_codesign.models import Status


def _board_step(path: Path, width: float, height: float, thickness: float) -> Path:
    try:
        from OCP.IFSelect import IFSelect_RetDone
        from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
        from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer
    except ImportError:
        pytest.skip("cadquery-ocp is unavailable")
    shape = BRepPrimAPI_MakeBox(width, height, thickness).Shape()
    writer = STEPControl_Writer()
    assert writer.Transfer(shape, STEPControl_AsIs) == IFSelect_RetDone
    assert writer.Write(str(path)) == IFSelect_RetDone
    return path


def _generated_contract(service, project):
    service.generate_all(project)
    root = service.workspace.require_project(project)
    graph = json.loads((root / "electronics" / "generated" / "electrical_graph.json").read_text(encoding="utf-8"))
    contract = json.loads((root / "mechanical" / "source" / "mechanical_contract.json").read_text(encoding="utf-8"))
    return root, graph, contract


def test_mechanical_source_is_parameterized_by_spec_and_electrical_graph(service, project):
    root, graph, contract = _generated_contract(service, project)
    j1 = next(item for item in graph["components"] if item["ref"] == "J1")
    j1_cutout = next(item for item in contract["connector_cutouts"] if item["ref"] == "J1")

    assert contract["selected_variant"] == service.read_spec(project)["mechanical"]["selected_variant"]
    assert j1_cutout["pcb_position_mm"] == j1["pcb_position_mm"]
    assert set(contract["connector_component_refs"]) == {item["ref"] for item in contract["connector_cutouts"]}

    manifest = json.loads((root / "mechanical" / "source" / "source_manifest.json").read_text(encoding="utf-8"))
    assert manifest["release_eligible"] is False
    for artifact in manifest["sources"]:
        source = root / "mechanical" / "source" / artifact["path"]
        assert source.is_file()
        assert sha256(source) == artifact["sha256"]


def test_native_mechanical_exports_variants_fixtures_and_manifest(service, project, tmp_path):
    _, _, contract = _generated_contract(service, project)
    board = contract["board"]
    board_step = _board_step(tmp_path / "board.step", board["width_mm"], board["height_mm"], board["thickness_mm"])
    output = tmp_path / "candidate"

    report = OpenCascadeMechanicalBackend().generate_from_contract(contract, output, board_step=board_step)

    assert report.status == Status.PASS
    assert report.metrics["assembly_interference_free"] is True
    assert report.metrics["board_step_imported"] is True
    assert report.metrics["variant_count"] == 3
    assert report.metrics["fixture_count"] == 3
    mechanical = output / "mechanical"
    expected = [
        "board.step", "enclosure.step", "enclosure.stl", "assembly.step",
        "mounting_plate.step", "frame_bracket_left.step", "frame_bracket_right.step",
        "variants/enclosure_sealed.step", "variants/enclosure_vented.step", "variants/enclosure_service.step",
    ]
    assert all((mechanical / name).is_file() for name in expected)
    manifest = json.loads((mechanical / "mechanical_manifest.json").read_text(encoding="utf-8"))
    assert manifest["candidate_only"] is True
    assert manifest["release_eligible"] is False
    assert manifest["provenance"]["tool_versions"]["cadquery-ocp"]
    assert manifest["provenance"]["command"]
    for artifact in manifest["artifacts"]:
        path = mechanical / artifact["path"]
        assert sha256(path) == artifact["sha256"]


def test_missing_native_board_step_blocks_mechanical_release(service, project, tmp_path):
    _, _, contract = _generated_contract(service, project)
    report = OpenCascadeMechanicalBackend().generate_from_contract(contract, tmp_path / "candidate")
    if report.failures and report.failures[0].code == "tool_unavailable":
        assert report.status == Status.BLOCKED
    else:
        assert report.status == Status.BLOCKED
        assert "board_step_missing" in {failure.code for failure in report.failures}


def test_geometry_interference_and_connector_drift_fail(service, project, tmp_path):
    _, _, contract = _generated_contract(service, project)
    board = contract["board"]
    board_step = _board_step(tmp_path / "board.step", board["width_mm"], board["height_mm"], board["thickness_mm"])

    collision = deepcopy(contract)
    collision["board"]["component_height_map"][0]["height_mm"] = collision["enclosure"]["internal_mm"][2]
    collision_report = OpenCascadeMechanicalBackend().generate_from_contract(collision, tmp_path / "collision", board_step=board_step)
    assert collision_report.status == Status.FAIL
    assert collision_report.metrics["component_lid_intersection_mm3"] > 0
    assert "assembly_interference" in {failure.code for failure in collision_report.failures}

    drifted = deepcopy(contract)
    next(item for item in drifted["connector_cutouts"] if item["ref"] == "J1")["pcb_position_mm"][1] = 25.0
    drift_report = OpenCascadeMechanicalBackend().generate_from_contract(drifted, tmp_path / "drift", board_step=board_step)
    assert drift_report.status == Status.FAIL
    assert "connector_cutout_alignment_failed" in {failure.code for failure in drift_report.failures}


def test_contract_builder_exposes_tolerance_and_height_map(service, project):
    service.generate_all(project)
    root = service.workspace.require_project(project)
    spec = service.read_spec(project)
    graph = json.loads((root / "electronics" / "generated" / "electrical_graph.json").read_text(encoding="utf-8"))
    contract = build_mechanical_contract(spec, graph)
    assert contract["clearances"]["tolerance_mm"] > 0
    assert len(contract["board"]["component_height_map"]) == len(graph["components"])
