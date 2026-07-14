/* Generated header: pca9685_servo_pwm - behavior: interface_stack */
#pragma once
#include <stddef.h>

#define PCA9685_SERVO_PWM_STACK_SIZE 1536
#define PCA9685_SERVO_PWM_INIT_ORDER 45

const char *pca9685_servo_pwm_stack_name(void);
const char *pca9685_servo_pwm_library_name(void);
size_t pca9685_servo_pwm_required_net_count(void);
size_t pca9685_servo_pwm_required_test_count(void);
const char *const *pca9685_servo_pwm_required_nets_ptr(void);
const char *const *pca9685_servo_pwm_required_tests_ptr(void);
int pca9685_servo_pwm_init_order(void);
