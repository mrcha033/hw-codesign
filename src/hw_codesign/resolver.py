from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from .models import Failure, FailureCategory, GateReport, ResolvedComponent, Status


ROLE_BY_CATEGORY = {
    "power_input": "power_input", "fuse": "fuse", "reverse_polarity": "reverse_polarity",
    "tvs": "tvs", "efuse": "efuse", "mcu": "mcu", "imu": "imu", "can": "can",
    "estop": "estop", "safety_gate": "safety_gate", "can_connector": "can_connector",
    "debug": "debug", "usb": "usb", "usb_esd": "usb_esd", "motor_io": "motor_io",
}


def role_for_component(component: dict[str, Any]) -> str:
    category = component["category"]
    if category == "regulator":
        return "regulator_5v" if component["ref"] == "U4" else "regulator_3v3"
    if category == "termination": return "resistor_120r"
    if category == "discharge": return "resistor_100k"
    if category == "pullup": return "resistor_4k7"
    if category == "decoupling": return "capacitor_100n"
    if category == "bulk_cap": return "capacitor_22u" if component["ref"] == "C9" else "capacitor_10u_50v"
    return ROLE_BY_CATEGORY.get(category, category)


class ComponentResolver:
    def __init__(self, parts_root: Path | str):
        self.parts_root = Path(parts_root)

    def resolve(self, spec: dict[str, Any], role_set: str, components: list[dict[str, Any]]) -> tuple[list[ResolvedComponent], GateReport]:
        role_path = self.parts_root / "role_sets" / f"{role_set}.yaml"
        component_dir = self.parts_root / "components"
        if not role_path.is_file() or not component_dir.is_dir():
            return [], GateReport("component_resolution", Status.BLOCKED, [Failure(FailureCategory.BOM_ERROR, "parts_db_missing", "Curated parts database or role set is missing")])
        role_data = yaml.safe_load(role_path.read_text(encoding="utf-8")) or {}
        role_schema_path = self.parts_root / "schemas" / "role_set.schema.json"
        component_schema_path = self.parts_root / "schemas" / "component.schema.json"
        if not role_schema_path.is_file() or not component_schema_path.is_file():
            return [], GateReport("component_resolution", Status.BLOCKED, [Failure(FailureCategory.BOM_ERROR, "parts_schema_missing", "Parts database schemas are missing")])
        import json
        role_errors = list(Draft202012Validator(json.loads(role_schema_path.read_text(encoding="utf-8"))).iter_errors(role_data))
        if role_errors:
            return [], GateReport("component_resolution", Status.FAIL, [Failure(FailureCategory.BOM_ERROR, "invalid_role_set", error.message) for error in role_errors])
        database: dict[str, dict[str, Any]] = {}
        schema = json.loads(component_schema_path.read_text(encoding="utf-8"))
        database_failures: list[Failure] = []
        for path in sorted(component_dir.glob("*.yaml")):
            payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            database_failures.extend(Failure(FailureCategory.BOM_ERROR, "invalid_component_db", error.message, path=str(path)) for error in Draft202012Validator(schema).iter_errors(payload))
            for item in payload.get("components", [payload] if payload.get("id") else []):
                database[item["id"]] = {**item, "_database_file": str(path)}
        if database_failures:
            return [], GateReport("component_resolution", Status.FAIL, database_failures)
        failures: list[Failure] = []
        resolved: list[ResolvedComponent] = []
        critical = set(role_data.get("critical_roles", []))
        for instance in components:
            role = role_for_component(instance)
            selection = role_data.get("roles", {}).get(role)
            if not selection:
                failures.append(Failure(FailureCategory.BOM_ERROR, "role_unresolved", f"No component selection for role {role}", path=instance["ref"]))
                continue
            resolution = selection.get("resolution", "unresolved")
            stored_part = database.get(selection.get("component_id"))
            part = dict(stored_part) if stored_part else None
            if not part:
                failures.append(Failure(FailureCategory.BOM_ERROR, "component_missing", f"Selected component {selection.get('component_id')} is absent from curated DB", path=instance["ref"]))
                continue
            if role in critical and resolution != "curated":
                failures.append(Failure(FailureCategory.BOM_ERROR, "critical_role_not_curated", f"Critical role {role} must resolve to curated data", path=instance["ref"]))
            if resolution == "registry_candidate":
                failures.append(Failure(FailureCategory.BOM_ERROR, "registry_candidate_not_release_eligible", f"Registry candidate for {role} requires curation", path=instance["ref"]))
            provenance = {"role_set": str(role_path), "database_file": part.pop("_database_file", None), "resolver": "in_repo_curated_v1"}
            resolved.append(ResolvedComponent(instance["ref"], role, part["id"], resolution, part, provenance))
        status = Status.FAIL if failures else Status.PASS
        return resolved, GateReport("component_resolution", status, failures, metrics={"resolved": len(resolved), "requested": len(components), "critical_roles": len(critical)}, artifacts=[str(role_path)], backend={"name": "ComponentResolver", "mutates_database": False})

    @staticmethod
    def serialize(items: list[ResolvedComponent]) -> list[dict[str, Any]]:
        return [asdict(item) for item in items]
