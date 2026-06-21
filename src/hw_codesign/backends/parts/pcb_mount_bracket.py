"""Parametric PCB mount bracket — L or U profile for extrusion or panel mounting."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ._base import (
    _EXTRUSION_SPECS,
    fastener_clearance,
    import_ocp,
    printability_report,
    write_step,
    write_stl,
)

# Schema describing the intent this part accepts
INTENT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": ["bracket_width_mm", "bracket_height_mm"],
    "additionalProperties": True,
    "properties": {
        "bracket_width_mm":   {"type": "number", "minimum": 10, "description": "Width spanning the PCB edge"},
        "bracket_height_mm":  {"type": "number", "minimum": 10, "description": "Height of the vertical back plate"},
        "leg_depth_mm":       {"type": "number", "minimum": 5,  "default": 15, "description": "Depth of horizontal mounting flange"},
        "thickness_mm":       {"type": "number", "minimum": 1.2, "default": 3.0, "description": "Wall thickness"},
        "fastener":           {"type": "string", "enum": ["M2", "M2.5", "M3", "M4", "M5"], "default": "M3"},
        "interface":          {"type": "string", "default": "custom", "description": "Extrusion or frame interface type"},
        "bracket_style":      {"type": "string", "enum": ["L", "U"], "default": "L"},
        "pcb_holes":          {
            "type": "array",
            "description": "PCB mounting hole positions on the vertical plate (from bottom-left)",
            "items": {"type": "object", "required": ["x_mm", "z_mm"], "properties": {
                "x_mm": {"type": "number"},
                "z_mm": {"type": "number"},
            }},
        },
        "frame_holes":        {
            "type": "array",
            "description": "Frame/extrusion mounting hole positions on the horizontal flange",
            "items": {"type": "object", "required": ["x_mm", "y_mm"], "properties": {
                "x_mm": {"type": "number"},
                "y_mm": {"type": "number"},
            }},
        },
        "max_overhang_angle_deg": {"type": "number", "default": 45, "minimum": 10, "maximum": 80},
    },
}


class PcbMountBracket:
    """L or U bracket for mounting a PCB to an extrusion or panel.

    Coordinate system:
      X = along bracket width
      Y = depth direction (into wall / extrusion)
      Z = height (vertical)

    Vertical back plate: X=[0..width], Y=[0..t], Z=[0..height]
    Horizontal leg:      X=[0..width], Y=[0..leg], Z=[-t..0]
    """

    def design(self, intent: dict[str, Any], output_dir: Path, part_name: str) -> dict[str, Any]:
        try:
            ocp = import_ocp()
        except ImportError:
            return {
                "status": "blocked",
                "code": "tool_unavailable",
                "message": "cadquery-ocp is not installed — install with: pip install cadquery-ocp",
                "part_name": part_name,
                "part_type": "pcb_mount_bracket",
            }

        width   = float(intent.get("bracket_width_mm", 60.0))
        height  = float(intent.get("bracket_height_mm", 40.0))
        leg     = float(intent.get("leg_depth_mm", 15.0))
        t       = float(intent.get("thickness_mm", 3.0))
        fastener = intent.get("fastener", "M3")
        style   = intent.get("bracket_style", "L")
        max_overhang = float(intent.get("max_overhang_angle_deg", 45.0))
        pcb_holes   = intent.get("pcb_holes", [])
        frame_holes = intent.get("frame_holes", [])

        MakeBox = ocp["BRepPrimAPI_MakeBox"]
        MakeCylinder = ocp["BRepPrimAPI_MakeCylinder"]
        Cut = ocp["BRepAlgoAPI_Cut"]
        Fuse = ocp["BRepAlgoAPI_Fuse"]
        BRepCheck = ocp["BRepCheck_Analyzer"]
        gp_Pnt = ocp["gp_Pnt"]
        gp_Ax2 = ocp["gp_Ax2"]
        gp_Dir = ocp["gp_Dir"]

        # Vertical back plate
        vert = MakeBox(gp_Pnt(0, 0, 0), width, t, height).Shape()
        # Horizontal leg (leg extends in +Y direction, sits at Z=[-t..0])
        horiz = MakeBox(gp_Pnt(0, 0, -t), width, leg, t).Shape()

        body = Fuse(vert, horiz).Shape()

        if style == "U":
            # Second vertical plate at the far end of the leg
            vert2 = MakeBox(gp_Pnt(0, leg - t, -t), width, t, height + t).Shape()
            body = Fuse(body, vert2).Shape()

        # Bore PCB mounting holes through vertical plate (Y direction)
        r_clear = fastener_clearance(fastener) / 2
        for hole in pcb_holes:
            x = float(hole["x_mm"])
            z = float(hole["z_mm"])
            bore = MakeCylinder(gp_Ax2(gp_Pnt(x, -1, z), gp_Dir(0, 1, 0)), r_clear, t + 2).Shape()
            body = Cut(body, bore).Shape()

        # Auto-generate two PCB holes if none specified
        if not pcb_holes:
            for x in [width * 0.25, width * 0.75]:
                z = height * 0.5
                bore = MakeCylinder(gp_Ax2(gp_Pnt(x, -1, z), gp_Dir(0, 1, 0)), r_clear, t + 2).Shape()
                body = Cut(body, bore).Shape()

        # Bore frame mounting holes through horizontal flange (Z direction)
        interface = intent.get("interface", "custom")
        frame_fastener = fastener
        if interface in _EXTRUSION_SPECS:
            spec = _EXTRUSION_SPECS[interface]
            frame_fastener = spec.get("t_nut_fastener") or fastener
        r_frame = fastener_clearance(frame_fastener) / 2

        for hole in frame_holes:
            x = float(hole["x_mm"])
            y = float(hole["y_mm"])
            bore = MakeCylinder(gp_Ax2(gp_Pnt(x, y, -t - 1), gp_Dir(0, 0, 1)), r_frame, t + 2).Shape()
            body = Cut(body, bore).Shape()

        # Auto-generate two frame holes if none specified
        if not frame_holes:
            for x in [width * 0.25, width * 0.75]:
                y = leg / 2
                bore = MakeCylinder(gp_Ax2(gp_Pnt(x, y, -t - 1), gp_Dir(0, 0, 1)), r_frame, t + 2).Shape()
                body = Cut(body, bore).Shape()

        valid = BRepCheck(body).IsValid()
        failures = [] if valid else [{"code": "invalid_solid", "message": "OCP solid is not valid", "severity": "error"}]

        step_path = output_dir / f"{part_name}.step"
        stl_path  = output_dir / f"{part_name}.stl"
        write_step(body, step_path, ocp)
        write_stl(body, stl_path, ocp)

        all_holes = [{"diameter_mm": fastener_clearance(fastener)}] * (len(pcb_holes) or 2)
        all_holes += [{"diameter_mm": fastener_clearance(frame_fastener)}] * (len(frame_holes) or 2)
        printability = printability_report(stl_path, t, all_holes, max_overhang, "back plate flat on bed")

        gate_status = "pass" if valid and printability["printable"] else "fail"
        if not valid:
            pass  # failures already set
        if not printability["printable"]:
            for v in printability["violations"]:
                failures.append({"code": "printability_violation", "message": v, "severity": "error"})

        return {
            "status": "generated" if gate_status == "pass" else "fail",
            "part_name": part_name,
            "part_type": "pcb_mount_bracket",
            "artifacts": [str(step_path), str(stl_path)],
            "printability": printability,
            "gate_report": {
                "gate": "part_design",
                "status": gate_status,
                "failures": failures,
                "metrics": {
                    "valid_solid": valid,
                    "stl_manifold": printability["stl_manifold"],
                    "width_mm": width,
                    "height_mm": height,
                    "leg_depth_mm": leg,
                    "thickness_mm": t,
                    "bracket_style": style,
                    "interface": interface,
                    "fastener": fastener,
                },
                "artifacts": [str(step_path), str(stl_path)],
                "backend": {"name": "OpenCASCADE", "part_type": "pcb_mount_bracket"},
            },
            "candidate_only": True,
            "release_eligible": False,
        }
