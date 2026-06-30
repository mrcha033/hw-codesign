#include "board.h"
#include "pinmap.h"
size_t board_motor_channel_count(void) { return 0; }
int board_estop_is_fail_safe(void) { return 0; }
int board_pinmap_self_test(void) { return PIN_QSPI_D3[0] != 0 && PIN_QSPI_D2[0] != 0 && PIN_QSPI_MISO[0] != 0 && PIN_QSPI_MOSI[0] != 0 && PIN_QSPI_CLK[0] != 0 && PIN_QSPI_CS[0] != 0 && PIN_USB_DM[0] != 0 && PIN_USB_DP[0] != 0 && PIN_XIN[0] != 0 && PIN_XOUT[0] != 0; }
