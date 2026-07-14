from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Any

from .footprint_library import canonical_footprint_geometry

# The reference backend emits a compact in-board representation of each curated
# footprint. Geometry is derived from the selected package/footprint contract,
# never from pin count alone, and is shared by placement and KiCad generation.
PAD_DIAMETER_MM = 0.75  # conservative fallback only

# KiCad's native board rules default copper-to-Edge.Cuts clearance to 0.5 mm.
# Keep placement and generated project settings on the same explicit contract;
# callers can override it in ``manufacturing.pcb.min_copper_edge_clearance_mm``.
DEFAULT_COPPER_EDGE_CLEARANCE_MM = 0.5

# Two components are unambiguously broken when their anchors land this close,
# whatever the footprints look like.
MIN_ANCHOR_SEPARATION_MM = 1.5

# Right-edge connectors mirror their pad grid inward so the pads stay on-board.
_MIRRORED_EDGE_REFS = frozenset(f"J{index}" for index in range(17, 23))

# Body dimensions for footprint identifiers whose size is not encoded in the
# KiCad library name. Values come from the curated package contract or the
# manufacturer's mechanical drawing. Entries with dimensions in their library
# name are parsed by ``_body_size_from_contract`` below.
_FOOTPRINT_BODY_SIZE_MM: dict[str, tuple[float, float]] = {
    "Nordic_nRF52840:nRF52840-QIAA": (7.0, 7.0),
    "RF_Module:ESP32-S3-WROOM-1": (18.0, 25.5),
    "RF_Module:ESP32-WROOM-32": (18.0, 25.5),
    "Package_LGA:LGA-14": (3.0, 2.5),
    "Package_DFN_QFN:VQFN-16": (4.0, 4.0),
    "Package_DFN_QFN:VQFN-24-1EP": (4.0, 4.0),
    "Package_DFN_QFN:WQFN-30": (6.0, 4.0),
    "Package_TO_SOT_SMD:SOT-23": (2.9, 1.3),
    "Package_TO_SOT_SMD:SOT-23-5": (3.0, 1.75),
    "Package_TO_SOT_SMD:SOT-23-6": (3.0, 1.75),
    "Package_TO_SOT_SMD:SOT-23-8": (3.0, 3.0),
    "Package_TO_SOT_SMD:SOT-223-3_TabPin2": (6.5, 3.5),
    "Package_TO_SOT_SMD:SOD-323": (2.5, 1.25),
    "Package_TO_SOT_SMD:SOT-323_SC-70": (2.0, 1.25),
    "Diode_SMD:D_SMC": (7.9, 6.2),
    "Crystal:Crystal_SMD_HC-49S": (11.4, 4.8),
    "Connector_USB:USB_C_GCT_USB4105": (9.0, 7.35),
    "Connector_Samtec:FTSH-105": (12.7, 5.1),
    "Connector_RJ45:RJ45_Hanrun_HR911105A": (16.0, 16.0),
    "Connector_Coaxial:Hirose_U.FL-R-SMT-1_Vertical": (3.0, 3.1),
    "Connector_JST:JST_PH_S2B-PH-K_1x02_P2.00mm_Horizontal": (7.5, 6.0),
    "TerminalBlock:Phoenix_3Pin": (15.0, 8.0),
    "HW_Curated:MIDI_Fuse": (10.0, 4.0),
    "HW_Curated:MicroFit_2Pin": (9.0, 9.0),
    "HW_Curated:MicroFit_3Pin": (12.0, 9.0),
    "HW_Curated:MicroFit_8Pin": (18.0, 10.0),
}

_PACKAGE_BODY_SIZE_MM: dict[str, tuple[float, float]] = {
    "aQFN-73": (7.0, 7.0),
    "LCC-41": (18.0, 25.5),
    "SOT-23-3": (2.9, 1.3),
    "SOT-23-5": (3.0, 1.75),
    "SOT-23-6": (3.0, 1.75),
    "SOT-23-8": (3.0, 3.0),
    "SOD-323": (2.5, 1.25),
    "SOT-323": (2.0, 1.25),
    "SMC": (7.9, 6.2),
}


@dataclass(frozen=True)
class FootprintGeometry:
    """Package-aware reference geometry expressed relative to its centre."""

    pads: tuple[tuple[str, float, float], ...]
    body: tuple[float, float, float, float]
    pitch: float
    columns: int
    pad_diameter_mm: float = PAD_DIAMETER_MM
    through_hole: bool = False
    source: str = "package_contract"
    extent_override: tuple[float, float, float, float] | None = None

    @property
    def extent(self) -> tuple[float, float, float, float]:
        """Anchor-relative ``(min_x, min_y, max_x, max_y)`` of body and pad copper."""
        if self.extent_override is not None:
            return self.extent_override
        radius = self.pad_diameter_mm / 2.0
        xs = [self.body[0], self.body[2]]
        ys = [self.body[1], self.body[3]]
        for _number, dx, dy in self.pads:
            xs.extend((dx - radius, dx + radius))
            ys.extend((dy - radius, dy + radius))
        return (min(xs), min(ys), max(xs), max(ys))


def copper_edge_clearance_mm(spec: dict[str, Any]) -> float:
    """Copper/body clearance from the board outline used by placement and KiCad."""
    value = spec.get("manufacturing", {}).get("pcb", {}).get(
        "min_copper_edge_clearance_mm", DEFAULT_COPPER_EDGE_CLEARANCE_MM
    )
    try:
        return max(0.0, float(value))
    except (TypeError, ValueError):
        return DEFAULT_COPPER_EDGE_CLEARANCE_MM


def connector_sides(spec: dict[str, Any]) -> dict[str, str]:
    """Board edge each declared connector must reach (ref -> side)."""
    return {
        str(interface["ref"]): str(interface.get("side", "front"))
        for interface in spec.get("mechanical", {}).get("connector_interfaces", [])
        if interface.get("ref")
    }


def _edge_seed_anchor(
    extent: tuple[float, float, float, float],
    side: str,
    offset: float,
    width: float,
    height: float,
) -> tuple[float, float]:
    """Anchor that lands a footprint flush against ``side``, ``offset`` along the edge."""
    min_x, min_y, max_x, max_y = extent
    if side == "rear":
        return (offset - min_x, height - _SEED_EDGE_MARGIN_MM - max_y)
    if side == "left":
        return (_SEED_EDGE_MARGIN_MM - min_x, offset - min_y)
    if side == "right":
        return (width - _SEED_EDGE_MARGIN_MM - max_x, offset - min_y)
    return (offset - min_x, _SEED_EDGE_MARGIN_MM - min_y)  # front


def mirrored_refs(spec: dict[str, Any]) -> frozenset[str]:
    """Refs whose pad grid is mirrored so it grows away from the right edge."""
    declared = {
        str(interface.get("ref"))
        for interface in spec.get("mechanical", {}).get("connector_interfaces", [])
        if interface.get("side") == "right" and interface.get("ref")
    }
    return frozenset(declared | set(_MIRRORED_EDGE_REFS))


def _body_size_from_contract(component: dict[str, Any]) -> tuple[tuple[float, float], str] | None:
    footprint = str(component.get("footprint") or "")
    package = str(component.get("package") or "")
    body_mm = component.get("mechanical", {}).get("body_mm") if isinstance(component.get("mechanical"), dict) else None
    if isinstance(body_mm, list) and len(body_mm) == 2 and all(isinstance(value, (int, float)) and value > 0 for value in body_mm):
        return (float(body_mm[0]), float(body_mm[1])), "project_mechanical_contract"
    if footprint in _FOOTPRINT_BODY_SIZE_MM:
        return _FOOTPRINT_BODY_SIZE_MM[footprint], "verified_footprint"
    if package in _PACKAGE_BODY_SIZE_MM:
        return _PACKAGE_BODY_SIZE_MM[package], "package_contract"

    pin_header = re.search(r"PinHeader_(\d+)x(\d+)_P(\d+(?:\.\d+)?)mm", footprint)
    if pin_header:
        columns, rows, pitch = (
            int(pin_header.group(1)),
            int(pin_header.group(2)),
            float(pin_header.group(3)),
        )
        return (
            max(2.5, columns * pitch),
            max(2.5, rows * pitch),
        ), "kicad_pin_header_name"

    metric = re.search(r"_(\d{4})Metric(?:_|$)", footprint)
    if metric:
        code = metric.group(1)
        return (int(code[:2]) / 10.0, int(code[2:]) / 10.0), "kicad_metric_name"

    sized = re.search(r"_(\d+(?:\.\d+)?)x(\d+(?:\.\d+)?)mm(?:_|$)", footprint)
    if sized:
        return (float(sized.group(1)), float(sized.group(2))), "kicad_dimensioned_name"

    return None


def _pitch_from_contract(component: dict[str, Any], pin_count: int) -> float:
    footprint = str(component.get("footprint") or "")
    pitch_match = re.search(r"_P(\d+(?:\.\d+)?)mm(?:_|$)", footprint)
    if pitch_match:
        return float(pitch_match.group(1))
    if "ESP32-S3-WROOM-1" in footprint:
        return 1.27
    if "nRF52840-QIAA" in footprint:
        return 0.5
    if any(marker in footprint for marker in ("SOT-23", "SOT-323", "SC-70")):
        return 0.95
    if pin_count <= 2:
        return 1.0
    return 1.27


def _is_through_hole_footprint(footprint: str) -> bool:
    markers = (
        "PinHeader_", "JST_PH_", "TerminalBlock:", "Phoenix_", "MicroFit_",
        "MIDI_Fuse", "RJ45_", "FTSH-105",
    )
    return any(marker in footprint for marker in markers)


def _grid_pads(
    numbers: list[str], rows: int, columns: int, pitch: float, *, mirror_x: bool
) -> tuple[tuple[str, float, float], ...]:
    width = (columns - 1) * pitch
    height = (rows - 1) * pitch
    sign = -1.0 if mirror_x else 1.0
    return tuple(
        (
            number,
            ((index % columns) * pitch - width / 2.0) * sign,
            (index // columns) * pitch - height / 2.0,
        )
        for index, number in enumerate(numbers)
    )


def _perimeter_pads(
    numbers: list[str], width: float, height: float, pitch: float, *, mirror_x: bool
) -> tuple[tuple[str, float, float], ...]:
    if len(numbers) <= 2:
        return _grid_pads(numbers, 1, max(1, len(numbers)), min(pitch, max(width, 1.0)), mirror_x=mirror_x)

    perimeter_numbers = numbers
    centre_number: str | None = None
    if len(numbers) % 4 == 1 and len(numbers) >= 9:
        perimeter_numbers, centre_number = numbers[:-1], numbers[-1]
    side_count = max(1, math.ceil(len(perimeter_numbers) / 4))
    x_edge = max(0.0, width / 2.0 - min(0.35, width / 4.0))
    y_edge = max(0.0, height / 2.0 - min(0.35, height / 4.0))
    positions: list[tuple[float, float]] = []
    for index in range(len(perimeter_numbers)):
        side, offset_index = divmod(index, side_count)
        count_on_side = min(side_count, len(perimeter_numbers) - side * side_count)
        # Keep the end pads away from shared corners. The previous full-edge
        # interpolation placed adjacent sides on the same coordinate, creating
        # copper shorts inside the synthetic footprint itself.
        axis_limit = y_edge if side in {0, 2} else x_edge
        corner_gap = min(max(0.35, pitch * 0.5), axis_limit * 0.75)
        usable_span = max(0.0, (axis_limit - corner_gap) * 2.0)
        side_pitch = min(pitch, usable_span / max(1, count_on_side - 1))
        offset = (offset_index - (count_on_side - 1) / 2.0) * side_pitch
        if side == 0:
            point = (-x_edge, -offset)
        elif side == 1:
            point = (offset, -y_edge)
        elif side == 2:
            point = (x_edge, offset)
        else:
            point = (-offset, y_edge)
        positions.append(point)
    sign = -1.0 if mirror_x else 1.0
    pads = [
        (number, x * sign, y)
        for number, (x, y) in zip(perimeter_numbers, positions)
    ]
    if centre_number is not None:
        pads.append((centre_number, 0.0, 0.0))
    return tuple(pads)


def footprint_geometry(component: dict[str, Any], *, mirror_x: bool = False) -> FootprintGeometry:
    """Return package-aware geometry shared by placement and KiCad emission."""
    pins = component.get("pins", [])
    numbers = [str(pin.get("number")) for pin in pins]
    footprint = str(component.get("footprint") or "")
    canonical = canonical_footprint_geometry(footprint)
    physical = _body_size_from_contract(component)
    if canonical is not None:
        body_width = canonical.body_extent[2] - canonical.body_extent[0]
        body_height = canonical.body_extent[3] - canonical.body_extent[1]
        source = "canonical_kicad_snapshot"
    elif physical is None:
        # Unresolved/custom parts stay candidate-only, but use a bounded fallback
        # rather than a pin-count strip that can dwarf the entire board.
        side = max(3.0, min(12.0, math.sqrt(max(len(numbers), 1)) * 1.5))
        body_width, body_height = side, side
        source = "bounded_fallback"
    else:
        (body_width, body_height), source = physical
    pitch = _pitch_from_contract(component, len(numbers))
    through_hole = _is_through_hole_footprint(footprint)

    row_match = re.search(r"PinHeader_(\d+)x(\d+)_P(\d+(?:\.\d+)?)mm", footprint)
    if row_match:
        columns, rows = int(row_match.group(1)), int(row_match.group(2))
        pitch = float(row_match.group(3))
        pads = _grid_pads(numbers, rows, columns, pitch, mirror_x=mirror_x)
    elif "FTSH-105" in footprint:
        rows, columns = 2, 5
        pads = _grid_pads(numbers, rows, columns, 1.27, mirror_x=mirror_x)
    elif any(marker in footprint for marker in ("SOT-23", "SOT-323", "SC-70")):
        rows = max(1, math.ceil(len(numbers) / 2))
        left = numbers[:rows]
        right = numbers[rows:]
        y_pitch = min(pitch, max(0.4, (body_height - 0.5) / max(1, rows - 1)))
        left_y = [(index - (len(left) - 1) / 2.0) * y_pitch for index in range(len(left))]
        right_y = [((len(right) - 1) / 2.0 - index) * y_pitch for index in range(len(right))]
        x_edge = max(0.0, body_width / 2.0 - 0.2)
        sign = -1.0 if mirror_x else 1.0
        pads = tuple(
            [(number, -x_edge * sign, y) for number, y in zip(left, left_y)]
            + [(number, x_edge * sign, y) for number, y in zip(right, right_y)]
        )
        columns = 2
    elif "MicroFit_8Pin" in footprint:
        rows, columns = 2, 4
        pitch = 3.0
        pads = _grid_pads(numbers, rows, columns, pitch, mirror_x=mirror_x)
    elif "MicroFit_3Pin" in footprint:
        rows, columns = 1, 3
        pitch = 3.0
        pads = _grid_pads(numbers, rows, columns, pitch, mirror_x=mirror_x)
    elif "MicroFit_2Pin" in footprint:
        rows, columns = 1, 2
        pitch = 3.0
        pads = _grid_pads(numbers, rows, columns, pitch, mirror_x=mirror_x)
    elif through_hole:
        rows, columns = 1, max(1, len(numbers))
        through_pitch = max(pitch, min(5.08, max(1.27, body_width - 2.0)))
        pads = _grid_pads(numbers, rows, columns, through_pitch, mirror_x=mirror_x)
    else:
        columns = max(1, math.ceil(len(numbers) / 4))
        pads = _perimeter_pads(numbers, body_width, body_height, pitch, mirror_x=mirror_x)

    pad_diameter = 0.9 if through_hole else max(0.2, min(0.6, pitch * 0.5))
    if not through_hole and len(pads) > 1:
        minimum_pad_spacing = min(
            math.dist(left[1:], right[1:])
            for index, left in enumerate(pads)
            for right in pads[index + 1:]
        )
        pad_diameter = min(pad_diameter, max(0.2, minimum_pad_spacing * 0.7))
    extent_override = canonical.placement_extent if canonical is not None else None
    return FootprintGeometry(
        pads=pads,
        body=(-body_width / 2.0, -body_height / 2.0, body_width / 2.0, body_height / 2.0),
        pitch=pitch,
        columns=columns,
        pad_diameter_mm=pad_diameter,
        through_hole=through_hole,
        source=source,
        extent_override=extent_override,
    )


# Hand-tuned anchor coordinates for the robotics-controller reference design.
# These are the authoritative placement seed. Changes should be driven by
# explicit placement or physical-correctness gates so downstream routing and
# mechanical checks keep a traceable reason for coordinate movement.
_ANCHORS: dict[str, tuple[float, float]] = {
    "J1": (20.0, 5.0), "F1": (38.0, 5.0), "Q1": (56.0, 5.0), "D1": (74.0, 5.0),
    "U3": (92.0, 5.0), "U4": (112.0, 18.0), "U5": (132.0, 18.0),
    "J5": (120.0, 95.0), "D2": (120.0, 86.0), "R4": (60.0, 27.0), "U6": (90.0, 27.0),
    "J3": (80.0, 5.0), "R1": (104.0, 20.0), "U2": (22.0, 48.0), "R2": (42.0, 48.0),
    "R3": (58.0, 48.0), "J2": (140.0, 95.0), "Q2": (124.0, 48.0), "J4": (104.0, 69.0),
    "U1": (70.0, 37.0),
}

_SENSOR_DATA_LOGGER_ANCHORS: dict[str, tuple[float, float]] = {
    "J1": (18.0, 4.0),
    "F1": (26.0, 10.0),  # fuse, offset from USB-C CC pads; power path still routes to Q1
    "Q1": (34.0, 4.0),   # reverse-polarity ideal-diode, before regulator
    "D1": (30.0, 10.0),
    "U3": (44.0, 12.0),
    "U1": (44.0, 43.0),
    "U2": (18.0, 28.0),
    "J2": (54.0, 39.0),
    "R1": (18.0, 38.0),
    "R2": (27.0, 38.0),
    "R3": (50.0, 25.0),
    "C1": (35.0, 39.0),
    "C2": (44.0, 39.0),
    "C9": (56.0, 14.0),
}


def _seed_table() -> dict[str, tuple[tuple[float, float], str]]:
    """Provenance-tagged seed coordinates.

    Each entry maps a reference to ``((x_mm, y_mm), source)`` where ``source``
    records how the seed coordinate was derived: a hand-tuned anchor, a
    decoupling-capacitor row, or a connector pushed to a board edge.
    """
    table: dict[str, tuple[tuple[float, float], str]] = {
        ref: (xy, "curated_anchor") for ref, xy in _ANCHORS.items()
    }
    for index in range(10):
        table[f"C{index + 1}"] = ((24.0 + (index % 5) * 22.0, 76.0 + (index // 5) * 13.0), "decoupling_row_seed")
    for index in range(1, 13):
        side_index = (index - 1) % 6
        table[f"J{index + 10}"] = ((9.0 if index <= 6 else 151.0, 7.0 + side_index * 15.0), "connector_edge_seed")
    return table


def _sensor_data_logger_seed_table() -> dict[str, tuple[tuple[float, float], str]]:
    return {
        ref: (xy, "sensor_data_logger_anchor")
        for ref, xy in _SENSOR_DATA_LOGGER_ANCHORS.items()
    }


def _grid_fallback(index: int) -> tuple[float, float]:
    return (10.0 + (index % 7) * 20.0, 10.0 + (index // 7) * 15.0)


_SEED_EDGE_MARGIN_MM = 1.0
_SEED_GAP_MM = 0.5


def _shelf_pack(
    items: list[dict[str, Any]],
    occupied: list[tuple[float, float, float, float]],
    anchored_at: list[tuple[float, float]],
    width: float,
    height: float,
    mirrored: frozenset[str],
) -> dict[str, tuple[float, float]]:
    """Lay unanchored components out in shelves, skipping already-occupied boxes.

    A footprint-aware seed. It is deliberately dumb about connectivity — the cost
    solver refines from here — but it will not seed a part on top of an anchored
    one, which the old ``_grid_fallback`` did routinely. When the parts genuinely
    do not fit, it keeps laying shelves past the bottom edge so the containment
    check reports an honest overflow instead of a pile of coincident parts.
    """
    packed: dict[str, tuple[float, float]] = {}
    taken = list(occupied)
    anchors = list(anchored_at)
    cursor_x, cursor_y, shelf_height = _SEED_EDGE_MARGIN_MM, _SEED_EDGE_MARGIN_MM, 0.0
    extents = {
        item["ref"]: footprint_geometry(item, mirror_x=item["ref"] in mirrored).extent
        for item in items
    }
    # First-fit decreasing height: tall parts first, so short parts backfill the
    # shelves they open instead of each opening a shelf of its own.
    ordered = sorted(
        items,
        key=lambda item: (
            -(extents[item["ref"]][3] - extents[item["ref"]][1]),
            item["ref"],
        ),
    )
    for item in ordered:
        ref = item["ref"]
        min_x, min_y, max_x, max_y = extents[ref]
        span_w, span_h = max_x - min_x, max_y - min_y
        placed = False
        while not placed:
            if cursor_x + span_w > width - _SEED_EDGE_MARGIN_MM:
                cursor_x = _SEED_EDGE_MARGIN_MM
                cursor_y += shelf_height + _SEED_GAP_MM
                shelf_height = 0.0
            box = (cursor_x, cursor_y, cursor_x + span_w, cursor_y + span_h)
            clash = next(
                (
                    other for other in taken
                    if box[0] < other[2] + _SEED_GAP_MM and other[0] - _SEED_GAP_MM < box[2]
                    and box[1] < other[3] + _SEED_GAP_MM and other[1] - _SEED_GAP_MM < box[3]
                ),
                None,
            )
            if clash is not None:
                cursor_x = clash[2] + _SEED_GAP_MM
                continue
            anchor = (cursor_x - min_x, cursor_y - min_y)
            # Footprints can clear each other while their anchors (pin 1) sit almost
            # on top of one another, which the coincident-components gate rejects.
            if any(
                math.dist(anchor, other) < MIN_ANCHOR_SEPARATION_MM
                for other in anchors
            ):
                cursor_x += MIN_ANCHOR_SEPARATION_MM
                continue
            packed[ref] = anchor
            anchors.append(anchor)
            taken.append(box)
            cursor_x = box[2] + _SEED_GAP_MM
            shelf_height = max(shelf_height, span_h)
            placed = True
    return packed


def component_positions(
    graph: dict[str, Any],
    board_width_mm: float | None = None,
    board_height_mm: float | None = None,
    mirrored: frozenset[str] = frozenset(),
    edge_sides: dict[str, str] | None = None,
) -> dict[str, tuple[float, float]]:
    """Coordinate lookup (ref -> (x_mm, y_mm)).

    Prefers ``pcb_position_mm`` written by the placement pipeline so that all
    downstream consumers (reference backend, fabrication export) use the same
    coordinates the placement gate validated.  Falls back to the board family's
    seed table, then — when the board envelope is known — to a footprint-aware
    shelf pack.
    """
    table = _seed_table_for_graph(graph)
    positions: dict[str, tuple[float, float]] = {}
    unanchored: list[dict[str, Any]] = []
    for index, item in enumerate(graph.get("components", [])):
        ref = item["ref"]
        if "pcb_position_mm" in item:
            pos = item["pcb_position_mm"]
            positions[ref] = (float(pos[0]), float(pos[1]))
        elif item.get("category") == "usb_cc_pulldown":
            positions[ref] = _usb_c_rd_seed_position(item, graph, positions, table)
        elif item.get("category") == "xtal_cap":
            positions[ref] = _xtal_cap_seed_position(item, graph, positions, table)
        elif ref in table:
            positions[ref] = table[ref][0]
        elif board_width_mm and board_height_mm:
            unanchored.append(item)
        else:
            positions[ref] = _grid_fallback(index)

    if unanchored and board_width_mm and board_height_mm:
        # Connectors have to reach their declared edge, and the shelf pack fills the
        # board from the front inward — so seed them onto their edge first and let
        # everything else pack around them.
        sides = edge_sides or {}
        edge_offset: dict[str, float] = {}
        still_unanchored: list[dict[str, Any]] = []
        for item in unanchored:
            ref = item["ref"]
            side = sides.get(ref)
            if side is None:
                still_unanchored.append(item)
                continue
            extent = footprint_geometry(item, mirror_x=ref in mirrored).extent
            span = (extent[2] - extent[0]) if side in {"front", "rear"} else (extent[3] - extent[1])
            offset = edge_offset.get(side, _SEED_EDGE_MARGIN_MM)
            positions[ref] = _edge_seed_anchor(
                extent, side, offset, board_width_mm, board_height_mm
            )
            edge_offset[side] = offset + span + _SEED_GAP_MM
        unanchored = still_unanchored

        components = {item["ref"]: item for item in graph.get("components", [])}
        occupied = []
        for ref, (x_mm, y_mm) in positions.items():
            min_x, min_y, max_x, max_y = footprint_geometry(
                components[ref], mirror_x=ref in mirrored
            ).extent
            occupied.append((x_mm + min_x, y_mm + min_y, x_mm + max_x, y_mm + max_y))
        positions.update(
            _shelf_pack(
                unanchored,
                occupied,
                list(positions.values()),
                board_width_mm,
                board_height_mm,
                mirrored,
            )
        )
    return positions


def placement_sources(
    graph: dict[str, Any],
    board_width_mm: float | None = None,
    board_height_mm: float | None = None,
    edge_sides: dict[str, str] | None = None,
) -> dict[str, str]:
    """Provenance tag for each placed reference (mirrors ``component_positions``)."""
    table = _seed_table_for_graph(graph)
    sides = edge_sides or {}
    sources: dict[str, str] = {}
    for item in graph.get("components", []):
        ref = item["ref"]
        if "pcb_position_mm" in item and item.get("placement_source"):
            sources[ref] = str(item["placement_source"])
        elif item.get("category") == "usb_cc_pulldown" and ref not in table:
            sources[ref] = "usb_c_rd_connector_seed"
        elif item.get("category") == "xtal_cap" and ref not in table:
            sources[ref] = "crystal_load_cap_seed"
        elif ref in table:
            sources[ref] = table[ref][1]
        elif board_width_mm and board_height_mm and ref in sides:
            sources[ref] = "connector_edge_seed"
        elif board_width_mm and board_height_mm:
            sources[ref] = "shelf_pack_seed"
        else:
            sources[ref] = "grid_fallback"
    return sources


def _usb_c_rd_seed_position(
    item: dict[str, Any],
    graph: dict[str, Any],
    positions: dict[str, tuple[float, float]],
    table: dict[str, tuple[tuple[float, float], str]],
) -> tuple[float, float]:
    cc_nets = {pin.get("net") for pin in item.get("pins", []) if str(pin.get("net", "")).startswith("USB_CC")}
    for connector in graph.get("components", []):
        connector_ref = connector.get("ref")
        if not connector_ref or connector_ref == item.get("ref"):
            continue
        connector_nets = {pin.get("net") for pin in connector.get("pins", [])}
        if not (cc_nets & connector_nets):
            continue
        if connector_ref in positions:
            x_mm, y_mm = positions[connector_ref]
        elif connector_ref in table:
            x_mm, y_mm = table[connector_ref][0]
        else:
            continue
        x_offset = 4.0 if "USB_CC1" in cc_nets else 8.0
        return (x_mm + x_offset, y_mm + 3.0)
    return _grid_fallback(len(positions))


def _xtal_cap_seed_position(
    item: dict[str, Any],
    graph: dict[str, Any],
    positions: dict[str, tuple[float, float]],
    table: dict[str, tuple[tuple[float, float], str]],
) -> tuple[float, float]:
    cap_nets = {pin.get("net") for pin in item.get("pins", []) if pin.get("net") and pin.get("net") != "GND"}
    for crystal in graph.get("components", []):
        crystal_ref = crystal.get("ref")
        category = str(crystal.get("category", ""))
        if not crystal_ref or "crystal" not in category:
            continue
        crystal_nets = {pin.get("net") for pin in crystal.get("pins", []) if pin.get("net")}
        if not (cap_nets & crystal_nets):
            continue
        if crystal_ref in positions:
            x_mm, y_mm = positions[crystal_ref]
        elif crystal_ref in table:
            x_mm, y_mm = table[crystal_ref][0]
        else:
            continue
        y_offset = -3.0 if any(str(net).endswith(("XIN", "XIN32")) for net in cap_nets) else 3.0
        return (x_mm + 3.0, y_mm + y_offset)
    return _grid_fallback(len(positions))


_BLE_SENSOR_NODE_ANCHORS: dict[str, tuple[float, float]] = {
    # Power path: left edge top to right edge top
    "J1":  (12.0, 4.0),   # USB-C, top-left edge
    "F1":  (17.0, 4.0),   # fuse, next in power path
    "Q1":  (24.0, 4.0),   # reverse-polarity mosfet
    "U2":  (30.0, 4.0),   # LiPo charger, near power path
    "BT1": (43.0, 4.0),   # JST LiPo connector, top-right
    "R4":  (37.0, 4.0),   # Charge-set resistor, beside charger
    "C3":  (44.0, 10.0),  # 10uF VBAT bulk cap, near BT1; avoids the D1-2 USB_DP pad
    # LDO between charger rail and MCU
    "LD1": (32.0, 11.0),  # AP2112K LDO, between charger (top) and MCU (centre)
    # Centralised MCU + close decoupling
    "U1":  (25.0, 28.0),  # nRF52840 MCU, near rear edge for integral antenna clearance
    "C1":  (25.0, 12.0),  # 100nF decoupling, directly above MCU V3V3 pin
    # C2 was at (31,19): C2-2 GND landed at (33,19) = U1-5 I2C_SCL (same cell),
    # blocking freerouting from accessing the I2C_SCL pad. Moved to (26,19) so
    # C2-2 GND lands near the MCU GND cluster without sharing the component center.
    "C2":  (27.0, 19.0),  # 100nF decoupling, beside MCU GND cluster (avoids I2C_SCL pad)
    "C4":  (19.0, 19.0),  # 10uF V3V3 bulk cap, left of MCU
    # Sensors on left, away from nRF52840 RF antenna (top-right)
    "U5":  (10.0, 24.0),  # SHT31 temp/humidity, left of MCU and away from RF area
    "R1":  (10.0, 13.0),  # I2C SCL pull-up, near sensors
    "R2":  (15.0, 13.0),  # I2C SDA pull-up, near sensors
    # Fuel gauge and USB ESD on right; U3 moved UP to (40,6) so that U3-4 GND (index 3,
    # pitch=3 high-current layout) lands at y=15 instead of y=27, clearing the y=24-28
    # signal routing channel between U1 and J2.
    "U3":  (40.0, 6.0),   # BQ27441 fuel gauge; GND pad at y=6+3*3=15, above signal channel
    "D1":  (12.0, 10.0),  # USB ESD TVS, between USB-C and MCU USB pins
    "R3":  (38.0, 25.0),  # LED resistor, lower-right
    "D2":  (43.0, 25.0),  # Status LED, directly beside its current limiter
    # Debug header: placed at the left side of the board (x=6), clear of U1 which starts at x=25.
    # J2 row-0 pads land at x=6..18, row-1 at (6,30). Nearest mounting hole H3(3.5,31.5) is 2.9mm away.
    "J2":  (6.0, 28.0),   # SWD header, pads x=6..18mm row0 and (6,30) row1
}


def _ble_sensor_node_seed_table() -> dict[str, tuple[tuple[float, float], str]]:
    return {
        ref: (xy, "ble_sensor_node_anchor")
        for ref, xy in _BLE_SENSOR_NODE_ANCHORS.items()
    }


_RP2040_USB_HID_ANCHORS: dict[str, tuple[float, float]] = {
    # Board: 51x21 mm, usable area 1..50 x 1..20.
    # U2 (RP2040, 20 pins): 7-col placeholder, pads at (18-30, 4-8).
    # U3 (Flash, 8 pins): 7-col placeholder, pads at (33-45, 2-4).
    # QSPI_D3 path: U2(18,4) to U3(45,2); other QSPI paths are <= 20 mm.
    "J1": (3.0,  10.0),   # USB-C, left edge; pads (3-9, 10)
    "D1": (10.0, 10.0),   # USB ESD, inline on USB data path; pads (10-14, 10)
    "U1": (3.0,  15.0),   # 3V3 LDO, near USB_VBUS; pads (3-7, 15)
    "U2": (18.0,  4.0),   # RP2040 MCU, center; pads (18-30, 4-8)
    "U3": (33.0,  2.0),   # 2 MB QSPI Flash, right of MCU; pads (33-45, 2-4)
    "X1": (33.0, 10.0),   # 12 MHz crystal, near MCU XIN/XOUT; pads (33-35, 10)
    "C5": (36.0,  7.0),   # XIN load cap, beside crystal.
    "C6": (36.0, 13.0),   # XOUT load cap, beside crystal.
    "J2": (18.0, 12.0),   # SWD 10-pin, below MCU; pads (18-30, 12-14)
    "C1": (3.0,   5.0),   # 100 nF decoupling; pads (3-5, 5)
    "C2": (7.0,   5.0),   # 100 nF decoupling; pads (7-9, 5)
    "C3": (11.0,  5.0),   # 10 uF bulk cap; pads (11-13, 5)
    "C4": (9.0,  15.0),   # 10 uF USB_VBUS input bulk cap, near USB/LDO input path.
}


def _rp2040_usb_hid_seed_table() -> dict[str, tuple[tuple[float, float], str]]:
    return {
        ref: (xy, "rp2040_usb_hid_anchor")
        for ref, xy in _RP2040_USB_HID_ANCHORS.items()
    }


def _usb_hid_controller_seed_table() -> dict[str, tuple[tuple[float, float], str]]:
    anchors = dict(_RP2040_USB_HID_ANCHORS)
    # usb_hid_controller reuses the RP2040 topology but its refs differ:
    # U1 is the RP2040 MCU and U2 is the LDO. Keep the physical roles aligned
    # with the RP2040 seed so oscillator and USB placement stay grounded.
    anchors["U1"] = _RP2040_USB_HID_ANCHORS["U2"]
    anchors["U2"] = _RP2040_USB_HID_ANCHORS["U1"]
    anchors.pop("X1", None)
    anchors.pop("C5", None)
    anchors["Y1"] = (33.0, 10.0)
    anchors["C6"] = (36.0, 7.0)
    anchors["C7"] = (36.0, 13.0)
    anchors["R3"] = (41.0, 17.0)
    anchors["D2"] = (46.0, 17.0)
    return {
        ref: (xy, "usb_hid_controller_anchor")
        for ref, xy in anchors.items()
    }


def _bldc_esc_seed_table() -> dict[str, tuple[tuple[float, float], str]]:
    # The ESC is a 60x50 mm board. It used to inherit ``_seed_table()``, whose
    # anchors are the 160x100 mm robotics coordinates, so most of it seeded far
    # off-board. Only the two anchors that are meaningful on this board survive;
    # everything else is shelf-packed against the real envelope.
    return {
        "R1": ((40.0, 35.0), "bldc_status_led_anchor"),
        "D2": ((45.0, 35.0), "bldc_status_led_anchor"),
    }


_SAMD21_SENSOR_HUB_ANCHORS: dict[str, tuple[float, float]] = {
    # Board: 50x30 mm. USB-C must stay on the front edge; SWD exits the right edge.
    "J1": (12.0, 3.0),   # USB-C, front edge
    "D1": (18.0, 3.0),   # USB ESD, connector-side of the protected USB pair
    "U1": (28.0, 5.0),   # 3V3 LDO, close to VBUS but thermally separated from sensors/MCU
    "C3": (34.0, 5.0),   # V3V3 bulk cap beside the regulator output
    "U2": (24.0, 17.0),  # ATSAMD21G18A, central for USB/SWD/I2C fanout
    "X1": (18.0, 20.0),  # 32.768 kHz crystal, close to XIN32/XOUT32
    "C4": (21.0, 17.0),  # XIN32 load cap near crystal and MCU pins
    "C5": (21.0, 23.0),  # XOUT32 load cap near crystal and MCU pins
    "C6": (18.0, 24.0),  # VDDCORE cap near MCU core rail
    "C1": (20.0, 14.0),  # V3V3 decoupling near MCU power pins
    "C2": (34.0, 16.0),  # V3V3 decoupling near I2C sensors
    "U3": (36.0, 12.0),  # LSM6DSOX IMU on the sensor side of the bus
    "U4": (36.0, 21.0),  # BME280, separated from LDO heat source
    "R1": (29.0, 22.0),  # I2C SCL pull-up near sensors
    "R2": (29.0, 26.0),  # I2C SDA pull-up near sensors
    "J2": (47.0, 21.0),  # SWD 10-pin header, right edge
}


def _samd21_sensor_hub_seed_table() -> dict[str, tuple[tuple[float, float], str]]:
    return {
        ref: (xy, "samd21_sensor_hub_anchor")
        for ref, xy in _SAMD21_SENSOR_HUB_ANCHORS.items()
    }


_MINI_SERVO_ROBOT_ANCHORS: dict[str, tuple[float, float]] = {
    # 100x65 mm controller board. Six servo headers are deliberately distinct
    # edge anchors so a new project never starts with coincident connectors.
    "J1": (12.0, 4.0), "D1": (20.0, 4.0), "U1": (30.0, 7.0), "C3": (37.0, 7.0),
    "U2": (42.0, 28.0), "X1": (32.0, 30.0), "C4": (35.0, 27.0), "C5": (35.0, 33.0),
    "C6": (30.0, 36.0), "C1": (38.0, 23.0), "C2": (54.0, 27.0), "U3": (58.0, 22.0),
    "U4": (58.0, 34.0), "R1": (50.0, 38.0), "R2": (50.0, 43.0), "J2": (94.0, 54.0),
    "J20": (10.0, 58.0), "F20": (24.0, 58.0), "U20": (22.0, 47.0), "C20": (39.0, 51.0),
    "U21": (64.0, 46.0), "C21": (58.0, 46.0), "U22": (75.0, 52.0), "R20": (81.0, 52.0),
    "J27": (89.0, 58.0),
    "J21": (95.0, 8.0), "J22": (95.0, 17.0), "J23": (95.0, 26.0),
    "J24": (95.0, 35.0), "J25": (95.0, 44.0), "J26": (95.0, 53.0),
}


def _mini_servo_robot_seed_table() -> dict[str, tuple[tuple[float, float], str]]:
    return {ref: (xy, "mini_servo_robot_anchor") for ref, xy in _MINI_SERVO_ROBOT_ANCHORS.items()}


_AVR_32U4_HID_ANCHORS: dict[str, tuple[float, float]] = {
    # Board: 55x30 mm. USB-C enters from the left edge, ATmega32U4 is central,
    # and the 16 MHz crystal sits beside the XTAL1/XTAL2 pins for USB timing.
    "J1": (5.0, 10.0),
    "R2": (9.0, 13.0),
    "R3": (13.0, 13.0),
    "D1": (12.0, 10.0),
    "U1": (28.0, 14.0),
    "Y1": (36.0, 14.0),
    "C3": (24.0, 9.0),
    "C4": (28.0, 9.0),
    "C5": (18.0, 6.0),
    "C6": (23.0, 19.0),
    "J2": (50.0, 18.0),
    "R1": (34.0, 20.0),
}


def _avr_32u4_hid_seed_table() -> dict[str, tuple[tuple[float, float], str]]:
    return {
        ref: (xy, "avr_32u4_hid_anchor")
        for ref, xy in _AVR_32U4_HID_ANCHORS.items()
    }


def _seed_table_for_graph(graph: dict[str, Any]) -> dict[str, tuple[tuple[float, float], str]]:
    architecture = graph.get("design_basis", {}).get("architecture")
    if architecture == "nrf52840_ble_sensor":
        return _ble_sensor_node_seed_table()
    if architecture == "esp32s3_usb_i2c_sensor_data_logger":
        return _sensor_data_logger_seed_table()
    if architecture == "atsamd21g18a_lsm6dsox_bme280":
        return _samd21_sensor_hub_seed_table()
    if architecture == "samd21_pca9685_six_servo_robot":
        return _mini_servo_robot_seed_table()
    if architecture == "rp2040_usb_hid_qspi_flash":
        return _usb_hid_controller_seed_table()
    if architecture == "rp2040_qspi_usb_device":
        return _rp2040_usb_hid_seed_table()
    if architecture == "stm32g474_drv8323_3phase_foc_esc":
        return _bldc_esc_seed_table()
    if architecture == "atmega32u4_native_usb_hid":
        return _avr_32u4_hid_seed_table()
    if architecture == "protected_controller_and_external_driver_io":
        return _seed_table()
    # No curated anchors for this architecture. Returning the robotics table here
    # (the old default) seeded 160x100 mm coordinates onto boards as small as
    # 35x18 mm; an empty table sends every ref to the footprint-aware shelf pack.
    return {}
