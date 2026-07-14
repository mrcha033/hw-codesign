from __future__ import annotations

import json

import pytest

from hw_codesign import power_sim

# ---------------------------------------------------------------------------
# Solve-pipeline correctness against an independent (hand-computed) oracle
# ---------------------------------------------------------------------------

def _divider_graph() -> dict:
    # 5 V across two equal 1 kΩ resistors -> midpoint must solve to 2.5 V.
    return {
        "nets": [{"name": "V5"}, {"name": "MID"}, {"name": "GND"}],
        "components": [
            {"ref": "R1", "category": "resistor", "value": "1k",
             "pins": [{"number": "1", "net": "V5"}, {"number": "2", "net": "MID"}]},
            {"ref": "R2", "category": "resistor", "value": "1k",
             "pins": [{"number": "1", "net": "MID"}, {"number": "2", "net": "GND"}]},
        ],
    }


@pytest.mark.skipif(not power_sim.ngspice_available(), reason="ngspice not installed")
def test_ngspice_solves_known_divider_midpoint():
    result = power_sim.dc_operating_point(_divider_graph(), spec={})
    assert result["status"] == "advisory"
    # V5 sources at 5.0; the unpowered midpoint is a genuinely *computed* node.
    assert "MID" in result["intermediate_nets"]
    mid = result["node_voltages"]["MID"]
    assert abs(mid - 2.5) < 0.01, f"divider midpoint should solve to 2.5 V, got {mid}"
    assert result["rails"]["V5"]["within_tolerance"]


@pytest.mark.skipif(not power_sim.ngspice_available(), reason="ngspice not installed")
def test_ngspice_divider_ratio_tracks_resistor_values():
    # Change the ratio: 3k top / 1k bottom -> midpoint = 5 * 1/(3+1) = 1.25 V.
    graph = _divider_graph()
    graph["components"][0]["value"] = "3k"
    result = power_sim.dc_operating_point(graph, spec={})
    mid = result["node_voltages"]["MID"]
    assert abs(mid - 1.25) < 0.01, f"3k/1k divider should solve to 1.25 V, got {mid}"


def test_build_dc_netlist_sources_rails_and_omits_capacitors():
    graph = {
        "nets": [{"name": "V3V3"}, {"name": "SDA"}, {"name": "GND"}],
        "components": [
            {"ref": "R1", "category": "pullup", "value": "4k7",
             "pins": [{"net": "V3V3"}, {"net": "SDA"}]},
            {"ref": "C1", "category": "decoupling", "value": "100nF",
             "pins": [{"net": "V3V3"}, {"net": "GND"}]},
        ],
    }
    netlist = power_sim.build_dc_netlist(graph, spec={})
    # V3V3 is a grounded nominal rail -> gets an ideal source; capacitor is open at DC.
    assert "V3V3" in netlist.sourced_rails
    assert netlist.sourced_rails["V3V3"] == pytest.approx(3.3)
    assert netlist.resistor_count == 1  # only the pull-up, not the capacitor
    assert "C1" not in netlist.text and "decoupl" not in netlist.text.lower()


# ---------------------------------------------------------------------------
# Extraction sanity on a real generated design
# ---------------------------------------------------------------------------

@pytest.mark.skipif(not power_sim.ngspice_available(), reason="ngspice not installed")
def test_dc_operating_point_rails_resolve_to_nominal_on_real_design(service):
    project = "power_sim_rp2040"
    service.create_project(project, template="rp2040_usb_device")
    service.generate_electronics_only(project)
    project_path = service.workspace.require_project(project)
    graph = json.loads((project_path / "electronics" / "generated" / "electrical_graph.json").read_text(encoding="utf-8"))
    spec = service.read_spec(project)

    result = power_sim.dc_operating_point(graph, spec)

    assert result["status"] == "advisory"
    # Extraction sourced the right rails at the right nominal voltages.
    assert result["extraction_sourced_rails_ok"], f"rails did not resolve to nominal: {result['rails']}"
    assert result["rails"]["V3V3"]["solved_v"] == pytest.approx(3.3, abs=0.05)
    assert result["rails"]["USB_VBUS"]["solved_v"] == pytest.approx(5.0, abs=0.05)
    # Non-sourced nodes (e.g. pulled-up signal nets) are genuinely computed by ngspice
    # and must land within the powered rail envelope.
    for net, volts in result["intermediate_node_voltages"].items():
        assert -0.1 <= volts <= 25.0, f"computed node {net} = {volts} V is implausible"


# ---------------------------------------------------------------------------
# Tool-gated: blocked, never faked, when ngspice is unavailable
# ---------------------------------------------------------------------------

def test_dc_operating_point_blocked_without_ngspice(monkeypatch):
    monkeypatch.setattr(power_sim, "resolve_tool", lambda name: None)
    result = power_sim.dc_operating_point(_divider_graph(), spec={})
    assert result["status"] == "blocked"
    assert result["code"] == "ngspice_not_available"
    assert result["tier"] == "advisory"
