from __future__ import annotations

import math
import re
from copy import deepcopy
from dataclasses import replace
from pathlib import Path

import pytest
import yaml
from sexpdata import Symbol, loads

from hw_codesign.board_layout import component_positions, copper_edge_clearance_mm
from hw_codesign.footprint_library import (
    canonical_footprint_geometry,
    render_canonical_footprint,
)
from hw_codesign.placement import apply_placement_to_graph, check_placement, propose_placement
from hw_codesign.reference_backend import (
    _front_smd_plane_pad_sites,
    _kicad_board,
    build_graph,
)

_ROOT = Path(__file__).parents[1]
_TEMPLATE = _ROOT / "src" / "hw_codesign" / "templates" / "rp2040_usb_device.yaml"
_USB_FOOTPRINT = "Connector_USB:USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal"
_DEBUG_FOOTPRINT = "Connector_IDC:IDC-Header_2x05_P2.54mm_Vertical"
_ESP32_FOOTPRINT = "RF_Module:ESP32-S3-WROOM-1"


def _spec_and_resolved_geometry_graph() -> tuple[dict, dict]:
    spec = yaml.safe_load(_TEMPLATE.read_text(encoding="utf-8"))
    graph = build_graph(spec)
    resolved_footprints = {
        "USB_C_16Pin": _USB_FOOTPRINT,
        "SOT23-6": "Package_TO_SOT_SMD:SOT-23-6",
        "R0603": "Resistor_SMD:R_0603_1608Metric",
        "SOT-23-5": "Package_TO_SOT_SMD:SOT-23-5",
        "QFN-56": "Package_DFN_QFN:QFN-56-1EP_7x7mm_P0.4mm_EP3.2x3.2mm",
        "SOIC-8-208mil": "Package_SO:SOIC-8_5.3x5.3mm_P1.27mm",
        "Crystal_SMD_3225-4Pin": "Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm",
        "PinHeader-2x5": _DEBUG_FOOTPRINT,
        "C0402": "Capacitor_SMD:C_0402_1005Metric",
        "C0603": "Capacitor_SMD:C_0603_1608Metric",
    }
    # These are the verified library IDs selected by ComponentResolver during a
    # real generation. Supplying the complete mapping keeps this focused test
    # independent of supplier/cache state while exercising exact emitted pads.
    for component in graph["components"]:
        component["footprint"] = resolved_footprints[component["footprint"]]
    return spec, graph


def _absolute_extent(
    anchor: tuple[float, float],
    rotation_deg: float,
    local_extent: tuple[float, float, float, float],
) -> tuple[float, float, float, float]:
    theta = math.radians(rotation_deg)
    cosine, sine = math.cos(theta), math.sin(theta)
    points = [
        (
            anchor[0] + local_x * cosine + local_y * sine,
            anchor[1] - local_x * sine + local_y * cosine,
        )
        for local_x in (local_extent[0], local_extent[2])
        for local_y in (local_extent[1], local_extent[3])
    ]
    return (
        min(point[0] for point in points),
        min(point[1] for point in points),
        max(point[0] for point in points),
        max(point[1] for point in points),
    )


def _rendered_pad_angles(library_id: str, rotation_deg: float) -> dict[str, list[float]]:
    rendered, failures = render_canonical_footprint(
        library_id,
        {
            "ref": "U1",
            "value": "rotation fixture",
            "mpn": "fixture",
            "lifecycle": "active",
            "pins": [],
        },
        10.0,
        10.0,
        rotation_deg,
        {},
        ("F.Cu", "B.Cu"),
    )
    assert rendered is not None
    assert not failures
    ast = loads(rendered)
    angles: dict[str, list[float]] = {}
    for form in ast[2:]:
        if not (
            isinstance(form, list)
            and form
            and isinstance(form[0], Symbol)
            and form[0].value() == "pad"
        ):
            continue
        pad_number = str(form[1])
        at_form = next(
            item
            for item in form
            if isinstance(item, list)
            and item
            and isinstance(item[0], Symbol)
            and item[0].value() == "at"
        )
        assert len(at_form) >= 4
        angles.setdefault(pad_number, []).append(float(at_form[3]) % 360.0)
    return angles


def test_embedded_usb_pad_angles_inherit_placed_footprint_rotation():
    angles = _rendered_pad_angles(_USB_FOOTPRINT, 270.0)

    assert angles
    assert {angle for pad_angles in angles.values() for angle in pad_angles} == {270.0}


def test_embedded_pad_angles_compose_existing_local_rotation():
    angles = _rendered_pad_angles(_ESP32_FOOTPRINT, 90.0)

    assert angles["13"] == [90.0]  # omitted local 0 + footprint 90
    assert angles["14"] == [270.0]  # existing local 180 + footprint 90
    assert angles["15"] == [0.0]  # existing local 270 + footprint 90, normalized


def test_rp2040_usb_receptacle_uses_vendor_left_edge_datum_and_inboard_copper():
    spec, graph = _spec_and_resolved_geometry_graph()
    proposal = propose_placement(spec, graph)
    j1 = proposal.placements["J1"]
    geometry = canonical_footprint_geometry(_USB_FOOTPRINT)

    assert geometry is not None
    assert (j1.x_mm, j1.y_mm, j1.rotation_deg) == pytest.approx((3.1, 15.0, 270.0))

    footprint_text = (
        _ROOT
        / "src"
        / "hw_codesign"
        / "footprints"
        / "USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal.kicad_mod"
    ).read_text(encoding="utf-8")
    datum = re.search(
        r'\(fp_text user "PCB Edge"\s+\(at\s+([-+0-9.]+)\s+([-+0-9.]+)',
        footprint_text,
    )
    assert datum is not None
    local_x, local_y = float(datum.group(1)), float(datum.group(2))
    theta = math.radians(j1.rotation_deg)
    datum_x = j1.x_mm + local_x * math.cos(theta) + local_y * math.sin(theta)
    assert datum_x == pytest.approx(0.0, abs=1e-9)

    copper = _absolute_extent((j1.x_mm, j1.y_mm), j1.rotation_deg, geometry.copper_extent)
    assert copper[0] >= copper_edge_clearance_mm(spec)
    # The shell intentionally projects beyond the mating edge, while copper does not.
    assert j1.extent()[0] < 0.0

    placement_report = check_placement(proposal, graph)
    j1_blockers = {
        failure.code
        for failure in placement_report.failures
        if failure.details.get("ref") == "J1" and failure.severity == "error"
    }
    assert not ({"footprint_off_board", "footprint_edge_clearance"} & j1_blockers)

    placed_graph = apply_placement_to_graph(graph, proposal)
    board_text, routing_failures = _kicad_board(spec, placed_graph)
    assert not routing_failures
    assert re.search(
        rf'\(footprint "{re.escape(_USB_FOOTPRINT)}".*?\(at 3\.1 15\.0 270\.0\)',
        board_text,
        flags=re.DOTALL,
    )


def test_plane_pad_site_transform_matches_kicad_clockwise_rotation():
    spec, graph = _spec_and_resolved_geometry_graph()
    proposal = propose_placement(spec, graph)
    board_text, routing_failures = _kicad_board(
        spec,
        apply_placement_to_graph(graph, proposal),
    )

    assert not routing_failures
    j1_sites = {
        tuple(item["pad"] for item in site["logical_pads"]):
        tuple(round(value, 3) for value in site["pad_at_mm"])
        for site in _front_smd_plane_pad_sites(board_text, {"GND"})
        if site["ref"] == "J1"
    }

    # These absolute coordinates are the values reported by native KiCad DRC
    # for the 270-degree USB-C placement, not a counter-clockwise approximation.
    assert j1_sites == {
        ("A1", "B12"): (6.78, 11.8),
        ("A12", "B1"): (6.78, 18.2),
    }


def test_rp2040_exposed_pad_uses_official_nine_via_ground_array():
    spec, graph = _spec_and_resolved_geometry_graph()

    board_text, routing_failures = _kicad_board(spec, graph)

    assert not routing_failures
    board = loads(board_text)

    def is_form(value, name: str) -> bool:
        return (
            isinstance(value, list)
            and value
            and isinstance(value[0], Symbol)
            and value[0].value() == name
        )

    def direct(value, name: str):
        return [item for item in value[1:] if is_form(item, name)]

    u2 = next(
        footprint
        for footprint in direct(board, "footprint")
        if any(
            len(prop) >= 3 and str(prop[1]) == "Reference" and str(prop[2]) == "U2"
            for prop in direct(footprint, "property")
        )
    )
    pad_57_forms = [pad for pad in direct(u2, "pad") if str(pad[1]) == "57"]
    through_pads = [pad for pad in pad_57_forms if str(pad[2]) == "thru_hole"]
    smd_pads = [pad for pad in pad_57_forms if str(pad[2]) == "smd"]

    assert len(smd_pads) == 1
    assert len(through_pads) == 9
    assert {
        tuple(float(value) for value in direct(pad, "at")[0][1:3])
        for pad in through_pads
    } == {
        (x_mm, y_mm)
        for x_mm in (-1.275, 0.0, 1.275)
        for y_mm in (-1.275, 0.0, 1.275)
    }
    for pad in through_pads:
        assert tuple(float(value) for value in direct(pad, "size")[0][1:3]) == (0.6, 0.6)
        assert float(direct(pad, "drill")[0][1]) == 0.35
        assert [str(value) for value in direct(pad, "layers")[0][1:]] == ["*.Cu"]
        assert str(direct(pad, "net")[0][2]) == "GND"

    paste_apertures = [
        pad
        for pad in direct(u2, "pad")
        if str(pad[1]) == ""
        and [str(value) for value in direct(pad, "layers")[0][1:]] == ["F.Paste"]
    ]
    assert len(paste_apertures) == 4
    assert {
        tuple(float(value) for value in direct(pad, "at")[0][1:3])
        for pad in paste_apertures
    } == {
        (x_mm, y_mm)
        for x_mm in (-0.6375, 0.6375)
        for y_mm in (-0.6375, 0.6375)
    }
    for pad in paste_apertures:
        assert tuple(float(value) for value in direct(pad, "size")[0][1:3]) == (
            1.084435,
            1.084435,
        )
        assert float(direct(pad, "roundrect_rratio")[0][1]) == 0.230535

    # The plated pad-57 forms span the stackup themselves. The generic plane
    # escape generator must not add a tenth, free-standing via and fanout.
    assert not any(
        site["ref"] == "U2" and site["pad"] == "57"
        for site in _front_smd_plane_pad_sites(board_text, {"GND"})
    )
    u2_at = tuple(float(value) for value in direct(u2, "at")[0][1:3])
    assert not any(
        tuple(float(value) for value in direct(segment, endpoint)[0][1:3]) == u2_at
        for segment in direct(board, "segment")
        for endpoint in ("start", "end")
    )


def test_rp2040_board_declares_paste_layers_and_excludes_mounting_holes_from_pnp():
    spec, graph = _spec_and_resolved_geometry_graph()
    board_text, routing_failures = _kicad_board(spec, graph)

    assert not routing_failures
    assert '(34 "B.Paste" user)' in board_text
    assert '(35 "F.Paste" user)' in board_text
    for ref in ("H1", "H2", "H3", "H4"):
        footprint = re.search(
            rf'\(footprint "MountingHole:[^\n]+"[^\n]*\(attr exclude_from_bom exclude_from_pos_files\).*?\(property "Reference" "{ref}"',
            board_text,
            flags=re.DOTALL,
        )
        assert footprint is not None


def test_generated_zone_rules_follow_declared_process_minima():
    spec, graph = _spec_and_resolved_geometry_graph()
    spec["manufacturing"]["pcb"]["min_clearance_mm"] = 0.18
    spec["manufacturing"]["pcb"]["min_track_width_mm"] = 0.21

    board_text, routing_failures = _kicad_board(spec, graph)

    assert not routing_failures
    # A two-layer board uses one continuous B.Cu GND plane. Every F.Cu SMD
    # ground pad gets an explicit segment/via escape instead of relying on a
    # front pour that signal routing can fracture into disconnected islands.
    assert board_text.count('(net_name "GND") (layer "B.Cu")') == 1
    assert '(net_name "GND") (layer "F.Cu")' not in board_text
    assert board_text.count("(connect_pads (clearance 0.180))") == 1
    assert board_text.count("(min_thickness 0.210)") == 1
    assert board_text.count(
        "(fill yes (thermal_gap 0.180) (thermal_bridge_width 0.210)"
    ) == 1

    escape_sites = _front_smd_plane_pad_sites(board_text, {"GND"})
    assert escape_sites
    assert board_text.count('(layers "F.Cu" "B.Cu") (net ') >= len(escape_sites)


def test_plane_escape_segments_preserve_half_grid_pad_centres():
    spec, graph = _spec_and_resolved_geometry_graph()

    board_text, routing_failures = _kicad_board(spec, graph)

    assert not routing_failures
    escape_sites = _front_smd_plane_pad_sites(board_text, {"GND"})
    half_grid_sites = [
        site
        for site in escape_sites
        if any(
            not math.isclose(coordinate * 1000.0, round(coordinate * 1000.0))
            for coordinate in site["pad_at_mm"]
        )
    ]
    assert {
        (site["ref"], site["pad"])
        for site in half_grid_sites
    } == {("D1", "2"), ("U1", "2"), ("U2", "19"), ("U3", "4")}

    board = loads(board_text)
    segment_starts = {
        (float(start[1]), float(start[2]))
        for segment in board[1:]
        if isinstance(segment, list)
        and segment
        and isinstance(segment[0], Symbol)
        and segment[0].value() == "segment"
        for start in segment
        if isinstance(start, list)
        and start
        and isinstance(start[0], Symbol)
        and start[0].value() == "start"
    }
    for site in half_grid_sites:
        pad_at = tuple(float(value) for value in site["pad_at_mm"])
        assert pad_at in segment_starts


def test_edge_connector_body_overhang_exception_is_limited_to_declared_side():
    spec, graph = _spec_and_resolved_geometry_graph()
    proposal = propose_placement(spec, graph)

    no_edge_contract = replace(
        proposal,
        constraints=[
            constraint
            for constraint in proposal.constraints
            if not (constraint.kind == "connector_edge" and constraint.target_ref == "J1")
        ],
    )
    no_edge_report = check_placement(no_edge_contract, graph)
    assert any(
        failure.code == "footprint_off_board" and failure.details.get("ref") == "J1"
        for failure in no_edge_report.failures
    )

    wrong_side = deepcopy(proposal)
    wrong_side.constraints = [
        replace(constraint, params={**constraint.params, "side": "right"})
        if constraint.kind == "connector_edge" and constraint.target_ref == "J1"
        else constraint
        for constraint in proposal.constraints
    ]
    wrong_side_report = check_placement(wrong_side, graph)
    assert any(
        failure.code == "footprint_off_board" and failure.details.get("ref") == "J1"
        for failure in wrong_side_report.failures
    )


def test_rp2040_debug_header_courtyard_clears_h4_npth():
    spec, graph = _spec_and_resolved_geometry_graph()
    positions = component_positions(graph)
    geometry = canonical_footprint_geometry(_DEBUG_FOOTPRINT)

    assert geometry is not None and geometry.courtyard_extent is not None
    assert positions["J2"] == pytest.approx((55.0, 11.1))
    courtyard = _absolute_extent(positions["J2"], 0.0, geometry.courtyard_extent)
    h4 = spec["mechanical"]["mounting_holes"][3]
    hole_x, hole_y = float(h4["x_mm"]), float(h4["y_mm"])
    hole_radius = float(h4["diameter_mm"]) / 2.0
    dx = max(courtyard[0] - hole_x, 0.0, hole_x - courtyard[2])
    dy = max(courtyard[1] - hole_y, 0.0, hole_y - courtyard[3])

    assert math.hypot(dx, dy) >= hole_radius
    assert not (courtyard[0] <= hole_x <= courtyard[2] and courtyard[1] <= hole_y <= courtyard[3])

    # Geometry repairs must not relax the declared two-layer process minima.
    assert spec["electronics"]["pcb"]["layers"] == 2
    assert spec["manufacturing"]["pcb"]["layers"] == 2
    assert spec["electronics"]["pcb"]["min_trace_mm"] == pytest.approx(0.15)
    assert spec["electronics"]["pcb"]["min_space_mm"] == pytest.approx(0.15)
    assert spec["manufacturing"]["pcb"]["min_track_width_mm"] == pytest.approx(0.15)
    assert spec["manufacturing"]["pcb"]["min_clearance_mm"] == pytest.approx(0.15)
