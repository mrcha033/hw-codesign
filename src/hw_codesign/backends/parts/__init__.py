"""Parametric part library for agent-authored mechanical design."""
from __future__ import annotations

from typing import Any

from .cable_clip import CableClip
from .cable_clip import INTENT_SCHEMA as _CABLE_CLIP_SCHEMA
from .custom_enclosure_variant import CustomEnclosureVariant
from .custom_enclosure_variant import INTENT_SCHEMA as _ENCLOSURE_SCHEMA
from .din_rail_adapter import DinRailAdapter
from .din_rail_adapter import INTENT_SCHEMA as _DIN_SCHEMA
from .pcb_mount_bracket import PcbMountBracket
from .pcb_mount_bracket import INTENT_SCHEMA as _BRACKET_SCHEMA
from .standoff_tower import StandoffTower
from .standoff_tower import INTENT_SCHEMA as _STANDOFF_SCHEMA

PART_REGISTRY: dict[str, type] = {
    "pcb_mount_bracket":       PcbMountBracket,
    "standoff_tower":          StandoffTower,
    "cable_clip":              CableClip,
    "din_rail_adapter":        DinRailAdapter,
    "custom_enclosure_variant": CustomEnclosureVariant,
}

PART_INTENT_SCHEMAS: dict[str, dict[str, Any]] = {
    "pcb_mount_bracket":       _BRACKET_SCHEMA,
    "standoff_tower":          _STANDOFF_SCHEMA,
    "cable_clip":              _CABLE_CLIP_SCHEMA,
    "din_rail_adapter":        _DIN_SCHEMA,
    "custom_enclosure_variant": _ENCLOSURE_SCHEMA,
}

PART_DESCRIPTIONS: dict[str, str] = {
    "pcb_mount_bracket":       "L or U bracket for mounting a PCB to 2020/4040 extrusion or a flat panel. Produces PCB mounting holes and extrusion/frame holes.",
    "standoff_tower":          "Cylindrical standoff with threaded bore (M2–M4). Used to elevate a PCB from a mounting surface.",
    "cable_clip":              "Snap-fit cable retention clip. Mounts via screw or ziptie. Suitable for FDM printing.",
    "din_rail_adapter":        "TS-35 DIN rail adapter plate with standard clip hooks at top and/or bottom. Accepts device mounting holes.",
    "custom_enclosure_variant": "Rectangular enclosure with agent-specified panel cutouts, cable gland holes, and vent slot patterns. Produces base + lid STEP/STL.",
}

__all__ = [
    "PART_REGISTRY",
    "PART_INTENT_SCHEMAS",
    "PART_DESCRIPTIONS",
    "PcbMountBracket",
    "StandoffTower",
    "CableClip",
    "DinRailAdapter",
    "CustomEnclosureVariant",
]
