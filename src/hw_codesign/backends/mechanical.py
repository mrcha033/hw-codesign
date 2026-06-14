from __future__ import annotations

from pathlib import Path
from typing import Any

from ..models import Failure, FailureCategory, GateReport, Status


class OpenCascadeMechanicalBackend:
    def generate(self, spec: dict[str, Any], release: Path) -> GateReport:
        try:
            from OCP.BRep import BRep_Builder
            from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
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
        width, depth, body_height = internal[0] + 2 * wall, internal[1] + 2 * wall, internal[2] + wall
        outer = BRepPrimAPI_MakeBox(width, depth, body_height).Shape()
        inner = BRepPrimAPI_MakeBox(gp_Pnt(wall, wall, wall), gp_Pnt(width - wall, depth - wall, body_height + wall)).Shape()
        base = BRepAlgoAPI_Cut(outer, inner).Shape()
        hole_positions = ((8.0, 8.0), (width - 8.0, 8.0), (8.0, depth - 8.0), (width - 8.0, depth - 8.0))
        for x, y in hole_positions:
            hole = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x, y, -1), gp_Dir(0, 0, 1)), 1.6, wall + 2).Shape()
            base = BRepAlgoAPI_Cut(base, hole).Shape()
        lid = BRepPrimAPI_MakeBox(gp_Pnt(0, 0, body_height + 1.0), width, depth, wall).Shape()
        compound = TopoDS_Compound(); builder = BRep_Builder(); builder.MakeCompound(compound); builder.Add(compound, base); builder.Add(compound, lid)
        failures = []
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
        return GateReport("mechanical_export", Status.FAIL if failures else Status.PASS, failures, metrics={"exact_solid_valid": not failures, "mounting_holes": len(hole_positions), "outer_dimensions_mm": [width, depth, body_height]}, artifacts=artifacts, backend={"name": "OpenCASCADE", "deterministic_geometry": True})

    @staticmethod
    def _write_step(shape, path: Path, writer_type, mode, success) -> None:
        writer = writer_type()
        if writer.Transfer(shape, mode) != success or writer.Write(str(path)) != success:
            raise RuntimeError(f"Failed to export STEP: {path}")

