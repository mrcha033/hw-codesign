/* Generated module: lsm6dsox_driver — behavior: sensor_poll
 * Polls lsm6dsox over I2C every 5 ms into a ring buffer
 * of 64 entries.
 */
#include <zephyr/kernel.h>
#include <zephyr/sys/ring_buffer.h>
#include <zephyr/drivers/i2c.h>

static const struct device *i2c_dev;
#include "lsm6dsox_driver.h"

#define LSM6DSOX_DRIVER_POLL_MS   5
#define LSM6DSOX_DRIVER_RING_SIZE (64 * sizeof(struct lsm6dsox_driver_sample))

RING_BUF_DECLARE(lsm6dsox_driver_ring, LSM6DSOX_DRIVER_RING_SIZE);

K_THREAD_STACK_DEFINE(lsm6dsox_driver_stack, LSM6DSOX_DRIVER_STACK_SIZE);
static struct k_thread lsm6dsox_driver_thread_data;

static void lsm6dsox_driver_thread_fn(void *p1, void *p2, void *p3)
{
    ARG_UNUSED(p1); ARG_UNUSED(p2); ARG_UNUSED(p3);
    while (1) {
    uint8_t raw[6];
    if (i2c_read(i2c_dev, raw, sizeof(raw), 0x6A) == 0) {
        struct lsm6dsox_driver_sample sample;
        lsm6dsox_driver_parse(raw, &sample);
        ring_buf_put(&lsm6dsox_driver_ring, (uint8_t *)&sample, sizeof(sample));
    }
        k_msleep(LSM6DSOX_DRIVER_POLL_MS);
    }
}

void lsm6dsox_driver_parse(const uint8_t *raw, struct lsm6dsox_driver_sample *out)
{
    /* Parse raw sensor bytes into sample struct */
    out->value = (int32_t)((raw[0] << 8) | raw[1]);
}

int lsm6dsox_driver_get_latest(struct lsm6dsox_driver_sample *out)
{
    uint32_t available = ring_buf_size_get(&lsm6dsox_driver_ring);
    if (available < sizeof(struct lsm6dsox_driver_sample)) {
        return -ENODATA;
    }
    ring_buf_peek(&lsm6dsox_driver_ring, (uint8_t *)out, sizeof(*out));
    return 0;
}

void lsm6dsox_driver_init(void)
{
    i2c_dev = DEVICE_DT_GET(DT_NODELABEL(i2c0));
    ring_buf_reset(&lsm6dsox_driver_ring);
    k_thread_create(&lsm6dsox_driver_thread_data, lsm6dsox_driver_stack,
                    K_THREAD_STACK_SIZEOF(lsm6dsox_driver_stack),
                    lsm6dsox_driver_thread_fn, NULL, NULL, NULL,
                    LSM6DSOX_DRIVER_PRIORITY, 0, K_NO_WAIT);
    k_thread_name_set(&lsm6dsox_driver_thread_data, "lsm6dsox_driver");
}
