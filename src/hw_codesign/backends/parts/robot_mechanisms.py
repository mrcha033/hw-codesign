"""Robot mechanism primitives with fastening and kinematic contract checks."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ._base import fastener_clearance, import_ocp, printability_report, write_step, write_stl


def _schema(required: list[str], properties: dict[str, Any]) -> dict[str, Any]:
    return {"type": "object", "required": required, "additionalProperties": True, "properties": properties}


SERVO_HORN_SCHEMA = _schema(["arm_length_mm"], {
    "arm_length_mm": {"type": "number", "minimum": 8},
    "hub_diameter_mm": {"type": "number", "minimum": 5, "default": 12},
    "thickness_mm": {"type": "number", "minimum": 1.6, "default": 3},
    "shaft_bore_mm": {"type": "number", "minimum": 2, "default": 5.8},
    "link_fastener": {"type": "string", "enum": ["M2", "M2.5", "M3"], "default": "M2"},
    "link_hole_radius_mm": {"type": "number", "minimum": 4, "default": 10},
})

U_BRACKET_SCHEMA = _schema(["servo_width_mm", "servo_height_mm"], {
    "servo_width_mm": {"type": "number", "minimum": 8},
    "servo_height_mm": {"type": "number", "minimum": 8},
    "servo_depth_mm": {"type": "number", "minimum": 8, "default": 24},
    "wall_mm": {"type": "number", "minimum": 1.6, "default": 3},
    "joint_clearance_mm": {"type": "number", "minimum": 0.2, "default": 0.5},
    "pivot_fastener": {"type": "string", "enum": ["M2", "M2.5", "M3", "M4"], "default": "M3"},
    "motion_range_deg": {"type": "array", "minItems": 2, "maxItems": 2, "items": {"type": "number"}, "default": [-90, 90]},
})

L_BRACKET_SCHEMA = _schema(["leg_a_mm", "leg_b_mm", "width_mm"], {
    "leg_a_mm": {"type": "number", "minimum": 8},
    "leg_b_mm": {"type": "number", "minimum": 8},
    "width_mm": {"type": "number", "minimum": 8},
    "thickness_mm": {"type": "number", "minimum": 1.6, "default": 3},
    "fastener": {"type": "string", "enum": ["M2", "M2.5", "M3", "M4"], "default": "M3"},
})

LINK_SCHEMA = _schema(["length_mm", "width_mm"], {
    "length_mm": {"type": "number", "minimum": 15},
    "width_mm": {"type": "number", "minimum": 6},
    "thickness_mm": {"type": "number", "minimum": 1.6, "default": 4},
    "end_fastener": {"type": "string", "enum": ["M2", "M2.5", "M3", "M4"], "default": "M3"},
    "end_margin_mm": {"type": "number", "minimum": 3, "default": 6},
})

REVOLUTE_JOINT_SCHEMA = _schema(["inner_width_mm", "ear_height_mm"], {
    "inner_width_mm": {"type": "number", "minimum": 6},
    "ear_height_mm": {"type": "number", "minimum": 8},
    "ear_depth_mm": {"type": "number", "minimum": 8, "default": 14},
    "wall_mm": {"type": "number", "minimum": 1.6, "default": 3},
    "joint_clearance_mm": {"type": "number", "minimum": 0.2, "default": 0.5},
    "pivot_fastener": {"type": "string", "enum": ["M2", "M2.5", "M3", "M4"], "default": "M3"},
    "motion_range_deg": {"type": "array", "minItems": 2, "maxItems": 2, "items": {"type": "number"}, "default": [-90, 90]},
})

ROBOT_FOOT_SCHEMA = _schema(["length_mm", "width_mm"], {
    "length_mm": {"type": "number", "minimum": 25},
    "width_mm": {"type": "number", "minimum": 15},
    "thickness_mm": {"type": "number", "minimum": 2, "default": 5},
    "ankle_fastener": {"type": "string", "enum": ["M2", "M2.5", "M3", "M4"], "default": "M3"},
    "ankle_hole_spacing_mm": {"type": "number", "minimum": 5, "default": 12},
    "toe_clearance_deg": {"type": "number", "minimum": 0, "maximum": 45, "default": 12},
})


def _motion_failures(intent: dict[str, Any]) -> tuple[list[dict[str, Any]], list[float]]:
    motion = [float(value) for value in intent.get("motion_range_deg", [-90, 90])]
    failures: list[dict[str, Any]] = []
    if len(motion) != 2 or motion[0] >= motion[1]:
        failures.append({"code": "invalid_motion_range", "message": "motion_range_deg must be [minimum, maximum] with minimum < maximum", "severity": "error"})
    elif motion[1] - motion[0] > 270:
        failures.append({"code": "motion_range_exceeds_open_joint", "message": "Requested rotation exceeds the 270 degree analytical open-joint envelope", "severity": "error"})
    return failures, motion


def _finish(
    *,
    ocp: dict,
    body: Any,
    output_dir: Path,
    part_name: str,
    part_type: str,
    intent: dict[str, Any],
    wall_mm: float,
    holes: list[dict[str, Any]],
    failures: list[dict[str, Any]],
    metrics: dict[str, Any],
    orientation: str,
) -> dict[str, Any]:
    valid = ocp["BRepCheck_Analyzer"](body).IsValid()
    if not valid:
        failures.append({"code": "invalid_solid", "message": "OpenCASCADE produced an invalid solid", "severity": "error"})
    step_path = output_dir / f"{part_name}.step"
    stl_path = output_dir / f"{part_name}.stl"
    write_step(body, step_path, ocp)
    write_stl(body, stl_path, ocp)
    printability = printability_report(stl_path, wall_mm, holes or [{"diameter_mm": 99}], float(intent.get("max_overhang_angle_deg", 45)), orientation)
    for violation in printability["violations"]:
        failures.append({"code": "printability_violation", "message": violation, "severity": "error"})
    fastening_ok = all(float(hole.get("diameter_mm", 0)) >= 2.2 for hole in holes)
    if holes and not fastening_ok:
        failures.append({"code": "fastener_clearance_invalid", "message": "One or more fastening holes are below the supported clearance envelope", "severity": "error"})
    status = "pass" if valid and printability["printable"] and not failures else "fail"
    return {
        "status": "generated" if status == "pass" else "fail",
        "part_name": part_name,
        "part_type": part_type,
        "artifacts": [str(step_path), str(stl_path)],
        "printability": printability,
        "kinematic_contract": metrics.get("kinematic_contract"),
        "fastening_contract": {"verified": fastening_ok, "holes": holes},
        "interference_envelope": metrics.get("interference_envelope"),
        "gate_report": {
            "gate": "part_design",
            "status": status,
            "failures": failures,
            "metrics": {"valid_solid": valid, "fastening_verified": fastening_ok, **metrics},
            "artifacts": [str(step_path), str(stl_path)],
            "backend": {"name": "OpenCASCADE", "part_type": part_type, "contract": "robot_mechanism_v1"},
        },
        "candidate_only": True,
        "release_eligible": False,
    }


class _RobotPart:
    part_type = "robot_part"

    def design(self, intent: dict[str, Any], output_dir: Path, part_name: str) -> dict[str, Any]:
        try:
            ocp = import_ocp()
        except ImportError:
            return {"status": "blocked", "code": "tool_unavailable", "message": "cadquery-ocp is not installed", "part_name": part_name, "part_type": self.part_type}
        body, wall, holes, failures, metrics, orientation = self.build(ocp, intent)
        return _finish(ocp=ocp, body=body, output_dir=output_dir, part_name=part_name, part_type=self.part_type, intent=intent, wall_mm=wall, holes=holes, failures=failures, metrics=metrics, orientation=orientation)

    def build(self, ocp: dict, intent: dict[str, Any]) -> tuple[Any, float, list[dict[str, Any]], list[dict[str, Any]], dict[str, Any], str]:
        raise NotImplementedError


class ServoHorn(_RobotPart):
    part_type = "servo_horn"

    def build(self, o, i):
        arm, hub, t = float(i.get("arm_length_mm", 20)), float(i.get("hub_diameter_mm", 12)), float(i.get("thickness_mm", 3))
        bore, fastener, hole_r = float(i.get("shaft_bore_mm", 5.8)), i.get("link_fastener", "M2"), float(i.get("link_hole_radius_mm", 10))
        MakeBox, MakeCyl, Fuse, Cut = o["BRepPrimAPI_MakeBox"], o["BRepPrimAPI_MakeCylinder"], o["BRepAlgoAPI_Fuse"], o["BRepAlgoAPI_Cut"]
        P, Ax, D = o["gp_Pnt"], o["gp_Ax2"], o["gp_Dir"]
        body = Fuse(MakeCyl(Ax(P(0, 0, 0), D(0, 0, 1)), hub / 2, t).Shape(), MakeBox(P(0, -hub / 4, 0), arm, hub / 2, t).Shape()).Shape()
        body = Cut(body, MakeCyl(Ax(P(0, 0, -1), D(0, 0, 1)), bore / 2, t + 2).Shape()).Shape()
        link_d = fastener_clearance(fastener)
        body = Cut(body, MakeCyl(Ax(P(hole_r, 0, -1), D(0, 0, 1)), link_d / 2, t + 2).Shape()).Shape()
        failures = [] if 0 < hole_r < arm - link_d / 2 else [{"code": "link_hole_outside_horn", "message": "Link hole must remain inside the horn arm", "severity": "error"}]
        return body, t, [{"diameter_mm": bore}, {"diameter_mm": link_d}], failures, {"interference_envelope": {"x_mm": arm + hub / 2, "y_mm": hub, "z_mm": t}}, "largest face flat on bed"


class UBracket(_RobotPart):
    part_type = "servo_u_bracket"

    def build(self, o, i):
        sw, sh, depth = float(i["servo_width_mm"]), float(i["servo_height_mm"]), float(i.get("servo_depth_mm", 24))
        wall, clearance = float(i.get("wall_mm", 3)), float(i.get("joint_clearance_mm", 0.5))
        fastener = i.get("pivot_fastener", "M3"); hole_d = fastener_clearance(fastener)
        failures, motion = _motion_failures(i)
        if clearance < 0.3: failures.append({"code": "joint_clearance_too_small", "message": "At least 0.3 mm per-side joint clearance is required", "severity": "error"})
        inner = sw + 2 * clearance; total = inner + 2 * wall
        B, C, F, Cut, P, Ax, D = o["BRepPrimAPI_MakeBox"], o["BRepPrimAPI_MakeCylinder"], o["BRepAlgoAPI_Fuse"], o["BRepAlgoAPI_Cut"], o["gp_Pnt"], o["gp_Ax2"], o["gp_Dir"]
        body = F(B(P(0, 0, 0), total, depth, wall).Shape(), B(P(0, 0, wall), wall, depth, sh).Shape()).Shape()
        body = F(body, B(P(total - wall, 0, wall), wall, depth, sh).Shape()).Shape()
        for x in (wall / 2, total - wall / 2):
            body = Cut(body, C(Ax(P(x, -1, wall + sh * 0.65), D(0, 1, 0)), hole_d / 2, depth + 2).Shape()).Shape()
        metrics = {"kinematic_contract": {"axis": "Y", "motion_range_deg": motion, "joint_clearance_mm": clearance, "analytical_interference_free": not failures}, "interference_envelope": {"x_mm": total, "y_mm": depth, "z_mm": sh + wall}}
        return body, wall, [{"diameter_mm": hole_d}, {"diameter_mm": hole_d}], failures, metrics, "base flat on bed"


class LBracket(_RobotPart):
    part_type = "servo_l_bracket"

    def build(self, o, i):
        a, b, width, t = float(i["leg_a_mm"]), float(i["leg_b_mm"]), float(i["width_mm"]), float(i.get("thickness_mm", 3))
        hole_d = fastener_clearance(i.get("fastener", "M3")); B, C, F, Cut, P, Ax, D = o["BRepPrimAPI_MakeBox"], o["BRepPrimAPI_MakeCylinder"], o["BRepAlgoAPI_Fuse"], o["BRepAlgoAPI_Cut"], o["gp_Pnt"], o["gp_Ax2"], o["gp_Dir"]
        body = F(B(P(0, 0, 0), width, a, t).Shape(), B(P(0, 0, 0), width, t, b).Shape()).Shape()
        body = Cut(body, C(Ax(P(width / 2, a / 2, -1), D(0, 0, 1)), hole_d / 2, t + 2).Shape()).Shape()
        body = Cut(body, C(Ax(P(width / 2, -1, b / 2), D(0, 1, 0)), hole_d / 2, t + 2).Shape()).Shape()
        return body, t, [{"diameter_mm": hole_d}] * 2, [], {"interference_envelope": {"x_mm": width, "y_mm": a, "z_mm": b}}, "outside corner down with supports as required"


class RobotLink(_RobotPart):
    part_type = "robot_link"

    def build(self, o, i):
        length, width, t, margin = float(i["length_mm"]), float(i["width_mm"]), float(i.get("thickness_mm", 4)), float(i.get("end_margin_mm", 6))
        hole_d = fastener_clearance(i.get("end_fastener", "M3")); B, C, Cut, P, Ax, D = o["BRepPrimAPI_MakeBox"], o["BRepPrimAPI_MakeCylinder"], o["BRepAlgoAPI_Cut"], o["gp_Pnt"], o["gp_Ax2"], o["gp_Dir"]
        body = B(P(0, 0, 0), length, width, t).Shape(); failures = []
        if margin < hole_d / 2 + 1 or length <= 2 * margin:
            failures.append({"code": "link_fastener_edge_margin", "message": "Link holes need at least 1 mm material beyond fastener clearance", "severity": "error"})
        for x in (margin, length - margin):
            body = Cut(body, C(Ax(P(x, width / 2, -1), D(0, 0, 1)), hole_d / 2, t + 2).Shape()).Shape()
        return body, t, [{"diameter_mm": hole_d}] * 2, failures, {"kinematic_contract": {"joint_centers_mm": [margin, length - margin], "center_distance_mm": length - 2 * margin}, "interference_envelope": {"x_mm": length, "y_mm": width, "z_mm": t}}, "largest face flat on bed"


class RevoluteJoint(UBracket):
    part_type = "revolute_joint"

    def build(self, o, i):
        mapped = {**i, "servo_width_mm": i["inner_width_mm"], "servo_height_mm": i["ear_height_mm"], "servo_depth_mm": i.get("ear_depth_mm", 14)}
        return super().build(o, mapped)


class RobotFoot(_RobotPart):
    part_type = "robot_foot"

    def build(self, o, i):
        length, width, t = float(i["length_mm"]), float(i["width_mm"]), float(i.get("thickness_mm", 5))
        spacing = float(i.get("ankle_hole_spacing_mm", 12)); hole_d = fastener_clearance(i.get("ankle_fastener", "M3"))
        B, C, Cut, P, Ax, D = o["BRepPrimAPI_MakeBox"], o["BRepPrimAPI_MakeCylinder"], o["BRepAlgoAPI_Cut"], o["gp_Pnt"], o["gp_Ax2"], o["gp_Dir"]
        body = B(P(0, 0, 0), length, width, t).Shape(); failures = []
        if spacing + hole_d + 4 > width:
            failures.append({"code": "ankle_holes_exceed_foot_width", "message": "Ankle hole spacing leaves insufficient edge material", "severity": "error"})
        for y in ((width - spacing) / 2, (width + spacing) / 2):
            body = Cut(body, C(Ax(P(length * 0.45, y, -1), D(0, 0, 1)), hole_d / 2, t + 2).Shape()).Shape()
        metrics = {"kinematic_contract": {"toe_clearance_deg": float(i.get("toe_clearance_deg", 12)), "ankle_axis": "Y"}, "interference_envelope": {"x_mm": length, "y_mm": width, "z_mm": t}}
        return body, t, [{"diameter_mm": hole_d}] * 2, failures, metrics, "sole flat on bed"
