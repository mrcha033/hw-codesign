/* Generated header: lsm6dsox_driver — behavior: sensor_poll */
#pragma once
#include <stdint.h>
#include <stddef.h>

#define LSM6DSOX_DRIVER_STACK_SIZE 2048
#define LSM6DSOX_DRIVER_PRIORITY   6

struct lsm6dsox_driver_sample {
    int32_t value;
};

void lsm6dsox_driver_init(void);
void lsm6dsox_driver_parse(const uint8_t *raw, struct lsm6dsox_driver_sample *out);
int  lsm6dsox_driver_get_latest(struct lsm6dsox_driver_sample *out);
