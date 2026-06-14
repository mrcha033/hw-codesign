#include "board.h"
#include <assert.h>
#include <stdio.h>
int main(void) { assert(board_motor_channel_count() == 12); assert(board_estop_is_fail_safe()); assert(board_pinmap_self_test()); puts("bringup tests passed"); return 0; }
