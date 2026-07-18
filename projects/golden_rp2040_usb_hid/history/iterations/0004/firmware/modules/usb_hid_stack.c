/* Generated module: usb_hid_stack - behavior: interface_stack
 * Declares the usb firmware stack binding to graph-grounded nets.
 * This is an interface contract stub, not proof of behavior-level firmware correctness.
 */
#include <stddef.h>
#include "pinmap.h"
#include "usb_hid_stack.h"

#if !defined(PIN_USB_DP)
#error "usb_hid_stack requires firmware pinmap signal USB_DP"
#endif
#if !defined(PIN_USB_DM)
#error "usb_hid_stack requires firmware pinmap signal USB_DM"
#endif

static const char *const usb_hid_stack_required_nets[] = {
    "USB_DP",
    "USB_DM",
};

static const char *const usb_hid_stack_required_tests[] = {
    "usb_hid_enumeration",
};

const char *usb_hid_stack_stack_name(void)
{
    return "usb";
}

const char *usb_hid_stack_library_name(void)
{
    return "tinyusb";
}

size_t usb_hid_stack_required_net_count(void)
{
    return 2;
}

size_t usb_hid_stack_required_test_count(void)
{
    return 1;
}

const char *const *usb_hid_stack_required_nets_ptr(void)
{
    return usb_hid_stack_required_nets;
}

const char *const *usb_hid_stack_required_tests_ptr(void)
{
    return usb_hid_stack_required_tests;
}

int usb_hid_stack_init_order(void)
{
    return 30;
}
