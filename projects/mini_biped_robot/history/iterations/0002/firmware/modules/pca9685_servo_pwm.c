/* Generated module: pca9685_servo_pwm - behavior: interface_stack
 * Declares the i2c_pwm firmware stack binding to graph-grounded nets.
 * This is an interface contract stub, not proof of behavior-level firmware correctness.
 */
#include <stddef.h>
#include "pinmap.h"
#include "pca9685_servo_pwm.h"

#if !defined(PIN_I2C_SCL)
#error "pca9685_servo_pwm requires firmware pinmap signal I2C_SCL"
#endif
#if !defined(PIN_I2C_SDA)
#error "pca9685_servo_pwm requires firmware pinmap signal I2C_SDA"
#endif
#if !defined(PIN_SERVO_PWM_OE)
#error "pca9685_servo_pwm requires firmware pinmap signal SERVO_PWM_OE"
#endif

static const char *const pca9685_servo_pwm_required_nets[] = {
    "I2C_SCL",
    "I2C_SDA",
    "SERVO_PWM_OE",
};

static const char *const pca9685_servo_pwm_required_tests[] = {
    "pca9685_probe",
    "servo_neutral_pulse_scope",
    "all_channels_power_off_safe",
};

const char *pca9685_servo_pwm_stack_name(void)
{
    return "i2c_pwm";
}

const char *pca9685_servo_pwm_library_name(void)
{
    return "zephyr_i2c_pca9685";
}

size_t pca9685_servo_pwm_required_net_count(void)
{
    return 3;
}

size_t pca9685_servo_pwm_required_test_count(void)
{
    return 3;
}

const char *const *pca9685_servo_pwm_required_nets_ptr(void)
{
    return pca9685_servo_pwm_required_nets;
}

const char *const *pca9685_servo_pwm_required_tests_ptr(void)
{
    return pca9685_servo_pwm_required_tests;
}

int pca9685_servo_pwm_init_order(void)
{
    return 45;
}
