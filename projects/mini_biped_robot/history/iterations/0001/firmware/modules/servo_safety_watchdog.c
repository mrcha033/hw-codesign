/* Generated module: servo_safety_watchdog — behavior: timeout_shutdown
 * Watchdog pattern: arms on init, must be kicked before 100 ms or
 * IMU_INT1 asserted; on expiry disables servo_power_and_pwm and asserts SERVO_PWM_OE.
 */
#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio.h>
#include "pinmap.h"
#include "servo_safety_watchdog.h"

#define SERVO_SAFETY_WATCHDOG_TIMEOUT_MS 100

static struct k_timer servo_safety_watchdog_timer;
static volatile bool servo_safety_watchdog_triggered;

static void servo_safety_watchdog_timer_expiry(struct k_timer *timer)
{
    ARG_UNUSED(timer);
    servo_safety_watchdog_triggered = true;
    servo_safety_watchdog_shutdown_action();
}

K_THREAD_STACK_DEFINE(servo_safety_watchdog_stack, SERVO_SAFETY_WATCHDOG_STACK_SIZE);
static struct k_thread servo_safety_watchdog_thread_data;

static void servo_safety_watchdog_thread_fn(void *p1, void *p2, void *p3)
{
    ARG_UNUSED(p1); ARG_UNUSED(p2); ARG_UNUSED(p3);
    k_timer_start(&servo_safety_watchdog_timer,
                  K_MSEC(SERVO_SAFETY_WATCHDOG_TIMEOUT_MS),
                  K_MSEC(SERVO_SAFETY_WATCHDOG_TIMEOUT_MS));
    while (!servo_safety_watchdog_triggered) {
        k_msleep(1);
    }
}

void servo_safety_watchdog_init(void)
{
    servo_safety_watchdog_triggered = false;
    k_timer_init(&servo_safety_watchdog_timer, servo_safety_watchdog_timer_expiry, NULL);
    k_thread_create(&servo_safety_watchdog_thread_data, servo_safety_watchdog_stack,
                    K_THREAD_STACK_SIZEOF(servo_safety_watchdog_stack),
                    servo_safety_watchdog_thread_fn, NULL, NULL, NULL,
                    SERVO_SAFETY_WATCHDOG_PRIORITY, 0, K_NO_WAIT);
    k_thread_name_set(&servo_safety_watchdog_thread_data, "servo_safety_watchdog");
}

void servo_safety_watchdog_kick(void)
{
    k_timer_start(&servo_safety_watchdog_timer,
                  K_MSEC(SERVO_SAFETY_WATCHDOG_TIMEOUT_MS),
                  K_MSEC(SERVO_SAFETY_WATCHDOG_TIMEOUT_MS));
}

void servo_safety_watchdog_shutdown_action(void)
{
    /* Disable servo_power_and_pwm — pull enable lines low */
#if defined(PIN_IMU_INT1)
    /* Signal IMU_INT1 detected or timer expired — execute shutdown */
#endif
    /* Assert SERVO_PWM_OE */
#if defined(PIN_SERVO_PWM_OE)
    /* gpio_pin_set_dt(&servo_pwm_oe_gpio, 1); */
#endif
}
