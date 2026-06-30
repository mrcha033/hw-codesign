from __future__ import annotations

import re
from typing import Any

from ._base import ModuleOutput


_STACK_KCONFIG: dict[str, list[str]] = {
    "usb": ["CONFIG_USB_DEVICE_STACK=y", "CONFIG_USB_CDC_ACM=y"],
    "qspi": ["CONFIG_SPI=y"],
    "spi": ["CONFIG_SPI=y"],
    "pio": ["CONFIG_GPIO=y"],
}


def _safe_id(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]", "_", value).upper()


def render(module: dict[str, Any]) -> ModuleOutput:
    mid = module["id"]
    stack = str(module.get("stack", mid)).lower()
    library = str(module.get("library", "project"))
    required_nets = [str(item) for item in module.get("required_nets", [])]
    required_tests = [str(item) for item in module.get("required_tests", [])]
    init_order = int(module.get("init_order", 50))
    stack_size = int(module.get("stack_size_bytes", 1024))

    net_checks = "\n".join(
        f"#if !defined(PIN_{_safe_id(net)})\n"
        f"#error \"{mid} requires firmware pinmap signal {net}\"\n"
        f"#endif"
        for net in required_nets
    )
    net_table = "\n".join(f'    "{net}",' for net in required_nets) or "    NULL,"
    test_table = "\n".join(f'    "{test}",' for test in required_tests) or "    NULL,"

    c_source = f"""\
/* Generated module: {mid} - behavior: interface_stack
 * Declares the {stack} firmware stack binding to graph-grounded nets.
 * This is an interface contract stub, not proof of behavior-level firmware correctness.
 */
#include <stddef.h>
#include "pinmap.h"
#include "{mid}.h"

{net_checks}

static const char *const {mid}_required_nets[] = {{
{net_table}
}};

static const char *const {mid}_required_tests[] = {{
{test_table}
}};

const char *{mid}_stack_name(void)
{{
    return "{stack}";
}}

const char *{mid}_library_name(void)
{{
    return "{library}";
}}

size_t {mid}_required_net_count(void)
{{
    return {len(required_nets)};
}}

size_t {mid}_required_test_count(void)
{{
    return {len(required_tests)};
}}

const char *const *{mid}_required_nets_ptr(void)
{{
    return {mid}_required_nets;
}}

const char *const *{mid}_required_tests_ptr(void)
{{
    return {mid}_required_tests;
}}

int {mid}_init_order(void)
{{
    return {init_order};
}}
"""

    h_source = f"""\
/* Generated header: {mid} - behavior: interface_stack */
#pragma once
#include <stddef.h>

#define {mid.upper()}_STACK_SIZE {stack_size}
#define {mid.upper()}_INIT_ORDER {init_order}

const char *{mid}_stack_name(void);
const char *{mid}_library_name(void);
size_t {mid}_required_net_count(void);
size_t {mid}_required_test_count(void);
const char *const *{mid}_required_nets_ptr(void);
const char *const *{mid}_required_tests_ptr(void);
int {mid}_init_order(void);
"""

    return ModuleOutput(
        id=mid,
        behavior="interface_stack",
        c_source=c_source,
        h_source=h_source,
        dts_fragment=f"/* {mid}: {stack} stack binding via {library} */\n",
        kconfig_flags=_STACK_KCONFIG.get(stack, []),
        stack_size_bytes=stack_size,
        is_isr=False,
    )
