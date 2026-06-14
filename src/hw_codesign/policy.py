from __future__ import annotations

from dataclasses import dataclass, field

from .errors import UnsafeChangeError


PROTECTED_PREFIXES = ("safety.", "manufacturing.", "system.supply.", "actuation.motor_channel_peak_current_a", "mechanical.cooling", "mechanical.connectors", "release.")


@dataclass(frozen=True)
class ChangePolicy:
    allowed_changes: frozenset[str] = field(default_factory=lambda: frozenset({"spec", "electronics_source", "mechanical_source", "firmware_source"}))
    forbidden_changes: frozenset[str] = field(default_factory=lambda: frozenset({"manufacturing_limits_without_user_approval", "safety_requirements_without_user_approval"}))
    user_approved_paths: frozenset[str] = field(default_factory=frozenset)

    def check_spec_paths(self, paths: list[str]) -> None:
        rejected = [path for path in paths if path.startswith(PROTECTED_PREFIXES) and path not in self.user_approved_paths]
        if rejected:
            raise UnsafeChangeError("Protected requirements require explicit user approval: " + ", ".join(rejected))
