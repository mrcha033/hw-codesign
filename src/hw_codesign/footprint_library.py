from __future__ import annotations

import hashlib
import math
from copy import deepcopy
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from sexpdata import Symbol, dumps, loads

_ASSETS: dict[str, tuple[str, str]] = {
    "Capacitor_SMD:C_0402_1005Metric": (
        "C_0402_1005Metric.kicad_mod",
        "0403382fc4583ed510b461b1fa4a36dfaec6f4c0d9b1a67e6b0027837a54e1b5",
    ),
    "Capacitor_SMD:C_0603_1608Metric": (
        "C_0603_1608Metric.kicad_mod",
        "fe0dbfefbb181a0466f93a8de52d84ba7b00fcd9acdbb69575f4128a0af4e405",
    ),
    "Connector_IDC:IDC-Header_2x05_P2.54mm_Vertical": (
        "IDC-Header_2x05_P2.54mm_Vertical.kicad_mod",
        "b605d7a816a5b5681d09bd120b547ac748d74440e7d55a8371007b9c53afb092",
    ),
    "Connector_USB:USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal": (
        "USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal.kicad_mod",
        "3b8d7da3cae5114ec83022a759a78925113bc2eeec100ea447594f6d8687e4b8",
    ),
    "Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm": (
        "Crystal_SMD_3225-4Pin_3.2x2.5mm.kicad_mod",
        "7648bca15399a8bd7856b5da6a1d2bc3a87049dc63958f8e8a3ab7409941a8e4",
    ),
    "Package_DFN_QFN:QFN-56-1EP_7x7mm_P0.4mm_EP3.2x3.2mm": (
        "QFN-56-1EP_7x7mm_P0.4mm_EP3.2x3.2mm.kicad_mod",
        "516b5c14ad87b1a5ef29c098b603ec48c6bd9cefe21e8d479613cacf18458d8b",
    ),
    "Package_SO:SOIC-8_5.3x5.3mm_P1.27mm": (
        "SOIC-8_5.3x5.3mm_P1.27mm.kicad_mod",
        "cc86a7083c9df1c1bf808dfa469e913d446455fd7ab7a7941e18681b80e8b9b5",
    ),
    "Package_TO_SOT_SMD:SOT-23-5": (
        "SOT-23-5.kicad_mod",
        "455a3f7c3e5eb5b8847eaa5df23e18651e78ab9f75afd09a0883758a0d901761",
    ),
    "Package_TO_SOT_SMD:SOT-23-6": (
        "SOT-23-6.kicad_mod",
        "f341c73aac9dcb553456f68bf3fee3d26eb14acf6d8a1cae82b50418fe1d71ca",
    ),
    "RF_Module:ESP32-S3-WROOM-1": (
        "ESP32-S3-WROOM-1.kicad_mod",
        "d0cfbb31fef0c47396c0d061ec5a3bff60f0567d8d4ea8dd4769c84f52bd656f",
    ),
    "Resistor_SMD:R_0603_1608Metric": (
        "R_0603_1608Metric.kicad_mod",
        "7190ac4a00125b807e54129ef0d87d87f2a658eeb74d025a7028203419b09f23",
    ),
}


@dataclass(frozen=True)
class CanonicalFootprintGeometry:
    library_id: str
    body_extent: tuple[float, float, float, float]
    copper_extent: tuple[float, float, float, float]
    courtyard_extent: tuple[float, float, float, float] | None
    keepout_polygons: tuple[tuple[tuple[float, float], ...], ...]
    pad_forms: int
    numbered_pads: tuple[str, ...]
    sha256: str

    @property
    def placement_extent(self) -> tuple[float, float, float, float]:
        return _union_extents(self.body_extent, self.copper_extent)


def _head(form: Any, name: str) -> bool:
    return (
        isinstance(form, list)
        and bool(form)
        and isinstance(form[0], Symbol)
        and form[0].value() == name
    )


def _atom(value: Any) -> str:
    return value.value() if isinstance(value, Symbol) else str(value)


def _asset_path(library_id: str) -> Path | None:
    asset = _ASSETS.get(library_id)
    if asset is None:
        return None
    path = Path(__file__).with_name("footprints") / asset[0]
    return path if path.is_file() else None


@lru_cache(maxsize=None)
def _asset_ast(library_id: str) -> list[Any] | None:
    path = _asset_path(library_id)
    if path is None:
        return None
    expected_hash = _ASSETS[library_id][1]
    payload = path.read_bytes()
    actual_hash = hashlib.sha256(payload).hexdigest()
    if actual_hash != expected_hash:
        raise ValueError(
            f"Vendored footprint {library_id} hash mismatch: expected {expected_hash}, got {actual_hash}"
        )
    parsed = loads(payload.decode("utf-8"))
    if not isinstance(parsed, list) or not _head(parsed, "footprint"):
        raise ValueError(f"Vendored footprint {library_id} is not a KiCad footprint")
    return parsed


def _direct(form: list[Any], name: str) -> list[list[Any]]:
    return [item for item in form[2:] if _head(item, name)]


def _layer(form: list[Any]) -> str | None:
    layers = _direct(form, "layer")
    return _atom(layers[0][1]) if layers and len(layers[0]) > 1 else None


def _coordinates(form: Any) -> list[tuple[float, float]]:
    points: list[tuple[float, float]] = []
    if isinstance(form, list):
        if form and isinstance(form[0], Symbol) and form[0].value() in {"at", "start", "end", "xy", "center", "mid"}:
            if len(form) >= 3 and isinstance(form[1], (int, float)) and isinstance(form[2], (int, float)):
                points.append((float(form[1]), float(form[2])))
        for item in form[1:]:
            points.extend(_coordinates(item))
    return points


def _extent(points: list[tuple[float, float]]) -> tuple[float, float, float, float]:
    if not points:
        raise ValueError("No geometry points were found")
    return (
        min(point[0] for point in points),
        min(point[1] for point in points),
        max(point[0] for point in points),
        max(point[1] for point in points),
    )


def _union_extents(
    left: tuple[float, float, float, float],
    right: tuple[float, float, float, float],
) -> tuple[float, float, float, float]:
    return (
        min(left[0], right[0]),
        min(left[1], right[1]),
        max(left[2], right[2]),
        max(left[3], right[3]),
    )


def _pad_copper_extent(pad: list[Any]) -> tuple[float, float, float, float] | None:
    layer_forms = _direct(pad, "layers")
    if not layer_forms:
        return None
    layers = {_atom(item) for item in layer_forms[0][1:]}
    if not any(layer == "*.Cu" or layer.endswith(".Cu") for layer in layers):
        return None
    at_forms, size_forms = _direct(pad, "at"), _direct(pad, "size")
    if not at_forms or not size_forms or len(at_forms[0]) < 3 or len(size_forms[0]) < 3:
        return None
    x_mm, y_mm = float(at_forms[0][1]), float(at_forms[0][2])
    rotation = float(at_forms[0][3]) if len(at_forms[0]) > 3 else 0.0
    width, height = float(size_forms[0][1]), float(size_forms[0][2])
    theta = math.radians(rotation)
    box_width = abs(width * math.cos(theta)) + abs(height * math.sin(theta))
    box_height = abs(width * math.sin(theta)) + abs(height * math.cos(theta))
    return (
        x_mm - box_width / 2.0,
        y_mm - box_height / 2.0,
        x_mm + box_width / 2.0,
        y_mm + box_height / 2.0,
    )


@lru_cache(maxsize=None)
def canonical_footprint_geometry(library_id: str) -> CanonicalFootprintGeometry | None:
    ast = _asset_ast(library_id)
    if ast is None:
        return None
    fab_points: list[tuple[float, float]] = []
    courtyard_points: list[tuple[float, float]] = []
    keepouts: list[tuple[tuple[float, float], ...]] = []
    copper_extent: tuple[float, float, float, float] | None = None
    numbered_pads: set[str] = set()
    pads = _direct(ast, "pad")
    for form in ast[2:]:
        if not isinstance(form, list):
            continue
        if _layer(form) == "F.Fab" and any(_head(form, kind) for kind in ("fp_line", "fp_rect", "fp_poly", "fp_arc")):
            fab_points.extend(_coordinates(form))
        if _layer(form) == "F.CrtYd" and any(_head(form, kind) for kind in ("fp_line", "fp_rect", "fp_poly", "fp_arc")):
            courtyard_points.extend(_coordinates(form))
        if _head(form, "zone"):
            polygon = next((item for item in form if _head(item, "polygon")), None)
            if polygon is not None:
                points = tuple(_coordinates(polygon))
                if points:
                    keepouts.append(points)
    for pad in pads:
        if len(pad) > 1 and _atom(pad[1]):
            numbered_pads.add(_atom(pad[1]))
        pad_extent = _pad_copper_extent(pad)
        if pad_extent is not None:
            copper_extent = pad_extent if copper_extent is None else _union_extents(copper_extent, pad_extent)
    if copper_extent is None:
        raise ValueError(f"Canonical footprint {library_id} contains no copper pads")
    path = _asset_path(library_id)
    assert path is not None
    return CanonicalFootprintGeometry(
        library_id=library_id,
        body_extent=_extent(fab_points),
        copper_extent=copper_extent,
        courtyard_extent=_extent(courtyard_points) if courtyard_points else None,
        keepout_polygons=tuple(keepouts),
        pad_forms=len(pads),
        numbered_pads=tuple(sorted(numbered_pads, key=lambda value: (not value.isdigit(), int(value) if value.isdigit() else value))),
        sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
    )


def _scrub_uuid_fields(form: Any) -> Any:
    if not isinstance(form, list):
        return form
    cleaned: list[Any] = []
    for item in form:
        if _head(item, "uuid") or _head(item, "tstamp"):
            continue
        cleaned.append(_scrub_uuid_fields(item))
    return cleaned


def _compose_pad_rotation(at_form: list[Any], footprint_rotation_deg: float) -> None:
    """Write a pad's absolute KiCad board angle into its ``(at ...)`` form.

    Pad centres remain footprint-local, but KiCad board files store a child
    pad's angle in board coordinates.  Consequently an omitted local angle is
    not inherited from the footprint and must be serialized explicitly; an
    existing local angle must be composed with the placed footprint rotation.
    """
    if len(at_form) < 3:
        return
    local_rotation_deg = float(at_form[3]) if len(at_form) > 3 else 0.0
    composed = (local_rotation_deg + float(footprint_rotation_deg)) % 360.0
    if math.isclose(composed, 0.0, abs_tol=1e-12):
        composed = 0.0
    if len(at_form) > 3:
        at_form[3] = composed
    else:
        at_form.append(composed)


def render_canonical_footprint(
    library_id: str,
    component: dict[str, Any],
    x_mm: float,
    y_mm: float,
    rotation_deg: float,
    net_ids: dict[str, int],
    copper_layers: tuple[str, ...],
) -> tuple[str | None, list[dict[str, Any]]]:
    """Render a vendored footprint in board context and inject graph nets."""
    original = _asset_ast(library_id)
    geometry = canonical_footprint_geometry(library_id)
    if original is None or geometry is None:
        return None, []
    ast = _scrub_uuid_fields(deepcopy(original))
    assert isinstance(ast, list)
    ast[1] = library_id
    ast[2:] = [
        item for item in ast[2:]
        if not any(_head(item, name) for name in ("version", "generator", "generator_version", "embedded_fonts", "at"))
    ]
    layer_index = next((index for index, item in enumerate(ast) if _head(item, "layer")), 1)
    ast.insert(layer_index + 1, [Symbol("at"), float(x_mm), float(y_mm), float(rotation_deg)])

    properties = {str(item[1]): item for item in ast[2:] if _head(item, "property") and len(item) > 2}
    if "Reference" in properties:
        properties["Reference"][2] = str(component["ref"])
    if "Value" in properties:
        properties["Value"][2] = str(component.get("value") or library_id.split(":", 1)[-1])
    for name, value in (
        ("MPN", component.get("mpn", "")),
        ("Lifecycle", component.get("lifecycle", "")),
        ("Substitute_MPN", component.get("substitute_mpn") or ""),
    ):
        ast.append([Symbol("property"), name, str(value)])

    pin_nets = {
        str(pin.get("number")): str(pin["net"])
        for pin in component.get("pins", [])
        if pin.get("number") is not None and pin.get("net") in net_ids
    }
    missing = sorted(set(pin_nets) - set(geometry.numbered_pads))
    failures = [
        {
            "ref": component.get("ref"),
            "footprint": library_id,
            "code": "canonical_pad_mapping_missing",
            "pads": missing,
        }
    ] if missing else []
    for form in ast[2:]:
        if _head(form, "pad") and len(form) > 1:
            form[:] = [item for item in form if not _head(item, "net")]
            at_forms = _direct(form, "at")
            if at_forms:
                _compose_pad_rotation(at_forms[0], rotation_deg)
            pad_number = _atom(form[1])
            net_name = pin_nets.get(pad_number)
            if net_name is not None:
                form.append([Symbol("net"), int(net_ids[net_name]), net_name])
        elif _head(form, "zone"):
            for index, item in enumerate(form):
                if _head(item, "layers"):
                    form[index] = [Symbol("layers"), *copper_layers]
                    break
    return dumps(ast), failures
