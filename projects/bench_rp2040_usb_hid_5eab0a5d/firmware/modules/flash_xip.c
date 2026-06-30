/* Generated module: flash_xip - behavior: interface_stack
 * Declares the qspi firmware stack binding to graph-grounded nets.
 * This is an interface contract stub, not proof of behavior-level firmware correctness.
 */
#include <stddef.h>
#include "pinmap.h"
#include "flash_xip.h"

#if !defined(PIN_QSPI_CLK)
#error "flash_xip requires firmware pinmap signal QSPI_CLK"
#endif
#if !defined(PIN_QSPI_CS)
#error "flash_xip requires firmware pinmap signal QSPI_CS"
#endif
#if !defined(PIN_QSPI_MOSI)
#error "flash_xip requires firmware pinmap signal QSPI_MOSI"
#endif
#if !defined(PIN_QSPI_MISO)
#error "flash_xip requires firmware pinmap signal QSPI_MISO"
#endif
#if !defined(PIN_QSPI_D2)
#error "flash_xip requires firmware pinmap signal QSPI_D2"
#endif
#if !defined(PIN_QSPI_D3)
#error "flash_xip requires firmware pinmap signal QSPI_D3"
#endif

static const char *const flash_xip_required_nets[] = {
    "QSPI_CLK",
    "QSPI_CS",
    "QSPI_MOSI",
    "QSPI_MISO",
    "QSPI_D2",
    "QSPI_D3",
};

static const char *const flash_xip_required_tests[] = {
    "flash_xip_boot",
};

const char *flash_xip_stack_name(void)
{
    return "qspi";
}

const char *flash_xip_library_name(void)
{
    return "pico-sdk";
}

size_t flash_xip_required_net_count(void)
{
    return 6;
}

size_t flash_xip_required_test_count(void)
{
    return 1;
}

const char *const *flash_xip_required_nets_ptr(void)
{
    return flash_xip_required_nets;
}

const char *const *flash_xip_required_tests_ptr(void)
{
    return flash_xip_required_tests;
}

int flash_xip_init_order(void)
{
    return 10;
}
