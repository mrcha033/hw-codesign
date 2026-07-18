/* Generated header: usb_hid_stack - behavior: interface_stack */
#pragma once
#include <stddef.h>

#define USB_HID_STACK_STACK_SIZE 2048
#define USB_HID_STACK_INIT_ORDER 30

const char *usb_hid_stack_stack_name(void);
const char *usb_hid_stack_library_name(void);
size_t usb_hid_stack_required_net_count(void);
size_t usb_hid_stack_required_test_count(void);
const char *const *usb_hid_stack_required_nets_ptr(void);
const char *const *usb_hid_stack_required_tests_ptr(void);
int usb_hid_stack_init_order(void);
