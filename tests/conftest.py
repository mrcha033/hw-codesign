from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from hw_codesign.service import HardwareService


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

