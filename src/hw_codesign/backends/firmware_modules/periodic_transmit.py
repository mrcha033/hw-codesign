from __future__ import annotations

from typing import Any

from ._base import ModuleOutput

_TRANSPORT_KCONFIG: dict[str, list[str]] = {
    "can":  ["CONFIG_CAN=y"],
    "uart": ["CONFIG_UART_ASYNC_API=y"],
    "i2c":  ["CONFIG_I2C=y"],
}


def render(module: dict[str, Any]) -> ModuleOutput:
    mid = module["id"]
    interval_ms = int(module.get("interval_ms", 10))
    frame = module.get("frame", {})
    frame_id = int(frame.get("id", 0x100), 0) if isinstance(frame.get("id", 0x100), str) else int(frame.get("id", 0x100))
    dlc = int(frame.get("dlc", 8))
    content = frame.get("content", "motor_status")
    transport = module.get("transport", "can").lower()
    frame_id_hex = f"0x{frame_id:03X}" if isinstance(frame_id, int) else str(frame_id)

    kconfig = list(_TRANSPORT_KCONFIG.get(transport, ["CONFIG_CAN=y"]))

    if transport == "can":
        transmit_body = f"""\
    struct can_frame tx_frame = {{
        .id    = {frame_id_hex},
        .dlc   = {dlc},
        .flags = 0,
    }};
    {mid}_fill_payload(tx_frame.data, {dlc});
    can_send(can_dev, &tx_frame, K_NO_WAIT, NULL, NULL);"""
        dts_fragment = (
            f"/* {mid}: periodic CAN frame 0x{frame_id:03X} every {interval_ms} ms */\n"
        )
        extra_includes = "#include <zephyr/drivers/can.h>\n\nstatic const struct device *can_dev;"
        extra_init = "    can_dev = DEVICE_DT_GET(DT_CHOSEN(zephyr_canbus));"
    elif transport == "uart":
        transmit_body = f"""\
    uint8_t buf[{dlc}];
    {mid}_fill_payload(buf, {dlc});
    uart_tx(uart_dev, buf, {dlc}, SYS_FOREVER_US);"""
        dts_fragment = f"/* {mid}: periodic UART frame every {interval_ms} ms */\n"
        extra_includes = "#include <zephyr/drivers/uart.h>\n\nstatic const struct device *uart_dev;"
        extra_init = "    uart_dev = DEVICE_DT_GET(DT_CHOSEN(zephyr_console));"
    else:
        transmit_body = f"""\
    uint8_t buf[{dlc}];
    {mid}_fill_payload(buf, {dlc});
    i2c_write(i2c_dev, buf, {dlc}, {frame_id_hex});"""
        dts_fragment = f"/* {mid}: periodic I2C frame every {interval_ms} ms */\n"
        extra_includes = "#include <zephyr/drivers/i2c.h>\n\nstatic const struct device *i2c_dev;"
        extra_init = "    i2c_dev = DEVICE_DT_GET(DT_NODELABEL(i2c0));"

    c_source = f"""\
/* Generated module: {mid} — behavior: periodic_transmit
 * Transmits a {transport.upper()} frame (ID={frame_id_hex}, DLC={dlc}, content={content})
 * every {interval_ms} ms.
 */
#include <zephyr/kernel.h>
{extra_includes}
#include "{mid}.h"

#define {mid.upper()}_INTERVAL_MS {interval_ms}

static struct k_timer {mid}_timer;

K_THREAD_STACK_DEFINE({mid}_stack, {mid.upper()}_STACK_SIZE);
static struct k_thread {mid}_thread_data;

static void {mid}_thread_fn(void *p1, void *p2, void *p3)
{{
    ARG_UNUSED(p1); ARG_UNUSED(p2); ARG_UNUSED(p3);
    k_timer_start(&{mid}_timer,
                  K_MSEC({mid.upper()}_INTERVAL_MS),
                  K_MSEC({mid.upper()}_INTERVAL_MS));
    while (1) {{
        k_timer_status_sync(&{mid}_timer);
{transmit_body}
    }}
}}

void {mid}_fill_payload(uint8_t *buf, size_t len)
{{
    /* Populate {content} data into buf[0..len-1] */
    for (size_t i = 0; i < len; i++) {{
        buf[i] = 0;
    }}
}}

void {mid}_init(void)
{{
{extra_init}
    k_timer_init(&{mid}_timer, NULL, NULL);
    k_thread_create(&{mid}_thread_data, {mid}_stack,
                    K_THREAD_STACK_SIZEOF({mid}_stack),
                    {mid}_thread_fn, NULL, NULL, NULL,
                    {mid.upper()}_PRIORITY, 0, K_NO_WAIT);
    k_thread_name_set(&{mid}_thread_data, "{mid}");
}}
"""

    h_source = f"""\
/* Generated header: {mid} — behavior: periodic_transmit */
#pragma once
#include <stdint.h>
#include <stddef.h>

#define {mid.upper()}_STACK_SIZE 2048
#define {mid.upper()}_PRIORITY   5

void {mid}_init(void);
void {mid}_fill_payload(uint8_t *buf, size_t len);
"""

    return ModuleOutput(
        id=mid,
        behavior="periodic_transmit",
        c_source=c_source,
        h_source=h_source,
        dts_fragment=dts_fragment,
        kconfig_flags=kconfig,
        stack_size_bytes=2048,
        is_isr=False,
    )
