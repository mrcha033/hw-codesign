from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ._schemas import SHARED_SCHEMAS, ref  # noqa: F401 — ref imported for callers


@dataclass(frozen=True)
class ToolDef:
    name: str
    description: str
    input_schema: dict[str, Any]
    output_schema: dict[str, Any]
    # "local" = never routed to cloud; "async" = cloud-preferred; "both" = either
    execution_mode: str = "both"

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
            "output_schema": self.output_schema,
            "execution_mode": self.execution_mode,
        }


def _project_only(extra: dict[str, Any] | None = None) -> dict[str, Any]:
    props: dict[str, Any] = {"project": {"type": "string", "description": "Project name"}}
    if extra:
        props.update(extra)
    return {
        "type": "object",
        "properties": props,
        "required": ["project"],
        "additionalProperties": False,
    }


# ---------------------------------------------------------------------------
# Per-tool inline output schemas (used when a tool has a distinct shape not
# captured by any shared schema)
# ---------------------------------------------------------------------------

_CREATE_PROJECT_OUTPUT: dict[str, Any] = {
    "type": "object",
    "required": ["status", "project_path", "template"],
    "additionalProperties": True,
    "properties": {
        "status":       {"type": "string"},
        "project_path": {"type": "string"},
        "template":     {"type": "string"},
        "target":       {"type": "string"},
    },
}

_OPEN_PROJECT_OUTPUT: dict[str, Any] = {
    "type": "object",
    "required": ["status", "project", "project_path", "spec"],
    "additionalProperties": True,
    "properties": {
        "status":       {"type": "string"},
        "project":      {"type": "string"},
        "project_path": {"type": "string"},
        "spec":         {"type": "object", "additionalProperties": True,
                         "description": "Full merged project spec (opaque; structure is spec-version dependent)"},
    },
}

_SNAPSHOT_OUTPUT: dict[str, Any] = {
    "type": "object",
    "required": ["project", "iteration_id", "status"],
    "additionalProperties": False,
    "properties": {
        "project":      {"type": "string"},
        "iteration_id": {"type": "string"},
        "status":       {"type": "string"},
    },
}

_COMPARE_ITERATIONS_OUTPUT: dict[str, Any] = {
    "type": "object",
    "required": ["status", "project", "before", "after", "added", "removed", "changed"],
    "additionalProperties": False,
    "properties": {
        "status":  {"type": "string"},
        "project": {"type": "string"},
        "before":  {"type": "string"},
        "after":   {"type": "string"},
        "added":   {"type": "array", "items": {"type": "string"}},
        "removed": {"type": "array", "items": {"type": "string"}},
        "changed": {"type": "array", "items": {"type": "string"}},
    },
}

_READ_SPEC_OUTPUT: dict[str, Any] = {
    "type": "object",
    "required": ["status", "spec"],
    "additionalProperties": False,
    "properties": {
        "status": {"type": "string"},
        "spec":   {"type": "object", "additionalProperties": True,
                   "description": "Full merged project spec"},
    },
}

_UPDATE_SPEC_OUTPUT: dict[str, Any] = {
    "type": "object",
    "required": ["status", "changed_files", "user_approved"],
    "additionalProperties": False,
    "properties": {
        "status":        {"type": "string"},
        "changed_files": {"type": "array", "items": {"type": "string"}},
        "user_approved": {"type": "boolean"},
    },
}

_RESOLVE_ASSUMPTION_OUTPUT: dict[str, Any] = {
    "oneOf": [
        {
            "type": "object",
            "required": ["status", "assumption", "resolution"],
            "additionalProperties": False,
            "properties": {
                "status":     {"type": "string", "const": "pass"},
                "assumption": {"type": "string"},
                "resolution": {},
            },
        },
        {
            "type": "object",
            "required": ["status", "assumption", "message"],
            "additionalProperties": False,
            "properties": {
                "status":     {"type": "string", "const": "blocked"},
                "assumption": {"type": "string"},
                "message":    {"type": "string"},
            },
        },
    ],
}

_GENERATE_MECHANICAL_OUTPUT: dict[str, Any] = {
    "type": "object",
    "required": ["status", "backend", "files"],
    "additionalProperties": True,
    "properties": {
        "status":  {"type": "string"},
        "backend": {"type": "string"},
        "files":   {"type": "array", "items": {"type": "string"}},
    },
}

_GENERATE_FIRMWARE_OUTPUT: dict[str, Any] = {
    "type": "object",
    "required": ["status", "files"],
    "additionalProperties": True,
    "properties": {
        "status":    {"type": "string"},
        "framework": {"type": "string"},
        "files":     {"type": "array", "items": {"type": "string"}},
        "code":      {"type": "string", "description": "Error/block code when status is not generated"},
    },
}

_EXTRACT_GRAPH_OUTPUT: dict[str, Any] = {
    "type": "object",
    "required": ["status", "graph"],
    "additionalProperties": False,
    "properties": {
        "status": {"type": "string", "enum": ["generated", "blocked"]},
        "graph":  {"type": ["object", "null"], "additionalProperties": True},
    },
}

_DESIGN_REPORT_OUTPUT: dict[str, Any] = {
    "type": "object",
    "required": ["status", "file"],
    "additionalProperties": False,
    "properties": {
        "status": {"type": "string"},
        "file":   {"type": "string", "description": "Absolute path to the generated Markdown report"},
    },
}


# ---------------------------------------------------------------------------
# Tool registry
# ---------------------------------------------------------------------------

TOOL_REGISTRY: dict[str, ToolDef] = {

    # -------------------------------------------------------------------
    # Project management
    # -------------------------------------------------------------------
    "hw_create_project": ToolDef(
        name="hw_create_project",
        description="Create a new hardware project from a template and set its top-level target.",
        input_schema={
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Unique project name"},
                "template": {
                    "type": "string",
                    "description": "Starter template name",
                    "default": "robotics_controller_full",
                },
                "target": {
                    "type": "string",
                    "description": "High-level design target",
                    "default": "manufacturable_pcb_with_enclosure_and_firmware",
                },
            },
            "required": ["name"],
            "additionalProperties": False,
        },
        output_schema=_CREATE_PROJECT_OUTPUT,
    ),

    "hw_open_project": ToolDef(
        name="hw_open_project",
        description="Open an existing project and return its current spec.",
        input_schema=_project_only(),
        output_schema=_OPEN_PROJECT_OUTPUT,
    ),

    "hw_snapshot_project": ToolDef(
        name="hw_snapshot_project",
        description="Snapshot the current project state into iteration history and return the new iteration ID.",
        input_schema=_project_only(),
        output_schema=_SNAPSHOT_OUTPUT,
    ),

    "hw_compare_iterations": ToolDef(
        name="hw_compare_iterations",
        description="Diff two named iteration snapshots and return added/removed/changed file lists.",
        input_schema={
            "type": "object",
            "properties": {
                "project": {"type": "string"},
                "before":  {"type": "string", "description": "Iteration ID of the earlier snapshot"},
                "after":   {"type": "string", "description": "Iteration ID of the later snapshot"},
            },
            "required": ["project", "before", "after"],
            "additionalProperties": False,
        },
        output_schema=_COMPARE_ITERATIONS_OUTPUT,
    ),

    # -------------------------------------------------------------------
    # Spec read/write
    # -------------------------------------------------------------------
    "hw_read_spec": ToolDef(
        name="hw_read_spec",
        description="Return the full merged spec for a project.",
        input_schema=_project_only(),
        output_schema=_READ_SPEC_OUTPUT,
    ),

    "hw_validate_spec": ToolDef(
        name="hw_validate_spec",
        description="Validate the project spec against all platform JSON schemas and return errors.",
        input_schema=_project_only(),
        output_schema=ref("gate_report"),
    ),

    "hw_update_spec": ToolDef(
        name="hw_update_spec",
        description="Overwrite a top-level spec section. Requires user_approved=true for safety or manufacturing limits.",
        input_schema={
            "type": "object",
            "properties": {
                "project":       {"type": "string"},
                "section":       {"type": "string", "description": "Top-level spec key to update"},
                "value":         {"type": "object", "description": "New section content"},
                "user_approved": {"type": "boolean", "default": False},
            },
            "required": ["project", "section", "value"],
            "additionalProperties": False,
        },
        output_schema=_UPDATE_SPEC_OUTPUT,
    ),

    "hw_update_requirements": ToolDef(
        name="hw_update_requirements",
        description="Deterministically lower natural-language requirements text into the typed spec.",
        input_schema={
            "type": "object",
            "properties": {
                "project":           {"type": "string"},
                "requirements_text": {"type": "string", "description": "Free-form requirements paragraph"},
            },
            "required": ["project", "requirements_text"],
            "additionalProperties": False,
        },
        output_schema=ref("opaque_result"),
    ),

    "hw_list_assumptions": ToolDef(
        name="hw_list_assumptions",
        description="List all documented design assumptions from the project spec.",
        input_schema=_project_only(),
        output_schema=ref("opaque_result"),
    ),

    "hw_resolve_assumption": ToolDef(
        name="hw_resolve_assumption",
        description="Record a resolution decision for a named assumption. Requires approved=true.",
        input_schema={
            "type": "object",
            "properties": {
                "project":    {"type": "string"},
                "name":       {"type": "string", "description": "Assumption key"},
                "resolution": {"type": "string", "description": "Resolution text"},
                "approved":   {"type": "boolean", "default": False},
            },
            "required": ["project", "name", "resolution"],
            "additionalProperties": False,
        },
        output_schema=_RESOLVE_ASSUMPTION_OUTPUT,
    ),

    # -------------------------------------------------------------------
    # Generation
    # -------------------------------------------------------------------
    "hw_generate_all": ToolDef(
        name="hw_generate_all",
        description="Run all source generators (reference intent, electronics, mechanical, firmware) in one step.",
        input_schema=_project_only(),
        output_schema=ref("generate_all_result"),
        execution_mode="async",
    ),

    "hw_generate_reference_intent": ToolDef(
        name="hw_generate_reference_intent",
        description="Generate the reference design intent document from the project spec.",
        input_schema=_project_only(),
        output_schema=ref("electronics_source_result"),
    ),

    "hw_generate_electronics_source": ToolDef(
        name="hw_generate_electronics_source",
        description="Generate electronics source (KiCad schematic / tscircuit Circuit JSON) from spec.",
        input_schema=_project_only(),
        output_schema=ref("electronics_source_result"),
        execution_mode="async",
    ),

    "hw_generate_mechanical": ToolDef(
        name="hw_generate_mechanical",
        description="Generate mechanical enclosure source (build123d script by default).",
        input_schema={
            "type": "object",
            "properties": {
                "project": {"type": "string"},
                "backend": {"type": "string", "default": "build123d"},
            },
            "required": ["project"],
            "additionalProperties": False,
        },
        output_schema=_GENERATE_MECHANICAL_OUTPUT,
        execution_mode="async",
    ),

    "hw_generate_firmware": ToolDef(
        name="hw_generate_firmware",
        description="Generate firmware source for the target framework (Zephyr by default).",
        input_schema={
            "type": "object",
            "properties": {
                "project":   {"type": "string"},
                "framework": {"type": "string", "default": "zephyr"},
            },
            "required": ["project"],
            "additionalProperties": False,
        },
        output_schema=_GENERATE_FIRMWARE_OUTPUT,
        execution_mode="async",
    ),

    # -------------------------------------------------------------------
    # ERC / DRC / electrical checks
    # -------------------------------------------------------------------
    "hw_run_erc": ToolDef(
        name="hw_run_erc",
        description="Run KiCad Electrical Rules Check (ERC) on the generated schematic.",
        input_schema=_project_only(),
        output_schema=ref("gate_report"),
        execution_mode="async",
    ),

    "hw_run_drc": ToolDef(
        name="hw_run_drc",
        description="Run KiCad Design Rules Check (DRC) on the generated board against a fabrication profile.",
        input_schema={
            "type": "object",
            "properties": {
                "project": {"type": "string"},
                "profile": {"type": "string", "default": "jlcpcb_4layer"},
            },
            "required": ["project"],
            "additionalProperties": False,
        },
        output_schema=ref("gate_report"),
        execution_mode="async",
    ),

    "hw_check_electrical_semantics": ToolDef(
        name="hw_check_electrical_semantics",
        description="Run semantic electrical checks (power rails, protection, decoupling) from spec alone.",
        input_schema=_project_only(),
        output_schema=ref("gate_report"),
    ),

    "hw_extract_electrical_graph": ToolDef(
        name="hw_extract_electrical_graph",
        description="Return the generated electrical connectivity graph (JSON). Blocked when not yet generated.",
        input_schema=_project_only(),
        output_schema=_EXTRACT_GRAPH_OUTPUT,
    ),

    # -------------------------------------------------------------------
    # Fabrication exports (currently blocked — require native KiCad/CAD)
    # -------------------------------------------------------------------
    "hw_export_pcb_fabrication": ToolDef(
        name="hw_export_pcb_fabrication",
        description="Export Gerber and drill files for PCB fabrication. Requires a generated, DRC-passing board.",
        input_schema=_project_only(),
        output_schema=ref("blocked_result"),
        execution_mode="local",
    ),

    # -------------------------------------------------------------------
    # Mechanical checks and exports
    # -------------------------------------------------------------------
    "hw_check_mechanical_fit": ToolDef(
        name="hw_check_mechanical_fit",
        description="Check PCB-to-enclosure dimensional fit, connector clearance, and mounting constraints.",
        input_schema=_project_only(),
        output_schema=ref("gate_report"),
    ),

    "hw_import_board_step": ToolDef(
        name="hw_import_board_step",
        description="Import a validated STEP file as the board mechanical model. Currently blocked.",
        input_schema={
            "type": "object",
            "properties": {
                "project": {"type": "string"},
                "source":  {"type": "string", "description": "Path to source STEP file"},
            },
            "required": ["project", "source"],
            "additionalProperties": False,
        },
        output_schema=ref("blocked_result"),
        execution_mode="local",
    ),

    "hw_export_mechanical": ToolDef(
        name="hw_export_mechanical",
        description="Export STEP/STL files for the enclosure. Requires the pinned build123d backend. Currently blocked.",
        input_schema=_project_only(),
        output_schema=ref("blocked_result"),
        execution_mode="local",
    ),

    # -------------------------------------------------------------------
    # Firmware checks and build
    # -------------------------------------------------------------------
    "hw_check_pinmap": ToolDef(
        name="hw_check_pinmap",
        description="Verify that the firmware pin map matches the schematic net assignments.",
        input_schema=_project_only(),
        output_schema=ref("gate_report"),
    ),

    "hw_build_firmware": ToolDef(
        name="hw_build_firmware",
        description="Build the Zephyr RTOS firmware for the target MCU. Returns build artefact paths.",
        input_schema=_project_only(),
        output_schema=ref("gate_report"),
        execution_mode="async",
    ),

    "hw_generate_bringup_tests": ToolDef(
        name="hw_generate_bringup_tests",
        description="Generate hardware bring-up test scripts from the firmware source.",
        input_schema=_project_only(),
        output_schema=ref("generated_files_flat"),
    ),

    # -------------------------------------------------------------------
    # Validation / repair loop
    # -------------------------------------------------------------------
    "hw_run_all_checks": ToolDef(
        name="hw_run_all_checks",
        description="Run all registered gate checks. Set include_external=false to skip toolchain-dependent gates.",
        input_schema={
            "type": "object",
            "properties": {
                "project":          {"type": "string"},
                "include_external": {"type": "boolean", "default": True},
            },
            "required": ["project"],
            "additionalProperties": False,
        },
        output_schema=ref("gate_report_collection"),
        execution_mode="async",
    ),

    "hw_generate_repair_plan": ToolDef(
        name="hw_generate_repair_plan",
        description="Analyse failing gate reports and produce a structured repair plan.",
        input_schema=_project_only(),
        output_schema=ref("repair_plan"),
    ),

    "hw_get_failure_report": ToolDef(
        name="hw_get_failure_report",
        description="Return persisted gate failure reports. Optionally filter to a single gate.",
        input_schema={
            "type": "object",
            "properties": {
                "project": {"type": "string"},
                "gate":    {"type": ["string", "null"], "default": None},
            },
            "required": ["project"],
            "additionalProperties": False,
        },
        output_schema=ref("gate_report_collection"),
    ),

    "hw_apply_repair_plan": ToolDef(
        name="hw_apply_repair_plan",
        description="Apply the current repair plan patches to the spec. Requires approved=true.",
        input_schema={
            "type": "object",
            "properties": {
                "project":  {"type": "string"},
                "approved": {"type": "boolean", "default": False},
            },
            "required": ["project"],
            "additionalProperties": False,
        },
        output_schema=ref("apply_repair_result"),
    ),

    # -------------------------------------------------------------------
    # Design iteration
    # -------------------------------------------------------------------
    "hw_run_design_iteration": ToolDef(
        name="hw_run_design_iteration",
        description="Run one full design iteration: generate → check → repair. Returns the iteration result.",
        input_schema={
            "type": "object",
            "properties": {
                "project":          {"type": "string"},
                "goal":             {"type": "string", "default": "make all release gates pass"},
                "include_external": {"type": "boolean", "default": True},
            },
            "required": ["project"],
            "additionalProperties": False,
        },
        output_schema=ref("iteration_result"),
        execution_mode="async",
    ),

    "hw_design_until_release": ToolDef(
        name="hw_design_until_release",
        description="Run design iterations until the release gate passes or max_iterations is reached.",
        input_schema={
            "type": "object",
            "properties": {
                "project":          {"type": "string"},
                "max_iterations":   {"type": "integer", "default": 8, "minimum": 1},
                "include_external": {"type": "boolean", "default": False},
            },
            "required": ["project"],
            "additionalProperties": False,
        },
        output_schema=ref("multi_iteration_result"),
        execution_mode="async",
    ),

    # -------------------------------------------------------------------
    # Release
    # -------------------------------------------------------------------
    "hw_check_release_gate": ToolDef(
        name="hw_check_release_gate",
        description="Evaluate the release gate and return pass/fail with blocking issues.",
        input_schema=_project_only(),
        output_schema=ref("gate_report"),
    ),

    "hw_generate_design_report": ToolDef(
        name="hw_generate_design_report",
        description="Generate a human-readable design report summarising spec, checks, and assumptions.",
        input_schema=_project_only(),
        output_schema=_DESIGN_REPORT_OUTPUT,
    ),

    "hw_export_release_bundle": ToolDef(
        name="hw_export_release_bundle",
        description="Package all release artefacts (gerbers, BOM, firmware hex, enclosure) into a signed ZIP.",
        input_schema=_project_only(),
        output_schema=ref("release_bundle_result"),
        execution_mode="async",
    ),

    "hw_verify_release": ToolDef(
        name="hw_verify_release",
        description="Verify SHA-256 integrity of all artefacts in the most recent release bundle.",
        input_schema=_project_only(),
        output_schema=ref("gate_report"),
        execution_mode="local",
    ),
}
