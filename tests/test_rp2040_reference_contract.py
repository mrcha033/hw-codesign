from __future__ import annotations

import json
from copy import deepcopy
from typing import Any, Callable

import pytest


def _generated_graph(service, template: str, project: str) -> tuple[dict[str, Any], dict[str, Any]]:
    service.create_project(project, template=template)
    service.generate_electronics_only(project)
    project_path = service.workspace.require_project(project)
    graph = json.loads((project_path / "electronics" / "generated" / "electrical_graph.json").read_text(encoding="utf-8"))
    return service.read_spec(project), graph


def _component_by_mpn(graph: dict[str, Any], mpn: str) -> dict[str, Any]:
    return next(component for component in graph["components"] if component.get("mpn") == mpn)


def _component_on_nets(graph: dict[str, Any], nets: set[str]) -> dict[str, Any]:
    return next(
        component
        for component in graph["components"]
        if {pin.get("net") for pin in component.get("pins", []) if pin.get("net")} == nets
        and len(component.get("pins", [])) == 2
    )


def _pin(component: dict[str, Any], number: str) -> dict[str, Any]:
    return next(pin for pin in component["pins"] if str(pin.get("number")) == number)


@pytest.mark.parametrize("template", ["rp2040_usb_device", "usb_hid_controller"])
def test_rp2040_reference_contract_passes_supported_templates(service, template: str):
    spec, graph = _generated_graph(service, template, f"{template}_reference_contract")

    assert service.validator.rp2040_reference_circuit_applicable(spec, graph) is True
    report = service.validator.check_rp2040_reference_circuit(graph)
    interface_report = service.validator.check_interface_integrity(graph)

    assert report.status.value == "pass", [failure.__dict__ for failure in report.failures]
    assert report.metrics["contract"] == "rp2040_usb_qspi_reference_v1"
    assert interface_report.status.value == "pass", [failure.__dict__ for failure in interface_report.failures]
    assert interface_report.metrics["usb_staged_protection_present"] is True
    assert interface_report.metrics["usb_series_resistors_checked"] == 2
    support_report = service._support_circuit_completeness_report(spec, graph)
    assert {
        "crystal_load_cap_missing",
        "crystal_load_cap_ground_missing",
        "crystal_load_cap_value_missing",
        "crystal_load_cap_value_out_of_range",
    }.isdisjoint({failure.code for failure in support_report.failures})


def test_generated_rp2040_uses_literal_manufacturer_pin_locations(service):
    # This literal oracle intentionally does not import graph-generator or
    # validation constants. A shared bad constant must not make the test pass.
    _spec, graph = _generated_graph(service, "rp2040_usb_device", "rp2040_literal_pin_oracle")
    mcu = _component_by_mpn(graph, "RP2040")
    pins = {str(pin["number"]): pin.get("net") for pin in mcu["pins"]}

    assert set(pins) == {str(number) for number in range(1, 58)}
    assert {number: pins[number] for number in (
        "1", "10", "19", "20", "21", "22", "23", "24", "25", "26", "33", "42", "43", "44", "45", "46", "47",
        "48", "49", "50", "51", "52", "53", "54", "55", "56", "57",
    )} == {
        "1": "V3V3",
        "10": "V3V3",
        "19": "GND",
        "20": "XIN",
        "21": "XOUT",
        "22": "V3V3",
        "23": "V1V1",
        "24": "SWCLK",
        "25": "SWDIO",
        "26": "MCU_RUN",
        "33": "V3V3",
        "42": "V3V3",
        "43": "V3V3",
        "44": "V3V3",
        "45": "V1V1",
        "46": "USB_DM",
        "47": "USB_DP",
        "48": "V3V3",
        "49": "V3V3",
        "50": "V1V1",
        "51": "QSPI_D3",
        "52": "QSPI_CLK",
        "53": "QSPI_MOSI",
        "54": "QSPI_D2",
        "55": "QSPI_MISO",
        "56": "QSPI_CS",
        "57": "GND",
    }

    mcu_decoupling_targets = {
        str(component["decouples"]["pin"])
        for component in graph["components"]
        if isinstance(component.get("decouples"), dict) and component["decouples"].get("ref") == mcu["ref"]
    }
    assert mcu_decoupling_targets == {"1", "10", "22", "23", "33", "42", "43", "44", "45", "48", "49", "50"}
    assert mcu["power_transfers"] == [{"input_pin": "44", "output_pin": "45", "kind": "internal_regulator"}]


def test_rp2040_reference_contract_rejects_unsafe_graph_mutations(service):
    _spec, graph = _generated_graph(service, "rp2040_usb_device", "rp2040_reference_mutations")
    mcu_ref = _component_by_mpn(graph, "RP2040")["ref"]
    flash_ref = _component_by_mpn(graph, "W25Q16JVSSIQ")["ref"]

    def missing_package_pin(mutated: dict[str, Any]) -> None:
        mcu = _component_by_mpn(mutated, "RP2040")
        mcu["pins"] = [pin for pin in mcu["pins"] if str(pin["number"]) != "50"]

    def wrong_core_supply(mutated: dict[str, Any]) -> None:
        _pin(_component_by_mpn(mutated, "RP2040"), "45")["net"] = "V3V3"

    def missing_mcu_decap(mutated: dict[str, Any]) -> None:
        mutated["components"] = [
            component
            for component in mutated["components"]
            if not (
                isinstance(component.get("decouples"), dict)
                and component["decouples"].get("ref") == mcu_ref
                and str(component["decouples"].get("pin")) == "23"
            )
        ]

    def swap_esd_output(mutated: dict[str, Any]) -> None:
        _pin(_component_by_mpn(mutated, "USBLC6-2SC6"), "4")["net"] = "USB_DP_ESD"

    def wrong_usb_series_value(mutated: dict[str, Any]) -> None:
        _component_on_nets(mutated, {"USB_DP_ESD", "USB_DP"})["value"] = "47R"

    def unground_crystal_case(mutated: dict[str, Any]) -> None:
        _pin(_component_by_mpn(mutated, "ABM8-272-T3"), "2")["net"] = "V3V3"

    def remove_crystal_feedback(mutated: dict[str, Any]) -> None:
        target = _component_on_nets(mutated, {"XOUT", "XTAL_RETURN"})
        mutated["components"] = [component for component in mutated["components"] if component["ref"] != target["ref"]]

    def wrong_crystal_load_value(mutated: dict[str, Any]) -> None:
        _component_on_nets(mutated, {"XIN", "GND"})["value"] = "33pF"

    def swap_flash_data(mutated: dict[str, Any]) -> None:
        _pin(_component_by_mpn(mutated, "W25Q16JVSSIQ"), "3")["net"] = "QSPI_D3"

    def missing_flash_decap(mutated: dict[str, Any]) -> None:
        mutated["components"] = [
            component
            for component in mutated["components"]
            if not (
                isinstance(component.get("decouples"), dict)
                and component["decouples"].get("ref") == flash_ref
                and str(component["decouples"].get("pin")) == "8"
            )
        ]

    def remove_flash_cs_pullup(mutated: dict[str, Any]) -> None:
        target = _component_on_nets(mutated, {"QSPI_CS", "V3V3"})
        mutated["components"] = [component for component in mutated["components"] if component["ref"] != target["ref"]]

    mutations: list[tuple[str, Callable[[dict[str, Any]], None], str]] = [
        ("missing package pin", missing_package_pin, "rp2040_mcu_pin_set_invalid"),
        ("wrong core supply", wrong_core_supply, "rp2040_mcu_pinout_invalid"),
        ("missing MCU bypass", missing_mcu_decap, "rp2040_decoupling_contract_invalid"),
        ("swapped ESD output", swap_esd_output, "rp2040_usb_esd_contract_invalid"),
        ("wrong USB series value", wrong_usb_series_value, "rp2040_usb_series_resistor_invalid"),
        ("ungrounded crystal case", unground_crystal_case, "rp2040_crystal_contract_invalid"),
        ("missing crystal feedback", remove_crystal_feedback, "rp2040_crystal_feedback_resistor_invalid"),
        ("wrong crystal load", wrong_crystal_load_value, "rp2040_crystal_load_capacitor_invalid"),
        ("swapped flash data", swap_flash_data, "rp2040_flash_contract_invalid"),
        ("missing flash bypass", missing_flash_decap, "rp2040_flash_decoupling_invalid"),
        ("missing flash CS pull-up", remove_flash_cs_pullup, "rp2040_flash_cs_pullup_invalid"),
    ]

    for label, mutate, expected_code in mutations:
        mutated = deepcopy(graph)
        mutate(mutated)
        report = service.validator.check_rp2040_reference_circuit(mutated)
        assert report.status.value == "fail", label
        assert expected_code in {failure.code for failure in report.failures}, label


def test_generic_usb_integrity_rejects_broken_staged_protection_paths(service):
    _spec, graph = _generated_graph(service, "rp2040_usb_device", "rp2040_usb_path_mutations")

    def missing_series_resistor(mutated: dict[str, Any]) -> None:
        target = _component_on_nets(mutated, {"USB_DP_ESD", "USB_DP"})
        mutated["components"] = [component for component in mutated["components"] if component["ref"] != target["ref"]]

    def wrong_series_resistor(mutated: dict[str, Any]) -> None:
        _component_on_nets(mutated, {"USB_DP_ESD", "USB_DP"})["value"] = "47R"

    def swapped_tvs_inputs(mutated: dict[str, Any]) -> None:
        esd = _component_by_mpn(mutated, "USBLC6-2SC6")
        _pin(esd, "1")["net"], _pin(esd, "3")["net"] = _pin(esd, "3")["net"], _pin(esd, "1")["net"]

    def swapped_series_pairs(mutated: dict[str, Any]) -> None:
        dp = _component_on_nets(mutated, {"USB_DP_ESD", "USB_DP"})
        dm = _component_on_nets(mutated, {"USB_DM_ESD", "USB_DM"})
        next(pin for pin in dp["pins"] if pin.get("net") == "USB_DP")["net"] = "USB_DM"
        next(pin for pin in dm["pins"] if pin.get("net") == "USB_DM")["net"] = "USB_DP"

    def missing_dp_net(mutated: dict[str, Any]) -> None:
        mutated["nets"] = [net for net in mutated["nets"] if net.get("name") != "USB_DP"]

    mutations: list[tuple[str, Callable[[dict[str, Any]], None], str]] = [
        ("missing series resistor", missing_series_resistor, "usb_series_resistor_missing"),
        ("wrong series resistor", wrong_series_resistor, "usb_series_resistor_value_invalid"),
        ("swapped TVS inputs", swapped_tvs_inputs, "usb_esd_bridge_pin_net_mismatch"),
        ("swapped series pairs", swapped_series_pairs, "usb_series_resistor_missing"),
        ("missing protected D+", missing_dp_net, "usb_differential_pair_incomplete"),
    ]

    for label, mutate, expected_code in mutations:
        mutated = deepcopy(graph)
        mutate(mutated)
        report = service.validator.check_interface_integrity(mutated)
        assert report.status.value == "fail", label
        assert expected_code in {failure.code for failure in report.failures}, label


def test_power_tree_uses_declared_internal_transfer_and_rejects_missing_or_malformed_metadata(service):
    spec, graph = _generated_graph(service, "rp2040_usb_device", "rp2040_internal_power_transfer")

    report = service.validator.check_power_tree(graph, spec)
    assert report.status.value == "pass", [failure.__dict__ for failure in report.failures]
    assert report.metrics["declared_power_transfers_checked"] == 1
    assert report.metrics["invalid_declared_power_transfers"] == 0
    assert "V1V1" in report.metrics["source_nets"]

    missing = deepcopy(graph)
    _component_by_mpn(missing, "RP2040").pop("power_transfers")
    missing_report = service.validator.check_power_tree(missing, spec)
    assert missing_report.status.value == "fail"
    assert any(
        failure.code == "power_net_unreachable" and failure.details.get("net_name") == "V1V1"
        for failure in missing_report.failures
    )

    malformed = deepcopy(graph)
    _component_by_mpn(malformed, "RP2040")["power_transfers"] = [
        {"input_pin": "999", "output_pin": "45", "kind": "internal_regulator"}
    ]
    malformed_report = service.validator.check_power_tree(malformed, spec)
    assert malformed_report.status.value == "fail"
    failure = next(failure for failure in malformed_report.failures if failure.code == "power_transfer_contract_invalid")
    assert failure.details["issues"] == ["input_pin_unresolved"]
    assert malformed_report.metrics["declared_power_transfers_checked"] == 0
    assert malformed_report.metrics["invalid_declared_power_transfers"] == 1


def test_normal_checks_include_rp2040_contract_only_for_rp2040_targets(service):
    rp_project = "rp2040_normal_gate"
    service.create_project(rp_project, template="rp2040_usb_device")
    service.generate_all(rp_project)
    project_path = service.workspace.require_project(rp_project)
    graph = json.loads((project_path / "electronics" / "generated" / "electrical_graph.json").read_text(encoding="utf-8"))
    pinmap = json.loads((project_path / "firmware" / "generated" / "pinmap.json").read_text(encoding="utf-8"))

    mcu = _component_by_mpn(graph, "RP2040")
    pins_by_endpoint = {f"{mcu['ref']}.{pin['number']}": pin for pin in mcu["pins"]}
    assert {item["net_name"] for item in pinmap}.isdisjoint({"V3V3", "V1V1", "GND"})
    assert all(pins_by_endpoint[item["graph_pin"]]["role"] not in {"power_in", "power_out", "ground"} for item in pinmap)
    assert service.validator.check_pinmap(pinmap).status.value == "pass"

    duplicated_signal = [*pinmap, deepcopy(pinmap[0])]
    conflict_report = service.validator.check_pinmap(duplicated_signal)
    assert conflict_report.status.value == "fail"
    assert "pin_conflict" in {failure.code for failure in conflict_report.failures}

    checks = service.run_all_checks(rp_project, include_external=False)
    reports = {report["gate"]: report for report in checks["reports"]}
    assert reports["rp2040_reference_circuit"]["status"] == "pass"

    non_rp_spec = {
        "project": {"template": "samd21_sensor_hub"},
        "compute": {"mcu": {"family": "SAMD21"}},
    }
    non_rp_graph = {"design_basis": {"architecture": "samd21_usb_sensor"}, "components": [], "nets": []}
    assert service.validator.rp2040_reference_circuit_applicable(non_rp_spec, non_rp_graph) is False
