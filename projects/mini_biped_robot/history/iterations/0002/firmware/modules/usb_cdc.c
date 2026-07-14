/* Generated module: usb_cdc - behavior: interface_stack
 * Declares the usb firmware stack binding to graph-grounded nets.
 * This is an interface contract stub, not proof of behavior-level firmware correctness.
 */
#include <stddef.h>
#include "pinmap.h"
#include "usb_cdc.h"

#if !defined(PIN_USB_DP)
#error "usb_cdc requires firmware pinmap signal USB_DP"
#endif
#if !defined(PIN_USB_DM)
#error "usb_cdc requires firmware pinmap signal USB_DM"
#endif

static const char *const usb_cdc_required_nets[] = {
    "USB_DP",
    "USB_DM",
};

static const char *const usb_cdc_required_tests[] = {
    "usb_cdc_enumeration",
};

const char *usb_cdc_stack_name(void)
{
    return "usb";
}

const char *usb_cdc_library_name(void)
{
    return "zephyr_usb_cdc_acm";
}

size_t usb_cdc_required_net_count(void)
{
    return 2;
}

size_t usb_cdc_required_test_count(void)
{
    return 1;
}

const char *const *usb_cdc_required_nets_ptr(void)
{
    return usb_cdc_required_nets;
}

const char *const *usb_cdc_required_tests_ptr(void)
{
    return usb_cdc_required_tests;
}

int usb_cdc_init_order(void)
{
    return 20;
}
