from __future__ import annotations

from pathlib import Path
from typing import Any

from ..models import Failure, FailureCategory, GateReport, Status


class OpenCascadeMechanicalBackend:
    def generate(self, spec: dict[str, Any], release: Path) -> GateReport:
        try:
            from OCP.BRep import BRep_Builder
            from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
            from OCP.BRepCheck import BRepCheck_Analyzer
            from OCP.BRepMesh import BRepMesh_IncrementalMesh
            from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
            from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt
            from OCP.IFSelect import IFSelect_RetDone
            from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer
            from OCP.StlAPI import StlAPI_Writer
            from OCP.TopoDS import TopoDS_Compound
        except ImportError:
            return GateReport("mechanical_export", Status.BLOCKED, [Failure(FailureCategory.TOOL_ERROR, "tool_unavailable", "cadquery-ocp is not installed")])

        mechanical = spec["mechanical"]
        internal = mechanical["enclosure_internal_mm"]
        wall = float(mechanical["wall_thickness_mm"])
        envelope = mechanical["envelope"]
        insertion_clearance = 2.0
        width, depth, body_height = internal[0] + 2 * wall, internal[1] + 2 * wall, internal[2] + wall
        outer = BRepPrimAPI_MakeBox(width, depth, body_height).Shape()
        inner = BRepPrimAPI_MakeBox(gp_Pnt(wall, wall, wall), gp_Pnt(width - wall, depth - wall, body_height + wall)).Shape()
        base = BRepAlgoAPI_Cut(outer, inner).Shape()
        hole_positions = ((wall + 6.0, wall + 6.0), (wall + envelope["board_width_mm"] - 6.0, wall + 6.0), (wall + 6.0, wall + envelope["board_height_mm"] - 6.0), (wall + envelope["board_width_mm"] - 6.0, wall + envelope["board_height_mm"] - 6.0))
        for x, y in hole_positions:
            boss = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x, y, wall), gp_Dir(0, 0, 1)), 3.2, 4.0).Shape()
            base = BRepAlgoAPI_Fuse(base, boss).Shape()
            hole = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x, y, -1), gp_Dir(0, 0, 1)), 1.6, wall + 2).Shape()
            base = BRepAlgoAPI_Cut(base, hole).Shape()
        cutouts = ((-1.0, 18.0, wall + 2.0, 12.0, 10.0), (width - wall - 1.0, 50.0, wall + 2.0, 12.0, 16.0))
        for x, y, thickness, cutout_width, cutout_height in cutouts:
            cutter = BRepPrimAPI_MakeBox(gp_Pnt(x, y, wall + 4.0), thickness, cutout_width, cutout_height).Shape()
            base = BRepAlgoAPI_Cut(base, cutter).Shape()
        lid = BRepPrimAPI_MakeBox(gp_Pnt(0, 0, body_height + 1.0), width, depth, wall).Shape()
        compound = TopoDS_Compound(); builder = BRep_Builder(); builder.MakeCompound(compound); builder.Add(compound, base); builder.Add(compound, lid)
        failures = []
        board_fit = internal[0] >= envelope["board_width_mm"] + insertion_clearance and internal[1] >= envelope["board_height_mm"] + insertion_clearance
        component_clearance = internal[2] >= envelope["board_thickness_mm"] + envelope["max_component_height_top_mm"] + envelope["max_component_height_bottom_mm"] + insertion_clearance
        wall_valid = wall >= spec.get("manufacturing", {}).get("mechanical", {}).get("min_wall_thickness_mm", 1.6)
        mounting_alignment = all(wall <= x <= width - wall and wall <= y <= depth - wall for x, y in hole_positions)
        cutout_alignment = len(cutouts) >= 2 and all(item[3] > 0 and item[4] > 0 for item in cutouts)
        assembly_interference_free = component_clearance and board_fit
        if not board_fit: failures.append(Failure(FailureCategory.MECHANICAL_ERROR, "board_fit_failed", "Board envelope plus insertion clearance does not fit enclosure"))
        if not component_clearance: failures.append(Failure(FailureCategory.MECHANICAL_ERROR, "component_height_clearance_failed", "Component height map intersects lid/base clearance"))
        if not wall_valid: failures.append(Failure(FailureCategory.MECHANICAL_ERROR, "wall_thickness_failed", "Wall thickness is below manufacturing minimum"))
        if not mounting_alignment: failures.append(Failure(FailureCategory.MECHANICAL_ERROR, "mounting_hole_alignment_failed", "Mounting holes do not align within board/enclosure envelope"))
        if not cutout_alignment: failures.append(Failure(FailureCategory.MECHANICAL_ERROR, "connector_cutout_alignment_failed", "Connector cutouts are incomplete or misaligned"))
        if not assembly_interference_free: failures.append(Failure(FailureCategory.MECHANICAL_ERROR, "assembly_interference", "Board/component envelope interferes with enclosure assembly"))
        if not BRepCheck_Analyzer(base).IsValid():
            failures.append(Failure(FailureCategory.MECHANICAL_ERROR, "invalid_solid", "OpenCASCADE enclosure base is invalid"))
        if not BRepCheck_Analyzer(compound).IsValid():
            failures.append(Failure(FailureCategory.MECHANICAL_ERROR, "invalid_assembly", "OpenCASCADE assembly compound is invalid"))
        target = release / "mechanical"; target.mkdir(parents=True, exist_ok=True)
        if not failures:
            self._write_step(base, target / "enclosure.step", STEPControl_Writer, STEPControl_AsIs, IFSelect_RetDone)
            self._write_step(compound, target / "assembly.step", STEPControl_Writer, STEPControl_AsIs, IFSelect_RetDone)
            BRepMesh_IncrementalMesh(base, 0.15)
            if not StlAPI_Writer().Write(base, str(target / "enclosure.stl")):
                failures.append(Failure(FailureCategory.MECHANICAL_ERROR, "stl_export_failed", "OpenCASCADE STL export failed"))
        artifacts = [str(target / name) for name in ("enclosure.step", "enclosure.stl", "assembly.step") if (target / name).is_file()]
        stl_manifold = (target / "enclosure.stl").is_file() and (target / "enclosure.stl").stat().st_size > 100
        if not failures and not stl_manifold: failures.append(Failure(FailureCategory.MECHANICAL_ERROR, "non_manifold_stl", "STL export is empty or structurally invalid"))
        return GateReport("mechanical_export", Status.FAIL if failures else Status.PASS, failures, metrics={"valid_solid": not any(f.code == "invalid_solid" for f in failures), "stl_manifold": stl_manifold, "board_fit": board_fit, "component_height_clearance": component_clearance, "connector_cutout_alignment": cutout_alignment, "mounting_hole_alignment": mounting_alignment, "assembly_interference_free": assembly_interference_free, "wall_thickness_mm": wall, "insertion_clearance_mm": insertion_clearance, "mounting_holes": len(hole_positions), "outer_dimensions_mm": [width, depth, body_height]}, artifacts=artifacts, backend={"name": "OpenCASCADE", "deterministic_geometry": True})

    @staticmethod
    def _write_step(shape, path: Path, writer_type, mode, success) -> None:
        writer = writer_type()
        if writer.Transfer(shape, mode) != success or writer.Write(str(path)) != success:
            raise RuntimeError(f"Failed to export STEP: {path}")
