/* Generated module: bme280_driver — behavior: sensor_poll
 * Polls bme280 over I2C every 1000 ms into a ring buffer
 * of 4 entries.
 */
#include <zephyr/kernel.h>
#include <zephyr/sys/ring_buffer.h>
#include <zephyr/drivers/i2c.h>

static const struct device *i2c_dev;
#include "bme280_driver.h"

#define BME280_DRIVER_POLL_MS   1000
#define BME280_DRIVER_RING_SIZE (4 * sizeof(struct bme280_driver_sample))

RING_BUF_DECLARE(bme280_driver_ring, BME280_DRIVER_RING_SIZE);

K_THREAD_STACK_DEFINE(bme280_driver_stack, BME280_DRIVER_STACK_SIZE);
static struct k_thread bme280_driver_thread_data;

static void bme280_driver_thread_fn(void *p1, void *p2, void *p3)
{
    ARG_UNUSED(p1); ARG_UNUSED(p2); ARG_UNUSED(p3);
    while (1) {
    uint8_t raw[6];
    if (i2c_read(i2c_dev, raw, sizeof(raw), 118) == 0) {
        struct bme280_driver_sample sample;
        bme280_driver_parse(raw, &sample);
        ring_buf_put(&bme280_driver_ring, (uint8_t *)&sample, sizeof(sample));
    }
        k_msleep(BME280_DRIVER_POLL_MS);
    }
}

void bme280_driver_parse(const uint8_t *raw, struct bme280_driver_sample *out)
{
    /* Parse raw sensor bytes into sample struct */
    out->value = (int32_t)((raw[0] << 8) | raw[1]);
}

int bme280_driver_get_latest(struct bme280_driver_sample *out)
{
    uint32_t available = ring_buf_size_get(&bme280_driver_ring);
    if (available < sizeof(struct bme280_driver_sample)) {
        return -ENODATA;
    }
    ring_buf_peek(&bme280_driver_ring, (uint8_t *)out, sizeof(*out));
    return 0;
}

void bme280_driver_init(void)
{
    i2c_dev = DEVICE_DT_GET(DT_NODELABEL(i2c0));
    ring_buf_reset(&bme280_driver_ring);
    k_thread_create(&bme280_driver_thread_data, bme280_driver_stack,
                    K_THREAD_STACK_SIZEOF(bme280_driver_stack),
                    bme280_driver_thread_fn, NULL, NULL, NULL,
                    BME280_DRIVER_PRIORITY, 0, K_NO_WAIT);
    k_thread_name_set(&bme280_driver_thread_data, "bme280_driver");
}
