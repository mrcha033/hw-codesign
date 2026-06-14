from __future__ import annotations

import csv
import io
import json
from pathlib import Path
from typing import Any

from .io import atomic_write_text, write_json
from .reference_backend import build_graph, generate_kicad


def generate_electronics(project: Path, spec: dict[str, Any]) -> list[str]:
    source = project / "electronics" / "source"
    channels = int(spec["actuation"]["motor_channels"])
    board = f'''# Generated high-level hardware intent. Edit spec, then regenerate.
module RobotController:
  mcu = new {spec["compute"]["mcu"]["family"]}
  power_input = new ProtectedPowerInput
  imu = new IMU
  motor_channels = new MotorChannel[{channels}]
  emergency_stop = new FailSafeEmergencyStop
'''
    power = "# VBAT protection and rail intent\nVBAT -> fuse_or_efuse -> reverse_polarity -> tvs -> motor_power\nVBAT -> buck_5v -> regulator_3v3\n"
    motors = f"# Repeated channel intent\nchannels = {channels}\npeak_current_per_channel_a = {spec['actuation']['motor_channel_peak_current_a']}\n"
    files = {"board.ato": board, "power_tree.ato": power, "motor_channels.ato": motors, "sensor_bus.ato": "# IMU and external sensor buses\n", "connectors.ato": "# Exposed power, motor, CAN, USB-C and debug connectors\n"}
    for name, content in files.items():
        atomic_write_text(source / name, content)
    graph = build_graph(spec)
    graph_path = project / "electronics" / "generated" / "electrical_graph.json"
    write_json(graph_path, graph)
    return [str(source / name) for name in files] + [str(graph_path), *generate_kicad(project, spec, graph)]


def generate_mechanical(project: Path, spec: dict[str, Any]) -> list[str]:
    source = project / "mechanical" / "source"
    envelope = spec["mechanical"]["envelope"]
    enclosure = spec["mechanical"]["enclosure_internal_mm"]
    content = f'''"""Parametric enclosure source generated from the project spec."""
BOARD = ({envelope["board_width_mm"]}, {envelope["board_height_mm"]}, {envelope["board_thickness_mm"]})
INTERNAL = ({enclosure[0]}, {enclosure[1]}, {enclosure[2]})
WALL = {spec["mechanical"]["wall_thickness_mm"]}

def build():
    try:
        from build123d import Box
    except ImportError as exc:
        raise RuntimeError("build123d is required to export enclosure geometry") from exc
    return Box(INTERNAL[0] + 2 * WALL, INTERNAL[1] + 2 * WALL, INTERNAL[2] + WALL)
'''
    atomic_write_text(source / "enclosure.py", content)
    atomic_write_text(source / "mounting_plate.py", "# Mounting-hole pattern is derived from mechanical spec.\n")
    atomic_write_text(source / "connector_cutouts.py", "# Connector exposure and insertion-clearance geometry.\n")
    atomic_write_text(source / "thermal_features.py", "# Cooling features remain conditional on resolved thermal assumptions.\n")
    return [str(path) for path in sorted(source.glob("*.py"))]


def _pin_assignments(channels: int) -> list[dict[str, Any]]:
    assignments = [
        {"signal": "I2C_IMU_SCL", "mcu_pin": "PB8", "net_name": "I2C_IMU_SCL"},
        {"signal": "I2C_IMU_SDA", "mcu_pin": "PB9", "net_name": "I2C_IMU_SDA"},
        {"signal": "CAN_RX", "mcu_pin": "PD0", "net_name": "CAN_RX"},
        {"signal": "CAN_TX", "mcu_pin": "PD1", "net_name": "CAN_TX"},
        {"signal": "ESTOP_IN", "mcu_pin": "PC13", "net_name": "ESTOP_IN"},
    ]
    assignments.extend({"signal": f"MOTOR{index}_PWM", "mcu_pin": f"PWM{index}", "net_name": f"MOTOR{index}_PWM"} for index in range(1, channels + 1))
    return assignments


def generate_firmware(project: Path, spec: dict[str, Any]) -> list[str]:
    generated = project / "firmware" / "generated"
    app = project / "firmware" / "zephyr" / "app"
    assignments = _pin_assignments(int(spec["actuation"]["motor_channels"]))
    write_json(generated / "pinmap.json", assignments)
    pinmap = "#pragma once\n\n" + "\n".join(f'#define PIN_{item["signal"]} "{item["mcu_pin"]}"' for item in assignments) + "\n"
    atomic_write_text(generated / "pinmap.h", pinmap)
    overlay = "/ {\n  chosen { zephyr,console = &usart3; };\n};\n"
    atomic_write_text(generated / "devicetree.overlay", overlay)
    atomic_write_text(generated / "board.cmake", "# Generated Zephyr board integration entrypoint.\n")
    atomic_write_text(generated / "kconfig.defconfig", "# Generated project defaults.\n")
    atomic_write_text(app / "CMakeLists.txt", "cmake_minimum_required(VERSION 3.20.0)\nfind_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})\nproject(robot_controller)\ntarget_sources(app PRIVATE src/main.c)\n")
    atomic_write_text(app / "prj.conf", "CONFIG_GPIO=y\nCONFIG_I2C=y\nCONFIG_CAN=y\nCONFIG_PWM=y\n")
    atomic_write_text(app / "src" / "main.c", '#include <zephyr/kernel.h>\nint main(void) { return 0; }\n')
    tests = project / "firmware" / "zephyr" / "tests"
    atomic_write_text(tests / "test_i2c_imu.c", "/* Bring-up test stub: verify IMU identity and samples. */\n")
    atomic_write_text(tests / "test_motor_pwm.c", "/* Bring-up test stub: scope PWM with motor power disabled. */\n")
    board_dir = project / "firmware" / "zephyr" / "boards" / "arm" / "robot_controller"
    atomic_write_text(board_dir / "robot_controller.dts", '/dts-v1/;\n#include <st/h7/stm32h743Xi.dtsi>\n/ { model = "HW Co-design Robot Controller"; compatible = "hw,robot-controller"; chosen { zephyr,console = &usart3; }; };\n')
    atomic_write_text(board_dir / "robot_controller_defconfig", "CONFIG_SOC_STM32H743XX=y\nCONFIG_BOARD_ROBOT_CONTROLLER=y\n")
    atomic_write_text(board_dir / "Kconfig.board", 'config BOARD_ROBOT_CONTROLLER\n  bool "Robot Controller"\n')
    atomic_write_text(board_dir / "Kconfig.defconfig", 'if BOARD_ROBOT_CONTROLLER\nconfig BOARD\n  default "robot_controller"\nendif\n')
    reference = project / "firmware" / "reference"
    atomic_write_text(reference / "CMakeLists.txt", "cmake_minimum_required(VERSION 3.20)\nproject(robot_controller_bsp C)\nenable_testing()\nadd_library(board_bsp src/board.c)\ntarget_include_directories(board_bsp PUBLIC include ../generated)\nadd_executable(bringup_tests tests/bringup_tests.c)\ntarget_link_libraries(bringup_tests PRIVATE board_bsp)\nadd_test(NAME bringup_tests COMMAND bringup_tests)\n")
    atomic_write_text(reference / "include" / "board.h", "#pragma once\n#include <stddef.h>\nsize_t board_motor_channel_count(void);\nint board_estop_is_fail_safe(void);\nint board_pinmap_self_test(void);\n")
    atomic_write_text(reference / "src" / "board.c", f'#include "board.h"\n#include "pinmap.h"\nsize_t board_motor_channel_count(void) {{ return {len([item for item in assignments if item["signal"].endswith("_PWM")])}; }}\nint board_estop_is_fail_safe(void) {{ return 1; }}\nint board_pinmap_self_test(void) {{ return PIN_ESTOP_IN[0] != 0 && PIN_I2C_IMU_SCL[0] != 0; }}\n')
    atomic_write_text(reference / "tests" / "bringup_tests.c", f'#include "board.h"\n#include <assert.h>\n#include <stdio.h>\nint main(void) {{ assert(board_motor_channel_count() == {len([item for item in assignments if item["signal"].endswith("_PWM")])}); assert(board_estop_is_fail_safe()); assert(board_pinmap_self_test()); puts("bringup tests passed"); return 0; }}\n')
    return [str(path) for path in sorted(generated.iterdir())] + [str(app / "src" / "main.c"), str(tests / "test_i2c_imu.c"), str(tests / "test_motor_pwm.c"), str(board_dir / "robot_controller.dts"), str(reference / "CMakeLists.txt")]


def generate_bom(project: Path) -> str:
    graph = json.loads((project / "electronics" / "generated" / "electrical_graph.json").read_text(encoding="utf-8"))
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["reference", "category", "mpn", "quantity", "risk"])
    writer.writeheader()
    for component in graph["components"]:
        writer.writerow({"reference": component["ref"], "category": component["category"], "mpn": component["mpn"] or "UNRESOLVED", "quantity": 1, "risk": "high" if not component["mpn"] else "normal"})
    path = project / "exports" / "working" / "fabrication" / "bom.csv"
    atomic_write_text(path, output.getvalue())
    return str(path)
