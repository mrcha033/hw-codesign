"""hw_codesign.contracts — public contract surface for local and cloud MCP tool execution.

This package is the single source of truth for:
- Tool names, descriptions, and input schemas (TOOL_REGISTRY)
- Protocol message formats (JobSubmit, JobStatus, GateEvent, ErrorEnvelope)
- Compatibility version metadata (PROTOCOL_VERSION, ENGINE_VERSION, TOOLCHAIN_PINS)
- Manifest generation and validation utilities

hw-cloud imports this package (or a generated manifest JSON) to:
- Route job_submit requests to the right worker
- Reject requests whose compatibility headers don't match an available worker
- Enforce that its implemented tool set exactly matches the declared manifest
"""
from __future__ import annotations

from ._manifest import generate_manifest, validate_manifest
from ._messages import (
    MESSAGE_SCHEMAS,
    CompatibilityHeader,
    ErrorEnvelope,
    GateEvent,
    JobStatus,
    JobSubmit,
)
from ._schemas import SHARED_SCHEMAS
from ._tools import TOOL_REGISTRY, ToolDef
from ._versions import (
    ENGINE_VERSION,
    PROTOCOL_VERSION,
    TOOLCHAIN_PINS,
    TOOLCHAIN_PROFILE,
    toolchain_digest,
)

__all__ = [
    # Tool registry
    "TOOL_REGISTRY",
    "ToolDef",
    # Shared output schemas
    "SHARED_SCHEMAS",
    # Message types
    "CompatibilityHeader",
    "JobSubmit",
    "JobStatus",
    "GateEvent",
    "ErrorEnvelope",
    "MESSAGE_SCHEMAS",
    # Versions
    "PROTOCOL_VERSION",
    "ENGINE_VERSION",
    "TOOLCHAIN_PROFILE",
    "TOOLCHAIN_PINS",
    "toolchain_digest",
    # Manifest
    "generate_manifest",
    "validate_manifest",
]
