from __future__ import annotations

from pathlib import Path

import pytest

from hw_codesign.errors import InvalidProjectNameError
from hw_codesign.workspace import SUPPORTED_TEMPLATES


def test_create_project_builds_full_workspace(service):
    result = service.create_project("robot_controller")
    path = Path(result["project_path"])
    assert result["status"] == "generated"
    assert (path / "spec" / "system.yaml").is_file()
    assert (path / "electronics" / "generated" / "kicad").is_dir()
    assert (path / "mechanical" / "generated" / "drawings").is_dir()
    assert (path / "firmware" / "zephyr" / "tests").is_dir()
    assert (path / "validation" / "reports").is_dir()
    assert (path / "history" / "iterations").is_dir()


@pytest.mark.parametrize("template", sorted(SUPPORTED_TEMPLATES))
def test_every_supported_template_conforms_to_current_spec_schemas(service, template):
    project = f"{template}_schema_check"
    service.create_project(project, template=template)

    report = service.validator.validate_spec(service.read_spec(project))

    assert report.status.value == "pass", [failure.__dict__ for failure in report.failures]


def test_project_name_prevents_path_traversal(service):
    with pytest.raises(InvalidProjectNameError):
        service.create_project("../../escape")


def test_snapshot_is_monotonic(service, project):
    assert service.workspace.snapshot(project) == "0001"
    assert service.workspace.snapshot(project) == "0002"
