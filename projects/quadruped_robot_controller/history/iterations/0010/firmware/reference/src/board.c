#include "board.h"
#include "pinmap.h"
size_t board_motor_channel_count(void) { return 12; }
int board_estop_is_fail_safe(void) { return 1; }
int board_pinmap_self_test(void) { return PIN_ESTOP_IN[0] != 0 && PIN_I2C_IMU_SCL[0] != 0; }
