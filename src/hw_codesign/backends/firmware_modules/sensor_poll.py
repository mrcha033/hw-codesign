from __future__ import annotations

from typing import Any

from ._base import ModuleOutput

_BUS_KCONFIG: dict[str, list[str]] = {
    "i2c": ["CONFIG_I2C=y", "CONFIG_SENSOR=y"],
    "adc": ["CONFIG_ADC=y"],
    "spi": ["CONFIG_SPI=y"],
}


def render(module: dict[str, Any]) -> ModuleOutput:
    mid = module["id"]
    bus = module.get("bus", "i2c").lower()
    poll_interval_ms = int(module.get("poll_interval_ms", 100))
    sensor = module.get("sensor", "imu")
    ring_buf_size = int(module.get("ring_buf_entries", 16))
    addr = module.get("address", "0x68")

    kconfig = list(_BUS_KCONFIG.get(bus, ["CONFIG_I2C=y", "CONFIG_SENSOR=y"]))
    kconfig.append("CONFIG_RING_BUFFER=y")

    if bus == "i2c":
        read_body = f"""\
    uint8_t raw[6];
    if (i2c_read(i2c_dev, raw, sizeof(raw), {addr}) == 0) {{
        struct {mid}_sample sample;
        {mid}_parse(raw, &sample);
        ring_buf_put(&{mid}_ring, (uint8_t *)&sample, sizeof(sample));
    }}"""
        extra_includes = "#include <zephyr/drivers/i2c.h>\n\nstatic const struct device *i2c_dev;"
        extra_init = f"    i2c_dev = DEVICE_DT_GET(DT_NODELABEL(i2c0));"
        dts_fragment = (
            f"/* {mid}: {sensor} on I2C addr {addr} polled every {poll_interval_ms} ms */\n"
        )
    elif bus == "adc":
        read_body = f"""\
    int32_t val_mv;
    struct adc_sequence seq = {{
        .channels = BIT(0),
        .buffer   = &val_mv,
        .buffer_size = sizeof(val_mv),
    }};
    if (adc_read(adc_dev, &seq) == 0) {{
        struct {mid}_sample sample = {{ .value = val_mv }};
        ring_buf_put(&{mid}_ring, (uint8_t *)&sample, sizeof(sample));
    }}"""
        extra_includes = "#include <zephyr/drivers/adc.h>\n\nstatic const struct device *adc_dev;"
        extra_init = "    adc_dev = DEVICE_DT_GET(DT_NODELABEL(adc0));"
        dts_fragment = f"/* {mid}: ADC polled every {poll_interval_ms} ms */\n"
    else:
        read_body = f"""\
    uint8_t raw[6];
    struct spi_buf rx_buf = {{ .buf = raw, .len = sizeof(raw) }};
    struct spi_buf_set rx_set = {{ .buffers = &rx_buf, .count = 1 }};
    if (spi_read(spi_dev, &spi_cfg, &rx_set) == 0) {{
        struct {mid}_sample sample;
        {mid}_parse(raw, &sample);
        ring_buf_put(&{mid}_ring, (uint8_t *)&sample, sizeof(sample));
    }}"""
        extra_includes = "#include <zephyr/drivers/spi.h>\n\nstatic const struct device *spi_dev;\nstatic struct spi_config spi_cfg;"
        extra_init = "    spi_dev = DEVICE_DT_GET(DT_NODELABEL(spi0));"
        dts_fragment = f"/* {mid}: SPI sensor polled every {poll_interval_ms} ms */\n"

    c_source = f"""\
/* Generated module: {mid} — behavior: sensor_poll
 * Polls {sensor} over {bus.upper()} every {poll_interval_ms} ms into a ring buffer
 * of {ring_buf_size} entries.
 */
#include <zephyr/kernel.h>
#include <zephyr/sys/ring_buffer.h>
{extra_includes}
#include "{mid}.h"

#define {mid.upper()}_POLL_MS   {poll_interval_ms}
#define {mid.upper()}_RING_SIZE ({ring_buf_size} * sizeof(struct {mid}_sample))

RING_BUF_DECLARE({mid}_ring, {mid.upper()}_RING_SIZE);

K_THREAD_STACK_DEFINE({mid}_stack, {mid.upper()}_STACK_SIZE);
static struct k_thread {mid}_thread_data;

static void {mid}_thread_fn(void *p1, void *p2, void *p3)
{{
    ARG_UNUSED(p1); ARG_UNUSED(p2); ARG_UNUSED(p3);
    while (1) {{
{read_body}
        k_msleep({mid.upper()}_POLL_MS);
    }}
}}

void {mid}_parse(const uint8_t *raw, struct {mid}_sample *out)
{{
    /* Parse raw sensor bytes into sample struct */
    out->value = (int32_t)((raw[0] << 8) | raw[1]);
}}

int {mid}_get_latest(struct {mid}_sample *out)
{{
    uint32_t available = ring_buf_size_get(&{mid}_ring);
    if (available < sizeof(struct {mid}_sample)) {{
        return -ENODATA;
    }}
    ring_buf_peek(&{mid}_ring, (uint8_t *)out, sizeof(*out));
    return 0;
}}

void {mid}_init(void)
{{
{extra_init}
    ring_buf_reset(&{mid}_ring);
    k_thread_create(&{mid}_thread_data, {mid}_stack,
                    K_THREAD_STACK_SIZEOF({mid}_stack),
                    {mid}_thread_fn, NULL, NULL, NULL,
                    {mid.upper()}_PRIORITY, 0, K_NO_WAIT);
    k_thread_name_set(&{mid}_thread_data, "{mid}");
}}
"""

    h_source = f"""\
/* Generated header: {mid} — behavior: sensor_poll */
#pragma once
#include <stdint.h>
#include <stddef.h>

#define {mid.upper()}_STACK_SIZE 2048
#define {mid.upper()}_PRIORITY   6

struct {mid}_sample {{
    int32_t value;
}};

void {mid}_init(void);
void {mid}_parse(const uint8_t *raw, struct {mid}_sample *out);
int  {mid}_get_latest(struct {mid}_sample *out);
"""

    return ModuleOutput(
        id=mid,
        behavior="sensor_poll",
        c_source=c_source,
        h_source=h_source,
        dts_fragment=dts_fragment,
        kconfig_flags=kconfig,
        stack_size_bytes=2048,
        is_isr=False,
    )
