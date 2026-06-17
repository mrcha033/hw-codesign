from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ModuleOutput:
    id: str
    behavior: str
    c_source: str
    h_source: str
    dts_fragment: str | None = None
    kconfig_flags: list[str] = field(default_factory=list)
    stack_size_bytes: int = 2048
    is_isr: bool = False
