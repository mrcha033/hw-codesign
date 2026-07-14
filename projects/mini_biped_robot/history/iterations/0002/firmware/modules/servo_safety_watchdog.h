/* Generated header: servo_safety_watchdog — behavior: timeout_shutdown */
#pragma once

#define SERVO_SAFETY_WATCHDOG_STACK_SIZE 2048
#define SERVO_SAFETY_WATCHDOG_PRIORITY   2

void servo_safety_watchdog_init(void);
void servo_safety_watchdog_kick(void);
void servo_safety_watchdog_shutdown_action(void);
