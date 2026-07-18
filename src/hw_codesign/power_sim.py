"""H1 physics-evidence (advisory): DC operating-point bridge to ngspice.

This is the first *computed* (not heuristic) physics evidence in the platform. It
extracts a conservative DC netlist from the extracted electrical graph and solves
the operating point with ngspice:

* power rails (nets with a grounded nominal voltage) become ideal DC voltage
  sources at that voltage — the same `_rail_nominal_voltages` mapping the existing
  power checks use, so no new invented data;
* resistors become R elements between their two nets (0 Ω jumpers clamped to a
  tiny value); capacitors are open at DC and omitted;
* every non-ground node gets a 1 TΩ bleeder to ground so floating signal nets do
  not make the nodal matrix singular (negligible: <10 pA at rail voltages).

**Release tier: `advisory`.** A DC operating point is a computed estimate, not a
release-authoritative claim. Its correctness cannot be shown by inject-and-catch
alone (that is why H1 stays advisory until correlated against bench measurement —
see docs/h1-physics-evidence-plan.md). The solve *pipeline* is verified against a
hand-computed divider; extraction sanity is verified by rails resolving to their
nominal voltages. When ngspice is absent the result is `blocked`, never faked.
"""

from __future__ import annotations

import re
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .backends.command import resolve_tool
from .validation import (
    _component_resistance_ohms,
    _net_nominal_voltage,
    _rail_nominal_voltages,
)

# A tiny series value stands in for a 0 Ω jumper so ngspice keeps a distinct node.
_JUMPER_OHMS = 1e-3
# Leakage bleeder to keep otherwise-floating nodes solvable (negligible current).
_BLEEDER_OHMS = 1e12
# Rails are considered to resolve correctly if within this fraction of nominal.
_RAIL_TOLERANCE = 0.02


def ngspice_available() -> bool:
    return resolve_tool("ngspice") is not None


def _spice_node(net: str) -> str:
    """Map a net name to a SPICE node identifier (ground is node 0)."""
    if net == "GND":
        return "0"
    return "N_" + re.sub(r"[^A-Za-z0-9_]", "_", net)


@dataclass
class DcNetlist:
    text: str
    node_by_net: dict[str, str]
    sourced_rails: dict[str, float]  # net -> nominal voltage of its ideal source
    resistor_count: int = 0
    intermediate_nets: list[str] = field(default_factory=list)  # solvable non-rail nodes


def build_dc_netlist(graph: dict[str, Any], spec: dict[str, Any]) -> DcNetlist:
    rail_nominal = _rail_nominal_voltages(spec)
    components = graph.get("components", [])

    # Collect every net that appears on a resistor or a powered node.
    nets: set[str] = set()
    for net in graph.get("nets", []):
        if net.get("name"):
            nets.add(str(net["name"]))
    for component in components:
        for pin in component.get("pins", []):
            if pin.get("net"):
                nets.add(str(pin["net"]))

    node_by_net = {net: _spice_node(net) for net in sorted(nets)}

    sourced_rails: dict[str, float] = {}
    for net in sorted(nets):
        if net == "GND":
            continue
        voltage = _net_nominal_voltage(net, rail_nominal)
        if voltage is not None and voltage > 0.0:
            sourced_rails[net] = float(voltage)

    lines: list[str] = ["* hw-codesign DC operating point (advisory)"]

    for idx, (net, voltage) in enumerate(sorted(sourced_rails.items())):
        lines.append(f"V{idx} {node_by_net[net]} 0 DC {voltage:g}")

    resistor_count = 0
    for component in components:
        ohms = _component_resistance_ohms(component)
        if ohms is None:
            continue
        pin_nets = [str(pin.get("net")) for pin in component.get("pins", []) if pin.get("net")]
        distinct = list(dict.fromkeys(pin_nets))
        if len(distinct) != 2:
            # Not a clean two-terminal resistor in this net view; skip conservatively.
            continue
        a, b = distinct
        value = ohms if ohms > 0.0 else _JUMPER_OHMS
        ref = re.sub(r"[^A-Za-z0-9_]", "_", str(component.get("ref", f"r{resistor_count}")))
        lines.append(f"RR_{ref} {node_by_net[a]} {node_by_net[b]} {value:g}")
        resistor_count += 1

    # Bleeders on every non-ground node keep the matrix non-singular.
    for net, node in sorted(node_by_net.items()):
        if node != "0":
            lines.append(f"RBLEED_{node} {node} 0 {_BLEEDER_OHMS:g}")

    lines.extend([".control", "op", "print all", ".endc", ".end", ""])

    intermediate = sorted(net for net in node_by_net if net != "GND" and net not in sourced_rails)
    return DcNetlist(
        text="\n".join(lines),
        node_by_net=node_by_net,
        sourced_rails=sourced_rails,
        resistor_count=resistor_count,
        intermediate_nets=intermediate,
    )


def run_ngspice(netlist_text: str) -> dict[str, float]:
    """Run ngspice in batch mode and return solved node voltages by SPICE node name."""
    tool = resolve_tool("ngspice")
    if tool is None:
        raise RuntimeError("ngspice_not_available")
    with tempfile.TemporaryDirectory() as tmp:
        deck = Path(tmp) / "dc.cir"
        deck.write_text(netlist_text, encoding="utf-8")
        proc = subprocess.run(
            [tool, "-b", str(deck)],
            capture_output=True,
            text=True,
            timeout=60,
        )
    voltages: dict[str, float] = {}
    for line in proc.stdout.splitlines():
        match = re.match(r"^\s*([A-Za-z0-9_]+)\s*=\s*(-?[\d.]+e?[-+]?\d*)\s*$", line)
        if not match:
            continue
        name, raw = match.group(1), match.group(2)
        if name.endswith("branch") or "#" in name:
            continue
        try:
            voltages[name.lower()] = float(raw)
        except ValueError:
            continue
    return voltages


def dc_operating_point(graph: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
    """Advisory DC operating point. Returns a blocked result when ngspice is absent."""
    if not ngspice_available():
        return {
            "status": "blocked",
            "tier": "advisory",
            "code": "ngspice_not_available",
            "message": "Install ngspice to compute the DC operating point (advisory physics evidence).",
        }
    netlist = build_dc_netlist(graph, spec)
    if not netlist.sourced_rails:
        return {
            "status": "blocked",
            "tier": "advisory",
            "code": "no_powered_rails",
            "message": "No net resolved to a grounded nominal rail voltage; nothing to solve.",
        }
    solved = run_ngspice(netlist.text)

    def _v(net: str) -> float | None:
        node = netlist.node_by_net[net]
        return solved.get(node.lower())

    rails: dict[str, Any] = {}
    for net, nominal in sorted(netlist.sourced_rails.items()):
        got = _v(net)
        within = got is not None and abs(got - nominal) <= _RAIL_TOLERANCE * nominal
        rails[net] = {"nominal_v": nominal, "solved_v": got, "within_tolerance": within}

    nodes = {net: _v(net) for net in netlist.node_by_net if _v(net) is not None}
    # `rails` are modelled as ideal sources, so their solved value echoes the
    # nominal — this confirms the *extraction* sourced the right nets at the right
    # voltages, but is not itself a physics result. The genuinely computed evidence
    # is `intermediate_node_voltages`: divider/bias/sense nodes with no direct source,
    # whose value ngspice derives from the resistor network.
    extraction_ok = all(info["within_tolerance"] for info in rails.values())
    intermediate_node_voltages = {
        net: _v(net) for net in netlist.intermediate_nets if _v(net) is not None
    }
    return {
        "status": "advisory",
        "tier": "advisory",
        "tool": "ngspice",
        "rails": rails,
        "extraction_sourced_rails_ok": extraction_ok,
        "node_voltages": nodes,
        "intermediate_node_voltages": intermediate_node_voltages,
        "resistor_count": netlist.resistor_count,
        "intermediate_nets": netlist.intermediate_nets,
    }
