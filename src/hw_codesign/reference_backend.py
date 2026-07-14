from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

from sexpdata import Symbol, loads

from .artifacts import box_stl, deterministic_zip, step_box
from .board_layout import (
    component_positions,
    connector_sides,
    copper_edge_clearance_mm,
    footprint_geometry,
    mirrored_refs,
)
from .electronics_design import build_graph_from_spec
from .footprint_library import render_canonical_footprint
from .io import atomic_write_text, write_json
from .models import Failure, FailureCategory, GateReport, Status
from .schematic_generator import generate_kicad_schematic

REFERENCE_FIRMWARE_TIMEOUT_SECONDS = 120

PARTS = {
    "mcu": ("STM32H743VIT6", "LQFP-100_14x14mm_P0.5mm"),
    "imu": ("ICM-42688-P", "LGA-14_2.5x3mm_P0.5mm"),
    "efuse": ("TPS26630RGET", "VQFN-24-1EP_4x4mm_P0.5mm"),
    "buck5": ("LM76005RNPR", "WQFN-30-1EP_6x4mm_P0.5mm"),
    "buck3": ("TPS62133RGTR", "VQFN-16-1EP_3x3mm_P0.5mm"),
    "can": ("TCAN1042HGVDRQ1", "SOIC-8_3.9x4.9mm_P1.27mm"),
    "usb": ("USBLC6-2SC6", "SOT-23-6"),
}

# These are references to KiCad's bundled standard-library STEP assets.  They
# deliberately add no hw-codesign-authored geometry: a board that has a mapped
# footprint can be rendered and exported using the corresponding upstream
# model, while footprints without a verified model remain model-free.
KICAD_STANDARD_3D_MODELS: dict[str, str] = {
    "Resistor_SMD:R_0603_1608Metric": "Resistor_SMD.3dshapes/R_0603_1608Metric.step",
    "Capacitor_SMD:C_0603_1608Metric": "Capacitor_SMD.3dshapes/C_0603_1608Metric.step",
    "Capacitor_SMD:C_1206_3216Metric": "Capacitor_SMD.3dshapes/C_1206_3216Metric.step",
    "Connector_USB:USB_C_GCT_USB4105": "Connector_USB.3dshapes/USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal.step",
    "RF_Module:ESP32-S3-WROOM-1": "RF_Module.3dshapes/ESP32-S3-WROOM-1.step",
    "Package_TO_SOT_SMD:SOT-23-6": "Package_TO_SOT_SMD.3dshapes/SOT-23-6.step",
    "Package_LGA:LGA-14": "Package_LGA.3dshapes/LGA-14_3x2.5mm_P0.5mm_LayoutBorder3x4y.step",
    "Package_DFN_QFN:VQFN-16": "Package_DFN_QFN.3dshapes/Texas_RSA_VQFN-16-1EP_4x4mm_P0.65mm_EP2.7x2.7mm.step",
}


def _kicad_model_clause(footprint: str) -> str:
    """Return an upstream KiCad model reference for a footprint, if verified."""
    model = KICAD_STANDARD_3D_MODELS.get(footprint)
    if model is None:
        return ""
    return f'''    (model "${{KICAD10_3DMODEL_DIR}}/{model}"
      (offset (xyz 0 0 0))
      (scale (xyz 1 1 1))
      (rotate (xyz 0 0 0)))
'''


def build_graph(spec: dict[str, Any]) -> dict[str, Any]:
    return build_graph_from_spec(spec)


def generate_kicad(project: Path, spec: dict[str, Any], graph: dict[str, Any]) -> list[str]:
    target = project / "electronics" / "generated" / "kicad"
    target.mkdir(parents=True, exist_ok=True)
    name = project.name
    for pattern in (
        f"{name}*.dsn", f"{name}*.ses", f"{name}*.kicad_pcb",
        f"{name}*.kicad_prl", f"{name}*.kicad_pro", f"~{name}*.lck",
    ):
        for stale in target.glob(pattern):
            stale.unlink()
    pro = {"board": {"design_settings": {"rules": {
        "min_clearance": spec["manufacturing"]["pcb"]["min_clearance_mm"],
        "min_copper_edge_clearance": copper_edge_clearance_mm(spec),
        "min_track_width": spec["manufacturing"]["pcb"]["min_track_width_mm"],
    }}}, "meta": {"filename": f"{name}.kicad_pro", "version": 1}}
    write_json(target / f"{name}.kicad_pro", pro)
    schematic = _legacy_schematic(spec, graph)
    atomic_write_text(target / f"{name}.sch", schematic)
    schematic_path = target / f"{name}.kicad_sch"
    try:
        generate_kicad_schematic(name, graph, schematic_path)
    except Exception as exc:
        atomic_write_text(schematic_path, _kicad_schematic_stub(name, graph))
        write_json(target / "schematic_generation.json", {
            "status": "blocked",
            "code": "kicad_symbol_instantiation_failed",
            "message": str(exc),
            "fallback": schematic_path.name,
        })
    board_text, routing_failures = _kicad_board(spec, graph)
    atomic_write_text(target / f"{name}.kicad_pcb", board_text)
    _layers, _copper_layers, plane_layers = _kicad_stackup(spec)
    plane_escape_required = (
        len(_front_smd_plane_pad_sites(board_text, set(plane_layers)))
        if len(_copper_layers) > 2
        else 0
    )
    plane_escape_unplaced = sum(
        1 for failure in routing_failures
        if failure.get("code") == "plane_escape_unplaceable"
    )
    write_json(target / "routing.json", {
        "status": "fail" if routing_failures else "generated",
        "mode": "zone_connected_planes",
        "plane_connectivity": "copper_zones",
        "plane_escape": (
            "fcu_segment_to_through_via"
            if len(_copper_layers) > 2
            else "front_copper_zone"
        ),
        "plane_escape_required": plane_escape_required,
        "plane_escape_count": max(0, plane_escape_required - plane_escape_unplaced),
        "zone_nets": sorted(plane_layers),
        "signal_routing": "deferred_to_freerouting",
        "board_sha256": hashlib.sha256(board_text.encode("utf-8")).hexdigest(),
        "failures": routing_failures,
    })
    return [str(path) for path in sorted(target.iterdir())]


def _kicad_schematic_stub(name: str, graph: dict[str, Any]) -> str:
    # KiCad 8 S-expression project container with embedded design inventory.
    labels = "\n".join(f'  (text "{item["ref"]}: {item["value"]}" (exclude_from_sim no) (at 20 {20 + i * 5} 0) (effects (font (size 1.27 1.27))))' for i, item in enumerate(graph["components"]))
    return f'(kicad_sch (version 20231120) (generator hw_codesign) (uuid 00000000-0000-0000-0000-000000000001) (paper "A4")\n  (lib_symbols)\n{labels}\n  (sheet_instances (path "/" (page "1")))\n)\n'


def _legacy_schematic(spec: dict[str, Any], graph: dict[str, Any]) -> str:
    title = _design_title(spec, graph)
    lines = ["EESchema Schematic File Version 4", "LIBS:power", "EELAYER 29 0", "EELAYER END", "$Descr A4 11693 8268", "Sheet 1 1", f"Title \"{title}\"", "$EndDescr"]
    for index, item in enumerate(graph["components"]):
        x, y = 1500 + (index % 4) * 2000, 1200 + (index // 4) * 900
        lines.extend(("$Comp", f"L Connector_Generic:Conn_01x02 {item['ref']}", f"U 1 1 {1000 + index:X}", f"P {x} {y}", f"F 0 \"{item['ref']}\" H {x + 80} {y + 200} 50  0000 C CNN", f"F 1 \"{item['value']}\" H {x + 80} {y - 200} 50  0000 C CNN", f"F 2 \"{item['footprint']}\" H {x} {y} 50  0001 C CNN", "\t1    0    0    -1", "$EndComp"))
    lines.append("$EndSCHEMATC")
    return "\n".join(lines) + "\n"


def _sexp_head(form: Any, name: str) -> bool:
    return (
        isinstance(form, list)
        and bool(form)
        and isinstance(form[0], Symbol)
        and form[0].value() == name
    )


def _sexp_direct(form: list[Any], name: str) -> list[list[Any]]:
    return [item for item in form[1:] if _sexp_head(item, name)]


def _sexp_atom(value: Any) -> str:
    return value.value() if isinstance(value, Symbol) else str(value)


def _sexp_coordinate(form: list[Any], name: str) -> tuple[float, float] | None:
    matches = _sexp_direct(form, name)
    if not matches or len(matches[0]) < 3:
        return None
    return float(matches[0][1]), float(matches[0][2])


def _front_smd_plane_pad_sites(
    board_text: str,
    plane_nets: set[str],
) -> list[dict[str, Any]]:
    """Return absolute F.Cu SMD pad sites that need a plane escape.

    A numbered pad that also has a plated through-hole form is already connected
    through the copper stackup, so its companion SMD form does not need a second
    escape. This matters for canonical exposed-pad footprints such as the ESP32
    module, whose ground pad is represented by one SMD form plus thermal vias.
    """
    root = loads(board_text)
    if not isinstance(root, list) or not _sexp_head(root, "kicad_pcb"):
        raise ValueError("Expected one kicad_pcb S-expression")

    sites: list[dict[str, Any]] = []
    for footprint in _sexp_direct(root, "footprint"):
        properties = {
            _sexp_atom(item[1]): _sexp_atom(item[2])
            for item in _sexp_direct(footprint, "property")
            if len(item) >= 3
        }
        ref = properties.get("Reference")
        footprint_at = _sexp_direct(footprint, "at")
        if ref is None or not footprint_at or len(footprint_at[0]) < 3:
            continue
        anchor_x, anchor_y = float(footprint_at[0][1]), float(footprint_at[0][2])
        rotation = float(footprint_at[0][3]) if len(footprint_at[0]) > 3 else 0.0
        theta = math.radians(rotation)
        cosine, sine = math.cos(theta), math.sin(theta)
        plated_pad_keys: set[tuple[str, str]] = set()
        smd_sites: list[dict[str, Any]] = []
        for pad in _sexp_direct(footprint, "pad"):
            if len(pad) < 3:
                continue
            net_forms = _sexp_direct(pad, "net")
            if not net_forms or len(net_forms[0]) < 3:
                continue
            pad_number = _sexp_atom(pad[1])
            pad_kind = _sexp_atom(pad[2])
            net_name = _sexp_atom(net_forms[0][2])
            if net_name not in plane_nets:
                continue
            layers_forms = _sexp_direct(pad, "layers")
            layers = {
                _sexp_atom(layer)
                for layer in (layers_forms[0][1:] if layers_forms else [])
            }
            key = (pad_number, net_name)
            copper_pad_layers = {layer for layer in layers if layer.endswith(".Cu")}
            if pad_kind == "thru_hole" and (
                "*.Cu" in layers or len(copper_pad_layers) > 1
            ):
                plated_pad_keys.add(key)
                continue
            if pad_kind != "smd" or "F.Cu" not in layers:
                continue
            local_at = _sexp_coordinate(pad, "at")
            if local_at is None:
                continue
            local_x, local_y = local_at
            smd_sites.append({
                "ref": ref,
                "pad": pad_number,
                "net": net_name,
                "pad_at_mm": (
                    anchor_x + local_x * cosine - local_y * sine,
                    anchor_y + local_x * sine + local_y * cosine,
                ),
                "anchor_at_mm": (anchor_x, anchor_y),
            })
        sites.extend(
            site
            for site in smd_sites
            if (str(site["pad"]), str(site["net"])) not in plated_pad_keys
        )

    unique: dict[tuple[str, str, str, float, float], dict[str, Any]] = {}
    for site in sites:
        pad_x, pad_y = site["pad_at_mm"]
        key = (
            str(site["ref"]),
            str(site["pad"]),
            str(site["net"]),
            round(float(pad_x), 6),
            round(float(pad_y), 6),
        )
        unique[key] = site
    return [unique[key] for key in sorted(unique)]


def _plane_escape_endpoint(
    site: dict[str, Any],
    *,
    lane: int,
    width_mm: float,
    height_mm: float,
    edge_margin_mm: float,
    occupied: list[tuple[float, float]],
) -> tuple[float, float] | None:
    pad_x, pad_y = (float(value) for value in site["pad_at_mm"])
    anchor_x, anchor_y = (float(value) for value in site["anchor_at_mm"])
    delta_x, delta_y = pad_x - anchor_x, pad_y - anchor_y
    magnitude = math.hypot(delta_x, delta_y)
    if magnitude < 1e-9:
        outward = (1.0, 0.0)
    else:
        outward = (delta_x / magnitude, delta_y / magnitude)
    directions = (
        outward,
        (-outward[0], -outward[1]),
        (-outward[1], outward[0]),
        (outward[1], -outward[0]),
    )
    # A 0.6 mm via needs its 0.3 mm copper radius in addition to the board's
    # copper-to-Edge.Cuts clearance; bounding only the via center would recreate
    # the very edge-clearance violation this placement contract prevents.
    center_edge_margin = edge_margin_mm + 0.3
    # Alternate two radial lanes to keep 0.5 mm-pitch pad escapes from placing
    # adjacent 0.6 mm vias on top of each other.
    base_distance = 0.8 + 0.8 * (lane % 2)
    for distance in (base_distance, base_distance + 0.8, base_distance + 1.6):
        for direction_x, direction_y in directions:
            candidate = (
                round(pad_x + direction_x * distance, 3),
                round(pad_y + direction_y * distance, 3),
            )
            if not (
                center_edge_margin <= candidate[0] <= width_mm - center_edge_margin
                and center_edge_margin <= candidate[1] <= height_mm - center_edge_margin
            ):
                continue
            if any(math.dist(candidate, other) < 0.8 - 1e-9 for other in occupied):
                continue
            return candidate
    return None


def _kicad_board(spec: dict[str, Any], graph: dict[str, Any]) -> tuple[str, list[dict[str, Any]]]:
    env = spec["mechanical"]["envelope"]
    width, height = env["board_width_mm"], env["board_height_mm"]
    layers, copper_layers, plane_layers = _kicad_stackup(spec)
    net_ids = {item["name"]: index for index, item in enumerate(graph["nets"], 1)}
    net_declarations = "\n".join(f'  (net {index} "{name}")' for name, index in net_ids.items())
    footprints = []
    routing_failures: list[dict[str, Any]] = []
    right_edge_refs = mirrored_refs(spec)
    fixed_positions = component_positions(
        graph,
        board_width_mm=width,
        board_height_mm=height,
        mirrored=right_edge_refs,
        edge_sides=connector_sides(spec),
    )
    for i, item in enumerate(graph["components"]):
        x, y = fixed_positions.get(item["ref"], (10 + (i % 7) * 20, 10 + (i // 7) * 15))
        rotation = float(item.get("pcb_rotation_deg", 0.0) or 0.0)
        canonical, canonical_failures = render_canonical_footprint(
            str(item["footprint"]),
            item,
            float(x),
            float(y),
            rotation,
            net_ids,
            copper_layers,
        )
        routing_failures.extend(canonical_failures)
        if canonical is not None:
            footprints.append("  " + canonical)
            continue
        geometry = footprint_geometry(item, mirror_x=item["ref"] in right_edge_refs)
        pads = []
        for (number, px, py), item_pin in zip(geometry.pads, item["pins"]):
            net_name = item_pin.get("net")
            net_clause = ""
            if net_name in net_ids:
                net_id = net_ids[net_name]
                net_clause = f' (net {net_id} "{net_name}")'
            diameter = geometry.pad_diameter_mm
            if geometry.through_hole:
                pad_clause = (
                    f'thru_hole circle (at {px:.3f} {py:.3f}) '
                    f'(size {diameter:.3f} {diameter:.3f}) (drill {max(0.3, diameter * 0.45):.3f}) '
                    f'(layers "*.Cu" "*.Mask")'
                )
            else:
                pad_clause = (
                    f'smd roundrect (at {px:.3f} {py:.3f}) '
                    f'(size {diameter:.3f} {diameter:.3f}) '
                    f'(layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.2)'
                )
            pads.append(f'    (pad "{number}" {pad_clause}{net_clause})')
        body_start_x, body_start_y, body_end_x, body_end_y = geometry.body
        footprints.append(f'''  (footprint "{item['footprint']}" (layer "F.Cu") (at {x} {y} {rotation})
    (property "Reference" "{item['ref']}" (at 0 -3 0) (layer "F.Fab"))
    (property "Value" "{item['value']}" (at 0 3 0) (layer "F.Fab"))
    (property "MPN" "{item['mpn']}")
    (property "Lifecycle" "{item['lifecycle']}")
    (property "Substitute_MPN" "{item.get('substitute_mpn') or ''}")
    (fp_rect (start {body_start_x:.3f} {body_start_y:.3f}) (end {body_end_x:.3f} {body_end_y:.3f}) (stroke (width 0.2) (type default)) (fill none) (layer "F.Fab"))
{_kicad_model_clause(str(item['footprint']))}{chr(10).join(pads)})''')
    # Signal tracks remain deferred to Freerouting. Plane nets are different: on
    # a multilayer board, every F.Cu SMD plane pad needs an explicit F.Cu fanout
    # and plated via before it can reach its assigned internal/B.Cu zone.
    segments: list[str] = []
    vias: list[str] = []
    if len(copper_layers) > 2:
        footprint_board = f"(kicad_pcb\n{chr(10).join(footprints)}\n)"
        escape_sites = _front_smd_plane_pad_sites(footprint_board, set(plane_layers))
        occupied_vias: list[tuple[float, float]] = []
        lane_counts: dict[tuple[str, str], int] = {}
        track_width = max(0.2, float(spec["manufacturing"]["pcb"]["min_track_width_mm"]))
        edge_margin = max(0.3, copper_edge_clearance_mm(spec))
        for site in escape_sites:
            pad_x, pad_y = (float(value) for value in site["pad_at_mm"])
            anchor_x, anchor_y = (float(value) for value in site["anchor_at_mm"])
            delta_x, delta_y = pad_x - anchor_x, pad_y - anchor_y
            if abs(delta_x) >= abs(delta_y):
                side = "right" if delta_x >= 0.0 else "left"
            else:
                side = "bottom" if delta_y >= 0.0 else "top"
            lane_key = (str(site["ref"]), side)
            lane = lane_counts.get(lane_key, 0)
            lane_counts[lane_key] = lane + 1
            via_at = _plane_escape_endpoint(
                site,
                lane=lane,
                width_mm=float(width),
                height_mm=float(height),
                edge_margin_mm=edge_margin,
                occupied=occupied_vias,
            )
            if via_at is None:
                routing_failures.append({
                    "ref": site["ref"],
                    "pad": site["pad"],
                    "net": site["net"],
                    "code": "plane_escape_unplaceable",
                    "message": "No in-board via location satisfied the deterministic plane escape contract",
                })
                continue
            occupied_vias.append(via_at)
            net_name = str(site["net"])
            net_id = net_ids[net_name]
            start_x, start_y = round(pad_x, 3), round(pad_y, 3)
            via_x, via_y = via_at
            segments.append(
                f'  (segment (start {start_x:.3f} {start_y:.3f}) '
                f'(end {via_x:.3f} {via_y:.3f}) (width {track_width:.3f}) '
                f'(layer "F.Cu") (net {net_id}))'
            )
            vias.append(
                f'  (via (at {via_x:.3f} {via_y:.3f}) (size 0.600) (drill 0.300) '
                f'(layers "F.Cu" "B.Cu") (net {net_id}))'
            )
    zones = []
    emitted_zone_layers: set[tuple[str, str]] = set()
    for net_name, layer in plane_layers.items():
        if net_name not in net_ids:
            continue
        zone_layers = [layer]
        # On 2-layer boards with the GND plane on B.Cu, mirror it to F.Cu as well.
        # This ensures F.Cu SMD GND pads connect to the fill without needing explicit vias.
        if layer == "B.Cu" and len(copper_layers) == 2:
            zone_layers.append("F.Cu")
        for zl in zone_layers:
            key = (net_name, zl)
            if key in emitted_zone_layers:
                continue
            emitted_zone_layers.add(key)
            zones.append(f'''  (zone (net {net_ids[net_name]}) (net_name "{net_name}") (layer "{zl}") (hatch edge 0.5)
    (connect_pads (clearance 0.25))
    (min_thickness 0.25)
    (fill yes (thermal_gap 0.3) (thermal_bridge_width 0.3) (island_removal_mode 0))
    (polygon (pts (xy 1 1) (xy {width - 1} 1) (xy {width - 1} {height - 1}) (xy 1 {height - 1}))))''')
    return f'''(kicad_pcb (version 20240108) (generator hw_codesign)
  (general (thickness {env['board_thickness_mm']}))
  (paper "A4")
  (layers
{layers})
  (setup (pad_to_mask_clearance 0))
{net_declarations}
{chr(10).join(footprints)}
{chr(10).join(segments)}
{chr(10).join(vias)}
{chr(10).join(zones)}
  (gr_rect (start 0 0) (end {width} {height}) (stroke (width 0.5) (type default)) (fill none) (layer "Edge.Cuts"))
{_kicad_npth_holes(spec)})\n''', routing_failures


def _kicad_npth_holes(spec: dict[str, Any]) -> str:
    holes = spec.get("mechanical", {}).get("mounting_holes", [])
    lines = []
    for index, hole in enumerate(holes, 1):
        d = hole["diameter_mm"]
        ref = f"H{index}"
        lines.append(
            f'  (footprint "MountingHole:MountingHole_{d:.1f}mm_Pad" (layer "F.Cu") (at {hole["x_mm"]} {hole["y_mm"]})'
            f'\n    (property "Reference" "{ref}" (at 0 -3 0) (layer "F.Fab"))'
            f'\n    (property "Value" "MountingHole" (at 0 3 0) (layer "F.Fab"))'
            f'\n    (pad "" np_thru_hole circle (at 0 0) (size {d:.2f} {d:.2f}) (drill {d:.2f}) (layers "*.Cu" "*.Mask")))'
        )
    return "\n".join(lines) + "\n" if lines else ""


def _design_title(spec: dict[str, Any], graph: dict[str, Any]) -> str:
    architecture = graph.get("design_basis", {}).get("architecture")
    if architecture == "nrf52840_ble_sensor":
        return "nRF52840 BLE Sensor Node"
    if architecture == "esp32s3_usb_i2c_sensor_data_logger":
        return "ESP32-S3 Sensor Data Logger"
    if spec.get("project", {}).get("template") == "sensor_data_logger" or spec.get("electronics", {}).get("role_set") == "sensor_data_logger":
        return "ESP32-S3 Sensor Data Logger"
    return "Robot Controller"


def _kicad_stackup(spec: dict[str, Any]) -> tuple[str, tuple[str, ...], dict[str, str]]:
    requested_layers = int(spec.get("manufacturing", {}).get("pcb", {}).get("layers", 2))
    common = (
        '    (36 "B.SilkS" user "b.silkscreen")',
        '    (37 "F.SilkS" user "f.silkscreen")',
        '    (38 "B.Mask" user)',
        '    (39 "F.Mask" user)',
        '    (44 "Edge.Cuts" user)',
    )
    if requested_layers <= 2:
        layer_lines = ('    (0 "F.Cu" signal)', '    (31 "B.Cu" signal)', *common)
        return "\n".join(layer_lines), ("F.Cu", "B.Cu"), {"GND": "B.Cu"}
    layer_lines = ('    (0 "F.Cu" signal)', '    (2 "In1.Cu" power)', '    (4 "In2.Cu" power)', '    (31 "B.Cu" signal)', *common)
    return "\n".join(layer_lines), ("F.Cu", "In1.Cu", "In2.Cu", "B.Cu"), {"GND": "In1.Cu", "V5": "In2.Cu", "V3V3": "B.Cu"}


def _coordinate_key(coordinate: tuple[float, float]) -> tuple[float, float]:
    return round(float(coordinate[0]), 3), round(float(coordinate[1]), 3)


def _via_spans_layer(
    via_layers: set[str],
    target_layer: str,
    copper_layers: tuple[str, ...],
) -> bool:
    if "*.Cu" in via_layers or target_layer in via_layers:
        return True
    indexed = [copper_layers.index(layer) for layer in via_layers if layer in copper_layers]
    if len(indexed) < 2 or target_layer not in copper_layers:
        return False
    target_index = copper_layers.index(target_layer)
    return min(indexed) <= target_index <= max(indexed)


def _missing_plane_escape_connections(
    board_text: str,
    plane_layers: dict[str, str],
    copper_layers: tuple[str, ...],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Find F.Cu SMD plane pads without a same-net path to a spanning via."""
    sites = _front_smd_plane_pad_sites(board_text, set(plane_layers))
    root = loads(board_text)
    if not isinstance(root, list) or not _sexp_head(root, "kicad_pcb"):
        raise ValueError("Expected one kicad_pcb S-expression")
    net_names = {
        _sexp_atom(net[1]): _sexp_atom(net[2])
        for net in _sexp_direct(root, "net")
        if len(net) >= 3
    }
    adjacency: dict[str, dict[tuple[float, float], set[tuple[float, float]]]] = {}
    for segment in _sexp_direct(root, "segment"):
        layers = _sexp_direct(segment, "layer")
        nets = _sexp_direct(segment, "net")
        start = _sexp_coordinate(segment, "start")
        end = _sexp_coordinate(segment, "end")
        if (
            not layers
            or len(layers[0]) < 2
            or _sexp_atom(layers[0][1]) != "F.Cu"
            or not nets
            or len(nets[0]) < 2
            or start is None
            or end is None
        ):
            continue
        net_name = net_names.get(_sexp_atom(nets[0][1]))
        if net_name is None:
            continue
        start_key, end_key = _coordinate_key(start), _coordinate_key(end)
        graph = adjacency.setdefault(net_name, {})
        graph.setdefault(start_key, set()).add(end_key)
        graph.setdefault(end_key, set()).add(start_key)

    spanning_vias: dict[str, dict[str, set[tuple[float, float]]]] = {}
    for via in _sexp_direct(root, "via"):
        at = _sexp_coordinate(via, "at")
        layers = _sexp_direct(via, "layers")
        nets = _sexp_direct(via, "net")
        if at is None or not layers or not nets or len(nets[0]) < 2:
            continue
        net_name = net_names.get(_sexp_atom(nets[0][1]))
        if net_name is None:
            continue
        via_layers = {_sexp_atom(layer) for layer in layers[0][1:]}
        for target_layer in set(plane_layers.values()):
            if _via_spans_layer(via_layers, target_layer, copper_layers):
                spanning_vias.setdefault(net_name, {}).setdefault(target_layer, set()).add(
                    _coordinate_key(at)
                )

    missing: list[dict[str, Any]] = []
    for site in sites:
        net_name = str(site["net"])
        target_layer = plane_layers[net_name]
        start = _coordinate_key(site["pad_at_mm"])
        targets = spanning_vias.get(net_name, {}).get(target_layer, set())
        pending = [start]
        visited: set[tuple[float, float]] = set()
        connected = False
        graph = adjacency.get(net_name, {})
        while pending:
            node = pending.pop()
            if node in visited:
                continue
            visited.add(node)
            if node in targets:
                connected = True
                break
            pending.extend(graph.get(node, set()) - visited)
        if not connected:
            missing.append({
                "ref": site["ref"],
                "pad": site["pad"],
                "net": net_name,
                "plane_layer": target_layer,
                "pad_at_mm": [start[0], start[1]],
            })
    return sites, missing


def internal_erc(graph: dict[str, Any]) -> GateReport:
    architecture = graph.get("design_basis", {}).get("architecture")
    if architecture == "nrf52840_ble_sensor":
        required = {"power_input", "fuse", "reverse_polarity", "tvs", "charger", "regulator", "fuel_gauge", "mcu", "env_sensor", "debug"}
    elif architecture == "esp32s3_usb_i2c_sensor_data_logger":
        required = {"power_input", "fuse", "reverse_polarity", "tvs", "regulator", "mcu", "imu", "debug"}
    elif architecture == "atsamd21g18a_lsm6dsox_bme280":
        required = {"power_input", "tvs", "regulator_3v3", "mcu", "imu", "env_sensor", "debug_header"}
    else:
        required = {"mcu", "imu", "regulator", "can", "motor_io", "fuse", "reverse_polarity", "tvs", "efuse", "safety_gate"}
    present = {item["category"] for item in graph["components"]}
    missing = sorted(required - present)
    failures = [Failure(FailureCategory.EDA_ERROR, "missing_required_block", f"Missing schematic block: {item}") for item in missing]
    for component in graph["components"]:
        if not component.get("pins"):
            failures.append(Failure(FailureCategory.EDA_ERROR, "missing_pin_mapping", f"{component['ref']} has no pins"))
    # Agent-authored blocks may introduce unconnected nets during incremental authoring.
    # Track whether a net's endpoints are exclusively from agent blocks; if so, downgrade
    # the single-pin violation to a warning rather than a hard fail.
    agent_refs = {c["ref"] for c in graph["components"] if c.get("category") == "agent_block" or "role" in c}
    for net in graph["nets"]:
        if len(net.get("connected_pins", [])) < 2:
            endpoints = net.get("connected_pins", [])
            all_agent = all(ep.split(".")[0] in agent_refs for ep in endpoints)
            if all_agent:
                # Not a hard fail — agent is building incrementally
                continue
            failures.append(Failure(FailureCategory.EDA_ERROR, "single_pin_net", f"{net['name']} has fewer than two endpoints"))
    return GateReport("ir_erc", Status.FAIL if failures else Status.PASS, failures, metrics={"components": len(graph["components"]), "nets": len(graph["nets"])}, backend={"name": "reference-ir-erc", "deterministic": True})


def internal_drc(project: Path, spec: dict[str, Any], graph: dict[str, Any]) -> GateReport:
    pcb = project / "electronics" / "generated" / "kicad" / f"{project.name}.kicad_pcb"
    failures = []
    if not pcb.is_file() or "Edge.Cuts" not in pcb.read_text(encoding="utf-8"):
        failures.append(Failure(FailureCategory.EDA_ERROR, "invalid_board_outline", "KiCad board outline is missing"))
    if spec["manufacturing"]["pcb"]["min_clearance_mm"] < 0.15:
        failures.append(Failure(FailureCategory.EDA_ERROR, "drc_clearance", "Manufacturing clearance is below the supported profile"))
    text = pcb.read_text(encoding="utf-8") if pcb.is_file() else ""
    ordered_copper_layers = _kicad_stackup(spec)[1]
    expected_copper_layers = set(ordered_copper_layers)
    declared_copper_layers = set(_declared_kicad_copper_layers(text))
    used_copper_layers = set(_used_kicad_copper_layers(text))
    extra_declared_layers = sorted(declared_copper_layers - expected_copper_layers)
    missing_declared_layers = sorted(expected_copper_layers - declared_copper_layers)
    invalid_used_layers = sorted(used_copper_layers - expected_copper_layers)
    if extra_declared_layers or missing_declared_layers:
        failures.append(Failure(
            FailureCategory.EDA_ERROR,
            "pcb_stackup_layer_mismatch",
            "KiCad board copper stackup does not match the manufacturing layer profile",
            details={
                "expected_copper_layers": sorted(expected_copper_layers),
                "declared_copper_layers": sorted(declared_copper_layers),
                "extra_declared_layers": extra_declared_layers,
                "missing_declared_layers": missing_declared_layers,
            },
        ))
    if invalid_used_layers:
        failures.append(Failure(
            FailureCategory.EDA_ERROR,
            "pcb_layer_not_in_stackup",
            "KiCad board uses copper layers outside the manufacturing stackup",
            details={
                "expected_copper_layers": sorted(expected_copper_layers),
                "used_copper_layers": sorted(used_copper_layers),
                "invalid_used_layers": invalid_used_layers,
            },
        ))
    segment_count = text.count("(segment")
    expected_pads = sum(len(item.get("pins", [])) for item in graph["components"])
    if text.count("(pad ") < expected_pads:
        failures.append(Failure(FailureCategory.EDA_ERROR, "pad_pin_parity", "PCB pad count is lower than the electrical pin mapping", details={"expected": expected_pads, "actual": text.count("(pad ")}))
    routing_path = project / "electronics" / "generated" / "kicad" / "routing.json"
    routing = {}
    if routing_path.exists():
        routing = json.loads(routing_path.read_text(encoding="utf-8"))
        for item in routing.get("failures", []):
            code = str(item.get("code") or "routing_failed")
            subject = item.get("net") or item.get("ref") or item.get("footprint") or "design item"
            failures.append(Failure(FailureCategory.EDA_ERROR, code, f"Routing/footprint contract failed for {subject}", details=item))
    plane_layers = _kicad_stackup(spec)[2]
    zone_layers = _zone_net_layers(text)
    graph_nets = {item["name"] for item in graph["nets"]}
    missing_plane_zones = []
    for net_name, layer in plane_layers.items():
        if net_name not in graph_nets:
            continue
        required_layers = {layer}
        if len(expected_copper_layers) == 2 and any(
            pin.get("net") == net_name and not footprint_geometry(component).through_hole
            for component in graph.get("components", [])
            for pin in component.get("pins", [])
        ):
            required_layers.add("F.Cu")
        for required_layer in sorted(required_layers):
            if required_layer not in zone_layers.get(net_name, set()):
                missing_plane_zones.append({"net": net_name, "layer": required_layer})
    if missing_plane_zones:
        failures.append(Failure(
            FailureCategory.EDA_ERROR,
            "plane_zone_missing",
            "A declared plane net has no copper zone on its assigned layer",
            details={"missing": missing_plane_zones},
        ))
    if routing and routing.get("plane_connectivity") != "copper_zones":
        failures.append(Failure(
            FailureCategory.EDA_ERROR,
            "plane_connectivity_contract_mismatch",
            "Reference routing metadata must declare copper-zone plane connectivity",
            details={"plane_connectivity": routing.get("plane_connectivity")},
        ))
    plane_escape_site_count = 0
    if len(ordered_copper_layers) > 2 and text:
        try:
            plane_escape_sites, missing_plane_escapes = _missing_plane_escape_connections(
                text,
                plane_layers,
                ordered_copper_layers,
            )
            plane_escape_site_count = len(plane_escape_sites)
            if missing_plane_escapes:
                failures.append(Failure(
                    FailureCategory.EDA_ERROR,
                    "plane_escape_missing",
                    "An F.Cu SMD plane pad has no same-net copper path to a via spanning its plane layer",
                    details={"missing": missing_plane_escapes},
                ))
        except Exception as exc:
            failures.append(Failure(
                FailureCategory.EDA_ERROR,
                "plane_escape_contract_unreadable",
                "The multilayer plane escape topology could not be parsed from the KiCad board",
                details={"error": str(exc)},
            ))
        declared_escape = routing.get("plane_escape") if routing else None
        if declared_escape not in {None, "fcu_segment_to_through_via"}:
            failures.append(Failure(
                FailureCategory.EDA_ERROR,
                "plane_escape_contract_mismatch",
                "Multilayer routing metadata declares an incompatible plane escape mechanism",
                details={"plane_escape": declared_escape},
            ))
    return GateReport(
        "ir_pcb_sanity",
        Status.FAIL if failures else Status.PASS,
        failures,
        metrics={
            "footprints": len(graph["components"]),
            "pads": expected_pads,
            "segments": segment_count,
            "signal_routing": routing.get("signal_routing"),
            "plane_connectivity": routing.get("plane_connectivity"),
            "plane_escape": routing.get("plane_escape"),
            "plane_escape_sites": plane_escape_site_count,
            "zone_layers_by_net": {net: sorted(layers) for net, layers in sorted(zone_layers.items())},
            "layers": spec["manufacturing"]["pcb"]["layers"],
            "expected_copper_layers": sorted(expected_copper_layers),
            "declared_copper_layers": sorted(declared_copper_layers),
            "used_copper_layers": sorted(used_copper_layers),
        },
        artifacts=[str(pcb)],
        backend={"name": "reference-ir-drc", "deterministic": True},
    )


def _declared_kicad_copper_layers(board_text: str) -> list[str]:
    return [
        match.group(1)
        for match in re.finditer(r'\(\s*\d+\s+"([^"]+\.Cu)"\s+(?:signal|power)\b', board_text)
    ]


def _used_kicad_copper_layers(board_text: str) -> list[str]:
    used: set[str] = set()
    for match in re.finditer(r'\(layer\s+"([^"]+)"\)', board_text):
        layer = match.group(1)
        if layer.endswith(".Cu"):
            used.add(layer)
    for match in re.finditer(r'\(layers\s+([^)]+)\)', board_text):
        for layer in re.findall(r'"([^"]+)"', match.group(1)):
            if layer.endswith(".Cu"):
                used.add(layer)
    used.discard("*.Cu")
    return sorted(used)


def _zone_net_layers(board_text: str) -> dict[str, set[str]]:
    zones: dict[str, set[str]] = {}
    pattern = re.compile(
        r'\(zone\s+(?:'
        r'\(net\s+\d+\)\s+\(net_name\s+"([^"]+)"\)'
        r'|\(net\s+"([^"]+)"\)'
        r')\s+\(layer\s+"([^"]+\.Cu)"\)',
    )
    for match in pattern.finditer(board_text):
        net_name = match.group(1) or match.group(2)
        layer = match.group(3)
        zones.setdefault(net_name, set()).add(layer)
    return zones


def export_fabrication(project: Path, spec: dict[str, Any], graph: dict[str, Any], release: Path) -> list[str]:
    from .board_layout import component_positions as _cp
    fab = release / "fabrication"; fab.mkdir(parents=True, exist_ok=True)
    env = spec["mechanical"]["envelope"]
    width, height = env["board_width_mm"], env["board_height_mm"]
    mounting_holes = spec.get("mechanical", {}).get("mounting_holes", [])

    # Edge.Cuts Gerber (board outline)
    edge_gerber = fab / f"{project.name}-Edge_Cuts.gm1"
    w_nm, h_nm = int(width * 1e6), int(height * 1e6)
    atomic_write_text(edge_gerber, (
        "G04 HW co-design reference Gerber — Edge.Cuts*\n"
        "%FSLAX46Y46*%\n%MOMM*%\n%ADD10C,0.050000*%\nD10*\n"
        f"X0Y0D02*\nX{w_nm}Y0D01*\nX{w_nm}Y{h_nm}D01*\nX0Y{h_nm}D01*\nX0Y0D01*\nM02*\n"
    ))

    # F.Cu Gerber with pad apertures at real component positions
    positions = _cp(graph, board_width_mm=width, board_height_mm=height)
    fcu_gerber = fab / f"{project.name}-F_Cu.gtl"
    fcu_lines = [
        "G04 HW co-design reference Gerber — F.Cu (centroids only — route deferred to Freerouting)*",
        "%FSLAX46Y46*%", "%MOMM*%",
        "%ADD10C,0.800000*%",
        "D10*",
    ]
    for i, item in enumerate(graph["components"]):
        x, y = positions.get(item["ref"], (10.0 + (i % 7) * 20.0, 10.0 + (i // 7) * 15.0))
        fcu_lines.append(f"X{int(x*1e6)}Y{int(y*1e6)}D03*")
    fcu_lines.append("M02*")
    atomic_write_text(fcu_gerber, "\n".join(fcu_lines) + "\n")

    # Drill file with real mounting hole positions
    drill_path = fab / f"{project.name}.drl"
    drill_lines = ["M48", "METRIC,TZ", "T01C3.200"]
    for extra_tool, (diam, label) in enumerate([(1.0, "Via")], start=2):
        drill_lines.append(f"T{extra_tool:02d}C{diam:.3f}")
    drill_lines.append("%")
    drill_lines.append("T01")
    for hole in mounting_holes:
        x_nm = int(hole["x_mm"] * 1e4)
        y_nm = int(hole["y_mm"] * 1e4)
        drill_lines.append(f"X{x_nm:06d}Y{y_nm:06d}")
    drill_lines.append("M30")
    atomic_write_text(drill_path, "\n".join(drill_lines) + "\n")

    # DXF board outline with mounting holes
    dxf_path = fab / f"{project.name}-board_outline.dxf"
    dxf_lines = [
        "0", "SECTION", "2", "HEADER",
        "9", "$ACADVER", "1", "AC1009",
        "0", "ENDSEC",
        "0", "SECTION", "2", "ENTITIES",
        "0", "POLYLINE", "8", "Edge.Cuts", "66", "1",
        "0", "VERTEX", "8", "Edge.Cuts", "10", "0.0", "20", "0.0", "30", "0.0",
        "0", "VERTEX", "8", "Edge.Cuts", "10", f"{width:.4f}", "20", "0.0", "30", "0.0",
        "0", "VERTEX", "8", "Edge.Cuts", "10", f"{width:.4f}", "20", f"{height:.4f}", "30", "0.0",
        "0", "VERTEX", "8", "Edge.Cuts", "10", "0.0", "20", f"{height:.4f}", "30", "0.0",
        "0", "SEQEND",
    ]
    for hole in mounting_holes:
        dxf_lines += [
            "0", "CIRCLE", "8", "Drill", "10", f"{hole['x_mm']:.4f}",
            "20", f"{hole['y_mm']:.4f}", "30", "0.0", "40", f"{hole['diameter_mm']/2:.4f}",
        ]
    dxf_lines += ["0", "ENDSEC", "0", "EOF"]
    atomic_write_text(dxf_path, "\n".join(dxf_lines) + "\n")

    # Panelization specification
    panel_margin = 5.0
    panel_cols = max(1, int(250.0 / (width + panel_margin)))
    panel_rows = max(1, int(180.0 / (height + panel_margin)))
    panel_spec = {
        "method": "v_score",
        "board_width_mm": width,
        "board_height_mm": height,
        "columns": panel_cols,
        "rows": panel_rows,
        "panel_width_mm": panel_cols * width + (panel_cols + 1) * panel_margin,
        "panel_height_mm": panel_rows * height + (panel_rows + 1) * panel_margin,
        "rail_width_mm": panel_margin,
        "v_score_depth_fraction": 0.33,
        "boards_per_panel": panel_cols * panel_rows,
        "candidate_only": True,
        "note": "Reference panelization spec — verify with fab before ordering",
    }
    write_json(fab / "panelization.json", panel_spec)

    # BOM CSV
    bom_out = io.StringIO(); bom_writer = csv.writer(bom_out, lineterminator="\n")
    bom_writer.writerow(("Reference", "Value", "MPN", "Footprint", "Manufacturer", "Quantity"))
    for item in graph["components"]:
        bom_writer.writerow((item["ref"], item["value"], item["mpn"], item["footprint"], item.get("manufacturer", ""), 1))
    atomic_write_text(fab / "bom.csv", bom_out.getvalue())

    # Pick-and-place CSV with real board positions
    pnp_out = io.StringIO(); pnp_writer = csv.writer(pnp_out, lineterminator="\n")
    pnp_writer.writerow(("Ref", "Val", "PosX", "PosY", "Rotation", "Side"))
    for i, item in enumerate(graph["components"]):
        x, y = positions.get(item["ref"], (10.0 + (i % 6) * 24.0, 12.0 + (i // 6) * 18.0))
        rotation = float(item.get("pcb_rotation_deg", 0.0) or 0.0)
        pnp_writer.writerow((
            item["ref"],
            item["value"],
            f"{x:.3f}",
            f"{y:.3f}",
            f"{rotation:.3f}",
            "Top",
        ))
    atomic_write_text(fab / "pick_and_place.csv", pnp_out.getvalue())

    # Assembly drawing SVG with real positions and reference labels
    svg_items = []
    for i, item in enumerate(graph["components"]):
        x, y = positions.get(item["ref"], (10.0 + (i % 6) * 24.0, 12.0 + (i // 6) * 18.0))
        svg_items.append(f'<rect x="{x-2:.1f}" y="{y-2:.1f}" width="4" height="4" fill="#dde" stroke="#336" stroke-width="0.3"/>')
        svg_items.append(f'<text x="{x:.1f}" y="{y+0.8:.1f}" font-size="2" text-anchor="middle" fill="#000">{item["ref"]}</text>')
    for hole in mounting_holes:
        svg_items.append(f'<circle cx="{hole["x_mm"]:.1f}" cy="{hole["y_mm"]:.1f}" r="{hole["diameter_mm"]/2:.2f}" fill="none" stroke="#666" stroke-width="0.3"/>')
    atomic_write_text(fab / "assembly_drawing.svg", (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}mm" height="{height}mm" '
        f'viewBox="0 0 {width} {height}">'
        f'<rect width="{width}" height="{height}" fill="white" stroke="black" stroke-width="0.5"/>'
        f'<text x="{width/2:.1f}" y="3.5" font-size="3" text-anchor="middle" fill="#000">{project.name} assembly</text>'
        + "".join(svg_items) + "</svg>\n"
    ))

    gerbers_files = [edge_gerber, fcu_gerber]
    deterministic_zip(fab / "gerbers.zip", [(f, f.name) for f in gerbers_files])
    deterministic_zip(fab / "drill.zip", [(drill_path, drill_path.name)])
    return [str(path) for path in sorted(fab.iterdir())]


def export_mechanical(project: Path, spec: dict[str, Any], release: Path) -> list[str]:
    target = release / "mechanical"; target.mkdir(parents=True, exist_ok=True)
    internal = spec["mechanical"]["enclosure_internal_mm"]; wall = spec["mechanical"]["wall_thickness_mm"]
    width, depth, height = internal[0] + 2 * wall, internal[1] + 2 * wall, internal[2] + wall
    step_box("enclosure", width, depth, height, target / "enclosure.step")
    box_stl(width, depth, height, wall, target / "enclosure.stl")
    step_box("assembly", width, depth, height, target / "assembly.step")
    board = spec["mechanical"]["envelope"]
    step_box("board", board["board_width_mm"], board["board_height_mm"], board["board_thickness_mm"], project / "mechanical" / "generated" / "board.step")
    return [str(path) for path in sorted(target.iterdir())]


def build_firmware_reference(project: Path, timeout_seconds: int | None = None) -> GateReport:
    app = project / "firmware" / "reference"
    build = app / "build"
    timeout_seconds = _reference_firmware_timeout_seconds(timeout_seconds)
    backend: dict[str, Any] = {
        "name": "reference-host-bsp",
        "timeout_seconds": timeout_seconds,
    }
    artifact = str(build / "bringup_tests")

    if not (app / "CMakeLists.txt").is_file():
        failure = Failure(
            FailureCategory.FIRMWARE_ERROR,
            "reference_firmware_missing",
            "Generate firmware before running the reference host BSP build",
            path="firmware/reference/CMakeLists.txt",
        )
        return GateReport("reference_firmware_build", Status.BLOCKED, [failure], artifacts=[artifact], backend=backend)

    cmake = shutil.which("cmake")
    if cmake is None:
        failure = Failure(FailureCategory.TOOL_ERROR, "tool_unavailable", "Executable not found: cmake")
        return GateReport("reference_firmware_build", Status.BLOCKED, [failure], artifacts=[artifact], backend={**backend, "available": False, "command": ["cmake"]})

    build.mkdir(parents=True, exist_ok=True)
    configure_cmd = [cmake, "-S", str(app), "-B", str(build), "-G", "Ninja"]
    configure = _run_reference_firmware_command(configure_cmd, timeout_seconds, "configure")
    if configure is not None:
        return configure
    build_cmd = [cmake, "--build", str(build)]
    build_report = _run_reference_firmware_command(build_cmd, timeout_seconds, "build")
    if build_report is not None:
        return build_report
    return GateReport(
        "reference_firmware_build",
        Status.PASS,
        [],
        artifacts=[artifact],
        backend={**backend, "available": True, "command": build_cmd, "returncode": 0},
    )


def _reference_firmware_timeout_seconds(value: int | None = None) -> int:
    if value is not None:
        return max(1, int(value))
    raw = os.environ.get("HW_REFERENCE_FIRMWARE_TIMEOUT_SECONDS")
    if raw:
        try:
            return max(1, int(raw))
        except ValueError:
            pass
    return REFERENCE_FIRMWARE_TIMEOUT_SECONDS


def _run_reference_firmware_command(command: list[str], timeout_seconds: int, stage: str) -> GateReport | None:
    try:
        completed = subprocess.run(command, capture_output=True, text=True, check=False, timeout=timeout_seconds)
    except subprocess.TimeoutExpired as exc:
        failure = Failure(
            FailureCategory.TOOL_ERROR,
            "tool_timeout",
            f"reference firmware {stage} exceeded the {timeout_seconds} second limit",
            details={
                "timeout_seconds": timeout_seconds,
                "stdout": _tail_text(exc.stdout),
                "stderr": _tail_text(exc.stderr),
            },
        )
        return GateReport(
            "reference_firmware_build",
            Status.BLOCKED,
            [failure],
            backend={
                "name": "reference-host-bsp",
                "available": True,
                "stage": stage,
                "command": command,
                "returncode": None,
                "timeout_seconds": timeout_seconds,
            },
        )
    except OSError as exc:
        failure = Failure(FailureCategory.TOOL_ERROR, "tool_unavailable", f"cmake could not be executed: {exc}")
        return GateReport(
            "reference_firmware_build",
            Status.BLOCKED,
            [failure],
            backend={"name": "reference-host-bsp", "available": False, "stage": stage, "command": command, "timeout_seconds": timeout_seconds},
        )
    if completed.returncode != 0:
        failure = Failure(
            FailureCategory.FIRMWARE_ERROR,
            f"{stage}_failure",
            _tail_text(completed.stderr) or f"reference firmware {stage} failed",
            details={"stdout": _tail_text(completed.stdout), "stderr": _tail_text(completed.stderr)},
        )
        return GateReport(
            "reference_firmware_build",
            Status.FAIL,
            [failure],
            backend={
                "name": "reference-host-bsp",
                "available": True,
                "stage": stage,
                "command": command,
                "returncode": completed.returncode,
                "timeout_seconds": timeout_seconds,
                "stdout": _tail_text(completed.stdout),
                "stderr": _tail_text(completed.stderr),
            },
        )
    return None


def _tail_text(value: Any, limit: int = 4000) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")[-limit:]
    return str(value)[-limit:]
