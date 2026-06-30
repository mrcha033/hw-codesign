/* Generated header: pio_ws2812 - behavior: interface_stack */
#pragma once
#include <stddef.h>

#define PIO_WS2812_STACK_SIZE 512
#define PIO_WS2812_INIT_ORDER 80

const char *pio_ws2812_stack_name(void);
const char *pio_ws2812_library_name(void);
size_t pio_ws2812_required_net_count(void);
size_t pio_ws2812_required_test_count(void);
const char *const *pio_ws2812_required_nets_ptr(void);
const char *const *pio_ws2812_required_tests_ptr(void);
int pio_ws2812_init_order(void);
