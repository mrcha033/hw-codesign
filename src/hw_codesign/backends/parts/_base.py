"""Shared OCP helpers, STEP/STL export, and FDM printability analysis for parametric parts."""
from __future__ import annotations

import math
import struct
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


_FASTENER_SPECS: dict[str, dict[str, float]] = {
    "M2":   {"clearance_mm": 2.4,  "bore_mm": 1.6},
    "M2.5": {"clearance_mm": 2.9,  "bore_mm": 2.05},
    "M3":   {"clearance_mm": 3.4,  "bore_mm": 2.5},
    "M4":   {"clearance_mm": 4.5,  "bore_mm": 3.3},
    "M5":   {"clearance_mm": 5.5,  "bore_mm": 4.2},
}

_EXTRUSION_SPECS: dict[str, dict[str, Any]] = {
    "2020_extrusion_slot_6": {"width_mm": 20.0, "slot_mm": 6.0, "t_nut_fastener": "M5"},
    "4040_extrusion_slot_8": {"width_mm": 40.0, "slot_mm": 8.0, "t_nut_fastener": "M5"},
    "misumi_hfs5_2020":      {"width_mm": 20.0, "slot_mm": 6.0, "t_nut_fastener": "M5"},
    "custom":                {"width_mm": None,  "slot_mm": None, "t_nut_fastener": None},
}

# FDM printability thresholds
_MIN_WALL_MM = 1.2       # thinnest wall FDM can reliably print
_MIN_HOLE_MM = 2.0       # smallest clearance hole for M2
_MAX_OVERHANG_DEFAULT = 45.0  # degrees from vertical, default FDM limit


def fastener_clearance(fastener: str) -> float:
    return _FASTENER_SPECS.get(fastener, _FASTENER_SPECS["M3"])["clearance_mm"]


def fastener_bore(fastener: str) -> float:
    return _FASTENER_SPECS.get(fastener, _FASTENER_SPECS["M3"])["bore_mm"]


def import_ocp():
    """Import OCP modules; raise ImportError if not available."""
    from OCP.BRep import BRep_Builder
    from OCP.BRepAlgoAPI import BRepAlgoAPI_Common, BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
    from OCP.BRepCheck import BRepCheck_Analyzer
    from OCP.BRepGProp import BRepGProp
    from OCP.BRepMesh import BRepMesh_IncrementalMesh
    from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
    from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt, gp_Trsf, gp_Vec
    from OCP.GProp import GProp_GProps
    from OCP.IFSelect import IFSelect_RetDone
    from OCP.STEPControl import STEPControl_AsIs, STEPControl_Writer
    from OCP.StlAPI import StlAPI_Writer
    from OCP.TopoDS import TopoDS_Compound
    return {
        "BRep_Builder": BRep_Builder,
        "BRepAlgoAPI_Common": BRepAlgoAPI_Common,
        "BRepAlgoAPI_Cut": BRepAlgoAPI_Cut,
        "BRepAlgoAPI_Fuse": BRepAlgoAPI_Fuse,
        "BRepCheck_Analyzer": BRepCheck_Analyzer,
        "BRepGProp": BRepGProp,
        "BRepMesh_IncrementalMesh": BRepMesh_IncrementalMesh,
        "BRepPrimAPI_MakeBox": BRepPrimAPI_MakeBox,
        "BRepPrimAPI_MakeCylinder": BRepPrimAPI_MakeCylinder,
        "gp_Ax2": gp_Ax2,
        "gp_Dir": gp_Dir,
        "gp_Pnt": gp_Pnt,
        "gp_Trsf": gp_Trsf,
        "gp_Vec": gp_Vec,
        "GProp_GProps": GProp_GProps,
        "IFSelect_RetDone": IFSelect_RetDone,
        "STEPControl_AsIs": STEPControl_AsIs,
        "STEPControl_Writer": STEPControl_Writer,
        "StlAPI_Writer": StlAPI_Writer,
        "TopoDS_Compound": TopoDS_Compound,
    }


def write_step(shape, path: Path, ocp: dict) -> None:
    writer = ocp["STEPControl_Writer"]()
    ret = ocp["STEPControl_AsIs"]
    if writer.Transfer(shape, ret) != ocp["IFSelect_RetDone"] or writer.Write(str(path)) != ocp["IFSelect_RetDone"]:
        raise RuntimeError(f"STEP export failed: {path}")


def write_stl(shape, path: Path, ocp: dict, linear_deflection: float = 0.12) -> None:
    ocp["BRepMesh_IncrementalMesh"](shape, linear_deflection)
    ocp["StlAPI_Writer"]().Write(shape, str(path))


def stl_is_manifold(path: Path) -> bool:
    if not path.is_file() or path.stat().st_size < 84:
        return False
    data = path.read_bytes()
    triangles: list[tuple] = []
    count = struct.unpack_from("<I", data, 80)[0]
    if 84 + count * 50 == len(data):
        for i in range(count):
            values = struct.unpack_from("<12fH", data, 84 + i * 50)
            triangles.append((values[3:6], values[6:9], values[9:12]))
    else:
        vertices = []
        for line in data.decode("ascii", errors="ignore").splitlines():
            if line.strip().startswith("vertex "):
                vertices.append(tuple(map(float, line.split()[1:4])))
        triangles = [tuple(vertices[i:i + 3]) for i in range(0, len(vertices), 3) if len(vertices[i:i + 3]) == 3]
    edges: Counter = Counter()
    for tri in triangles:
        pts = [tuple(round(v, 5) for v in p) for p in tri]
        for a, b in ((pts[0], pts[1]), (pts[1], pts[2]), (pts[2], pts[0])):
            edges[tuple(sorted((a, b)))] += 1
    return bool(triangles) and all(n == 2 for n in edges.values())


def analyze_overhangs(path: Path, max_angle_deg: float = _MAX_OVERHANG_DEFAULT) -> dict[str, Any]:
    """Analyze an STL for overhangs exceeding max_angle_deg from vertical."""
    if not path.is_file() or path.stat().st_size < 84:
        return {"max_overhang_deg": 0.0, "overhang_triangle_count": 0, "violations": []}
    data = path.read_bytes()
    normals: list[tuple[float, float, float]] = []
    count = struct.unpack_from("<I", data, 80)[0]
    if 84 + count * 50 == len(data):
        for i in range(count):
            nx, ny, nz = struct.unpack_from("<3f", data, 84 + i * 50)
            normals.append((nx, ny, nz))
    else:
        current_normal: tuple[float, float, float] | None = None
        for line in data.decode("ascii", errors="ignore").splitlines():
            line = line.strip()
            if line.startswith("facet normal "):
                parts = line.split()
                current_normal = (float(parts[2]), float(parts[3]), float(parts[4]))
            elif line == "endfacet" and current_normal is not None:
                normals.append(current_normal)
                current_normal = None

    max_seen = 0.0
    violation_count = 0
    for nx, ny, nz in normals:
        if nz >= 0:
            continue
        # angle from vertical = arccos(|nz| / magnitude)
        mag = math.sqrt(nx * nx + ny * ny + nz * nz)
        if mag < 1e-9:
            continue
        angle_from_vertical = math.degrees(math.acos(min(1.0, abs(nz) / mag)))
        max_seen = max(max_seen, angle_from_vertical)
        if angle_from_vertical > max_angle_deg:
            violation_count += 1

    violations = []
    if violation_count > 0:
        violations.append(f"{violation_count} downward-facing triangles exceed {max_angle_deg}° overhang limit")
    return {
        "max_overhang_deg": round(max_seen, 1),
        "overhang_triangle_count": violation_count,
        "violations": violations,
    }


def check_hole_diameters(holes: list[dict[str, Any]]) -> list[str]:
    violations = []
    for hole in holes:
        d = float(hole.get("diameter_mm", 0))
        if d < _MIN_HOLE_MM:
            violations.append(f"hole diameter {d} mm is below FDM minimum {_MIN_HOLE_MM} mm")
    return violations


def printability_report(
    stl_path: Path,
    wall_thickness_mm: float,
    holes: list[dict[str, Any]],
    max_overhang_deg: float = _MAX_OVERHANG_DEFAULT,
    recommended_orientation: str = "flat on bed",
) -> dict[str, Any]:
    overhang = analyze_overhangs(stl_path, max_overhang_deg)
    manifold = stl_is_manifold(stl_path)
    hole_violations = check_hole_diameters(holes)
    wall_violations = [] if wall_thickness_mm >= _MIN_WALL_MM else [f"wall {wall_thickness_mm} mm is below FDM minimum {_MIN_WALL_MM} mm"]
    violations = overhang["violations"] + hole_violations + wall_violations
    if not manifold:
        violations.append("STL mesh is not a closed two-manifold — cannot be sliced")
    return {
        "printable": len(violations) == 0,
        "max_overhang_deg": overhang["max_overhang_deg"],
        "min_wall_mm": wall_thickness_mm,
        "min_hole_mm": min((float(h.get("diameter_mm", 99)) for h in holes), default=99.0),
        "stl_manifold": manifold,
        "recommended_orientation": recommended_orientation,
        "violations": violations,
    }


def part_manifest(
    part_name: str,
    part_type: str,
    intent: dict[str, Any],
    artifacts: list[str],
    printability: dict[str, Any],
    gate_status: str,
) -> dict[str, Any]:
    return {
        "part_name": part_name,
        "part_type": part_type,
        "intent": intent,
        "artifacts": artifacts,
        "printability": printability,
        "gate_status": gate_status,
        "generated": datetime.now(UTC).isoformat(),
        "candidate_only": True,
        "release_eligible": False,
    }
