"""Shared reusable output schemas for hw-codesign tool results.

Each schema is a JSON Schema draft-2020-12 document with a stable $id.
Tool output schemas reference these via $ref; validators register the full
SHARED_SCHEMAS map before resolving.

URN scheme: urn:hw-codesign:contracts:{name}
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any

_BASE = "urn:hw-codesign:contracts:"


def _id(name: str) -> str:
    return _BASE + name


# ---------------------------------------------------------------------------
# Sub-object definitions (reused inline; not top-level schemas)
# ---------------------------------------------------------------------------

_FAILURE_ITEM: dict[str, Any] = {
    "type": "object",
    "required": ["category", "code", "message", "severity"],
    "additionalProperties": True,
    "properties": {
        "category":               {"type": "string"},
        "code":                   {"type": "string"},
        "message":                {"type": "string"},
        "severity":               {"type": "string", "enum": ["error", "warning", "info"]},
        "path":                   {"type": ["string", "null"]},
        "details":                {"type": "object"},
        "requires_user_decision": {"type": "boolean"},
    },
}

_STATUS_ENUM: dict[str, Any] = {
    "type": "string",
    "enum": ["pass", "fail", "blocked", "candidate", "released", "generated", "created"],
}

_REPAIR_PATCH: dict[str, Any] = {
    "type": "object",
    "required": ["section", "spec_path", "value", "operation"],
    "additionalProperties": True,
    "properties": {
        "section":           {"type": "string"},
        "spec_path":         {"type": "string"},
        "value":             {},
        "operation":         {"type": "string", "enum": ["replace"]},
        "requires_approval": {"type": "boolean"},
        "safety_class":      {"type": "string"},
        "source_gate":       {"type": "string"},
        "source_failure":    {"type": "string"},
    },
}

_REPAIR_ACTION: dict[str, Any] = {
    "type": "object",
    "required": ["gate", "failure_code", "action", "patches", "requires_user_decision"],
    "additionalProperties": True,
    "properties": {
        "gate":                  {"type": "string"},
        "failure_code":          {"type": "string"},
        "action":                {"type": "string"},
        "patches":               {"type": "array", "items": _REPAIR_PATCH},
        "requires_user_decision": {"type": "boolean"},
    },
}

_ITERATION_SUMMARY: dict[str, Any] = {
    "type": "object",
    "required": ["iteration_id", "status", "failed_gates"],
    "additionalProperties": True,
    "properties": {
        "iteration_id": {"type": "string"},
        "status":       _STATUS_ENUM,
        "failed_gates": {"type": "array", "items": {"type": "string"}},
    },
}

_ENVELOPE_PROPERTIES: dict[str, Any] = {
    "release_eligible": {
        "type": "boolean",
        "description": "True only when the tool result authoritatively permits release promotion.",
    },
    "candidate_only": {
        "type": "boolean",
        "description": "True when the result is a candidate artifact or otherwise not release-approved.",
    },
    "release_blocking_failures": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Known blockers that prevent release; empty only when no blockers are known.",
    },
}
_ENVELOPE_REQUIRED = ["release_eligible", "candidate_only", "release_blocking_failures"]

# ---------------------------------------------------------------------------
# Top-level shared schemas (each has a stable $id)
# ---------------------------------------------------------------------------

SHARED_SCHEMAS: dict[str, dict[str, Any]] = {

    # -------------------------------------------------------------------
    # mcp_response_envelope — required on every public MCP tool response
    # -------------------------------------------------------------------
    "mcp_response_envelope": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("mcp_response_envelope"),
        "title": "MCPResponseEnvelope",
        "description": "Stable top-level release-safety envelope present on every MCP tool response.",
        "type": "object",
        "required": list(_ENVELOPE_REQUIRED),
        "additionalProperties": True,
        "properties": deepcopy(_ENVELOPE_PROPERTIES),
    },

    # -------------------------------------------------------------------
    # gate_report — single gate check result (GateReport.to_dict())
    # -------------------------------------------------------------------
    "gate_report": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("gate_report"),
        "title": "GateReport",
        "description": "Result of a single gate check. Returned by most check/build/validate tools.",
        "type": "object",
        "required": ["gate", "status", "failures", "metrics", "artifacts", "backend"],
        "additionalProperties": True,
        "properties": {
            "gate":      {"type": "string"},
            "status":    {"type": "string", "enum": ["pass", "fail", "blocked", "candidate", "released"]},
            "failures":  {"type": "array", "items": _FAILURE_ITEM},
            "metrics":   {"type": "object"},
            "artifacts": {"type": "array", "items": {"type": "string"}},
            "backend":   {"type": "object"},
        },
    },

    # -------------------------------------------------------------------
    # gate_report_collection — result of run_all_checks / get_failure_report
    # -------------------------------------------------------------------
    "gate_report_collection": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("gate_report_collection"),
        "title": "GateReportCollection",
        "description": "Aggregated gate check results.",
        "type": "object",
        "required": ["status", "reports"],
        "additionalProperties": True,
        "properties": {
            "status":  {"type": "string", "enum": ["pass", "fail", "blocked"]},
            "reports": {
                "type": "array",
                "items": {"$ref": _id("gate_report")},
            },
        },
    },

    # -------------------------------------------------------------------
    # generated_files_flat — {status, files: string[]}
    # Used by mechanical, firmware, bringup_tests generators.
    # -------------------------------------------------------------------
    "generated_files_flat": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("generated_files_flat"),
        "title": "GeneratedFilesFlat",
        "description": "Generation result where output is a flat list of file paths.",
        "type": "object",
        "required": ["status", "files"],
        "additionalProperties": True,
        "properties": {
            "status": _STATUS_ENUM,
            "files":  {"type": "array", "items": {"type": "string"}},
        },
    },

    # -------------------------------------------------------------------
    # electronics_source_result — generate_electronics_only output
    # -------------------------------------------------------------------
    "electronics_source_result": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("electronics_source_result"),
        "title": "ElectronicsSourceResult",
        "description": "Result of generating electronics source files (schematic, netlist, Circuit JSON).",
        "type": "object",
        "required": ["status", "files"],
        "additionalProperties": True,
        "properties": {
            "status":                      _STATUS_ENUM,
            "files":                       {"type": "array", "items": {"type": "string"}},
            "component_resolution":        {"type": ["array", "null"], "items": {"type": "object", "additionalProperties": True}},
            "resolution_report":           {"type": ["object", "null"]},
            "supplier_availability_report": {"type": ["object", "null"]},
            "datasheet_evidence_report":   {"type": ["object", "null"]},
        },
    },

    # -------------------------------------------------------------------
    # generate_all_result — generate_all output (files as nested dict)
    # -------------------------------------------------------------------
    "generate_all_result": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("generate_all_result"),
        "title": "GenerateAllResult",
        "description": "Result of running all source generators in one step.",
        "type": "object",
        "required": ["status", "backend", "files"],
        "additionalProperties": True,
        "properties": {
            "status":  _STATUS_ENUM,
            "backend": {"type": "string"},
            "files": {
                "type": "object",
                "properties": {
                    "electronics": {"type": "array", "items": {"type": "string"}},
                    "mechanical":  {"type": "array", "items": {"type": "string"}},
                    "firmware":    {"type": "array", "items": {"type": "string"}},
                    "bom":         {"type": "array", "items": {"type": "string"}},
                },
                "additionalProperties": True,
            },
            "component_resolution": {"type": ["array", "null"], "items": {"type": "object", "additionalProperties": True}},
            "resolution_report":    {"type": ["object", "null"]},
        },
    },

    # -------------------------------------------------------------------
    # design_candidate_result — design_candidate output
    # -------------------------------------------------------------------
    "design_candidate_result": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("design_candidate_result"),
        "title": "DesignCandidateResult",
        "description": "Result of generating a cross-domain hardware candidate and packaging it for review.",
        "type": "object",
        "required": [
            "status",
            "project",
            "iteration_id",
            "design_goal",
            "backend",
            "release_eligible",
            "candidate_only",
            "design_domains",
            "semantic_representation",
            "sourcing_choices",
            "reviewable_artifacts",
            "dependency_graph",
            "grounding_summary",
            "gate_summary",
            "candidate",
            "promotion",
        ],
        "additionalProperties": True,
        "properties": {
            "status":                    {"type": "string", "const": "candidate"},
            "project":                   {"type": "string"},
            "iteration_id":              {"type": "string"},
            "design_goal":               {"type": "string"},
            "backend":                   {"type": "string"},
            "backend_release_eligible":  {"type": "boolean"},
            "release_eligible":          {"type": "boolean", "const": False},
            "candidate_only":            {"type": "boolean", "const": True},
            "release_blocking_failures": {"type": "array", "items": {"type": "string"}},
            "requirements_update":       {"type": ["object", "null"], "additionalProperties": True},
            "generated":                 {"$ref": _id("generate_all_result")},
            "design_domains": {
                "type": "object",
                "properties": {
                    "electronics":   {"type": "array", "items": {"type": "string"}},
                    "mechanical":    {"type": "array", "items": {"type": "string"}},
                    "firmware":      {"type": "array", "items": {"type": "string"}},
                    "sourcing":      {"type": "array", "items": {"type": "string"}},
                    "manufacturing": {"type": "array", "items": {"type": "string"}},
                },
                "additionalProperties": True,
            },
            "semantic_representation": {
                "type": "object",
                "required": ["authoring_model", "layers", "native_outputs"],
                "additionalProperties": True,
                "properties": {
                    "authoring_model": {"type": "string"},
                    "purpose":         {"type": "string"},
                    "layers": {
                        "type": "object",
                        "additionalProperties": True,
                        "properties": {
                            "requirements":        {"type": "array", "items": {"type": "string"}},
                            "electronics_graph":   {"type": ["string", "null"]},
                            "semantic_schematic":  {"type": ["string", "null"]},
                            "semantic_schematic_code": {"type": ["string", "null"]},
                            "electronics_intent":  {"type": "array", "items": {"type": "string"}},
                            "relative_placement":  {"type": "object", "additionalProperties": True},
                            "mechanical_contract": {"type": ["string", "null"]},
                            "firmware_pinmap":     {"type": ["string", "null"]},
                        },
                    },
                    "native_outputs": {"type": "object", "additionalProperties": True},
                    "representation_contract": {"type": "object", "additionalProperties": True},
                },
            },
            "sourcing_choices": {
                "type": "array",
                "items": {"type": "object", "additionalProperties": True},
            },
            "reviewable_artifacts": {
                "type": "object",
                "properties": {
                    "candidate_bundle":   {"type": ["string", "null"]},
                    "candidate_manifest": {"type": ["string", "null"]},
                    "review_bundle":      {"type": ["string", "null"]},
                    "review_html":        {"type": ["string", "null"]},
                    "physical_qualification_plan": {"type": ["string", "null"]},
                    "physical_qualification_plan_markdown": {"type": ["string", "null"]},
                    "electronics":        {"type": "array", "items": {"type": "string"}},
                    "mechanical":         {"type": "array", "items": {"type": "string"}},
                    "firmware":           {"type": "array", "items": {"type": "string"}},
                    "manufacturing":      {"type": "array", "items": {"type": "string"}},
                },
                "additionalProperties": True,
            },
            "dependency_graph": {"type": ["object", "null"], "additionalProperties": True},
            "grounding_summary": {
                "type": "object",
                "properties": {
                    "component_grounding": {"type": "object", "additionalProperties": True},
                    "risk_areas":          {"type": "array", "items": {"type": "object", "additionalProperties": True}},
                    "physical_oracle_gaps": {"type": "array", "items": {"type": "string"}},
                },
                "additionalProperties": True,
            },
            "gate_summary":   {"type": "object", "additionalProperties": True},
            "blocking_gates": {"type": "array", "items": {"type": "object", "additionalProperties": True}},
            "candidate":      {"type": "object", "additionalProperties": True},
            "review_bundle":  {"type": ["object", "null"], "additionalProperties": True},
            "promotion":      {"type": "object", "additionalProperties": True},
        },
    },

    # -------------------------------------------------------------------
    # design_space_exploration_result — explore_design_space output
    # -------------------------------------------------------------------
    "design_space_exploration_result": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("design_space_exploration_result"),
        "title": "DesignSpaceExplorationResult",
        "description": "Ranked deterministic design-space alternatives with evidence and blockers.",
        "type": "object",
        "required": ["status", "project", "candidate_only", "release_eligible", "exploration_model", "axes", "selected_candidate", "candidates", "artifact"],
        "additionalProperties": True,
        "properties": {
            "status":            {"type": "string", "const": "generated"},
            "project":           {"type": "string"},
            "candidate_only":    {"type": "boolean", "const": True},
            "release_eligible":  {"type": "boolean", "const": False},
            "exploration_model": {"type": "string"},
            "axes":              {"type": "array", "items": {"type": "string"}},
            "max_candidates":    {"type": "integer"},
            "generated_summary": {"type": "object", "additionalProperties": True},
            "gate_summary":      {"type": "object", "additionalProperties": True},
            "selected_candidate": {"type": ["object", "null"], "additionalProperties": True},
            "candidates": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["id", "axis", "title", "score", "rank", "metrics", "tradeoffs", "blockers", "evidence"],
                    "additionalProperties": True,
                    "properties": {
                        "id":              {"type": "string"},
                        "axis":            {"type": "string"},
                        "title":           {"type": "string"},
                        "score":           {"type": "number"},
                        "rank":            {"type": "integer"},
                        "score_breakdown": {"type": "object", "additionalProperties": True},
                        "patch":           {"type": ["object", "null"], "additionalProperties": True},
                        "metrics":         {"type": "object", "additionalProperties": True},
                        "tradeoffs":       {"type": "array", "items": {"type": "string"}},
                        "blockers":        {"type": "array", "items": {"type": "object", "additionalProperties": True}},
                        "evidence":        {"type": "array", "items": {"type": "string"}},
                    },
                },
            },
            "all_candidate_count": {"type": "integer"},
            "recommendation":      {"type": "string"},
            "artifact":            {"type": "string"},
        },
    },

    # -------------------------------------------------------------------
    # physical_qualification_plan_result — generate_physical_qualification_plan output
    # -------------------------------------------------------------------
    "physical_qualification_plan_result": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("physical_qualification_plan_result"),
        "title": "PhysicalQualificationPlanResult",
        "description": "Machine-readable physical qualification plan and evidence requirements.",
        "type": "object",
        "required": ["status", "project", "artifact", "markdown", "required_tests", "evidence_directory", "plan"],
        "additionalProperties": True,
        "properties": {
            "status":             {"type": "string", "const": "generated"},
            "project":            {"type": "string"},
            "artifact":           {"type": "string"},
            "markdown":           {"type": "string"},
            "required_tests":     {"type": "array", "items": {"type": "string"}},
            "evidence_directory": {"type": "string"},
            "plan": {
                "type": "object",
                "required": ["artifact_type", "status", "project", "release_gate", "tests", "oracle_boundary"],
                "additionalProperties": True,
                "properties": {
                    "artifact_type": {"type": "string", "const": "physical_qualification_plan"},
                    "status":        {"type": "string"},
                    "project":       {"type": "string"},
                    "release_gate":  {"type": "string"},
                    "tests":         {"type": "array", "items": {"type": "object", "additionalProperties": True}},
                    "oracle_boundary": {"type": "array", "items": {"type": "string"}},
                },
            },
        },
    },

    # -------------------------------------------------------------------
    # physical_evidence_result — record_physical_evidence output
    # -------------------------------------------------------------------
    "physical_evidence_result": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("physical_evidence_result"),
        "title": "PhysicalEvidenceResult",
        "description": "Result of recording external physical qualification evidence.",
        "type": "object",
        "required": ["status", "project"],
        "additionalProperties": True,
        "properties": {
            "status": {"type": "string", "enum": ["generated", "blocked"]},
            "project": {"type": "string"},
            "record": {"type": "string"},
            "gate": {"$ref": _id("gate_report")},
            "code": {"type": "string"},
            "test_id": {"type": ["string", "null"]},
            "known_tests": {"type": "array", "items": {"type": "string"}},
        },
    },

    # -------------------------------------------------------------------
    # grounding_benchmark_result — run_grounding_benchmark output
    # -------------------------------------------------------------------
    "grounding_benchmark_result": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("grounding_benchmark_result"),
        "title": "GroundingBenchmarkResult",
        "description": "Deterministic adversarial benchmark for plausible-but-wrong hardware grounding failures.",
        "type": "object",
        "required": ["status", "project", "benchmark"],
        "additionalProperties": True,
        "properties": {
            "status":    {"type": "string", "enum": ["pass", "fail", "blocked"]},
            "project":   {"type": "string"},
            "benchmark": {"type": "string", "const": "hardware_grounding_v0"},
            "summary": {
                "type": "object",
                "additionalProperties": True,
                "properties": {
                    "total_cases":    {"type": "integer"},
                    "detected_cases": {"type": "integer"},
                    "missed_cases":   {"type": "integer"},
                },
            },
            "cases": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["id", "risk", "mutation", "expected_gate", "expected_codes", "observed_status", "observed_codes", "detected"],
                    "additionalProperties": True,
                    "properties": {
                        "id":              {"type": "string"},
                        "risk":            {"type": "string"},
                        "mutation":        {"type": "string"},
                        "expected_gate":   {"type": "string"},
                        "expected_codes":  {"type": "array", "items": {"type": "string"}},
                        "observed_status": {"type": "string"},
                        "observed_codes":  {"type": "array", "items": {"type": "string"}},
                        "detected":        {"type": "boolean"},
                        "report":          {"$ref": _id("gate_report")},
                    },
                },
            },
            "physical_oracle_limits": {"type": "array", "items": {"type": "string"}},
            "artifact":               {"type": "string"},
            "code":                   {"type": "string"},
            "missing_artifacts":      {"type": "array", "items": {"type": "string"}},
            "message":                {"type": "string"},
        },
    },

    # -------------------------------------------------------------------
    # design_benchmark_result — run_design_benchmark output
    # -------------------------------------------------------------------
    "design_benchmark_result": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("design_benchmark_result"),
        "title": "DesignBenchmarkResult",
        "description": "Result of the held-out design benchmark: one-line intent → design_until_release pass-rate.",
        "type": "object",
        "required": ["status", "benchmark", "summary", "specs"],
        "additionalProperties": True,
        "properties": {
            "status":           {"type": "string", "enum": ["pass", "fail", "partial"]},
            "benchmark":        {"type": "string"},
            "include_external": {"type": "boolean"},
            "summary": {
                "type": "object",
                "additionalProperties": True,
                "properties": {
                    "total":                      {"type": "integer"},
                    "passed":                     {"type": "integer"},
                    "software_gates_ready":        {"type": "integer",
                                                   "description": "Specs where all software gates pass, pending native toolchain run"},
                    "failed":                     {"type": "integer"},
                    "pass_rate":                  {"type": "number",
                                                   "description": "Fraction of specs that reached released status (requires native gates)"},
                    "software_gates_ready_rate":   {"type": "number",
                                                   "description": "Fraction of specs where software gates are ready; CI-measurable win-condition"},
                    "mean_iterations":            {"type": "number"},
                    "software_gate_pass_rate":    {"type": "number",
                                                   "description": "Mean fraction of non-external gates that pass; CI-measurable without native toolchain"},
                    "physical_qualification_ready": {"type": "integer",
                                                     "description": "Specs with approved passing evidence for every required physical qualification test"},
                    "physical_qualification_ready_rate": {"type": "number",
                                                          "description": "Fraction of specs whose physical qualification gate passes"},
                    "physical_qualification_required_tests": {"type": "integer"},
                    "physical_qualification_approved_passed": {"type": "integer"},
                    "physical_qualification_missing_or_unapproved": {"type": "integer"},
                    "physical_qualification_failed": {"type": "integer"},
                    "physical_qualification_gap_categories": {"type": "array", "items": {"type": "string"}},
                },
            },
            "specs": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["id", "template", "intent", "status"],
                    "additionalProperties": True,
                    "properties": {
                        "id":                       {"type": "string"},
                        "template":                 {"type": "string"},
                        "intent":                   {"type": "string"},
                        "status":                   {"type": "string", "enum": ["released", "software_gates_ready", "fail", "blocked", "error", "partial"]},
                        "iterations":               {"type": "integer"},
                        "gate_summary":             {"type": "object", "additionalProperties": True},
                        "software_gate_pass_rate":  {"type": "number"},
                        "native_gate_pass_rate":    {"type": "number"},
                        "physical_qualification_summary": {
                            "type": "object",
                            "additionalProperties": True,
                            "properties": {
                                "status": {"type": "string"},
                                "required_tests": {"type": "integer"},
                                "approved_passed": {"type": "integer"},
                                "missing_or_unapproved": {"type": "integer"},
                                "failed": {"type": "integer"},
                                "gap_categories": {"type": "array", "items": {"type": "string"}},
                                "gate": {"$ref": _id("gate_report")},
                            },
                        },
                        "error":                    {"type": "string"},
                    },
                },
            },
            "artifact": {"type": "string"},
        },
    },

    # -------------------------------------------------------------------
    # repair_plan — generate_repair_plan output
    # -------------------------------------------------------------------
    "repair_plan": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("repair_plan"),
        "title": "RepairPlan",
        "description": "Structured list of actions and spec patches to resolve failing gates.",
        "type": "object",
        "required": ["status", "project", "requires_user_decision", "actions"],
        "additionalProperties": True,
        "properties": {
            "status":                 {"type": "string"},
            "project":                {"type": "string"},
            "requires_user_decision": {"type": "boolean"},
            "actions":                {"type": "array", "items": _REPAIR_ACTION},
        },
    },

    # -------------------------------------------------------------------
    # apply_repair_result — apply_repair_plan output
    # -------------------------------------------------------------------
    "apply_repair_result": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("apply_repair_result"),
        "title": "ApplyRepairResult",
        "description": "Result of applying spec patches from the repair plan.",
        "type": "object",
        "required": ["status", "applied", "proposals"],
        "additionalProperties": True,
        "properties": {
            "status":                 {"type": "string", "enum": ["pass", "blocked", "generated"]},
            "applied":                {"type": "array", "items": _REPAIR_PATCH},
            "proposals":              {"type": "array", "items": {"type": "object"}},
            "iteration_id":           {"type": "string"},
            "requires_user_decision": {"type": "boolean"},
        },
    },

    # -------------------------------------------------------------------
    # iteration_result — run_design_iteration output
    # -------------------------------------------------------------------
    "iteration_result": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("iteration_result"),
        "title": "IterationResult",
        "description": "Result of one full generate→check→repair design iteration.",
        "type": "object",
        "required": ["status", "iteration_id", "passed_gates", "failed_gates"],
        "additionalProperties": True,
        "properties": {
            "status":       {"type": "string", "enum": ["pass", "fail", "blocked"]},
            "iteration_id": {"type": "string"},
            "passed_gates": {"type": "array", "items": {"type": "string"}},
            "failed_gates": {"type": "array", "items": {"type": "string"}},
            "repair_plan":  {"$ref": _id("repair_plan")},
            "release_gate": {
                "type": "object",
                "properties": {"status": {"type": "string"}},
            },
        },
    },

    # -------------------------------------------------------------------
    # multi_iteration_result — design_until_release output
    # -------------------------------------------------------------------
    "multi_iteration_result": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("multi_iteration_result"),
        "title": "MultiIterationResult",
        "description": "Result of running design iterations until release or exhaustion.",
        "type": "object",
        "required": ["status", "iterations"],
        "additionalProperties": True,
        "properties": {
            "status":     {"type": "string", "enum": ["released", "fail", "blocked"]},
            "iterations": {"type": "array", "items": _ITERATION_SUMMARY},
            "release":    {"type": "object"},
            "code":       {"type": "string"},
        },
    },

    # -------------------------------------------------------------------
    # release_bundle_result — export_release_bundle output
    # -------------------------------------------------------------------
    "release_bundle_result": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("release_bundle_result"),
        "title": "ReleaseBundleResult",
        "description": "Result of packaging a release bundle ZIP.",
        "type": "object",
        "required": ["status"],
        "additionalProperties": True,
        "properties": {
            "status": {"type": "string", "enum": ["released", "blocked", "fail"]},
            "bundle": {"type": "string", "description": "Absolute path to the ZIP file"},
            "sha256": {"type": "string"},
            "bytes":  {"type": "integer"},
        },
    },

    # -------------------------------------------------------------------
    # blocked_result — any permanently-blocked tool response
    # -------------------------------------------------------------------
    "blocked_result": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("blocked_result"),
        "title": "BlockedResult",
        "description": "Returned by tools that are blocked pending toolchain or user action.",
        "type": "object",
        "required": ["status", "code"],
        "additionalProperties": True,
        "properties": {
            "status":  {"type": "string", "const": "blocked"},
            "code":    {"type": "string"},
            "message": {"type": "string"},
        },
    },

    # -------------------------------------------------------------------
    # capabilities_result — hw_get_capabilities output
    # -------------------------------------------------------------------
    "capabilities_result": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("capabilities_result"),
        "title": "CapabilitiesResult",
        "description": "Available backends, explicit release tiers, external tools, and which gates each enables.",
        "type": "object",
        "required": [
            "status", "backends", "release_tiers", "release_eligible_backends",
            "canonical_fabrication_backends", "canonical_fabrication_flow",
            "fabrication_release_backends", "netlist_release_backends",
            "source_release_backends", "candidate_only_backends",
            "external_tools", "missing_external_gates", "platform_root",
        ],
        "additionalProperties": True,
        "properties": {
            "status":                      {"type": "string"},
            "backends":                    {"type": "object", "additionalProperties": True},
            "release_tiers":               {"type": "object", "additionalProperties": {"type": "string"}},
            "release_eligible_backends":   {"type": "array", "items": {"type": "string"}},
            "canonical_fabrication_backends": {"type": "array", "items": {"type": "string"}},
            "canonical_fabrication_flow":   {"type": "object", "additionalProperties": {"type": "string"}},
            "fabrication_release_backends": {"type": "array", "items": {"type": "string"}},
            "netlist_release_backends":    {"type": "array", "items": {"type": "string"}},
            "source_release_backends":     {"type": "array", "items": {"type": "string"}},
            "candidate_only_backends":     {"type": "array", "items": {"type": "string"}},
            "external_tools":              {"type": "object", "additionalProperties": True},
            "missing_external_gates":      {"type": "array", "items": {"type": "string"}},
            "platform_root":               {"type": "string"},
        },
    },

    # -------------------------------------------------------------------
    # release_readiness_result — hw_review_release_readiness output
    # -------------------------------------------------------------------
    "release_readiness_result": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("release_readiness_result"),
        "title": "ReleaseReadinessResult",
        "description": "Aggregated release-readiness summary from persisted gate reports, requirements, and assumptions.",
        "type": "object",
        "required": ["status", "release_eligible", "release_gate_authoritative", "readiness_estimate", "candidate_only", "release_blocking_failures", "project", "revision", "backend", "backend_release_eligible", "gate_data", "data_freshness", "gate_summary", "blocking_gates", "blocker_categories", "assumptions", "recommendation"],
        "additionalProperties": True,
        "properties": {
            "status":                      {"type": "string", "enum": ["pass", "fail", "blocked"]},
            "release_eligible":            {"type": "boolean", "const": False, "description": "Always false — only hw_check_release_gate (status pass) confers release eligibility."},
            "release_gate_authoritative":  {"type": "boolean", "const": False, "description": "Always false — this tool reads persisted reports and is not the release gate."},
            "readiness_estimate":          {"type": "string", "enum": ["pass", "fail", "blocked"], "description": "Assessment based on persisted reports; not a gate outcome."},
            "candidate_only":              {"type": "boolean"},
            "release_blocking_failures":   {"type": "array", "items": {"type": "string"}},
            "project":                     {"type": "string"},
            "revision":                    {"type": "string"},
            "backend":                     {"type": "string"},
            "backend_release_eligible":    {"type": "boolean"},
            "gate_data":                   {"type": "string", "enum": ["persisted", "none"]},
            "data_freshness":              {"type": "string", "enum": ["current", "possibly_stale", "unknown", "none"], "description": "Heuristic freshness based on spec vs report file mtimes. possibly_stale means spec was modified after last check run."},
            "gate_summary":                {"type": "object"},
            "blocking_gates":              {"type": "array", "items": {"type": "object"}},
            "blocker_categories":          {"type": "array", "items": {"type": "string"}},
            "requirements":                {"type": ["object", "null"]},
            "assumptions":                 {"type": "object"},
            "physical_qualification_gaps": {"type": "array", "items": {"type": "string"}},
            "recommendation":              {"type": "string"},
        },
    },

    # -------------------------------------------------------------------
    # candidate_bundle_result — hw_export_candidate_bundle output
    # -------------------------------------------------------------------
    "candidate_bundle_result": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("candidate_bundle_result"),
        "title": "CandidateBundleResult",
        "description": "Candidate bundle export — not release-eligible. Distinct from release_bundle_result.",
        "type": "object",
        "required": ["status", "candidate_only", "release_eligible", "release_blocking_failures", "iteration_id", "backend", "gate_status", "bundle", "path"],
        "additionalProperties": True,
        "properties": {
            "status":                    {"type": "string", "const": "candidate"},
            "candidate_only":            {"type": "boolean", "const": True},
            "release_eligible":          {"type": "boolean", "const": False},
            "release_blocking_failures": {"type": "array", "items": {"type": "string"}},
            "iteration_id":              {"type": "string"},
            "backend":                   {"type": "string"},
            "gate_status":               {"type": "string"},
            "bundle":                    {"type": "string"},
            "path":                      {"type": "string"},
        },
    },

    # -------------------------------------------------------------------
    # candidate_list_result — hw_list_candidates output
    # -------------------------------------------------------------------
    "candidate_list_result": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("candidate_list_result"),
        "title": "CandidateListResult",
        "type": "object",
        "required": ["status", "project", "candidates", "count"],
        "additionalProperties": True,
        "properties": {
            "status":     {"type": "string"},
            "project":    {"type": "string"},
            "count":      {"type": "integer"},
            "candidates": {"type": "array", "items": {"type": "object", "additionalProperties": True}},
        },
    },

    # -------------------------------------------------------------------
    # candidate_review_result — hw_review_candidate output
    # -------------------------------------------------------------------
    "candidate_review_result": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("candidate_review_result"),
        "title": "CandidateReviewResult",
        "description": "Readiness summary for a single candidate from its frozen gate reports.",
        "type": "object",
        "required": ["status", "project", "candidate_id", "backend", "backend_release_eligible", "gate_summary", "blocking_gates", "release_blocking_failures", "recommendation"],
        "additionalProperties": True,
        "properties": {
            "status":                    {"type": "string"},
            "project":                   {"type": "string"},
            "candidate_id":              {"type": "string"},
            "backend":                   {"type": "string"},
            "backend_release_eligible":  {"type": "boolean"},
            "gate_summary":              {"type": "object"},
            "blocking_gates":            {"type": "array", "items": {"type": "object"}},
            "release_blocking_failures": {"type": "array", "items": {"type": "string"}},
            "assumptions":               {"type": ["object", "null"]},
            "recommendation":            {"type": "string"},
        },
    },

    # -------------------------------------------------------------------
    # compare_candidates_result — hw_compare_candidates output
    # -------------------------------------------------------------------
    "compare_candidates_result": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("compare_candidates_result"),
        "title": "CompareCandidatesResult",
        "description": "Delta between two candidate snapshots across gates, artifacts, and risk.",
        "type": "object",
        "required": ["status", "project", "candidate_a", "candidate_b", "readiness_delta", "artifact_delta", "risk_delta", "recommendation"],
        "additionalProperties": True,
        "properties": {
            "status":      {"type": "string"},
            "project":     {"type": "string"},
            "candidate_a": {"type": "string"},
            "candidate_b": {"type": "string"},
            "readiness_delta": {
                "type": "object",
                "required": ["blocking_gates_removed", "blocking_gates_added", "pass_count_delta", "fail_count_delta", "blocked_count_delta"],
                "additionalProperties": True,
                "properties": {
                    "blocking_gates_removed": {"type": "array", "items": {"type": "string"}},
                    "blocking_gates_added":   {"type": "array", "items": {"type": "string"}},
                    "pass_count_delta":       {"type": "integer"},
                    "fail_count_delta":       {"type": "integer"},
                    "blocked_count_delta":    {"type": "integer"},
                },
            },
            "artifact_delta": {
                "type": "object",
                "required": ["added", "removed", "changed"],
                "additionalProperties": True,
                "properties": {
                    "added":   {"type": "array", "items": {"type": "string"}},
                    "removed": {"type": "array", "items": {"type": "string"}},
                    "changed": {"type": "array", "items": {"type": "string"}},
                },
            },
            "risk_delta": {
                "type": "object",
                "required": ["new_physical_gaps", "resolved_assumptions", "new_unresolved_assumptions"],
                "additionalProperties": True,
                "properties": {
                    "new_physical_gaps":          {"type": "array", "items": {"type": "string"}},
                    "resolved_assumptions":       {"type": "array", "items": {"type": "string"}},
                    "new_unresolved_assumptions": {"type": "array", "items": {"type": "string"}},
                },
            },
            "recommendation": {"type": "string"},
        },
    },

    # -------------------------------------------------------------------
    # fabrication_review_result — hw_prepare_fabrication_review output
    # -------------------------------------------------------------------
    "fabrication_review_result": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("fabrication_review_result"),
        "title": "FabricationReviewResult",
        "description": "Structured fabrication review packet. label determines ordering readiness.",
        "type": "object",
        "required": ["status", "project", "label", "backend", "backend_release_eligible", "gate_status", "erc_status", "drc_status", "artifact_presence", "unresolved_assumptions", "unresolved_requirements", "physical_qualification_gaps", "fab_review_checklist"],
        "additionalProperties": True,
        "properties": {
            "status":                   {"type": "string"},
            "project":                  {"type": "string"},
            "candidate_id":             {"type": ["string", "null"]},
            "label":                    {"type": "string", "enum": ["do_not_fabricate", "review_only", "release_candidate"]},
            "backend":                  {"type": "string"},
            "backend_release_eligible": {"type": "boolean"},
            "gate_status":              {"type": "object"},
            "erc_status":               {"type": "string"},
            "drc_status":               {"type": "string"},
            "toolchain_versions":       {"type": "object"},
            "artifact_presence":        {"type": "object"},
            "unresolved_assumptions":   {"type": "array", "items": {"type": "string"}},
            "unresolved_requirements":  {"type": "array"},
            "physical_qualification_gaps": {"type": "array", "items": {"type": "string"}},
            "fab_review_checklist":     {"type": "array", "items": {"type": "string"}},
        },
    },

    # -------------------------------------------------------------------
    # environment_diagnosis_result — hw_diagnose_environment output
    # -------------------------------------------------------------------
    "environment_diagnosis_result": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("environment_diagnosis_result"),
        "title": "EnvironmentDiagnosisResult",
        "description": "Target-conditioned diagnosis of missing tools and blocked gates.",
        "type": "object",
        "required": ["status", "target", "ready", "missing_tools", "blocked_gates", "install_hints", "tool_availability"],
        "additionalProperties": True,
        "properties": {
            "status":           {"type": "string", "enum": ["pass", "fail", "blocked"]},
            "target":           {"type": "string"},
            "backend":          {"type": ["string", "null"]},
            "description":      {"type": "string"},
            "ready":            {"type": "boolean"},
            "missing_tools":    {"type": "array", "items": {"type": "string"}},
            "blocked_gates":    {"type": "array", "items": {"type": "string"}},
            "install_hints":    {"type": "object", "additionalProperties": {"type": "array", "items": {"type": "string"}}},
            "tool_availability": {"type": "object", "additionalProperties": {"type": "boolean"}},
        },
    },

    # -------------------------------------------------------------------
    # part_design_result — hw_design_part output
    # -------------------------------------------------------------------
    "part_design_result": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("part_design_result"),
        "title": "PartDesignResult",
        "description": "Result of designing a parametric mechanical part from agent intent.",
        "type": "object",
        "required": ["status", "part_name", "part_type"],
        "additionalProperties": True,
        "properties": {
            "status":          _STATUS_ENUM,
            "part_name":       {"type": "string"},
            "part_type":       {"type": "string"},
            "artifacts":       {"type": "array", "items": {"type": "string"}},
            "printability":    {
                "type": "object",
                "properties": {
                    "printable":              {"type": "boolean"},
                    "max_overhang_deg":       {"type": "number"},
                    "min_wall_mm":            {"type": "number"},
                    "min_hole_mm":            {"type": "number"},
                    "stl_manifold":           {"type": "boolean"},
                    "recommended_orientation": {"type": "string"},
                    "violations":             {"type": "array", "items": {"type": "string"}},
                },
            },
            "gate_report":     {"$ref": _id("gate_report")},
            "candidate_only":  {"type": "boolean"},
            "release_eligible": {"type": "boolean"},
        },
    },

    # -------------------------------------------------------------------
    # part_list_result — hw_list_parts output
    # -------------------------------------------------------------------
    "part_list_result": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("part_list_result"),
        "title": "PartListResult",
        "type": "object",
        "required": ["status", "project", "parts", "count"],
        "additionalProperties": True,
        "properties": {
            "status":  {"type": "string"},
            "project": {"type": "string"},
            "count":   {"type": "integer"},
            "parts":   {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["part_name", "part_type", "gate_status"],
                    "additionalProperties": True,
                    "properties": {
                        "part_name":      {"type": "string"},
                        "part_type":      {"type": "string"},
                        "gate_status":    {"type": "string"},
                        "printability":   {"type": ["boolean", "null"]},
                        "artifact_count": {"type": "integer"},
                    },
                },
            },
        },
    },

    # -------------------------------------------------------------------
    # part_types_result — hw_get_part_types output
    # -------------------------------------------------------------------
    "part_types_result": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("part_types_result"),
        "title": "PartTypesResult",
        "type": "object",
        "required": ["status", "part_types", "count"],
        "additionalProperties": True,
        "properties": {
            "status":     {"type": "string"},
            "count":      {"type": "integer"},
            "part_types": {
                "type": "object",
                "additionalProperties": {
                    "type": "object",
                    "required": ["description", "intent_schema"],
                    "additionalProperties": True,
                    "properties": {
                        "description":   {"type": "string"},
                        "intent_schema": {"type": "object"},
                    },
                },
            },
        },
    },

    # -------------------------------------------------------------------
    # circuit_block_proposal_result — hw_propose_circuit_block output
    # -------------------------------------------------------------------
    "circuit_block_proposal_result": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("circuit_block_proposal_result"),
        "title": "CircuitBlockProposalResult",
        "description": "Curated component candidates for a given circuit category.",
        "type": "object",
        "required": ["status", "category", "candidates", "count"],
        "additionalProperties": True,
        "properties": {
            "status":     {"type": "string"},
            "category":   {"type": "string"},
            "candidates": {"type": "array", "items": {"type": "object", "additionalProperties": True}},
            "count":      {"type": "integer"},
            "usage_hint": {"type": "string"},
        },
    },

    # -------------------------------------------------------------------
    # circuit_block_result — hw_add_circuit_block output
    # -------------------------------------------------------------------
    "circuit_block_result": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("circuit_block_result"),
        "title": "CircuitBlockResult",
        "description": "Result of adding an agent-authored circuit block to the design.",
        "type": "object",
        "required": ["status", "project", "ref"],
        "additionalProperties": True,
        "properties": {
            "status":            {"type": "string"},
            "project":           {"type": "string"},
            "ref":               {"type": "string"},
            "components_total":  {"type": "integer"},
            "nets_total":        {"type": "integer"},
            "gate_report":       {"type": "object", "additionalProperties": True},
        },
    },

    # -------------------------------------------------------------------
    # circuit_block_list_result — hw_list_circuit_blocks output
    # -------------------------------------------------------------------
    "circuit_block_list_result": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("circuit_block_list_result"),
        "title": "CircuitBlockListResult",
        "description": "List of agent-authored circuit blocks for a project.",
        "type": "object",
        "required": ["status", "project", "blocks", "count"],
        "additionalProperties": True,
        "properties": {
            "status":  {"type": "string"},
            "project": {"type": "string"},
            "blocks":  {"type": "array", "items": {"type": "object", "additionalProperties": True}},
            "count":   {"type": "integer"},
        },
    },

    # -------------------------------------------------------------------
    # placement_constraint_result — hw_set_placement_constraint output
    # -------------------------------------------------------------------
    "placement_constraint_result": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("placement_constraint_result"),
        "title": "PlacementConstraintResult",
        "description": "Result of setting a PCB placement constraint.",
        "type": "object",
        "required": ["status", "project", "ref", "constraint"],
        "additionalProperties": True,
        "properties": {
            "status":           {"type": "string"},
            "project":          {"type": "string"},
            "ref":              {"type": "string"},
            "constraint":       {"type": "object", "additionalProperties": True},
            "constraint_count": {"type": "integer"},
        },
    },

    # -------------------------------------------------------------------
    # placement_constraint_list_result — hw_list_placement_constraints output
    # -------------------------------------------------------------------
    "placement_constraint_list_result": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("placement_constraint_list_result"),
        "title": "PlacementConstraintListResult",
        "description": "List of agent-authored PCB placement constraints for a project.",
        "type": "object",
        "required": ["status", "project", "constraints", "count"],
        "additionalProperties": True,
        "properties": {
            "status":      {"type": "string"},
            "project":     {"type": "string"},
            "constraints": {"type": "array", "items": {"type": "object", "additionalProperties": True}},
            "count":       {"type": "integer"},
        },
    },

    # -------------------------------------------------------------------
    # design_decision_result — hw_record_design_decision output
    # -------------------------------------------------------------------
    "design_decision_result": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("design_decision_result"),
        "title": "DesignDecisionResult",
        "description": "Result of recording an agent design decision to the project journal.",
        "type": "object",
        "required": ["status", "project", "decision_id", "domain", "decision", "rationale"],
        "additionalProperties": True,
        "properties": {
            "status":      {"type": "string"},
            "project":     {"type": "string"},
            "decision_id": {"type": "string"},
            "domain":      {"type": "string"},
            "decision":    {"type": "string"},
            "rationale":   {"type": "string"},
        },
    },

    # -------------------------------------------------------------------
    # opaque_result — explicit fallback for not-yet-modeled outputs
    # -------------------------------------------------------------------
    "opaque_result": {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _id("opaque_result"),
        "title": "OpaqueResult",
        "description": "Output not yet formally modeled; shape is implementation-defined. "
                       "Presence of this schema in a tool's output_schema field marks it as "
                       "a known gap, not an oversight.",
        "type": "object",
        "additionalProperties": True,
    },
}


def ref(name: str) -> dict[str, Any]:
    """Return a $ref to a named shared schema."""
    if name not in SHARED_SCHEMAS:
        raise KeyError(f"Unknown shared schema: {name!r}. Available: {sorted(SHARED_SCHEMAS)}")
    return {"$ref": _id(name)}


def enveloped(schema: dict[str, Any]) -> dict[str, Any]:
    """Return a public MCP output schema with the release-safety envelope at top level.

    Inline strict schemas get the envelope properties merged in so
    additionalProperties=false remains usable. Shared-schema refs are composed
    with mcp_response_envelope because the shared result schemas are open
    objects by contract.
    """
    copied = deepcopy(schema)
    if copied.get("$ref"):
        return {"allOf": [ref("mcp_response_envelope"), copied]}
    if "oneOf" in copied:
        branches = [enveloped(item) for item in copied.pop("oneOf")]
        required = list(dict.fromkeys([*copied.get("required", []), *_ENVELOPE_REQUIRED]))
        properties = {**deepcopy(_ENVELOPE_PROPERTIES), **copied.get("properties", {})}
        copied.update({"type": "object", "required": required, "properties": properties, "oneOf": branches})
        return copied
    if copied.get("type") == "object" or "properties" in copied:
        required = list(dict.fromkeys([*copied.get("required", []), *_ENVELOPE_REQUIRED]))
        properties = {**deepcopy(_ENVELOPE_PROPERTIES), **copied.get("properties", {})}
        copied["required"] = required
        copied["properties"] = properties
        return copied
    return {"allOf": [ref("mcp_response_envelope"), copied]}
