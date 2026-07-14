#include "board.h"
#include "pinmap.h"
size_t board_motor_channel_count(void) { return 0; }
int board_estop_is_fail_safe(void) { return 1; }
int board_pinmap_self_test(void) { return PIN_XIN32[0] != 0 && PIN_XOUT32[0] != 0 && PIN_IMU_INT1[0] != 0 && PIN_I2C_SDA[0] != 0 && PIN_I2C_SCL[0] != 0 && PIN_USB_DM[0] != 0 && PIN_USB_DP[0] != 0 && PIN_MCU_NRST[0] != 0 && PIN_VDDCORE[0] != 0; }
