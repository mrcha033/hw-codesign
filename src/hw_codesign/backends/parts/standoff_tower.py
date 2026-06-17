"""Parametric standoff tower — hex or round, M2.5–M4, with threaded bore and through hole."""
from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ._base import (
    _MIN_WALL_MM, fastener_bore, fastener_clearance,
    import_ocp, printability_report, write_step, write_stl,
)

INTENT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": ["height_mm"],
    "additionalProperties": True,
    "properties": {
        "height_mm":            {"type": "number", "minimum": 2, "description": "Total standoff height"},
        "outer_diameter_mm":    {"type": "number", "minimum": 3, "default": 8.0, "description": "Outer diameter"},
        "fastener":             {"type": "string", "enum": ["M2", "M2.5", "M3", "M4"], "default": "M3"},
        "thread_depth_mm":      {"type": "number", "default": 6.0, "description": "Threaded bore depth from top"},
        "through_bore":         {"type": "boolean", "default": True, "description": "Whether the through-hole goes all the way (for pass-through screws)"},
        "base_style":           {"type": "string", "enum": ["flat", "flanged"], "default": "flat"},
        "flange_diameter_mm":   {"type": "number", "default": 12.0, "description": "Flange outer diameter (when base_style=flanged)"},
        "flange_height_mm":     {"type": "number", "default": 2.0},
        "max_overhang_angle_deg": {"type": "number", "default": 45},
        "count":                {"type": "integer", "minimum": 1, "default": 1, "description": "How many identical standoffs are needed (informational)"},
    },
}


class StandoffTower:
    """Cylindrical standoff with optional hex faceting, threaded blind bore (top) and clearance bore (bottom).

    Prints vertically — no overhangs. Orientation: axis along Z.
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
                "part_type": "standoff_tower",
            }

        height      = float(intent.get("height_mm", 10.0))
        outer_r     = float(intent.get("outer_diameter_mm", 8.0)) / 2
        fastener    = intent.get("fastener", "M3")
        thread_d    = float(intent.get("thread_depth_mm", 6.0))
        through     = bool(intent.get("through_bore", True))
        base_style  = intent.get("base_style", "flat")
        flange_r    = float(intent.get("flange_diameter_mm", 12.0)) / 2
        flange_h    = float(intent.get("flange_height_mm", 2.0))
        max_overhang = float(intent.get("max_overhang_angle_deg", 45.0))

        bore_r  = fastener_bore(fastener) / 2        # threaded/clearance bore radius
        clear_r = fastener_clearance(fastener) / 2   # through-hole clearance radius

        MakeBox = ocp["BRepPrimAPI_MakeBox"]
        MakeCyl = ocp["BRepPrimAPI_MakeCylinder"]
        Cut     = ocp["BRepAlgoAPI_Cut"]
        Fuse    = ocp["BRepAlgoAPI_Fuse"]
        BRepCheck = ocp["BRepCheck_Analyzer"]
        gp_Pnt  = ocp["gp_Pnt"]
        gp_Ax2  = ocp["gp_Ax2"]
        gp_Dir  = ocp["gp_Dir"]

        # Main cylinder (axis along Z)
        body = MakeCyl(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1)), outer_r, height).Shape()

        # Optional flange at base
        if base_style == "flanged" and flange_r > outer_r:
            flange = MakeCyl(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1)), flange_r, flange_h).Shape()
            body = Fuse(body, flange).Shape()

        # Threaded bore at top (blind or through)
        if through:
            bore = MakeCyl(gp_Ax2(gp_Pnt(0, 0, -1), gp_Dir(0, 0, 1)), bore_r, height + 2).Shape()
        else:
            bore = MakeCyl(gp_Ax2(gp_Pnt(0, 0, height - thread_d), gp_Dir(0, 0, 1)), bore_r, thread_d + 1).Shape()
        body = Cut(body, bore).Shape()

        # Clearance bore at bottom (for screw head pass-through, slightly larger)
        if not through:
            bottom_bore = MakeCyl(gp_Ax2(gp_Pnt(0, 0, -1), gp_Dir(0, 0, 1)), clear_r, height - thread_d + 1).Shape()
            body = Cut(body, bottom_bore).Shape()

        valid = BRepCheck(body).IsValid()
        failures = [] if valid else [{"code": "invalid_solid", "message": "OCP solid is not valid", "severity": "error"}]

        min_wall = outer_r - bore_r
        step_path = output_dir / f"{part_name}.step"
        stl_path  = output_dir / f"{part_name}.stl"
        write_step(body, step_path, ocp)
        write_stl(body, stl_path, ocp)

        holes = [{"diameter_mm": bore_r * 2}]
        printability = printability_report(stl_path, min_wall * 2, holes, max_overhang, "vertical (Z axis up)")

        gate_status = "pass" if valid and printability["printable"] else "fail"
        if not printability["printable"]:
            for v in printability["violations"]:
                failures.append({"code": "printability_violation", "message": v, "severity": "error"})

        return {
            "status": "generated" if gate_status == "pass" else "fail",
            "part_name": part_name,
            "part_type": "standoff_tower",
            "artifacts": [str(step_path), str(stl_path)],
            "printability": printability,
            "gate_report": {
                "gate": "part_design",
                "status": gate_status,
                "failures": failures,
                "metrics": {
                    "valid_solid": valid,
                    "height_mm": height,
                    "outer_diameter_mm": outer_r * 2,
                    "fastener": fastener,
                    "through_bore": through,
                    "wall_mm": round(min_wall, 2),
                },
                "artifacts": [str(step_path), str(stl_path)],
                "backend": {"name": "OpenCASCADE", "part_type": "standoff_tower"},
            },
            "candidate_only": True,
            "release_eligible": False,
        }
