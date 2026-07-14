"""Parametric part library for agent-authored mechanical design."""
from __future__ import annotations

from typing import Any

from .cable_clip import INTENT_SCHEMA as _CABLE_CLIP_SCHEMA
from .cable_clip import CableClip
from .custom_enclosure_variant import INTENT_SCHEMA as _ENCLOSURE_SCHEMA
from .custom_enclosure_variant import CustomEnclosureVariant
from .din_rail_adapter import INTENT_SCHEMA as _DIN_SCHEMA
from .din_rail_adapter import DinRailAdapter
from .pcb_mount_bracket import INTENT_SCHEMA as _BRACKET_SCHEMA
from .pcb_mount_bracket import PcbMountBracket
from .robot_mechanisms import (
    L_BRACKET_SCHEMA,
    LINK_SCHEMA,
    REVOLUTE_JOINT_SCHEMA,
    ROBOT_FOOT_SCHEMA,
    SERVO_HORN_SCHEMA,
    U_BRACKET_SCHEMA,
    LBracket,
    RevoluteJoint,
    RobotFoot,
    RobotLink,
    ServoHorn,
    UBracket,
)
from .standoff_tower import INTENT_SCHEMA as _STANDOFF_SCHEMA
from .standoff_tower import StandoffTower

PART_REGISTRY: dict[str, type] = {
    "pcb_mount_bracket":       PcbMountBracket,
    "standoff_tower":          StandoffTower,
    "cable_clip":              CableClip,
    "din_rail_adapter":        DinRailAdapter,
    "custom_enclosure_variant": CustomEnclosureVariant,
    "servo_horn": ServoHorn,
    "servo_u_bracket": UBracket,
    "servo_l_bracket": LBracket,
    "robot_link": RobotLink,
    "revolute_joint": RevoluteJoint,
    "robot_foot": RobotFoot,
}

PART_INTENT_SCHEMAS: dict[str, dict[str, Any]] = {
    "pcb_mount_bracket":       _BRACKET_SCHEMA,
    "standoff_tower":          _STANDOFF_SCHEMA,
    "cable_clip":              _CABLE_CLIP_SCHEMA,
    "din_rail_adapter":        _DIN_SCHEMA,
    "custom_enclosure_variant": _ENCLOSURE_SCHEMA,
    "servo_horn": SERVO_HORN_SCHEMA,
    "servo_u_bracket": U_BRACKET_SCHEMA,
    "servo_l_bracket": L_BRACKET_SCHEMA,
    "robot_link": LINK_SCHEMA,
    "revolute_joint": REVOLUTE_JOINT_SCHEMA,
    "robot_foot": ROBOT_FOOT_SCHEMA,
}

PART_DESCRIPTIONS: dict[str, str] = {
    "pcb_mount_bracket":       "L or U bracket for mounting a PCB to 2020/4040 extrusion or a flat panel. Produces PCB mounting holes and extrusion/frame holes.",
    "standoff_tower":          "Cylindrical standoff with threaded bore (M2–M4). Used to elevate a PCB from a mounting surface.",
    "cable_clip":              "Snap-fit cable retention clip. Mounts via screw or ziptie. Suitable for FDM printing.",
    "din_rail_adapter":        "TS-35 DIN rail adapter plate with standard clip hooks at top and/or bottom. Accepts device mounting holes.",
    "custom_enclosure_variant": "Rectangular enclosure with agent-specified panel cutouts, cable gland holes, and vent slot patterns. Produces base + lid STEP/STL.",
    "servo_horn": "Parametric servo horn with reviewed shaft bore, link hole, fastening contract, and interference envelope.",
    "servo_u_bracket": "Servo-sized U bracket with pivot holes, per-side clearance, and an analytical motion-range contract.",
    "servo_l_bracket": "Right-angle robot bracket with two fastening planes and verified hole clearances.",
    "robot_link": "Two-pivot robot link with explicit joint-center distance and fastener edge-margin verification.",
    "revolute_joint": "Generic clevis-style revolute joint with motion range, joint clearance, and fastening verification.",
    "robot_foot": "Robot foot plate with ankle interface, toe-clearance contract, and fastening edge checks.",
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
    "ServoHorn",
    "UBracket",
    "LBracket",
    "RobotLink",
    "RevoluteJoint",
    "RobotFoot",
]
