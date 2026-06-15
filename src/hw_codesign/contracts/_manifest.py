from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from ._messages import MESSAGE_SCHEMAS
from ._schemas import SHARED_SCHEMAS
from ._tools import TOOL_REGISTRY
from ._versions import ENGINE_VERSION, PROTOCOL_VERSION, TOOLCHAIN_PROFILE, toolchain_digest


def generate_manifest() -> dict[str, Any]:
    """Return a serialisable manifest capturing the full public contract surface."""
    return {
        "protocol_version":  PROTOCOL_VERSION,
        "engine_version":    ENGINE_VERSION,
        "toolchain_profile": TOOLCHAIN_PROFILE,
        "toolchain_digest":  toolchain_digest(),
        "tools": {name: td.to_dict() for name, td in TOOL_REGISTRY.items()},
        "shared_schemas":    SHARED_SCHEMAS,
        "message_schemas":   MESSAGE_SCHEMAS,
        "generated_at":      datetime.now(UTC).isoformat(),
    }


def validate_manifest(manifest: dict[str, Any], implemented_names: set[str]) -> list[str]:
    """Compare a manifest against the set of tool names an implementation provides.

    Returns a list of human-readable error strings; empty means the implementation
    is compatible with this manifest.
    """
    errors: list[str] = []
    declared: set[str] = set((manifest.get("tools") or {}).keys())

    for name in sorted(declared - implemented_names):
        errors.append(f"tool '{name}' declared in manifest but not implemented")
    for name in sorted(implemented_names - declared):
        errors.append(f"tool '{name}' implemented but absent from manifest")

    manifest_proto = manifest.get("protocol_version")
    if manifest_proto != PROTOCOL_VERSION:
        errors.append(
            f"protocol_version mismatch: manifest={manifest_proto!r} local={PROTOCOL_VERSION!r}"
        )

    return errors
