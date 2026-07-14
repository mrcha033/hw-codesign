/* Generated header: bme280_driver — behavior: sensor_poll */
#pragma once
#include <stdint.h>
#include <stddef.h>

#define BME280_DRIVER_STACK_SIZE 2048
#define BME280_DRIVER_PRIORITY   6

struct bme280_driver_sample {
    int32_t value;
};

void bme280_driver_init(void);
void bme280_driver_parse(const uint8_t *raw, struct bme280_driver_sample *out);
int  bme280_driver_get_latest(struct bme280_driver_sample *out);
