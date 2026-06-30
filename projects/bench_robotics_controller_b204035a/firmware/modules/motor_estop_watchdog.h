/* Generated header: motor_estop_watchdog — behavior: timeout_shutdown */
#pragma once

#define MOTOR_ESTOP_WATCHDOG_STACK_SIZE 2048
#define MOTOR_ESTOP_WATCHDOG_PRIORITY   2

void motor_estop_watchdog_init(void);
void motor_estop_watchdog_kick(void);
void motor_estop_watchdog_shutdown_action(void);
