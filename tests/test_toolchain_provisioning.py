from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HAL_RPI_PICO_REVISION = "7b57b24588797e6e7bf18b6bda168e6b96374264"


def _text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_macos_bootstrap_rejects_compiler_without_arm_newlib() -> None:
    script = _text("scripts/bootstrap_toolchains.sh")

    assert "brew install arm-none-eabi-gcc" not in script
    assert "-print-file-name=nosys.specs" in script
    assert '[[ "$specs" == "nosys.specs" || ! -f "$specs" ]]' in script
    assert "arm-gnu-toolchain-downloads" in script


def test_all_provisioners_pin_the_zephyr_42_rpi_pico_hal() -> None:
    for path in (
        "scripts/bootstrap_toolchains.sh",
        "docker/Dockerfile",
        ".github/workflows/ci.yml",
    ):
        provisioner = _text(path)
        assert HAL_RPI_PICO_REVISION in provisioner, path
        assert "hal_rpi_pico.git" in provisioner, path


def test_linux_provisioners_install_and_verify_arm_newlib() -> None:
    dockerfile = _text("docker/Dockerfile")
    workflow = _text(".github/workflows/ci.yml")

    for path, provisioner in (("docker/Dockerfile", dockerfile), (".github/workflows/ci.yml", workflow)):
        assert "libnewlib-arm-none-eabi" in provisioner, path
        assert "-print-file-name=nosys.specs" in provisioner, path
        assert "test -f" in provisioner, path


def test_ubuntu_2404_container_avoids_unavailable_freecad_package() -> None:
    dockerfile = _text("docker/Dockerfile")

    assert dockerfile.startswith("FROM ubuntu:24.04\n")
    assert " freecad" not in dockerfile
    assert "cadquery-ocp" in _text("pyproject.toml")


def test_ci_has_a_bounded_native_rp2040_zephyr_gate() -> None:
    workflow = _text(".github/workflows/ci.yml")

    assert "native-zephyr-rp2040:" in workflow
    assert "timeout-minutes: 30" in workflow
    assert 'ZephyrBackend().build(project, "rp2040_usb_device")' in workflow
    assert 'report.status is not Status.PASS' in workflow
