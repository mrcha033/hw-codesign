from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .io import read_yaml, write_yaml
from .models import Failure, FailureCategory

PROJECT_PARTS_FILE = "parts.local.yaml"


def load_project_parts(project: Path, schema_root: Path) -> tuple[dict[str, Any], list[Failure]]:
    path = project / PROJECT_PARTS_FILE
    if not path.is_file():
        return {"version": 1, "roles": {}, "components": []}, []
    try:
        payload = read_yaml(path)
    except (OSError, ValueError) as exc:
        return {}, [Failure(FailureCategory.BOM_ERROR, "invalid_project_parts", str(exc), path=str(path))]
    schema_path = schema_root / "project_parts.schema.json"
    if not schema_path.is_file():
        return {}, [Failure(FailureCategory.BOM_ERROR, "project_parts_schema_missing", "Project parts schema is missing", path=str(schema_path))]
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    failures = [
        Failure(
            FailureCategory.BOM_ERROR,
            "invalid_project_parts",
            error.message,
            path=f"{path}:{'.'.join(str(item) for item in error.absolute_path)}",
        )
        for error in Draft202012Validator(schema).iter_errors(payload)
    ]
    ids = [str(item.get("id")) for item in payload.get("components", []) if item.get("id")]
    duplicate_ids = sorted({item for item in ids if ids.count(item) > 1})
    for component_id in duplicate_ids:
        failures.append(Failure(FailureCategory.BOM_ERROR, "ambiguous_project_component_id", f"Duplicate project component id {component_id}", path=str(path)))
    known = set(ids)
    for role, selection in payload.get("roles", {}).items():
        if selection.get("component_id") not in known:
            failures.append(Failure(FailureCategory.BOM_ERROR, "project_role_component_missing", f"Project role {role} selects unknown component {selection.get('component_id')}", path=str(path)))
    return payload, failures


def register_project_part(project: Path, schema_root: Path, registration: dict[str, Any]) -> dict[str, Any]:
    current, failures = load_project_parts(project, schema_root)
    if failures:
        raise ValueError("Existing parts.local.yaml is invalid: " + "; ".join(item.message for item in failures))
    role = registration.get("role")
    component_id = registration.get("id")
    if not role or not component_id:
        raise ValueError("Project part registration requires id and role")
    components = [item for item in current.get("components", []) if item.get("id") != component_id]
    components.append(registration)
    current["components"] = sorted(components, key=lambda item: str(item.get("id", "")))
    current.setdefault("roles", {})[str(role)] = {
        "component_id": str(component_id),
        "resolution": "project_owned",
        "rationale": str(registration.get("rationale") or "Registered by project owner"),
    }
    schema = json.loads((schema_root / "project_parts.schema.json").read_text(encoding="utf-8"))
    validation_errors = list(Draft202012Validator(schema).iter_errors(current))
    if validation_errors:
        raise ValueError("Invalid project part registration: " + "; ".join(error.message for error in validation_errors))
    destination = project / PROJECT_PARTS_FILE
    write_yaml(destination, current)
    return {"status": "generated", "project_part": component_id, "role": role, "file": str(destination)}
