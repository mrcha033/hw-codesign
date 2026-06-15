from __future__ import annotations

import sysconfig
from pathlib import Path


def resource_root(workspace_root: Path) -> Path:
    """Locate repository resources or their wheel-installed fallback."""
    if (workspace_root / "schemas").is_dir() and (workspace_root / "parts").is_dir():
        return workspace_root
    source_root = Path(__file__).resolve().parents[2]
    if (source_root / "schemas").is_dir() and (source_root / "parts").is_dir():
        return source_root
    return Path(sysconfig.get_path("data")) / "share" / "hw-codesign"
