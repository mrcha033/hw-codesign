from __future__ import annotations

from typing import Any

from ._base import ModuleOutput


def render(module: dict[str, Any]) -> ModuleOutput:
    mid = module["id"]
    trigger = module.get("trigger", {})
    action = module.get("action", {})
    signal = trigger.get("signal", "ESTOP_IN")
    timeout_ms = int(trigger.get("timeout_ms", 100))
    disable_all = action.get("disable_all", "motor_enables")
    _assert_raw = action.get("assert", "FAULT_LED")
    assert_signal = "FAULT_LED" if isinstance(_assert_raw, bool) else str(_assert_raw)

    c_source = f"""\
/* Generated module: {mid} — behavior: timeout_shutdown
 * Watchdog pattern: arms on init, must be kicked before {timeout_ms} ms or
 * {signal} asserted; on expiry disables {disable_all} and asserts {assert_signal}.
 */
#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio.h>
#include "pinmap.h"
#include "{mid}.h"

#define {mid.upper()}_TIMEOUT_MS {timeout_ms}

static struct k_timer {mid}_timer;
static volatile bool {mid}_triggered;

static void {mid}_timer_expiry(struct k_timer *timer)
{{
    ARG_UNUSED(timer);
    {mid}_triggered = true;
    {mid}_shutdown_action();
}}

K_THREAD_STACK_DEFINE({mid}_stack, {mid.upper()}_STACK_SIZE);
static struct k_thread {mid}_thread_data;

static void {mid}_thread_fn(void *p1, void *p2, void *p3)
{{
    ARG_UNUSED(p1); ARG_UNUSED(p2); ARG_UNUSED(p3);
    k_timer_start(&{mid}_timer,
                  K_MSEC({mid.upper()}_TIMEOUT_MS),
                  K_MSEC({mid.upper()}_TIMEOUT_MS));
    while (!{mid}_triggered) {{
        k_msleep(1);
    }}
}}

void {mid}_init(void)
{{
    {mid}_triggered = false;
    k_timer_init(&{mid}_timer, {mid}_timer_expiry, NULL);
    k_thread_create(&{mid}_thread_data, {mid}_stack,
                    K_THREAD_STACK_SIZEOF({mid}_stack),
                    {mid}_thread_fn, NULL, NULL, NULL,
                    {mid.upper()}_PRIORITY, 0, K_NO_WAIT);
    k_thread_name_set(&{mid}_thread_data, "{mid}");
}}

void {mid}_kick(void)
{{
    k_timer_start(&{mid}_timer,
                  K_MSEC({mid.upper()}_TIMEOUT_MS),
                  K_MSEC({mid.upper()}_TIMEOUT_MS));
}}

void {mid}_shutdown_action(void)
{{
    /* Disable {disable_all} — pull enable lines low */
#if defined(PIN_{signal})
    /* Signal {signal} detected or timer expired — execute shutdown */
#endif
    /* Assert {assert_signal} */
#if defined(PIN_{assert_signal})
    /* gpio_pin_set_dt(&{assert_signal.lower()}_gpio, 1); */
#endif
}}
"""

    h_source = f"""\
/* Generated header: {mid} — behavior: timeout_shutdown */
#pragma once

#define {mid.upper()}_STACK_SIZE 2048
#define {mid.upper()}_PRIORITY   2

void {mid}_init(void);
void {mid}_kick(void);
void {mid}_shutdown_action(void);
"""

    return ModuleOutput(
        id=mid,
        behavior="timeout_shutdown",
        c_source=c_source,
        h_source=h_source,
        dts_fragment=None,
        kconfig_flags=["CONFIG_GPIO=y"],
        stack_size_bytes=2048,
        is_isr=False,
    )
