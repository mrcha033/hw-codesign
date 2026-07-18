from __future__ import annotations

import subprocess
from pathlib import Path

from hw_codesign.backends import zephyr
from hw_codesign.backends.command import ToolResult
from hw_codesign.backends.zephyr import ArmNewlibProbe, ZephyrBackend, probe_arm_newlib
from hw_codesign.models import Status


def _arm_toolchain(root: Path) -> tuple[Path, dict[str, Path]]:
    compiler = root / "bin" / "arm-none-eabi-gcc"
    compiler.parent.mkdir(parents=True)
    compiler.write_text("compiler placeholder\n", encoding="utf-8")
    files = {name: root / "arm-none-eabi" / "lib" / name for name in ("nosys.specs", "libc.a", "libnosys.a")}
    for artifact in files.values():
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text("placeholder\n", encoding="utf-8")
    return compiler, files


def _zephyr_project(tmp_path: Path) -> tuple[Path, Path]:
    root = tmp_path / "workspace"
    project = root / "projects" / "demo"
    (project / "firmware" / "zephyr" / "app").mkdir(parents=True)
    zephyr_base = root / ".toolchains" / "zephyr"
    for module in ("hal/stm32", "hal/cmsis_6", "hal/rpi_pico"):
        (zephyr_base / "modules" / module).mkdir(parents=True)
    return project, zephyr_base


def test_probe_arm_newlib_prefers_hw_override_and_resolves_required_files(tmp_path, monkeypatch):
    preferred_root = tmp_path / "preferred"
    compiler, artifacts = _arm_toolchain(preferred_root)
    monkeypatch.setenv("HW_ARM_TOOLCHAIN_ROOT", str(preferred_root))
    monkeypatch.setenv("GNUARMEMB_TOOLCHAIN_PATH", str(tmp_path / "ignored"))

    def fake_run(command, **kwargs):
        filename = command[1].split("=", 1)[1]
        return subprocess.CompletedProcess(command, 0, stdout=f"{artifacts[filename]}\n", stderr="")

    monkeypatch.setattr(zephyr.subprocess, "run", fake_run)

    probe = probe_arm_newlib()

    assert probe.available is True
    assert probe.compiler == str(compiler)
    assert probe.toolchain_root == str(preferred_root)
    assert probe.source == "HW_ARM_TOOLCHAIN_ROOT"
    assert probe.explicit_root is True
    assert probe.files == {name: str(path) for name, path in artifacts.items()}
    assert probe.missing == ()


def test_probe_arm_newlib_rejects_bare_names_and_missing_paths(tmp_path, monkeypatch):
    toolchain_root = tmp_path / "toolchain"
    _, artifacts = _arm_toolchain(toolchain_root)
    missing_libc = tmp_path / "does-not-exist" / "libc.a"

    def fake_run(command, **kwargs):
        filename = command[1].split("=", 1)[1]
        reported = {
            "nosys.specs": "nosys.specs",
            "libc.a": str(missing_libc),
            "libnosys.a": str(artifacts["libnosys.a"]),
        }[filename]
        return subprocess.CompletedProcess(command, 0, stdout=f"{reported}\n", stderr="")

    monkeypatch.setattr(zephyr.subprocess, "run", fake_run)

    probe = probe_arm_newlib(toolchain_root)

    assert probe.available is False
    assert probe.missing == ("nosys.specs", "libc.a")
    assert probe.files["nosys.specs"] == "nosys.specs"
    assert probe.files["libc.a"] == str(missing_libc)


def test_zephyr_build_blocks_incomplete_arm_newlib_before_cmake(tmp_path, monkeypatch):
    project, _ = _zephyr_project(tmp_path)
    probe = ArmNewlibProbe(
        compiler="/opt/toolchain/bin/arm-none-eabi-gcc",
        toolchain_root="/opt/toolchain",
        source="PATH",
        explicit_root=False,
        files={"nosys.specs": "nosys.specs", "libc.a": "libc.a", "libnosys.a": "libnosys.a"},
        missing=("nosys.specs", "libc.a", "libnosys.a"),
    )
    monkeypatch.setattr(zephyr, "probe_arm_newlib", lambda: probe)
    monkeypatch.setattr(zephyr, "run_tool", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("cmake must not run")))

    report = ZephyrBackend().build(project, "rp2040_usb_device")

    assert report.status == Status.BLOCKED
    assert report.failures[0].code == "arm_newlib_unavailable"
    assert report.failures[0].details["missing"] == ["nosys.specs", "libc.a", "libnosys.a"]
    assert report.backend["arm_newlib_probe"]["available"] is False


def test_zephyr_build_blocks_missing_arm_compiler_with_bundled_zephyr(tmp_path, monkeypatch):
    project, _ = _zephyr_project(tmp_path)
    probe = ArmNewlibProbe(
        compiler=None,
        toolchain_root=None,
        source="PATH",
        explicit_root=False,
        files={},
        missing=("nosys.specs", "libc.a", "libnosys.a"),
        error="arm-none-eabi-gcc was not found on PATH",
    )
    monkeypatch.setattr(zephyr, "probe_arm_newlib", lambda: probe)
    monkeypatch.setattr(zephyr, "run_tool", lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("west must not run")))

    report = ZephyrBackend().build(project, "rp2040_usb_device")

    assert report.status == Status.BLOCKED
    assert report.failures[0].code == "arm_newlib_unavailable"
    assert report.failures[0].details["compiler"] is None
    assert report.failures[0].details["error"] == "arm-none-eabi-gcc was not found on PATH"


def test_zephyr_build_passes_probed_explicit_root_to_cmake(tmp_path, monkeypatch):
    project, _ = _zephyr_project(tmp_path)
    stale_cache = project / "firmware" / "zephyr" / "build" / "bootloader" / "CMakeCache.txt"
    stale_cache.parent.mkdir(parents=True)
    stale_cache.write_text("CMAKE_C_COMPILER=/stale/compiler\n", encoding="utf-8")
    outside_marker = project / "firmware" / "zephyr" / "outside-build.marker"
    outside_marker.write_text("preserve\n", encoding="utf-8")
    toolchain_root = tmp_path / "native-arm"
    compiler, artifacts = _arm_toolchain(toolchain_root)
    probe = ArmNewlibProbe(
        compiler=str(compiler),
        toolchain_root=str(toolchain_root),
        source="HW_ARM_TOOLCHAIN_ROOT",
        explicit_root=True,
        files={name: str(path) for name, path in artifacts.items()},
        missing=(),
    )
    calls: list[dict[str, object]] = []

    def fake_run_tool(executable, arguments, cwd, timeout=300, env=None):
        calls.append({"executable": executable, "arguments": arguments, "cwd": cwd, "timeout": timeout, "env": env})
        return ToolResult([executable, *arguments], 0, "", "", True)

    monkeypatch.setattr(zephyr, "probe_arm_newlib", lambda: probe)
    monkeypatch.setattr(zephyr, "run_tool", fake_run_tool)

    report = ZephyrBackend().build(project, "rp2040_usb_device")

    assert report.status == Status.PASS
    assert len(calls) == 2
    assert calls[0]["arguments"][0] == "--fresh"
    assert all(call["env"]["GNUARMEMB_TOOLCHAIN_PATH"] == str(toolchain_root) for call in calls)
    assert not stale_cache.exists()
    assert outside_marker.read_text(encoding="utf-8") == "preserve\n"
    assert report.backend["arm_newlib_probe"]["available"] is True
    assert report.backend["build_directory_reset"] == {
        "path": str(project / "firmware" / "zephyr" / "build"),
        "removed_existing": True,
        "strategy": "delete_generated_build_before_configure",
    }
