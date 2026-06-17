"""Parametric DIN rail adapter — standard TS-35 clip for panel or enclosure mounting."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ._base import (
    fastener_clearance,
    import_ocp, printability_report, write_step, write_stl,
)

# TS-35 DIN rail standard dimensions (IEC 60715)
_DIN_RAIL_WIDTH_MM   = 35.0
_DIN_RAIL_HEIGHT_MM  = 7.5   # standard depth
_HOOK_DEPTH_MM       = 5.0   # how deep the hook engages the rail
_HOOK_WALL_MM        = 2.0

INTENT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": ["plate_width_mm", "plate_height_mm"],
    "additionalProperties": True,
    "properties": {
        "plate_width_mm":     {"type": "number", "minimum": 40, "description": "Width of the mounting plate"},
        "plate_height_mm":    {"type": "number", "minimum": 30, "description": "Height of the mounting plate"},
        "plate_thickness_mm": {"type": "number", "minimum": 1.2, "default": 3.0},
        "clip_position":      {"type": "string", "enum": ["top", "bottom", "both"], "default": "both",
                               "description": "Which edge(s) carry the DIN rail hooks"},
        "fastener":           {"type": "string", "enum": ["M2.5", "M3", "M4"], "default": "M3",
                               "description": "Fastener for attaching the device to this adapter"},
        "device_holes":       {
            "type": "array",
            "description": "Device mounting hole positions (from bottom-left of plate)",
            "items": {"type": "object", "required": ["x_mm", "y_mm"], "properties": {
                "x_mm": {"type": "number"},
                "y_mm": {"type": "number"},
            }},
        },
        "max_overhang_angle_deg": {"type": "number", "default": 45},
    },
}


class DinRailAdapter:
    """Flat plate with TS-35 DIN rail hooks at top and/or bottom.

    Coordinate system:
      X = plate width
      Y = plate thickness (into wall)
      Z = plate height

    The DIN hooks extend in the -Y direction (away from wall).
    Prints flat (plate face on bed).
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
                "part_type": "din_rail_adapter",
            }

        pw    = float(intent.get("plate_width_mm", 80.0))
        ph    = float(intent.get("plate_height_mm", 60.0))
        pt    = float(intent.get("plate_thickness_mm", 3.0))
        clip  = intent.get("clip_position", "both")
        fastener = intent.get("fastener", "M3")
        device_holes = intent.get("device_holes", [])
        max_overhang = float(intent.get("max_overhang_angle_deg", 45.0))

        MakeBox  = ocp["BRepPrimAPI_MakeBox"]
        MakeCyl  = ocp["BRepPrimAPI_MakeCylinder"]
        Cut      = ocp["BRepAlgoAPI_Cut"]
        Fuse     = ocp["BRepAlgoAPI_Fuse"]
        BRepCheck = ocp["BRepCheck_Analyzer"]
        gp_Pnt   = ocp["gp_Pnt"]
        gp_Ax2   = ocp["gp_Ax2"]
        gp_Dir   = ocp["gp_Dir"]

        # Main flat plate
        body = MakeBox(gp_Pnt(0, 0, 0), pw, pt, ph).Shape()

        # DIN hooks — snap over top and/or bottom edge of TS-35 rail
        # Hook geometry: an L-shaped bracket that clips under the rail flange
        hook_w = pw  # full plate width
        hook_h = _DIN_RAIL_HEIGHT_MM + _HOOK_WALL_MM

        def make_hook(z_origin: float) -> Any:
            # Horizontal back (attaches to plate)
            back = MakeBox(gp_Pnt(0, 0, z_origin), hook_w, _HOOK_DEPTH_MM + pt, _HOOK_WALL_MM).Shape()
            # Downward lip that engages rail flange
            lip = MakeBox(gp_Pnt(0, pt + _HOOK_DEPTH_MM - _HOOK_WALL_MM, z_origin - _DIN_RAIL_HEIGHT_MM), hook_w, _HOOK_WALL_MM, _DIN_RAIL_HEIGHT_MM).Shape()
            return Fuse(back, lip).Shape()

        if clip in ("top", "both"):
            body = Fuse(body, make_hook(ph - _HOOK_WALL_MM)).Shape()
        if clip in ("bottom", "both"):
            body = Fuse(body, make_hook(0)).Shape()

        # Device mounting holes (Z direction through plate)
        all_holes: list[dict] = []
        r_clear = fastener_clearance(fastener) / 2
        for hole in device_holes:
            x = float(hole["x_mm"])
            z = float(hole["y_mm"])  # "y" in intent means height on plate
            bore = MakeCyl(gp_Ax2(gp_Pnt(x, -1, z), gp_Dir(0, 1, 0)), r_clear, pt + 2).Shape()
            body = Cut(body, bore).Shape()
            all_holes.append({"diameter_mm": r_clear * 2})

        # Auto-generate four holes if none specified
        if not device_holes:
            for x in [pw * 0.2, pw * 0.8]:
                for z in [ph * 0.2, ph * 0.8]:
                    bore = MakeCyl(gp_Ax2(gp_Pnt(x, -1, z), gp_Dir(0, 1, 0)), r_clear, pt + 2).Shape()
                    body = Cut(body, bore).Shape()
                    all_holes.append({"diameter_mm": r_clear * 2})

        valid = BRepCheck(body).IsValid()
        failures = [] if valid else [{"code": "invalid_solid", "message": "OCP solid is not valid", "severity": "error"}]

        step_path = output_dir / f"{part_name}.step"
        stl_path  = output_dir / f"{part_name}.stl"
        write_step(body, step_path, ocp)
        write_stl(body, stl_path, ocp)

        printability = printability_report(stl_path, pt, all_holes, max_overhang, "plate face flat on bed")

        gate_status = "pass" if valid and printability["printable"] else "fail"
        if not printability["printable"]:
            for v in printability["violations"]:
                failures.append({"code": "printability_violation", "message": v, "severity": "error"})

        return {
            "status": "generated" if gate_status == "pass" else "fail",
            "part_name": part_name,
            "part_type": "din_rail_adapter",
            "artifacts": [str(step_path), str(stl_path)],
            "printability": printability,
            "gate_report": {
                "gate": "part_design",
                "status": gate_status,
                "failures": failures,
                "metrics": {
                    "valid_solid": valid,
                    "plate_width_mm": pw,
                    "plate_height_mm": ph,
                    "plate_thickness_mm": pt,
                    "clip_position": clip,
                    "din_rail_standard": "TS-35 (IEC 60715)",
                },
                "artifacts": [str(step_path), str(stl_path)],
                "backend": {"name": "OpenCASCADE", "part_type": "din_rail_adapter"},
            },
            "candidate_only": True,
            "release_eligible": False,
        }
