from __future__ import annotations

from typing import Any, Literal, TypedDict

# ---------------------------------------------------------------------------
# TypedDicts for protocol messages
# ---------------------------------------------------------------------------


class CompatibilityHeader(TypedDict):
    protocol_version: str
    engine_version: str
    toolchain_profile: str
    toolchain_digest: str


class JobSubmit(TypedDict):
    tool: str
    arguments: dict[str, Any]
    compatibility: CompatibilityHeader


class JobStatus(TypedDict):
    job_id: str
    status: Literal["queued", "running", "complete", "failed"]
    gate_events: list[dict[str, Any]]
    result: dict[str, Any] | None


class GateEvent(TypedDict):
    event_type: Literal["gate_started", "gate_complete", "gate_blocked", "gate_failed"]
    gate: str
    status: str
    timestamp: str
    metrics: dict[str, Any]


class ErrorEnvelope(TypedDict):
    error: str
    code: str
    compatibility_required: CompatibilityHeader | None


# ---------------------------------------------------------------------------
# JSON Schemas for the protocol messages (embedded; no file I/O at import)
# ---------------------------------------------------------------------------

_COMPAT_HEADER_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": ["protocol_version", "engine_version", "toolchain_profile", "toolchain_digest"],
    "additionalProperties": False,
    "properties": {
        "protocol_version": {"type": "string"},
        "engine_version":   {"type": "string"},
        "toolchain_profile": {"type": "string"},
        "toolchain_digest": {"type": "string", "pattern": r"^sha256:[0-9a-f]{64}$"},
    },
}

JOB_SUBMIT_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "hw-contracts JobSubmit",
    "type": "object",
    "required": ["tool", "arguments", "compatibility"],
    "additionalProperties": False,
    "properties": {
        "tool": {"type": "string", "description": "Registered tool name (hw_*)"},
        "arguments": {"type": "object", "description": "Tool input arguments"},
        "compatibility": _COMPAT_HEADER_SCHEMA,
    },
}

JOB_STATUS_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "hw-contracts JobStatus",
    "type": "object",
    "required": ["job_id", "status", "gate_events", "result"],
    "additionalProperties": False,
    "properties": {
        "job_id": {"type": "string"},
        "status": {"type": "string", "enum": ["queued", "running", "complete", "failed"]},
        "gate_events": {"type": "array", "items": {"type": "object"}},
        "result": {"type": ["object", "null"]},
    },
}

GATE_EVENT_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "hw-contracts GateEvent",
    "type": "object",
    "required": ["event_type", "gate", "status", "timestamp", "metrics"],
    "additionalProperties": False,
    "properties": {
        "event_type": {
            "type": "string",
            "enum": ["gate_started", "gate_complete", "gate_blocked", "gate_failed"],
        },
        "gate":      {"type": "string"},
        "status":    {"type": "string", "enum": ["pass", "fail", "blocked", "candidate", "released"]},
        "timestamp": {"type": "string", "format": "date-time"},
        "metrics":   {"type": "object"},
    },
}

ERROR_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "hw-contracts ErrorEnvelope",
    "type": "object",
    "required": ["error", "code"],
    "additionalProperties": False,
    "properties": {
        "error": {"type": "string"},
        "code":  {"type": "string"},
        "compatibility_required": {
            "oneOf": [_COMPAT_HEADER_SCHEMA, {"type": "null"}],
        },
    },
}

MESSAGE_SCHEMAS: dict[str, dict[str, Any]] = {
    "job_submit": JOB_SUBMIT_SCHEMA,
    "job_status": JOB_STATUS_SCHEMA,
    "gate_event": GATE_EVENT_SCHEMA,
    "error":      ERROR_SCHEMA,
}
