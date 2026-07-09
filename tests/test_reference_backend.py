from __future__ import annotations

import subprocess
from pathlib import Path

from hw_codesign.models import Status
from hw_codesign.reference_backend import build_firmware_reference


def _write_reference_app(project: Path) -> None:
    app = project / "firmware" / "reference"
    app.mkdir(parents=True)
    (app / "CMakeLists.txt").write_text("cmake_minimum_required(VERSION 3.20)\n", encoding="utf-8")


def test_reference_firmware_build_timeout_is_bounded_and_reported(tmp_path, monkeypatch):
    _write_reference_app(tmp_path)
    observed: dict[str, object] = {}
    monkeypatch.setattr("hw_codesign.reference_backend.shutil.which", lambda _: "/usr/bin/cmake")

    def fake_run(command, **kwargs):
        observed["timeout"] = kwargs["timeout"]
        raise subprocess.TimeoutExpired(command, kwargs["timeout"], output=b"partial", stderr=b"still running")

    monkeypatch.setattr("hw_codesign.reference_backend.subprocess.run", fake_run)

    report = build_firmware_reference(tmp_path, timeout_seconds=3)

    assert observed["timeout"] == 3
    assert report.status == Status.BLOCKED
    assert report.failures[0].code == "tool_timeout"
    assert report.failures[0].details["timeout_seconds"] == 3
    assert report.failures[0].details["stderr"] == "still running"
    assert report.backend["stage"] == "configure"
    assert report.backend["timeout_seconds"] == 3


def test_reference_firmware_build_missing_cmake_blocks(tmp_path, monkeypatch):
    _write_reference_app(tmp_path)
    monkeypatch.setattr("hw_codesign.reference_backend.shutil.which", lambda _: None)

    report = build_firmware_reference(tmp_path)

    assert report.status == Status.BLOCKED
    assert report.failures[0].code == "tool_unavailable"
    assert report.backend["available"] is False


def test_reference_firmware_build_missing_source_blocks(tmp_path):
    report = build_firmware_reference(tmp_path)

    assert report.status == Status.BLOCKED
    assert report.failures[0].code == "reference_firmware_missing"
    assert report.failures[0].path == "firmware/reference/CMakeLists.txt"


def test_reference_firmware_build_configure_error_fails(tmp_path, monkeypatch):
    _write_reference_app(tmp_path)
    monkeypatch.setattr("hw_codesign.reference_backend.shutil.which", lambda _: "/usr/bin/cmake")

    def fake_run(command, **kwargs):
        return subprocess.CompletedProcess(command, 1, stdout="configuring", stderr="bad cmake input")

    monkeypatch.setattr("hw_codesign.reference_backend.subprocess.run", fake_run)

    report = build_firmware_reference(tmp_path, timeout_seconds=5)

    assert report.status == Status.FAIL
    assert report.failures[0].code == "configure_failure"
    assert report.failures[0].message == "bad cmake input"
    assert report.backend["returncode"] == 1
