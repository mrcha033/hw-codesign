from __future__ import annotations

from typing import Any

from . import periodic_transmit, sensor_poll, state_machine, timeout_shutdown
from ._base import ModuleOutput

_RENDERERS = {
    "timeout_shutdown": timeout_shutdown.render,
    "periodic_transmit": periodic_transmit.render,
    "state_machine": state_machine.render,
    "sensor_poll": sensor_poll.render,
}

BEHAVIOR_DESCRIPTIONS: dict[str, str] = {
    "timeout_shutdown": (
        "Watchdog pattern: arms a timer on init; if not kicked within timeout_ms "
        "or the trigger signal asserts, disables the specified outputs and asserts a fault pin."
    ),
    "periodic_transmit": (
        "Scheduled frame transmit: sends a CAN/UART/I2C frame on a fixed interval. "
        "Frame ID, DLC, and content are parametric."
    ),
    "state_machine": (
        "Agent-specified state machine: states, transitions, and entry/exit actions are "
        "parameterized; generates a thread-safe enum-based FSM."
    ),
    "sensor_poll": (
        "Scheduled ADC/I2C/SPI read: polls a sensor every poll_interval_ms and writes "
        "readings into a fixed-size ring buffer."
    ),
}

BEHAVIOR_SCHEMAS: dict[str, dict[str, Any]] = {
    "timeout_shutdown": {
        "type": "object",
        "required": ["id", "behavior", "trigger", "action"],
        "properties": {
            "id":       {"type": "string", "description": "Module identifier (used as C symbol prefix and file name)"},
            "behavior": {"type": "string", "const": "timeout_shutdown"},
            "trigger": {
                "type": "object",
                "properties": {
                    "signal":     {"type": "string", "description": "GPIO signal name from pinmap (e.g. ESTOP_IN)"},
                    "timeout_ms": {"type": "integer", "description": "Watchdog timeout in milliseconds"},
                },
                "required": ["signal", "timeout_ms"],
            },
            "action": {
                "type": "object",
                "properties": {
                    "disable_all": {"type": "string", "description": "Logical group to disable (e.g. motor_enables)"},
                    "assert":      {"type": "string", "description": "Signal to assert on trigger (e.g. FAULT_LED)"},
                },
            },
        },
    },
    "periodic_transmit": {
        "type": "object",
        "required": ["id", "behavior", "interval_ms", "frame"],
        "properties": {
            "id":          {"type": "string"},
            "behavior":    {"type": "string", "const": "periodic_transmit"},
            "interval_ms": {"type": "integer", "description": "Transmit interval in milliseconds"},
            "transport":   {"type": "string", "enum": ["can", "uart", "i2c"], "default": "can"},
            "frame": {
                "type": "object",
                "properties": {
                    "id":      {"description": "Frame/register address (integer or hex string)"},
                    "dlc":     {"type": "integer", "description": "Data length in bytes"},
                    "content": {"type": "string", "description": "Logical content label (e.g. motor_status)"},
                },
                "required": ["id", "dlc"],
            },
        },
    },
    "state_machine": {
        "type": "object",
        "required": ["id", "behavior", "states", "transitions"],
        "properties": {
            "id":            {"type": "string"},
            "behavior":      {"type": "string", "const": "state_machine"},
            "initial_state": {"type": "string", "description": "Name of the initial state"},
            "states": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name":  {"type": "string"},
                        "entry": {"type": ["string", "null"]},
                        "exit":  {"type": ["string", "null"]},
                    },
                    "required": ["name"],
                },
            },
            "transitions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "from":    {"type": "string"},
                        "to":      {"type": "string"},
                        "trigger": {"type": "string"},
                    },
                    "required": ["from", "to", "trigger"],
                },
            },
        },
    },
    "sensor_poll": {
        "type": "object",
        "required": ["id", "behavior"],
        "properties": {
            "id":               {"type": "string"},
            "behavior":         {"type": "string", "const": "sensor_poll"},
            "bus":              {"type": "string", "enum": ["i2c", "adc", "spi"], "default": "i2c"},
            "sensor":           {"type": "string", "description": "Sensor label (e.g. imu, temperature)"},
            "address":          {"type": "string", "description": "I2C address or SPI CS index (e.g. 0x68)"},
            "poll_interval_ms": {"type": "integer", "default": 100},
            "ring_buf_entries": {"type": "integer", "default": 16},
        },
    },
}


def render_module(module: dict[str, Any]) -> ModuleOutput:
    """Dispatch to the appropriate behavior renderer."""
    behavior = module.get("behavior")
    renderer = _RENDERERS.get(behavior)
    if renderer is None:
        raise ValueError(f"Unknown firmware module behavior: {behavior!r}. Available: {sorted(_RENDERERS)}")
    return renderer(module)


__all__ = [
    "ModuleOutput",
    "render_module",
    "BEHAVIOR_DESCRIPTIONS",
    "BEHAVIOR_SCHEMAS",
    "_RENDERERS",
]
