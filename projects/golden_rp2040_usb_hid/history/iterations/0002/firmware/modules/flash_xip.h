/* Generated header: flash_xip - behavior: interface_stack */
#pragma once
#include <stddef.h>

#define FLASH_XIP_STACK_SIZE 1024
#define FLASH_XIP_INIT_ORDER 10

const char *flash_xip_stack_name(void);
const char *flash_xip_library_name(void);
size_t flash_xip_required_net_count(void);
size_t flash_xip_required_test_count(void);
const char *const *flash_xip_required_nets_ptr(void);
const char *const *flash_xip_required_tests_ptr(void);
int flash_xip_init_order(void);
