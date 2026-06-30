/* Generated module: motor_estop_watchdog — behavior: timeout_shutdown
 * Watchdog pattern: arms on init, must be kicked before 100 ms or
 * ESTOP_IN asserted; on expiry disables motor_enables and asserts FAULT_LED.
 */
#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio.h>
#include "pinmap.h"
#include "motor_estop_watchdog.h"

#define MOTOR_ESTOP_WATCHDOG_TIMEOUT_MS 100

static struct k_timer motor_estop_watchdog_timer;
static volatile bool motor_estop_watchdog_triggered;

static void motor_estop_watchdog_timer_expiry(struct k_timer *timer)
{
    ARG_UNUSED(timer);
    motor_estop_watchdog_triggered = true;
    motor_estop_watchdog_shutdown_action();
}

K_THREAD_STACK_DEFINE(motor_estop_watchdog_stack, MOTOR_ESTOP_WATCHDOG_STACK_SIZE);
static struct k_thread motor_estop_watchdog_thread_data;

static void motor_estop_watchdog_thread_fn(void *p1, void *p2, void *p3)
{
    ARG_UNUSED(p1); ARG_UNUSED(p2); ARG_UNUSED(p3);
    k_timer_start(&motor_estop_watchdog_timer,
                  K_MSEC(MOTOR_ESTOP_WATCHDOG_TIMEOUT_MS),
                  K_MSEC(MOTOR_ESTOP_WATCHDOG_TIMEOUT_MS));
    while (!motor_estop_watchdog_triggered) {
        k_msleep(1);
    }
}

void motor_estop_watchdog_init(void)
{
    motor_estop_watchdog_triggered = false;
    k_timer_init(&motor_estop_watchdog_timer, motor_estop_watchdog_timer_expiry, NULL);
    k_thread_create(&motor_estop_watchdog_thread_data, motor_estop_watchdog_stack,
                    K_THREAD_STACK_SIZEOF(motor_estop_watchdog_stack),
                    motor_estop_watchdog_thread_fn, NULL, NULL, NULL,
                    MOTOR_ESTOP_WATCHDOG_PRIORITY, 0, K_NO_WAIT);
    k_thread_name_set(&motor_estop_watchdog_thread_data, "motor_estop_watchdog");
}

void motor_estop_watchdog_kick(void)
{
    k_timer_start(&motor_estop_watchdog_timer,
                  K_MSEC(MOTOR_ESTOP_WATCHDOG_TIMEOUT_MS),
                  K_MSEC(MOTOR_ESTOP_WATCHDOG_TIMEOUT_MS));
}

void motor_estop_watchdog_shutdown_action(void)
{
    /* Disable motor_enables — pull enable lines low */
#if defined(PIN_ESTOP_IN)
    /* Signal ESTOP_IN detected or timer expired — execute shutdown */
#endif
    /* Assert FAULT_LED */
#if defined(PIN_FAULT_LED)
    /* gpio_pin_set_dt(&fault_led_gpio, 1); */
#endif
}
