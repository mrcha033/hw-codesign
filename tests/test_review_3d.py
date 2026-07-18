from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from hw_codesign import review_3d


def test_viewer_resource_resolves_from_installed_package(monkeypatch, tmp_path: Path) -> None:
    package = tmp_path / "site-packages" / "hw_codesign"
    package.mkdir(parents=True)
    viewer = package / "review_3d_viewer.js"
    viewer.write_text("export function mount() {}\n", encoding="utf-8")

    monkeypatch.setattr(review_3d, "files", lambda package_name: package)

    assert review_3d._viewer_resource() == viewer


def test_bundle_viewer_uses_package_resource(monkeypatch, tmp_path: Path) -> None:
    package = tmp_path / "site-packages" / "hw_codesign"
    package.mkdir(parents=True)
    viewer = package / "review_3d_viewer.js"
    viewer.write_text("export function mount() {}\n", encoding="utf-8")
    output = tmp_path / "review" / "viewer.js"
    output.parent.mkdir()
    calls: list[tuple[list[str], Path]] = []

    monkeypatch.setattr(review_3d, "files", lambda package_name: package)
    monkeypatch.setattr(review_3d.shutil, "which", lambda executable: "/tools/esbuild")

    def fake_run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        calls.append((command, kwargs["cwd"]))
        output.write_text("window.HWReview3D = {};\n", encoding="utf-8")
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(review_3d.subprocess, "run", fake_run)

    assert review_3d._bundle_viewer(output) is True
    assert calls == [
        (
            [
                "/tools/esbuild",
                str(viewer),
                "--bundle",
                "--format=iife",
                "--global-name=HWReview3D",
                "--target=es2020",
                "--minify",
                f"--outfile={output}",
            ],
            package,
        )
    ]


def test_bundle_viewer_copies_prebuilt_resource_without_node(monkeypatch, tmp_path: Path) -> None:
    package = tmp_path / "site-packages" / "hw_codesign"
    package.mkdir(parents=True)
    bundled = package / "review_3d_viewer.bundle.js"
    bundled.write_bytes(b"/*! Three.js MIT License */\nwindow.HWReview3D = {};\n")
    output = tmp_path / "review" / "viewer.js"
    output.parent.mkdir()

    monkeypatch.setattr(review_3d, "files", lambda package_name: package)
    monkeypatch.setattr(review_3d.shutil, "which", lambda executable: None)
    monkeypatch.setattr(
        review_3d.subprocess,
        "run",
        lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("esbuild must not run")),
    )

    assert review_3d._bundle_viewer(output) is True
    assert output.read_bytes() == bundled.read_bytes()


def test_viewer_resource_prefers_pyinstaller_data(monkeypatch, tmp_path: Path) -> None:
    frozen = tmp_path / "_MEIPASS" / "hw_codesign" / "review_3d_viewer.bundle.js"
    frozen.parent.mkdir(parents=True)
    frozen.write_text("export function mount() {}\n", encoding="utf-8")
    monkeypatch.setattr(review_3d.sys, "_MEIPASS", str(tmp_path / "_MEIPASS"), raising=False)
    monkeypatch.setattr(
        review_3d,
        "files",
        lambda package_name: (_ for _ in ()).throw(AssertionError("package lookup should not run")),
    )

    assert review_3d._viewer_bundle_resource() == frozen


def test_prebuilt_viewer_receipt_matches_packaged_source_and_license() -> None:
    root = Path(__file__).resolve().parents[1]
    bundle = root / "src" / "hw_codesign" / "review_3d_viewer.bundle.js"
    receipt = json.loads((root / "src" / "hw_codesign" / "review_3d_viewer.bundle.json").read_text(encoding="utf-8"))
    assert hashlib.sha256(bundle.read_bytes()).hexdigest() == receipt["bundle_sha256"]

    inputs = {record["path"]: record["sha256"] for record in receipt["inputs"]}
    source = root / "src" / "hw_codesign" / "review_3d_viewer.js"
    assert hashlib.sha256(source.read_bytes()).hexdigest() == inputs["src/hw_codesign/review_3d_viewer.js"]

    three_license = root / "src" / "hw_codesign" / "third_party" / "three" / "LICENSE"
    three_receipt = next(record for record in receipt["licenses"] if record["component"] == "three")
    assert hashlib.sha256(three_license.read_bytes()).hexdigest() == three_receipt["sha256"]
    assert b"Three.js MIT License" in bundle.read_bytes()[:2000]


def test_prebuilt_viewer_rebuild_is_deterministic() -> None:
    root = Path(__file__).resolve().parents[1]
    if shutil.which("node") is None or not (root / "node_modules" / "esbuild" / "bin" / "esbuild").is_file():
        pytest.skip("npm build toolchain is not installed")
    result = subprocess.run(
        [sys.executable, str(root / "scripts" / "build_review_3d_viewer.py"), "--check"],
        cwd=root,
        capture_output=True,
        text=True,
        timeout=90,
        check=False,
    )
    assert result.returncode == 0, result.stderr or result.stdout
