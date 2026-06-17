from __future__ import annotations

import re
from typing import Any

from ._base import ModuleOutput


def _safe_id(name: str) -> str:
    """Sanitize a state/event/trigger name to a valid C identifier fragment."""
    return re.sub(r"[^A-Za-z0-9_]", "_", name).upper()


def render(module: dict[str, Any]) -> ModuleOutput:
    mid = module["id"]
    states: list[dict[str, Any]] = module.get("states", [
        {"name": "IDLE", "entry": None, "exit": None},
        {"name": "RUNNING", "entry": None, "exit": None},
        {"name": "FAULT", "entry": None, "exit": None},
    ])
    transitions: list[dict[str, Any]] = module.get("transitions", [
        {"from": "IDLE", "to": "RUNNING", "trigger": "start"},
        {"from": "RUNNING", "to": "FAULT", "trigger": "fault"},
        {"from": "FAULT", "to": "IDLE", "trigger": "reset"},
    ])
    initial = _safe_id(module.get("initial_state", states[0]["name"] if states else "IDLE"))

    state_names = [_safe_id(s["name"]) for s in states]
    enum_values = ",\n    ".join(
        f"{mid.upper()}_STATE_{s}" for s in state_names
    )
    num_states = len(state_names)

    entry_cases = ""
    for s in states:
        action = s.get("entry")
        body = f"        /* entry: {action} */\n" if action else "        /* no entry action */\n"
        entry_cases += f"    case {mid.upper()}_STATE_{_safe_id(s['name'])}:\n{body}        break;\n"

    exit_cases = ""
    for s in states:
        action = s.get("exit")
        body = f"        /* exit: {action} */\n" if action else "        /* no exit action */\n"
        exit_cases += f"    case {mid.upper()}_STATE_{_safe_id(s['name'])}:\n{body}        break;\n"

    transition_table = ""
    for t in transitions:
        from_s = _safe_id(t.get("from", state_names[0]))
        to_s = _safe_id(t.get("to", state_names[-1]))
        trigger = _safe_id(t.get("trigger", "event"))
        raw_trigger = t.get("trigger", "event")
        transition_table += (
            f"    /* {raw_trigger}: {from_s} -> {to_s} */\n"
            f"    if (ctx->state == {mid.upper()}_STATE_{from_s} && event == {mid.upper()}_EVT_{trigger}) {{\n"
            f"        {mid}_exit_action(ctx->state);\n"
            f"        ctx->state = {mid.upper()}_STATE_{to_s};\n"
            f"        {mid}_entry_action(ctx->state);\n"
            f"        return 0;\n"
            f"    }}\n"
        )

    # Deduplicate triggers preserving first-seen order to avoid C enum redefinition
    seen_triggers: dict[str, None] = {}
    for t in transitions:
        seen_triggers[_safe_id(t.get("trigger", "event"))] = None
    event_enum = ",\n    ".join(
        f"{mid.upper()}_EVT_{trigger}"
        for trigger in seen_triggers
    )

    c_source = f"""\
/* Generated module: {mid} — behavior: state_machine
 * States: {', '.join(state_names)}
 * Transitions: {len(transitions)}
 */
#include <zephyr/kernel.h>
#include "{mid}.h"

static struct {mid}_ctx {{
    enum {mid}_state state;
}} {mid}_instance;

static void {mid}_entry_action(enum {mid}_state state)
{{
    switch (state) {{
{entry_cases}    default: break;
    }}
}}

static void {mid}_exit_action(enum {mid}_state state)
{{
    switch (state) {{
{exit_cases}    default: break;
    }}
}}

int {mid}_send_event(enum {mid}_event event)
{{
    struct {mid}_ctx *ctx = &{mid}_instance;
{transition_table}    return -EINVAL;
}}

enum {mid}_state {mid}_get_state(void)
{{
    return {mid}_instance.state;
}}

void {mid}_init(void)
{{
    {mid}_instance.state = {mid.upper()}_STATE_{initial};
    {mid}_entry_action({mid}_instance.state);
}}
"""

    h_source = f"""\
/* Generated header: {mid} — behavior: state_machine */
#pragma once

enum {mid}_state {{
    {enum_values},
    {mid.upper()}_STATE_COUNT = {num_states},
}};

enum {mid}_event {{
    {event_enum},
}};

void {mid}_init(void);
int  {mid}_send_event(enum {mid}_event event);
enum {mid}_state {mid}_get_state(void);
"""

    return ModuleOutput(
        id=mid,
        behavior="state_machine",
        c_source=c_source,
        h_source=h_source,
        dts_fragment=None,
        kconfig_flags=[],
        stack_size_bytes=0,
        is_isr=False,
    )
