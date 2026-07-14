/* Generated header: usb_cdc - behavior: interface_stack */
#pragma once
#include <stddef.h>

#define USB_CDC_STACK_SIZE 2048
#define USB_CDC_INIT_ORDER 20

const char *usb_cdc_stack_name(void);
const char *usb_cdc_library_name(void);
size_t usb_cdc_required_net_count(void);
size_t usb_cdc_required_test_count(void);
const char *const *usb_cdc_required_nets_ptr(void);
const char *const *usb_cdc_required_tests_ptr(void);
int usb_cdc_init_order(void);
