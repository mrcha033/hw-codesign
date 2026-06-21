"""Agent-specified enclosure variant — extends the existing box+lid with custom cutouts and features."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ._base import (
    import_ocp,
    printability_report,
    write_step,
    write_stl,
)

INTENT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": ["internal_mm"],
    "additionalProperties": True,
    "properties": {
        "internal_mm":       {
            "type": "array", "items": {"type": "number"}, "minItems": 3, "maxItems": 3,
            "description": "[width, depth, height] of internal cavity",
        },
        "wall_thickness_mm": {"type": "number", "minimum": 1.2, "default": 2.5},
        "panel_cutouts":     {
            "type": "array",
            "description": "Rectangular cutouts in enclosure walls for connectors, displays, etc.",
            "items": {
                "type": "object",
                "required": ["side", "width_mm", "height_mm", "center_x_mm", "center_z_mm"],
                "properties": {
                    "side":        {"type": "string", "enum": ["front", "rear", "left", "right"]},
                    "width_mm":    {"type": "number"},
                    "height_mm":   {"type": "number"},
                    "center_x_mm": {"type": "number", "description": "Position along the wall (from left edge)"},
                    "center_z_mm": {"type": "number", "description": "Vertical position (from bottom)"},
                    "label":       {"type": "string"},
                },
            },
        },
        "gland_holes":       {
            "type": "array",
            "description": "Circular cable gland holes",
            "items": {
                "type": "object",
                "required": ["side", "diameter_mm", "center_x_mm", "center_z_mm"],
                "properties": {
                    "side":         {"type": "string", "enum": ["front", "rear", "left", "right", "top", "bottom"]},
                    "diameter_mm":  {"type": "number", "minimum": 3},
                    "center_x_mm":  {"type": "number"},
                    "center_z_mm":  {"type": "number"},
                    "label":        {"type": "string"},
                },
            },
        },
        "vent_slots":        {
            "type": "object",
            "description": "Vent slot pattern on lid or walls",
            "properties": {
                "side":        {"type": "string", "enum": ["top", "front", "rear", "left", "right"], "default": "top"},
                "count":       {"type": "integer", "minimum": 1, "default": 5},
                "slot_width_mm": {"type": "number", "default": 2.5},
                "slot_height_mm": {"type": "number", "default": 15.0},
                "spacing_mm":  {"type": "number", "default": 5.0},
            },
        },
        "lid":               {"type": "boolean", "default": True, "description": "Include a removable lid"},
        "max_overhang_angle_deg": {"type": "number", "default": 45},
    },
}


class CustomEnclosureVariant:
    """Rectangular enclosure with agent-specified panel cutouts, gland holes, and vent patterns.

    Produces: base body + optional lid as separate STEP files plus an assembly STEP.
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
                "part_type": "custom_enclosure_variant",
            }

        internal  = [float(v) for v in intent.get("internal_mm", [100, 80, 40])]
        wall      = float(intent.get("wall_thickness_mm", 2.5))
        cutouts   = intent.get("panel_cutouts", [])
        glands    = intent.get("gland_holes", [])
        vents_cfg = intent.get("vent_slots")
        make_lid  = bool(intent.get("lid", True))
        max_overhang = float(intent.get("max_overhang_angle_deg", 45.0))

        iw, id_, ih = internal[0], internal[1], internal[2]
        ow = iw + 2 * wall
        od = id_ + 2 * wall
        body_h = ih + wall  # open top (lid separate)

        MakeBox  = ocp["BRepPrimAPI_MakeBox"]
        MakeCyl  = ocp["BRepPrimAPI_MakeCylinder"]
        Cut      = ocp["BRepAlgoAPI_Cut"]
        _Fuse    = ocp["BRepAlgoAPI_Fuse"]
        BRepCheck = ocp["BRepCheck_Analyzer"]
        BRep_Builder = ocp["BRep_Builder"]
        TopoDS_Compound = ocp["TopoDS_Compound"]
        gp_Pnt   = ocp["gp_Pnt"]
        gp_Ax2   = ocp["gp_Ax2"]
        gp_Dir   = ocp["gp_Dir"]
        _IFSelect_RetDone  = ocp["IFSelect_RetDone"]
        _STEPControl_Writer = ocp["STEPControl_Writer"]
        _STEPControl_AsIs   = ocp["STEPControl_AsIs"]

        # Base box
        outer = MakeBox(gp_Pnt(0, 0, 0), ow, od, body_h).Shape()
        inner = MakeBox(gp_Pnt(wall, wall, wall), iw, id_, ih + wall).Shape()
        base  = Cut(outer, inner).Shape()

        def _cut_rect(shape, side: str, cx: float, cz: float, w: float, h: float):
            """Cut a rectangular opening in the specified wall."""
            if side == "front":
                box = MakeBox(gp_Pnt(wall + cx - w/2, -1, wall + cz - h/2), w, wall + 2, h).Shape()
            elif side == "rear":
                box = MakeBox(gp_Pnt(wall + cx - w/2, od - wall - 1, wall + cz - h/2), w, wall + 2, h).Shape()
            elif side == "left":
                box = MakeBox(gp_Pnt(-1, wall + cx - w/2, wall + cz - h/2), wall + 2, w, h).Shape()
            else:  # right
                box = MakeBox(gp_Pnt(ow - wall - 1, wall + cx - w/2, wall + cz - h/2), wall + 2, w, h).Shape()
            return Cut(shape, box).Shape()

        def _cut_circle(shape, side: str, cx: float, cz: float, r: float):
            if side == "front":
                cyl = MakeCyl(gp_Ax2(gp_Pnt(wall + cx, -1, wall + cz), gp_Dir(0, 1, 0)), r, wall + 2).Shape()
            elif side == "rear":
                cyl = MakeCyl(gp_Ax2(gp_Pnt(wall + cx, od - wall - 1, wall + cz), gp_Dir(0, 1, 0)), r, wall + 2).Shape()
            elif side == "left":
                cyl = MakeCyl(gp_Ax2(gp_Pnt(-1, wall + cx, wall + cz), gp_Dir(1, 0, 0)), r, wall + 2).Shape()
            elif side == "right":
                cyl = MakeCyl(gp_Ax2(gp_Pnt(ow - wall - 1, wall + cx, wall + cz), gp_Dir(1, 0, 0)), r, wall + 2).Shape()
            elif side == "top":
                cyl = MakeCyl(gp_Ax2(gp_Pnt(wall + cx, wall + cz, body_h - 1), gp_Dir(0, 0, 1)), r, wall + 2).Shape()
            else:  # bottom
                cyl = MakeCyl(gp_Ax2(gp_Pnt(wall + cx, wall + cz, -1), gp_Dir(0, 0, 1)), r, wall + 2).Shape()
            return Cut(shape, cyl).Shape()

        for c in cutouts:
            base = _cut_rect(base, c["side"], float(c["center_x_mm"]), float(c["center_z_mm"]),
                             float(c["width_mm"]), float(c["height_mm"]))

        for g in glands:
            base = _cut_circle(base, g["side"], float(g["center_x_mm"]), float(g["center_z_mm"]),
                               float(g["diameter_mm"]) / 2)

        artifacts = []
        base_step = output_dir / f"{part_name}_base.step"
        base_stl  = output_dir / f"{part_name}_base.stl"
        write_step(base, base_step, ocp)
        write_stl(base, base_stl, ocp)
        artifacts.extend([str(base_step), str(base_stl)])

        lid_shape = None
        if make_lid:
            lid = MakeBox(gp_Pnt(0, 0, body_h), ow, od, wall).Shape()
            if vents_cfg:
                slot_w   = float(vents_cfg.get("slot_width_mm", 2.5))
                _slot_h  = float(vents_cfg.get("slot_height_mm", 15.0))
                count    = int(vents_cfg.get("count", 5))
                spacing  = float(vents_cfg.get("spacing_mm", 5.0))
                total_w  = count * slot_w + (count - 1) * spacing
                x_start  = (ow - total_w) / 2
                for i in range(count):
                    x = x_start + i * (slot_w + spacing)
                    slot = MakeBox(gp_Pnt(x, od * 0.3, body_h - 1), slot_w, od * 0.4, wall + 2).Shape()
                    lid = Cut(lid, slot).Shape()
            lid_shape = lid
            lid_step = output_dir / f"{part_name}_lid.step"
            lid_stl  = output_dir / f"{part_name}_lid.stl"
            write_step(lid, lid_step, ocp)
            write_stl(lid, lid_stl, ocp)
            artifacts.extend([str(lid_step), str(lid_stl)])

        # Assembly STEP (compound)
        compound = TopoDS_Compound()
        builder  = BRep_Builder()
        builder.MakeCompound(compound)
        builder.Add(compound, base)
        if lid_shape is not None:
            builder.Add(compound, lid_shape)
        asm_step = output_dir / f"{part_name}_assembly.step"
        write_step(compound, asm_step, ocp)
        artifacts.append(str(asm_step))

        valid    = BRepCheck(base).IsValid() and (lid_shape is None or BRepCheck(lid_shape).IsValid())
        failures = [] if valid else [{"code": "invalid_solid", "message": "OCP solid is not valid", "severity": "error"}]

        all_holes = [{"diameter_mm": float(g["diameter_mm"])} for g in glands]
        printability = printability_report(base_stl, wall, all_holes or [{"diameter_mm": 99}], max_overhang, "base flat on bed")

        gate_status = "pass" if valid and printability["printable"] else "fail"
        if not printability["printable"]:
            for v in printability["violations"]:
                failures.append({"code": "printability_violation", "message": v, "severity": "error"})

        return {
            "status": "generated" if gate_status == "pass" else "fail",
            "part_name": part_name,
            "part_type": "custom_enclosure_variant",
            "artifacts": artifacts,
            "printability": printability,
            "gate_report": {
                "gate": "part_design",
                "status": gate_status,
                "failures": failures,
                "metrics": {
                    "valid_solid": valid,
                    "internal_mm": internal,
                    "wall_thickness_mm": wall,
                    "panel_cutout_count": len(cutouts),
                    "gland_hole_count": len(glands),
                    "has_vent_slots": vents_cfg is not None,
                    "has_lid": make_lid,
                },
                "artifacts": artifacts,
                "backend": {"name": "OpenCASCADE", "part_type": "custom_enclosure_variant"},
            },
            "candidate_only": True,
            "release_eligible": False,
        }
