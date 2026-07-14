/* Generated header: data_streamer - behavior: interface_stack */
#pragma once
#include <stddef.h>

#define DATA_STREAMER_STACK_SIZE 2048
#define DATA_STREAMER_INIT_ORDER 60

const char *data_streamer_stack_name(void);
const char *data_streamer_library_name(void);
size_t data_streamer_required_net_count(void);
size_t data_streamer_required_test_count(void);
const char *const *data_streamer_required_nets_ptr(void);
const char *const *data_streamer_required_tests_ptr(void);
int data_streamer_init_order(void);
