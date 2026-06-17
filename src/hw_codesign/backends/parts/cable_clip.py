"""Parametric snap-fit cable clip — wall or extrusion mount."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ._base import (
    _MIN_WALL_MM, fastener_clearance,
    import_ocp, printability_report, write_step, write_stl,
)

INTENT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": ["cable_diameter_mm"],
    "additionalProperties": True,
    "properties": {
        "cable_diameter_mm":    {"type": "number", "minimum": 1, "description": "Outer diameter of cable (or bundle)"},
        "wall_mm":              {"type": "number", "minimum": 1.2, "default": 2.0, "description": "Clip wall thickness"},
        "mount_type":           {"type": "string", "enum": ["screw", "ziptie", "adhesive"], "default": "screw"},
        "fastener":             {"type": "string", "enum": ["M2", "M2.5", "M3", "M4"], "default": "M3"},
        "ear_width_mm":         {"type": "number", "default": 8.0, "description": "Width of mounting ear"},
        "ear_length_mm":        {"type": "number", "default": 8.0, "description": "Length of mounting ear from clip"},
        "opening_mm":           {"type": "number", "default": None, "description": "Snap opening width (defaults to cable_diameter * 0.85 for snap fit)"},
        "max_overhang_angle_deg": {"type": "number", "default": 45},
    },
}


class CableClip:
    """Snap-fit cable retention clip.

    Geometry:
      - Semi-circular arc body (>180° to snap over cable)
      - Flat mounting ear with screw hole or ziptie slot

    Prints flat (ear on bed, arc upright).
    """

    def design(self, intent: dict[str, Any], output_dir: Path, part_name: str) -> dict[str, Any]:
        try:
            ocp = import_ocp()
        except ImportError:
            return {
                "status": "blocked",
                "code": "tool_unavailable",
                "message": "cadquery-ocp is not installed",
                "part_name": part_name,
                "part_type": "cable_clip",
            }

        cable_r     = float(intent.get("cable_diameter_mm", 6.0)) / 2
        wall        = float(intent.get("wall_mm", 2.0))
        mount_type  = intent.get("mount_type", "screw")
        fastener    = intent.get("fastener", "M3")
        ear_w       = float(intent.get("ear_width_mm", 8.0))
        ear_l       = float(intent.get("ear_length_mm", 8.0))
        max_overhang = float(intent.get("max_overhang_angle_deg", 45.0))

        # Clip depth (extrusion direction, along cable axis)
        clip_depth  = max(cable_r * 2 + wall, 8.0)

        MakeBox = ocp["BRepPrimAPI_MakeBox"]
        MakeCyl = ocp["BRepPrimAPI_MakeCylinder"]
        Cut     = ocp["BRepAlgoAPI_Cut"]
        Fuse    = ocp["BRepAlgoAPI_Fuse"]
        BRepCheck = ocp["BRepCheck_Analyzer"]
        gp_Pnt  = ocp["gp_Pnt"]
        gp_Ax2  = ocp["gp_Ax2"]
        gp_Dir  = ocp["gp_Dir"]

        # Outer cylinder arc approximated as full cylinder - inner bore
        # then trimmed at rear by subtracting a box to leave ~270° arc
        outer_r = cable_r + wall
        cx = outer_r   # center of arc in XZ plane
        cz = outer_r

        # Outer shell cylinder
        outer_cyl = MakeCyl(gp_Ax2(gp_Pnt(cx, 0, cz), gp_Dir(0, 1, 0)), outer_r, clip_depth).Shape()
        # Inner bore
        inner_cyl = MakeCyl(gp_Ax2(gp_Pnt(cx, -1, cz), gp_Dir(0, 1, 0)), cable_r, clip_depth + 2).Shape()
        arc_body  = Cut(outer_cyl, inner_cyl).Shape()

        # Trim to open the snap opening (remove a wedge at the top)
        # The opening is at the "top" (Z = cz + outer_r region)
        opening_half = float(intent["opening_mm"]) / 2 if intent.get("opening_mm") else cable_r * 0.85
        trim = MakeBox(gp_Pnt(cx - opening_half, -1, cz), opening_half * 2, clip_depth + 2, outer_r + 2).Shape()
        arc_body = Cut(arc_body, trim).Shape()

        # Mounting ear: flat plate at the bottom of the clip
        ear_x_start = cx - ear_w / 2
        ear_z_start = -ear_l
        ear = MakeBox(gp_Pnt(ear_x_start, 0, ear_z_start), ear_w, clip_depth, ear_l + wall).Shape()
        body = Fuse(arc_body, ear).Shape()

        all_holes: list[dict] = []

        if mount_type == "screw":
            r_clear = fastener_clearance(fastener) / 2
            # Screw hole through ear (Z direction)
            screw_hole = MakeCyl(gp_Ax2(gp_Pnt(cx, clip_depth / 2, ear_z_start - 1), gp_Dir(0, 0, 1)), r_clear, ear_l + wall + 2).Shape()
            body = Cut(body, screw_hole).Shape()
            all_holes.append({"diameter_mm": r_clear * 2})
        elif mount_type == "ziptie":
            # Two rectangular ziptie slots in the ear
            slot_w, slot_h = 3.5, 1.5
            for y_offset in [clip_depth * 0.25, clip_depth * 0.75]:
                slot = MakeBox(gp_Pnt(ear_x_start - 1, y_offset - slot_w / 2, ear_z_start + ear_l * 0.3), ear_w + 2, slot_w, slot_h).Shape()
                body = Cut(body, slot).Shape()

        valid = BRepCheck(body).IsValid()
        failures = [] if valid else [{"code": "invalid_solid", "message": "OCP solid is not valid", "severity": "error"}]

        step_path = output_dir / f"{part_name}.step"
        stl_path  = output_dir / f"{part_name}.stl"
        write_step(body, step_path, ocp)
        write_stl(body, stl_path, ocp)

        printability = printability_report(stl_path, wall, all_holes or [{"diameter_mm": 99}], max_overhang, "ear flat on bed, arc upright")

        gate_status = "pass" if valid and printability["printable"] else "fail"
        if not printability["printable"]:
            for v in printability["violations"]:
                failures.append({"code": "printability_violation", "message": v, "severity": "error"})

        return {
            "status": "generated" if gate_status == "pass" else "fail",
            "part_name": part_name,
            "part_type": "cable_clip",
            "artifacts": [str(step_path), str(stl_path)],
            "printability": printability,
            "gate_report": {
                "gate": "part_design",
                "status": gate_status,
                "failures": failures,
                "metrics": {
                    "valid_solid": valid,
                    "cable_diameter_mm": cable_r * 2,
                    "wall_mm": wall,
                    "mount_type": mount_type,
                    "clip_depth_mm": clip_depth,
                },
                "artifacts": [str(step_path), str(stl_path)],
                "backend": {"name": "OpenCASCADE", "part_type": "cable_clip"},
            },
            "candidate_only": True,
            "release_eligible": False,
        }
