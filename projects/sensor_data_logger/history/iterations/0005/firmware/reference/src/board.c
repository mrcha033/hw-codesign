#include "board.h"
#include "pinmap.h"
size_t board_motor_channel_count(void) { return 0; }
int board_estop_is_fail_safe(void) { return 0; }
int board_pinmap_self_test(void) { return PIN_ESP_EN[0] != 0 && PIN_I2C_IMU_SCL[0] != 0 && PIN_USB_DM[0] != 0 && PIN_USB_DP[0] != 0 && PIN_I2C_IMU_SDA[0] != 0 && PIN_BOOT[0] != 0 && PIN_UART_RX[0] != 0 && PIN_UART_TX[0] != 0 && PIN_IMU_INT[0] != 0; }
