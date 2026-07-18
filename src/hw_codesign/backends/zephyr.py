from __future__ import annotations

import os
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from ..models import Failure, FailureCategory, GateReport, Status
from .command import run_tool, tool_report

# Boards whose Zephyr build requires the xtensa toolchain rather than ARM GCC.
# The bundled toolchain only ships arm-none-eabi-gcc; xtensa boards are BLOCKED.
_XTENSA_BOARDS = frozenset({
    "esp32", "esp32s2", "esp32s3", "esp32s3_devkitc", "esp32s3_devkitm",
    "esp32c3", "esp32c6",
})

# Board-family → extra Zephyr module directories (relative to zephyr_base/modules/).
# stm32 + cmsis_6 are always included for ARM builds.
_BOARD_EXTRA_MODULES: dict[str, list[str]] = {
    "nrf": ["hal_nordic"],
    "nordic": ["hal_nordic"],
    "nrf52": ["hal_nordic"],
    "nrf52840": ["hal_nordic"],
    "nrf52840dk": ["hal_nordic"],
    "nrf5340": ["hal_nordic"],
    "rp2040": ["hal/rpi_pico"],
}

_ARM_NEWLIB_FILES = ("nosys.specs", "libc.a", "libnosys.a")


@dataclass(frozen=True)
class ArmNewlibProbe:
    """Result of asking an ARM GCC driver for its required newlib artifacts."""

    compiler: str | None
    toolchain_root: str | None
    source: str
    explicit_root: bool
    files: dict[str, str]
    missing: tuple[str, ...]
    error: str | None = None

    @property
    def available(self) -> bool:
        return self.compiler is not None and not self.missing and self.error is None

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["missing"] = list(self.missing)
        payload["available"] = self.available
        return payload


def _compiler_in_toolchain_root(root: Path) -> Path | None:
    """Resolve GCC from either a GNU Arm root, its bin directory, or a direct path."""
    executable_names = ("arm-none-eabi-gcc.exe", "arm-none-eabi-gcc") if os.name == "nt" else ("arm-none-eabi-gcc",)
    if root.is_file() and root.name in executable_names:
        return root
    candidates = [*(root / "bin" / name for name in executable_names), *(root / name for name in executable_names)]
    return next((candidate for candidate in candidates if candidate.is_file()), None)


def probe_arm_newlib(toolchain_root: Path | None = None) -> ArmNewlibProbe:
    """Verify that ARM GCC can resolve the newlib files required by Zephyr.

    GCC deliberately echoes an unresolved ``-print-file-name`` argument as a
    bare filename.  Treat that response, an absent path, or a compiler that
    cannot execute on this host as unavailable instead of discovering the
    incomplete installation halfway through a native build.
    """
    source = "PATH"
    explicit_root = toolchain_root is not None
    selected_root = toolchain_root
    if selected_root is None:
        for variable in ("HW_ARM_TOOLCHAIN_ROOT", "GNUARMEMB_TOOLCHAIN_PATH"):
            value = os.environ.get(variable)
            if value:
                selected_root = Path(value).expanduser()
                source = variable
                explicit_root = True
                break
    else:
        source = "argument"

    compiler_path: Path | None
    if selected_root is not None:
        # CMake runs from the project directory, so preserve the caller's
        # meaning by converting a repo-relative override to an absolute root.
        selected_root = Path(os.path.abspath(selected_root.expanduser()))
        compiler_path = _compiler_in_toolchain_root(selected_root)
        if compiler_path is None:
            return ArmNewlibProbe(
                compiler=None,
                toolchain_root=str(selected_root),
                source=source,
                explicit_root=explicit_root,
                files={},
                missing=_ARM_NEWLIB_FILES,
                error=f"No arm-none-eabi-gcc executable was found under {selected_root}",
            )
    else:
        resolved = shutil.which("arm-none-eabi-gcc")
        compiler_path = Path(os.path.abspath(resolved)) if resolved else None
        if compiler_path is None:
            return ArmNewlibProbe(
                compiler=None,
                toolchain_root=None,
                source=source,
                explicit_root=False,
                files={},
                missing=_ARM_NEWLIB_FILES,
                error="arm-none-eabi-gcc was not found on PATH",
            )
        selected_root = compiler_path.parent.parent

    files: dict[str, str] = {}
    missing: list[str] = []
    errors: list[str] = []
    for filename in _ARM_NEWLIB_FILES:
        try:
            completed = subprocess.run(
                [str(compiler_path), f"-print-file-name={filename}"],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            missing.append(filename)
            errors.append(f"{filename}: {exc}")
            continue

        reported = completed.stdout.strip()
        if reported:
            files[filename] = reported
        if completed.returncode != 0:
            missing.append(filename)
            detail = completed.stderr.strip() or f"compiler exited with status {completed.returncode}"
            errors.append(f"{filename}: {detail}")
            continue
        # GCC echoes the bare input name when it cannot resolve the file.
        if reported == filename or not reported or not Path(reported).expanduser().is_file():
            missing.append(filename)

    return ArmNewlibProbe(
        compiler=str(compiler_path),
        toolchain_root=str(selected_root),
        source=source,
        explicit_root=explicit_root,
        files=files,
        missing=tuple(missing),
        error="; ".join(errors) or None,
    )


def _board_family(board: str) -> str:
    """Return a normalised family prefix for module selection."""
    # Strip Zephyr 4.x board revision suffix (e.g. "nrf52840dk/nrf52840" → "nrf52840dk")
    base = board.lower().split("/")[0]
    return base.split("_")[0] if "_" in base else base


def _with_arm_probe(
    report: GateReport,
    probe: ArmNewlibProbe,
    build_reset: dict[str, object] | None = None,
) -> GateReport:
    report.backend["arm_newlib_probe"] = probe.to_dict()
    if build_reset is not None:
        report.backend["build_directory_reset"] = build_reset
    return report


def _reset_generated_build_directory(build: Path) -> dict[str, object]:
    """Start native builds without reusing nested CMake ExternalProject state.

    ``cmake --fresh`` resets the top-level cache only.  RP2040's second-stage
    bootloader has its own cache below ``build/bootloader``; keeping that cache
    can silently retain an old compiler or omit ``FLASH_TYPE``.  The entire
    directory is generated output, so constrain cleanup to that exact path.
    """
    removed_existing = build.exists() or build.is_symlink()
    if build.is_symlink() or build.is_file():
        build.unlink()
    elif build.exists():
        shutil.rmtree(build)
    return {
        "path": str(build),
        "removed_existing": removed_existing,
        "strategy": "delete_generated_build_before_configure",
    }


class ZephyrBackend:
    def build(self, project: Path, board: str) -> GateReport:
        app = project / "firmware" / "zephyr" / "app"
        build = project / "firmware" / "zephyr" / "build"

        if not app.is_dir():
            return GateReport(
                "native_zephyr_build",
                Status.BLOCKED,
                [Failure(FailureCategory.TOOL_ERROR, "no_zephyr_app", "No firmware/zephyr/app directory — project does not use Zephyr")],
            )

        platform_root = Path(os.environ.get("HW_TOOLCHAIN_ROOT", project.parents[1]))
        zephyr_base = platform_root / ".toolchains" / "zephyr"

        # "unknown" means the project spec has no firmware.target → not a Zephyr project.
        if board.lower() in {"unknown", "", "none"}:
            return GateReport(
                "native_zephyr_build",
                Status.BLOCKED,
                [Failure(FailureCategory.TOOL_ERROR, "no_zephyr_target",
                         "Project spec has no firmware.target — project does not use Zephyr as its primary RTOS")],
            )

        # Xtensa (ESP32) boards require a different toolchain — not currently bundled.
        board_lower = board.lower()
        if any(board_lower.startswith(x) or board_lower == x for x in _XTENSA_BOARDS):
            return GateReport(
                "native_zephyr_build",
                Status.BLOCKED,
                [Failure(FailureCategory.TOOL_ERROR, "xtensa_toolchain_unavailable",
                         f"Board {board!r} requires the xtensa-esp toolchain which is not in the bundled toolchain set")],
            )

        arm_probe = probe_arm_newlib()
        if not arm_probe.available and (arm_probe.explicit_root or zephyr_base.is_dir()):
            details = arm_probe.to_dict()
            return GateReport(
                "native_zephyr_build",
                Status.BLOCKED,
                [Failure(
                    FailureCategory.TOOL_ERROR,
                    "arm_newlib_unavailable",
                    "The selected ARM GCC cannot resolve the newlib runtime required by Zephyr",
                    details=details,
                )],
                backend={"arm_newlib_probe": details},
            )

        if zephyr_base.is_dir() and arm_probe.available:
            stm32_mod = zephyr_base / "modules" / "hal" / "stm32"
            cmsis_6_mod = zephyr_base / "modules" / "hal" / "cmsis_6"
            base_modules = [stm32_mod, cmsis_6_mod] if stm32_mod.is_dir() and cmsis_6_mod.is_dir() else []

            family = _board_family(board)
            extra_names = _BOARD_EXTRA_MODULES.get(family, [])
            extra_modules = []
            for name in extra_names:
                candidate = zephyr_base / "modules" / name
                if candidate.is_dir():
                    extra_modules.append(candidate)

            all_modules = base_modules + extra_modules
            if all_modules:
                build_reset = _reset_generated_build_directory(build)
                # Include the project's custom board directory so project-specific
                # board definitions (e.g. boards/arm/ble_sensor_node/) are found.
                project_boards = project / "firmware" / "zephyr" / "boards"
                arguments = [
                    "--fresh", "-S", str(app), "-B", str(build), "-G", "Ninja", f"-DBOARD={board}",
                    f"-DZEPHYR_MODULES={';'.join(str(m) for m in all_modules)}",
                    f"-DPython3_EXECUTABLE={sys.executable}",
                ]
                if project_boards.is_dir():
                    arguments.append(f"-DBOARD_ROOT={project / 'firmware' / 'zephyr'}")
                if cmsis_6_mod.is_dir():
                    arguments += [
                        f"-DZEPHYR_CMSIS_6_MODULE_DIR={cmsis_6_mod}",
                        f"-DZEPHYR_CMSIS_6_CMAKE_DIR={zephyr_base / 'modules' / 'cmsis_6'}",
                    ]
                env = {
                    "ZEPHYR_BASE": str(zephyr_base),
                    "ZEPHYR_TOOLCHAIN_VARIANT": "gnuarmemb",
                    "GNUARMEMB_TOOLCHAIN_PATH": str(arm_probe.toolchain_root),
                }
                configure = run_tool("cmake", arguments, project, timeout=600, env=env)
                if not configure.available:
                    return _with_arm_probe(tool_report("native_zephyr_build", configure), arm_probe, build_reset)
                if configure.returncode != 0:
                    combined = configure.stdout + configure.stderr
                    if (
                        "No board named" in combined
                        or "not found" in combined and "board" in combined.lower()
                        or "Board qualifiers" in combined
                        or "BOARD_NOT_FOUND" in combined
                    ):
                        return GateReport(
                            "native_zephyr_build",
                            Status.BLOCKED,
                            [Failure(FailureCategory.TOOL_ERROR, "board_not_in_sdk",
                                     f"Board {board!r} is not in the installed Zephyr SDK — install the matching board support package")],
                            backend={"command": configure.command, "returncode": configure.returncode,
                                     "stderr": configure.stderr[-4000:], "arm_newlib_probe": arm_probe.to_dict(),
                                     "build_directory_reset": build_reset},
                        )
                    return _with_arm_probe(tool_report("native_zephyr_build", configure), arm_probe, build_reset)
                result = run_tool("cmake", ["--build", str(build)], project, timeout=1200, env=env)
                elf = build / "zephyr" / "zephyr.elf"
                return _with_arm_probe(
                    tool_report("native_zephyr_build", result, [str(elf)] if elf.exists() else []),
                    arm_probe,
                    build_reset,
                )

        result = run_tool("west", ["build", "-b", board, str(app), "-d", str(build)], project, timeout=1200)
        return tool_report("native_zephyr_build", result, [str(build / "zephyr" / "zephyr.elf")] if (build / "zephyr" / "zephyr.elf").exists() else [])
