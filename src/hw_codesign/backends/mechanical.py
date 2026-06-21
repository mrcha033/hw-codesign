from __future__ import annotations

import shutil
import struct
from collections import Counter
from datetime import UTC, datetime
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any

from ..artifacts import sha256
from ..io import write_json
from ..mechanical_contract import build_mechanical_contract
from ..models import Failure, FailureCategory, GateReport, Status


class OpenCascadeMechanicalBackend:
    def generate(
        self,
        spec: dict[str, Any],
        release: Path,
        *,
        graph: dict[str, Any] | None = None,
        board_step: Path | None = None,
        release_eligible: bool = False,
    ) -> GateReport:
        return self.generate_from_contract(build_mechanical_contract(spec, graph or {"components": []}), release, board_step=board_step, release_eligible=release_eligible)

    def generate_from_contract(self, contract: dict[str, Any], release: Path, *, board_step: Path | None = None, release_eligible: bool = False) -> GateReport:
        try:
            from OCP.BRep import BRep_Builder
            from OCP.BRepAlgoAPI import BRepAlgoAPI_Common, BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
            from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
            from OCP.BRepCheck import BRepCheck_Analyzer
            from OCP.BRepGProp import BRepGProp
            from OCP.BRepMesh import BRepMesh_IncrementalMesh
            from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
            from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt, gp_Trsf, gp_Vec
            from OCP.GProp import GProp_GProps
            from OCP.IFSelect import IFSelect_RetDone
            from OCP.STEPControl import STEPControl_AsIs, STEPControl_Reader, STEPControl_Writer
            from OCP.StlAPI import StlAPI_Writer
            from OCP.TopoDS import TopoDS_Compound
        except ImportError:
            return GateReport("mechanical_export", Status.BLOCKED, [Failure(FailureCategory.TOOL_ERROR, "tool_unavailable", "cadquery-ocp is not installed")])

        board = contract["board"]
        enclosure = contract["enclosure"]
        clearances = contract["clearances"]
        internal = enclosure["internal_mm"]
        wall = enclosure["wall_thickness_mm"]
        origin = board["origin_mm"]
        tolerance = clearances["tolerance_mm"]
        insertion = clearances["insertion_mm"]
        assembly_clearance = clearances["assembly_mm"]
        width, depth, body_height = internal[0] + 2 * wall, internal[1] + 2 * wall, internal[2] + wall

        failures: list[Failure] = []
        blocked = False
        variants = {item["name"]: item for item in contract["variants"]}
        selected = variants.get(contract["selected_variant"])
        if selected is None:
            return GateReport("mechanical_export", Status.FAIL, [Failure(FailureCategory.MECHANICAL_ERROR, "variant_not_found", "Selected enclosure variant is absent")])

        board_fit = (
            origin[0] >= insertion + tolerance
            and origin[1] >= insertion + tolerance
            and internal[0] - origin[0] - board["width_mm"] >= insertion + tolerance
            and internal[1] - origin[1] - board["height_mm"] >= insertion + tolerance
        )
        bottom_gap = origin[2] - board["max_component_height_bottom_mm"]
        top_gap = internal[2] - (origin[2] + board["thickness_mm"] + board["max_component_height_top_mm"])
        component_clearance = bottom_gap >= assembly_clearance + tolerance and top_gap >= assembly_clearance + tolerance
        if not board_fit:
            failures.append(Failure(FailureCategory.MECHANICAL_ERROR, "board_fit_failed", "Worst-case board edge clearance is below insertion clearance plus tolerance"))
        if not component_clearance:
            failures.append(Failure(FailureCategory.MECHANICAL_ERROR, "component_height_clearance_failed", "Worst-case component height envelope violates base or lid clearance", details={"top_gap_mm": top_gap, "bottom_gap_mm": bottom_gap}))

        mounting_alignment = True
        for hole in contract["mounting_holes"]:
            in_board = 0 <= hole["x_mm"] <= board["width_mm"] and 0 <= hole["y_mm"] <= board["height_mm"] and hole["diameter_mm"] > 0
            mounting_alignment &= in_board
        if not mounting_alignment:
            failures.append(Failure(FailureCategory.MECHANICAL_ERROR, "mounting_hole_alignment_failed", "Mounting-hole contract lies outside the board envelope"))

        expected_connectors = set(contract["connector_component_refs"])
        cutout_refs = {item["ref"] for item in contract["connector_cutouts"]}
        missing_cutouts = sorted(expected_connectors - cutout_refs)
        cutout_alignment = not missing_cutouts
        for cutout in contract["connector_cutouts"]:
            position = cutout.get("pcb_position_mm")
            if not cutout.get("component_present") or position is None:
                cutout_alignment = False
                failures.append(Failure(FailureCategory.MECHANICAL_ERROR, "connector_reference_missing", f"Cutout references absent electrical connector {cutout['ref']}"))
                continue
            edge_distance = self._edge_distance(cutout["side"], position, board["width_mm"], board["height_mm"])
            if edge_distance > clearances["max_connector_edge_distance_mm"] + cutout["position_tolerance_mm"]:
                cutout_alignment = False
                failures.append(Failure(FailureCategory.MECHANICAL_ERROR, "connector_cutout_alignment_failed", f"{cutout['ref']} is too far from enclosure {cutout['side']} wall", details={"edge_distance_mm": edge_distance}))
        if missing_cutouts:
            failures.append(Failure(FailureCategory.MECHANICAL_ERROR, "connector_cutout_missing", "Electrical connectors lack mechanical cutouts", details={"references": missing_cutouts}))

        def make_base():
            outer = BRepPrimAPI_MakeBox(width, depth, body_height).Shape()
            inner = BRepPrimAPI_MakeBox(gp_Pnt(wall, wall, wall), gp_Pnt(width - wall, depth - wall, body_height + wall)).Shape()
            shape = BRepAlgoAPI_Cut(outer, inner).Shape()
            for hole in contract["mounting_holes"]:
                x, y = wall + origin[0] + hole["x_mm"], wall + origin[1] + hole["y_mm"]
                boss = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x, y, wall), gp_Dir(0, 0, 1)), hole["diameter_mm"] / 2 + 1.6, max(origin[2] - wall, 1.0)).Shape()
                shape = BRepAlgoAPI_Fuse(shape, boss).Shape()
                bore = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x, y, -1), gp_Dir(0, 0, 1)), hole["diameter_mm"] / 2, body_height + 2).Shape()
                shape = BRepAlgoAPI_Cut(shape, bore).Shape()
            for cutout in contract["connector_cutouts"]:
                if cutout.get("enclosure_position_mm"):
                    shape = BRepAlgoAPI_Cut(shape, self._cutout_shape(cutout, width, depth, wall, BRepPrimAPI_MakeBox, gp_Pnt)).Shape()
            return shape

        def make_lid(variant):
            lid = BRepPrimAPI_MakeBox(gp_Pnt(0, 0, body_height), width, depth, wall).Shape()
            if variant["ventilation"] != "none":
                for index in range(5):
                    x = width * 0.35 + index * 6.0
                    vent = BRepPrimAPI_MakeBox(gp_Pnt(x, depth * 0.35, body_height - 1), 2.5, depth * 0.3, wall + 2).Shape()
                    lid = BRepAlgoAPI_Cut(lid, vent).Shape()
            return lid

        base = make_base()
        lids = {name: make_lid(variant) for name, variant in variants.items()}
        lid = lids[selected["name"]]

        fixture_shapes = []
        fixtures = contract.get("fixtures", {})
        plate_config = fixtures.get("mounting_plate", {})
        if plate_config.get("enabled"):
            margin = plate_config["edge_margin_mm"]
            thickness = plate_config["thickness_mm"]
            plate = BRepPrimAPI_MakeBox(gp_Pnt(-margin, -margin, -thickness), width + 2 * margin, depth + 2 * margin, thickness).Shape()
            for hole in contract["mounting_holes"]:
                x, y = wall + origin[0] + hole["x_mm"], wall + origin[1] + hole["y_mm"]
                bore = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x, y, -thickness - 1), gp_Dir(0, 0, 1)), hole["diameter_mm"] / 2, thickness + 2).Shape()
                plate = BRepAlgoAPI_Cut(plate, bore).Shape()
            fixture_shapes.append(("mounting_plate", plate))
        bracket_config = fixtures.get("frame_brackets", {})
        if bracket_config.get("enabled"):
            thickness, bracket_width, bracket_height = bracket_config["thickness_mm"], bracket_config["width_mm"], bracket_config["height_mm"]
            for side, x in (("left", -bracket_width), ("right", width)):
                horizontal = BRepPrimAPI_MakeBox(gp_Pnt(x, depth * 0.25, -thickness), bracket_width, depth * 0.5, thickness).Shape()
                vertical = BRepPrimAPI_MakeBox(gp_Pnt(x if side == "left" else width - thickness, depth * 0.25, 0), thickness, depth * 0.5, bracket_height).Shape()
                fixture_shapes.append((f"frame_bracket_{side}", BRepAlgoAPI_Fuse(horizontal, vertical).Shape()))

        board_shape = None
        board_step_imported = False
        if board_step and board_step.is_file():
            reader = STEPControl_Reader()
            if reader.ReadFile(str(board_step)) == IFSelect_RetDone and reader.TransferRoots() > 0:
                imported = reader.OneShape()
                transform = gp_Trsf(); transform.SetTranslation(gp_Vec(wall + origin[0], wall + origin[1], origin[2]))
                board_shape = BRepBuilderAPI_Transform(imported, transform, True).Shape()
                board_step_imported = not board_shape.IsNull() and BRepCheck_Analyzer(board_shape).IsValid()
        if not board_step_imported:
            blocked = True
            failures.append(Failure(FailureCategory.TOOL_ERROR, "board_step_missing", "Native board STEP is required for assembly import and interference validation"))
            board_shape = BRepPrimAPI_MakeBox(gp_Pnt(wall + origin[0], wall + origin[1], origin[2]), board["width_mm"], board["height_mm"], board["thickness_mm"]).Shape()

        valid_solid = BRepCheck_Analyzer(base).IsValid() and BRepCheck_Analyzer(lid).IsValid() and all(BRepCheck_Analyzer(shape).IsValid() for _, shape in fixture_shapes)
        if not valid_solid:
            failures.append(Failure(FailureCategory.MECHANICAL_ERROR, "invalid_solid", "One or more OpenCASCADE solids are invalid"))

        wall_shapes = [
            BRepPrimAPI_MakeBox(gp_Pnt(0, 0, 0), wall, depth, body_height).Shape(),
            BRepPrimAPI_MakeBox(gp_Pnt(width - wall, 0, 0), wall, depth, body_height).Shape(),
            BRepPrimAPI_MakeBox(gp_Pnt(wall, 0, 0), width - 2 * wall, wall, body_height).Shape(),
            BRepPrimAPI_MakeBox(gp_Pnt(wall, depth - wall, 0), width - 2 * wall, wall, body_height).Shape(),
        ]
        board_envelope = BRepPrimAPI_MakeBox(
            gp_Pnt(wall + origin[0], wall + origin[1], origin[2]),
            board["width_mm"], board["height_mm"], board["thickness_mm"],
        ).Shape()
        board_wall_intersection = sum(self._intersection_volume(board_envelope, shape, BRepAlgoAPI_Common, BRepGProp, GProp_GProps) for shape in wall_shapes)

        component_lid_intersection = 0.0
        for component in board.get("component_height_map", []):
            half = 1.5
            component_shape = BRepPrimAPI_MakeBox(
                gp_Pnt(
                    wall + origin[0] + component["x_mm"] - half,
                    wall + origin[1] + component["y_mm"] - half,
                    origin[2] + board["thickness_mm"],
                ),
                2 * half,
                2 * half,
                component["height_mm"],
            ).Shape()
            component_lid_intersection += self._intersection_volume(component_shape, lid, BRepAlgoAPI_Common, BRepGProp, GProp_GProps)

        connector_wall_intersection = 0.0
        for cutout in contract["connector_cutouts"]:
            if cutout.get("enclosure_position_mm"):
                insertion_shape = self._cutout_shape(cutout, width, depth, wall, BRepPrimAPI_MakeBox, gp_Pnt)
                connector_wall_intersection += self._intersection_volume(insertion_shape, base, BRepAlgoAPI_Common, BRepGProp, GProp_GProps)

        geometry_interference_free = max(board_wall_intersection, component_lid_intersection, connector_wall_intersection) <= 1e-5
        assembly_interference_free = board_fit and component_clearance and cutout_alignment and mounting_alignment and geometry_interference_free
        if not assembly_interference_free:
            failures.append(Failure(
                FailureCategory.MECHANICAL_ERROR,
                "assembly_interference",
                "Board, component envelope, or connector insertion volume interferes with the enclosure",
                details={
                    "board_wall_intersection_mm3": board_wall_intersection,
                    "component_lid_intersection_mm3": component_lid_intersection,
                    "connector_wall_intersection_mm3": connector_wall_intersection,
                },
            ))

        target = release / "mechanical"
        variants_target = target / "variants"
        target.mkdir(parents=True, exist_ok=True)
        variants_target.mkdir(parents=True, exist_ok=True)
        artifacts: list[str] = []
        if board_step_imported and board_step:
            board_copy = target / "board.step"
            if board_step.resolve() != board_copy.resolve():
                shutil.copy2(board_step, board_copy)
            artifacts.append(str(board_copy))
        self._write_step(base, target / "enclosure.step", STEPControl_Writer, STEPControl_AsIs, IFSelect_RetDone)
        BRepMesh_IncrementalMesh(base, 0.12)
        StlAPI_Writer().Write(base, str(target / "enclosure.stl"))
        artifacts.extend([str(target / "enclosure.step"), str(target / "enclosure.stl")])
        for name, variant_lid in lids.items():
            variant_compound = TopoDS_Compound(); variant_builder = BRep_Builder(); variant_builder.MakeCompound(variant_compound); variant_builder.Add(variant_compound, base); variant_builder.Add(variant_compound, variant_lid)
            variant_step = variants_target / f"enclosure_{name}.step"
            self._write_step(variant_compound, variant_step, STEPControl_Writer, STEPControl_AsIs, IFSelect_RetDone)
            artifacts.append(str(variant_step))
        for name, shape in fixture_shapes:
            output = target / f"{name}.step"
            self._write_step(shape, output, STEPControl_Writer, STEPControl_AsIs, IFSelect_RetDone)
            artifacts.append(str(output))
        compound = TopoDS_Compound(); builder = BRep_Builder(); builder.MakeCompound(compound)
        for shape in [base, lid, board_shape, *(shape for _, shape in fixture_shapes)]:
            builder.Add(compound, shape)
        self._write_step(compound, target / "assembly.step", STEPControl_Writer, STEPControl_AsIs, IFSelect_RetDone)
        artifacts.append(str(target / "assembly.step"))

        stl_manifold = self._stl_is_manifold(target / "enclosure.stl")
        if not stl_manifold:
            failures.append(Failure(FailureCategory.MECHANICAL_ERROR, "non_manifold_stl", "STL triangle topology is not a closed two-manifold"))
        manifest_path = target / "mechanical_manifest.json"
        try:
            ocp_version = version("cadquery-ocp")
        except PackageNotFoundError:
            ocp_version = "unknown"
        provenance = {
            **contract.get("provenance", {}),
            "backend": "opencascade",
            "tool_versions": {"cadquery-ocp": ocp_version},
            "compiler_version": ocp_version,
            "command": ["python", "mechanical/source/assembly.py", "--board-step", "<board.step>", "--output", "<output>"],
            "timestamp": datetime.fromtimestamp(0, UTC).isoformat(),
            "release_eligible": release_eligible,
        }
        write_json(manifest_path, {
            "selected_variant": selected["name"],
            "board_step_imported": board_step_imported,
            "candidate_only": not release_eligible,
            "release_eligible": release_eligible,
            "provenance": provenance,
            "artifacts": [{"path": Path(path).relative_to(target).as_posix(), "sha256": sha256(Path(path))} for path in artifacts],
        })
        artifacts.append(str(manifest_path))

        status = Status.FAIL if any(failure.category == FailureCategory.MECHANICAL_ERROR for failure in failures) else (Status.BLOCKED if blocked else Status.PASS)
        return GateReport(
            "mechanical_export",
            status,
            failures,
            metrics={
                "valid_solid": valid_solid,
                "stl_manifold": stl_manifold,
                "board_fit": board_fit,
                "component_height_clearance": component_clearance,
                "connector_cutout_alignment": cutout_alignment,
                "mounting_hole_alignment": mounting_alignment,
                "assembly_interference_free": assembly_interference_free,
                "board_wall_intersection_mm3": board_wall_intersection,
                "component_lid_intersection_mm3": component_lid_intersection,
                "connector_wall_intersection_mm3": connector_wall_intersection,
                "board_step_imported": board_step_imported,
                "variant_count": len(variants),
                "fixture_count": len(fixture_shapes),
                "tolerance_mm": tolerance,
                "insertion_clearance_mm": insertion,
                "top_clearance_mm": top_gap,
                "bottom_clearance_mm": bottom_gap,
            },
            artifacts=artifacts,
            backend={"name": "OpenCASCADE", "deterministic_geometry": True},
        )

    @staticmethod
    def _edge_distance(side: str, position: list[float], width: float, height: float) -> float:
        return {"front": position[1], "rear": height - position[1], "left": position[0], "right": width - position[0]}[side]

    @staticmethod
    def _cutout_shape(cutout, width, depth, wall, make_box, point):
        along, height = map(float, cutout["opening_mm"])
        center_z = float(cutout["center_z_mm"]) + wall
        x, y = cutout["enclosure_position_mm"]
        x += wall; y += wall
        if cutout["side"] == "front":
            return make_box(point(x - along / 2, -1, center_z - height / 2), along, wall + 2, height).Shape()
        if cutout["side"] == "rear":
            return make_box(point(x - along / 2, depth - wall - 1, center_z - height / 2), along, wall + 2, height).Shape()
        if cutout["side"] == "left":
            return make_box(point(-1, y - along / 2, center_z - height / 2), wall + 2, along, height).Shape()
        return make_box(point(width - wall - 1, y - along / 2, center_z - height / 2), wall + 2, along, height).Shape()

    @staticmethod
    def _write_step(shape, path: Path, writer_type, mode, success) -> None:
        writer = writer_type()
        if writer.Transfer(shape, mode) != success or writer.Write(str(path)) != success:
            raise RuntimeError(f"Failed to export STEP: {path}")

    @staticmethod
    def _intersection_volume(first, second, common_type, brep_gprop, props_type) -> float:
        common = common_type(first, second).Shape()
        if common.IsNull():
            return 0.0
        props = props_type()
        brep_gprop.VolumeProperties_s(common, props)
        return abs(float(props.Mass()))

    @staticmethod
    def _stl_is_manifold(path: Path) -> bool:
        if not path.is_file() or path.stat().st_size < 84:
            return False
        data = path.read_bytes()
        triangles: list[tuple[tuple[float, float, float], ...]] = []
        count = struct.unpack_from("<I", data, 80)[0]
        if 84 + count * 50 == len(data):
            for index in range(count):
                values = struct.unpack_from("<12fH", data, 84 + index * 50)
                triangles.append((values[3:6], values[6:9], values[9:12]))
        else:
            vertices = []
            for line in data.decode("ascii", errors="ignore").splitlines():
                if line.strip().startswith("vertex "):
                    vertices.append(tuple(map(float, line.split()[1:4])))
            triangles = [tuple(vertices[index:index + 3]) for index in range(0, len(vertices), 3) if len(vertices[index:index + 3]) == 3]
        edges = Counter()
        for triangle in triangles:
            points = [tuple(round(value, 5) for value in point) for point in triangle]
            for a, b in ((points[0], points[1]), (points[1], points[2]), (points[2], points[0])):
                edges[tuple(sorted((a, b)))] += 1
        return bool(triangles) and all(uses == 2 for uses in edges.values())
