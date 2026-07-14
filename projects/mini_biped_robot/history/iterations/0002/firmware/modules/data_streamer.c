/* Generated module: data_streamer - behavior: interface_stack
 * Declares the usb firmware stack binding to graph-grounded nets.
 * This is an interface contract stub, not proof of behavior-level firmware correctness.
 */
#include <stddef.h>
#include "pinmap.h"
#include "data_streamer.h"

#if !defined(PIN_USB_DP)
#error "data_streamer requires firmware pinmap signal USB_DP"
#endif
#if !defined(PIN_USB_DM)
#error "data_streamer requires firmware pinmap signal USB_DM"
#endif

static const char *const data_streamer_required_nets[] = {
    "USB_DP",
    "USB_DM",
};

static const char *const data_streamer_required_tests[] = {
    "sensor_data_streaming_1khz",
};

const char *data_streamer_stack_name(void)
{
    return "usb";
}

const char *data_streamer_library_name(void)
{
    return "zephyr_usb_cdc_acm";
}

size_t data_streamer_required_net_count(void)
{
    return 2;
}

size_t data_streamer_required_test_count(void)
{
    return 1;
}

const char *const *data_streamer_required_nets_ptr(void)
{
    return data_streamer_required_nets;
}

const char *const *data_streamer_required_tests_ptr(void)
{
    return data_streamer_required_tests;
}

int data_streamer_init_order(void)
{
    return 60;
}
