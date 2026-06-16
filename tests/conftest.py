from __future__ import annotations

import os
import shutil
from pathlib import Path

import pytest

from hw_codesign.service import HardwareService

_BUNDLED_KICAD_SYMBOLS = Path(__file__).parents[1] / "parts" / "kicad_symbols"

_KICAD_SYSTEM_PATHS = [
    Path("/usr/share/kicad/symbols"),
    Path("/usr/local/share/kicad/symbols"),
    Path.home() / ".local/share/kicad/symbols",
    Path("C:/Program Files/KiCad"),
    Path("C:/Program Files (x86)/KiCad"),
    Path.home() / "Documents/KiCad/symbols",
]


def _kicad_symbols_available() -> bool:
    if os.environ.get("KICAD_SYMBOL_DIR") or os.environ.get("KICAD8_SYMBOL_DIR") or os.environ.get("KICAD7_SYMBOL_DIR"):
        return True
    return any(p.exists() for p in _KICAD_SYSTEM_PATHS)


@pytest.fixture(autouse=True, scope="session")
def _ensure_kicad_symbols(tmp_path_factory: pytest.TempPathFactory) -> None:
    if not _kicad_symbols_available():
        os.environ["KICAD_SYMBOL_DIR"] = str(_BUNDLED_KICAD_SYMBOLS)


@pytest.fixture
def service(tmp_path: Path) -> HardwareService:
    source_schemas = Path(__file__).parents[1] / "schemas"
    shutil.copytree(source_schemas, tmp_path / "schemas")
    return HardwareService(tmp_path)


@pytest.fixture
def project(service: HardwareService) -> str:
    name = "quadruped_robot_controller"
    service.create_project(name)
    return name

