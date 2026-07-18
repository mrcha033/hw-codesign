from __future__ import annotations

import hashlib
import json
import subprocess
from copy import deepcopy
from pathlib import Path

import pytest

from hw_codesign.backends.freerouting import FreeroutingBackend
from hw_codesign.backends.kicad import KiCadBackend
from hw_codesign.backends.zephyr import ArmNewlibProbe
from hw_codesign.errors import UnsafeChangeError
from hw_codesign.reference_backend import _zone_net_layers, internal_drc, internal_erc
from hw_codesign.schematic_generator import generate_kicad_schematic


def test_generation_is_deterministic_and_cross_domain(service, project):
    first = service.generate_all(project)
    second = service.generate_all(project)
    assert first == second
    path = service.workspace.require_project(project)
    assert (path / "electronics" / "intent" / "board.intent.md").is_file()
    assert not list((path / "electronics" / "source").glob("*.ato"))
    assert (path / "mechanical" / "source" / "enclosure.py").is_file()
    assert (path / "firmware" / "generated" / "pinmap.h").is_file()
    assert (path / "electronics" / "generated" / "bom.csv").is_file()
    routing = json.loads((path / "electronics" / "generated" / "kicad" / "routing.json").read_text())
    assert routing["mode"] == "zone_connected_planes"
    assert routing["plane_connectivity"] == "copper_zones"
    assert routing["signal_routing"] == "deferred_to_freerouting"


def test_robotics_controller_kicad_artifacts_keep_four_layer_stackup(service, project):
    service.generate_electronics_only(project)
    path = service.workspace.require_project(project)
    kicad_dir = path / "electronics" / "generated" / "kicad"
    legacy_schematic = (kicad_dir / f"{project}.sch").read_text(encoding="utf-8")
    board = (kicad_dir / f"{project}.kicad_pcb").read_text(encoding="utf-8")
    routing = json.loads((kicad_dir / "routing.json").read_text(encoding="utf-8"))

    assert 'Title "Robot Controller"' in legacy_schematic
    assert '(0 "F.Cu" signal)' in board
    assert '(2 "In1.Cu" power)' in board
    assert '(4 "In2.Cu" power)' in board
    assert '(31 "B.Cu" signal)' in board
    assert '(net_name "GND") (layer "In1.Cu")' in board
    assert '(net_name "V5") (layer "In2.Cu")' in board
    assert '  (segment (start ' in board
    assert '  (via (at ' in board
    assert routing["plane_escape"] == "fcu_segment_to_through_via"
    assert routing["plane_escape_required"] > 0
    assert routing["plane_escape_count"] == routing["plane_escape_required"]


def test_ir_pcb_sanity_requires_multilayer_smd_plane_escape_via(service, project):
    service.generate_electronics_only(project)
    path = service.workspace.require_project(project)
    spec = service.read_spec(project)
    graph = json.loads(
        (path / "electronics" / "generated" / "electrical_graph.json").read_text(
            encoding="utf-8"
        )
    )
    board_path = path / "electronics" / "generated" / "kicad" / f"{project}.kicad_pcb"
    board = board_path.read_text(encoding="utf-8")
    start = board.index("  (via (at ")
    end = board.index("\n", start)
    board_path.write_text(board[:start] + board[end + 1:], encoding="utf-8")

    report = internal_drc(path, spec, graph)

    assert report.status.value == "fail"
    failure = next(item for item in report.failures if item.code == "plane_escape_missing")
    assert failure.details["missing"]
    assert {"ref", "pad", "net", "plane_layer", "pad_at_mm"} <= set(
        failure.details["missing"][0]
    )


def test_ir_pcb_sanity_rejects_layers_outside_stackup(service):
    project = "sensor_logger_bad_layer_artifact"
    service.create_project(project, template="sensor_data_logger")
    service.generate_electronics_only(project)
    path = service.workspace.require_project(project)
    spec = service.read_spec(project)
    graph = json.loads((path / "electronics" / "generated" / "electrical_graph.json").read_text(encoding="utf-8"))
    board_path = path / "electronics" / "generated" / "kicad" / f"{project}.kicad_pcb"
    board = board_path.read_text(encoding="utf-8")
    board = board.replace('    (31 "B.Cu" signal)', '    (2 "In1.Cu" power)\n    (31 "B.Cu" signal)', 1)
    board = board.replace(
        '  (gr_rect',
        '  (zone (net 1) (net_name "GND") (layer "In1.Cu") (polygon (pts (xy 1 1) (xy 2 1) (xy 2 2) (xy 1 2))))\n  (gr_rect',
        1,
    )
    board_path.write_text(board, encoding="utf-8")

    report = internal_drc(path, spec, graph)

    assert report.status.value == "fail"
    codes = {failure.code for failure in report.failures}
    assert "pcb_stackup_layer_mismatch" in codes
    assert "pcb_layer_not_in_stackup" in codes
    assert "In1.Cu" in report.metrics["declared_copper_layers"]


def test_ir_pcb_sanity_requires_zone_for_each_declared_plane(service):
    project = "sensor_logger_missing_plane_zone"
    service.create_project(project, template="sensor_data_logger")
    service.generate_electronics_only(project)
    path = service.workspace.require_project(project)
    spec = service.read_spec(project)
    graph = json.loads((path / "electronics" / "generated" / "electrical_graph.json").read_text(encoding="utf-8"))
    board_path = path / "electronics" / "generated" / "kicad" / f"{project}.kicad_pcb"
    board = board_path.read_text(encoding="utf-8")
    start = board.index('  (zone (net ', board.index('(net_name "GND")') - 30)
    end = board.index('  (gr_rect', start)
    board_path.write_text(board[:start] + board[end:], encoding="utf-8")

    report = internal_drc(path, spec, graph)

    assert report.status.value == "fail"
    assert "plane_zone_missing" in {failure.code for failure in report.failures}


def test_ir_pcb_sanity_requires_two_layer_smd_plane_escape_via(service):
    project = "sensor_logger_missing_plane_escape"
    service.create_project(project, template="sensor_data_logger")
    service.generate_electronics_only(project)
    path = service.workspace.require_project(project)
    spec = service.read_spec(project)
    graph = json.loads((path / "electronics" / "generated" / "electrical_graph.json").read_text(encoding="utf-8"))
    board_path = path / "electronics" / "generated" / "kicad" / f"{project}.kicad_pcb"
    board = board_path.read_text(encoding="utf-8")
    assert '(net_name "GND") (layer "B.Cu")' in board
    assert '(net_name "GND") (layer "F.Cu")' not in board
    start = board.index("  (via (at ")
    end = board.index("\n", start)
    board_path.write_text(board[:start] + board[end + 1:], encoding="utf-8")

    report = internal_drc(path, spec, graph)

    assert report.status.value == "fail"
    failure = next(item for item in report.failures if item.code == "plane_escape_missing")
    assert failure.details["missing"]


def test_zone_parser_accepts_generated_and_kicad_formatted_net_syntax():
    board = '''
  (zone (net 1) (net_name "GND") (layer "B.Cu") (hatch edge 0.5))
  (zone
    (net "GND")
    (layer "F.Cu")
    (hatch edge 0.5)
  )
'''

    assert _zone_net_layers(board) == {"GND": {"B.Cu", "F.Cu"}}


def test_kicad_artifact_selection_prefers_canonical_board(service):
    project = "rp2040_kicad_stale_duplicate_check"
    service.create_project(project, template="rp2040_usb_device")
    service.generate_electronics_only(project)
    path = service.workspace.require_project(project)
    kicad_dir = path / "electronics" / "generated" / "kicad"
    canonical = kicad_dir / f"{project}.kicad_pcb"
    stale = kicad_dir / f"{project} 2.kicad_pcb"
    stale_contents = '(kicad_pcb (version 20240108) (generator stale_duplicate))\n'
    stale.write_text(stale_contents, encoding="utf-8")

    assert KiCadBackend()._design_file(path, "*.kicad_pcb") == canonical

    service.generate_electronics_only(project)
    assert canonical.is_file()
    assert stale.read_text(encoding="utf-8") == stale_contents


def test_rp2040_qspi_flash_uses_all_quad_data_lines(service):
    project = "rp2040_usb_device_check"
    service.create_project(project, template="rp2040_usb_device")
    service.generate_electronics_only(project)
    path = service.workspace.require_project(project)
    graph = json.loads((path / "electronics" / "generated" / "electrical_graph.json").read_text(encoding="utf-8"))
    provenance_report = service.validator.check_component_metadata(graph["components"])
    assert provenance_report.status.value == "pass"
    interface_report = service.validator.check_interface_integrity(graph)
    assert interface_report.status.value == "pass"
    assert interface_report.metrics["usb_bridge_present"] is True
    power_tree_report = service.validator.check_power_tree(graph, service.read_spec(project))
    assert power_tree_report.status.value == "pass"
    assert {"USB_VBUS", "V3V3"} <= set(power_tree_report.metrics["source_nets"])
    power_integrity_report = service.validator.check_power_integrity_estimate(graph, service.read_spec(project))
    assert power_integrity_report.status.value == "pass"
    ldo_input_cap = next(
        item
        for item in graph["components"]
        if item.get("decouples") == {"ref": "U1", "pin": "3"}
    )
    assert ldo_input_cap["category"] == "decoupling"
    assert ldo_input_cap["value"].startswith("1uF")
    assert {pin["net"] for pin in ldo_input_cap["pins"]} == {"USB_VBUS", "GND"}

    flash = next(item for item in graph["components"] if item["ref"] == "U3")
    flash_pins = {pin["number"]: pin for pin in flash["pins"]}
    assert flash_pins["3"]["name"] == "IO2/~WP"
    assert flash_pins["3"]["net"] == "QSPI_D2"
    assert flash_pins["3"]["role"] == "bidirectional"
    assert flash_pins["7"]["name"] == "IO3/~HOLD"
    assert flash_pins["7"]["net"] == "QSPI_D3"
    assert flash_pins["7"]["role"] == "bidirectional"

    nets = {net["name"]: set(net["connected_pins"]) for net in graph["nets"]}
    assert {"J1.A6", "J1.B6", "D1.1"} <= nets["USB_DP_RAW"]
    assert {"J1.A7", "J1.B7", "D1.3"} <= nets["USB_DM_RAW"]
    assert {"D1.6", "R1.1"} <= nets["USB_DP_ESD"]
    assert {"D1.4", "R2.1"} <= nets["USB_DM_ESD"]
    assert {"R1.2", "U2.47"} <= nets["USB_DP"]
    assert {"R2.2", "U2.46"} <= nets["USB_DM"]
    assert {"U2.54", "U3.3"} <= nets["QSPI_D2"]
    assert {"U2.51", "U3.7"} <= nets["QSPI_D3"]

    positions = {item["ref"]: item["pcb_position_mm"] for item in graph["components"]}
    assert positions["J1"][0] < positions["U2"][0] < positions["U3"][0]
    assert all(0.0 <= coordinate <= limit for ref in ("J1", "U2", "U3") for coordinate, limit in zip(positions[ref], (51.0, 21.0), strict=True))

    debug_pins = {pin["number"]: pin for pin in next(item for item in graph["components"] if item["ref"] == "J2")["pins"]}
    assert debug_pins["6"]["name"] == "SWO"
    assert debug_pins["6"]["net"] is None
    assert debug_pins["6"]["role"] == "no_connect"
    assert debug_pins["10"]["name"] == "RUN"
    assert debug_pins["10"]["net"] == "MCU_RUN"
    assert internal_erc(graph).status.value == "pass"
    routing = json.loads((path / "electronics" / "generated" / "kicad" / "routing.json").read_text(encoding="utf-8"))
    assert routing["status"] == "generated"
    assert routing["failures"] == []
    spec = service.read_spec(project)
    assert spec["manufacturing"]["pcb"]["min_clearance_mm"] >= 0.15
    assert spec["manufacturing"]["pcb"]["min_track_width_mm"] >= 0.15
    ir_drc_report = internal_drc(path, spec, graph)
    assert ir_drc_report.status.value == "pass"

    board = (path / "electronics" / "generated" / "kicad" / f"{project}.kicad_pcb").read_text(encoding="utf-8")
    assert 'footprint "Package_DFN_QFN:QFN-56-1EP_7x7mm_P0.4mm_EP3.2x3.2mm"' in board
    assert 'footprint "Package_SO:SOIC-8_5.3x5.3mm_P1.27mm"' in board
    assert 'footprint "Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm"' in board


def test_rp2040_template_conforms_to_current_spec_schema(service):
    project = "rp2040_template_schema_check"
    service.create_project(project, template="rp2040_usb_device")

    report = service.validator.validate_spec(service.read_spec(project))

    assert report.status.value == "pass", [failure.__dict__ for failure in report.failures]


@pytest.mark.parametrize(
    "template",
    [
        "esp32_wifi_gateway",
        "avr_32u4_hid",
        "stm32g0_power_monitor",
        "samd21_sensor_hub",
        "nrf52840_dongle",
    ],
)
def test_usb_templates_bridge_raw_connector_nets_to_protected_usb_nets(service, template):
    project = f"{template}_usb_bridge_check"
    service.create_project(project, template=template)
    service.generate_electronics_only(project)
    path = service.workspace.require_project(project)
    graph = json.loads((path / "electronics" / "generated" / "electrical_graph.json").read_text(encoding="utf-8"))

    report = service.validator.check_interface_integrity(graph)
    codes = {failure.code for failure in report.failures}
    assert "usb_differential_pair_incomplete" not in codes
    assert "usb_esd_bridge_missing" not in codes
    assert report.metrics["usb_bridge_present"] is True

    metadata_report = service.validator.check_component_metadata(graph["components"])
    assert [failure.code for failure in metadata_report.failures if failure.path == "D1"] == []

    d1 = next(component for component in graph["components"] if component["ref"] == "D1")
    assert {pin["net"] for pin in d1["pins"] if pin.get("net")} == {
        "USB_DP_RAW",
        "USB_DM_RAW",
        "USB_DP",
        "USB_DM",
        "USB_VBUS",
        "GND",
    }
    nets = {net["name"]: set(net["connected_pins"]) for net in graph["nets"]}
    assert {"J1.A6", "J1.B6", "D1.1"} <= nets["USB_DP_RAW"]
    assert {"J1.A7", "J1.B7", "D1.3"} <= nets["USB_DM_RAW"]
    assert "D1.6" in nets["USB_DP"]
    assert "D1.4" in nets["USB_DM"]


@pytest.mark.parametrize("template", ["lora_sensor_node", "samd21_sensor_hub", "stm32g0_power_monitor"])
def test_i2c_templates_include_recognized_pullups_to_logic_rail(service, template):
    project = f"{template}_i2c_pullup_check"
    service.create_project(project, template=template)
    service.generate_electronics_only(project)
    path = service.workspace.require_project(project)
    graph = json.loads((path / "electronics" / "generated" / "electrical_graph.json").read_text(encoding="utf-8"))

    report = service.validator.check_interface_integrity(graph)

    assert report.status.value == "pass"
    assert "i2c_pullup_missing" not in {failure.code for failure in report.failures}
    nets = {net["name"]: set(net["connected_pins"]) for net in graph["nets"]}
    components_by_ref = {component["ref"]: component for component in graph["components"]}
    for net_name in ("I2C_SCL", "I2C_SDA"):
        pullup_refs = {
            endpoint.partition(".")[0]
            for endpoint in nets[net_name]
            if components_by_ref[endpoint.partition(".")[0]].get("category")
            in {"pullup", "i2c_pullup", "resistor_4k7"}
            and any(pin.get("net") == "V3V3" for pin in components_by_ref[endpoint.partition(".")[0]].get("pins", []))
        }
        assert pullup_refs


def test_samd21_sensor_hub_uses_curated_sensor_and_debug_pin_contracts(service):
    project = "samd21_sensor_contract_check"
    service.create_project(project, template="samd21_sensor_hub")
    service.generate_all(project)
    path = service.workspace.require_project(project)
    graph = json.loads((path / "electronics" / "generated" / "electrical_graph.json").read_text(encoding="utf-8"))
    mechanical_contract = json.loads((path / "mechanical" / "source" / "mechanical_contract.json").read_text(encoding="utf-8"))

    metadata_report = service.validator.check_component_metadata(graph["components"])
    assert metadata_report.status.value == "pass"
    assert mechanical_contract["connector_cutouts"]
    assert service.validator.validate_spec(service.read_spec(project)).status.value == "pass"
    assert service.validator.check_electrical_semantics(service.read_spec(project)).status.value == "pass"
    assert service.validator.check_mechanical(service.read_spec(project)).status.value == "pass"
    firmware_modules_report = service.validator.check_firmware_modules(
        service.read_spec(project)["firmware"]["modules"],
        json.loads((path / "firmware" / "generated" / "pinmap.json").read_text(encoding="utf-8")),
        spec=service.read_spec(project),
        graph=graph,
        module_dir=path / "firmware" / "modules",
    )
    assert firmware_modules_report.status.value == "pass"
    assert internal_erc(graph).status.value == "pass"

    components = {component["ref"]: component for component in graph["components"]}
    mcu_pins = {pin["number"]: pin for pin in components["U2"]["pins"]}
    assert mcu_pins["27"]["net"] == "IMU_INT1"
    imu_pins = {pin["number"]: pin for pin in components["U3"]["pins"]}
    assert imu_pins["2"]["name"] == "SDX"
    assert imu_pins["2"]["net"] == "I2C_SDA"
    assert imu_pins["3"]["name"] == "SCX"
    assert imu_pins["3"]["net"] == "I2C_SCL"
    assert imu_pins["4"]["net"] == "IMU_INT1"
    assert imu_pins["5"]["net"] is None
    assert imu_pins["5"]["role"] == "no_connect"

    env_pins = {pin["number"]: pin for pin in components["U4"]["pins"]}
    assert {number: env_pins[number]["name"] for number in map(str, range(1, 9))} == {
        "1": "VDD",
        "2": "VDDIO",
        "3": "GND",
        "4": "SDI_SDA",
        "5": "SCK_SCL",
        "6": "SDO_ADDR",
        "7": "CSB",
        "8": "GND2",
    }
    assert env_pins["4"]["net"] == "I2C_SDA"
    assert env_pins["5"]["net"] == "I2C_SCL"
    assert env_pins["8"]["net"] == "GND"
    assert env_pins["8"]["role"] == "ground"

    debug_pins = {pin["number"]: pin for pin in components["J2"]["pins"]}
    assert debug_pins["6"]["name"] == "SWO"
    assert debug_pins["6"]["net"] is None
    assert debug_pins["6"]["role"] == "no_connect"
    assert debug_pins["7"]["name"] == "KEY"
    assert debug_pins["7"]["net"] is None
    assert debug_pins["7"]["role"] == "no_connect"
    assert debug_pins["8"]["name"] == "NC"
    assert debug_pins["8"]["net"] is None
    assert debug_pins["8"]["role"] == "no_connect"
    assert debug_pins["10"]["name"] == "RESET"
    assert debug_pins["10"]["net"] == "MCU_NRST"

    vddcore_cap = components["C6"]
    assert vddcore_cap["component_id"] == "grm188_1uf"
    assert {pin["net"] for pin in vddcore_cap["pins"]} == {"VDDCORE", "GND"}

    positions = {item["ref"]: item["pcb_position_mm"] for item in graph["components"]}
    assert positions["J1"][0] < positions["U3"][0]
    assert positions["D1"][0] < positions["U4"][0]
    assert positions["J2"][0] > positions["U3"][0]
    assert all(ref in positions for ref in ("J1", "D1", "U3", "U4", "J2"))

    routing = json.loads((path / "electronics" / "generated" / "kicad" / "routing.json").read_text(encoding="utf-8"))
    assert routing["status"] == "generated"
    assert routing["failures"] == []
    assert internal_drc(path, service.read_spec(project), graph).status.value == "pass"


def test_generic_i2c_pullup_on_wrong_rail_fails_interface_integrity(service):
    project = "lora_sensor_node_i2c_wrong_rail_check"
    service.create_project(project, template="lora_sensor_node")
    service.generate_electronics_only(project)
    path = service.workspace.require_project(project)
    graph = json.loads((path / "electronics" / "generated" / "electrical_graph.json").read_text(encoding="utf-8"))
    bad_graph = deepcopy(graph)
    for component in bad_graph["components"]:
        if component.get("category") != "resistor_4k7":
            continue
        if not any(pin.get("net") in {"I2C_SCL", "I2C_SDA"} for pin in component.get("pins", [])):
            continue
        supply_pin = next(pin for pin in component["pins"] if pin.get("net") == "V3V3")
        supply_pin["net"] = "VBAT"

    report = service.validator.check_interface_integrity(bad_graph)

    assert report.status.value == "fail"
    failures = [failure for failure in report.failures if failure.code == "i2c_pullup_voltage_mismatch"]
    assert {failure.details["net_name"] for failure in failures} == {"I2C_SCL", "I2C_SDA"}
    for failure in failures:
        assert failure.details["pullup_rails"] == ["VBAT"]
        assert failure.details["endpoint_supply_nets"] == ["V3V3"]


@pytest.mark.parametrize(
    "template",
    [
        "ble_sensor_node",
        "usb_hid_controller",
        "lora_sensor_node",
        "bldc_esc",
        "esp32_wifi_gateway",
        "stm32g0_power_monitor",
        "rp2040_usb_device",
        "samd21_sensor_hub",
        "nrf52840_dongle",
    ],
)
def test_ap2112_regulators_match_curated_sot23_5_pin_contract(service, template):
    project = f"{template}_ap2112_pin_contract_check"
    service.create_project(project, template=template)
    service.generate_electronics_only(project)
    path = service.workspace.require_project(project)
    graph = json.loads((path / "electronics" / "generated" / "electrical_graph.json").read_text(encoding="utf-8"))
    regulators = [
        component
        for component in graph["components"]
        if component.get("mpn") == "AP2112K-3.3TRG1"
    ]

    assert regulators
    metadata_report = service.validator.check_component_metadata(graph["components"])
    for regulator in regulators:
        pins = {pin["number"]: pin for pin in regulator["pins"]}
        input_net = pins["3"]["net"]
        assert {number: pins[number]["name"] for number in ("1", "2", "3", "4", "5")} == {
            "1": "EN",
            "2": "GND",
            "3": "VIN",
            "4": "NC",
            "5": "VOUT",
        }
        assert pins["1"]["net"] == input_net
        assert pins["1"]["role"] == "input"
        assert pins["2"]["net"] == "GND"
        assert pins["2"]["role"] == "ground"
        assert pins["3"]["role"] == "power_in"
        assert pins["4"]["net"] is None
        assert pins["4"]["role"] == "no_connect"
        assert pins["5"]["net"] == "V3V3"
        assert pins["5"]["role"] == "power_out"
        regulator_failures = [
            failure
            for failure in metadata_report.failures
            if failure.details.get("ref") == regulator["ref"] or failure.path == regulator["ref"]
        ]
        assert regulator_failures == []


@pytest.mark.parametrize("template", ["esp32_wifi_gateway", "stm32g0_power_monitor", "nrf52840_dongle"])
def test_usb_vbus_loads_have_input_bulk_capacitor(service, template):
    project = f"{template}_usb_vbus_bulk_check"
    service.create_project(project, template=template)
    service.generate_electronics_only(project)
    path = service.workspace.require_project(project)
    spec = service.read_spec(project)
    graph = json.loads((path / "electronics" / "generated" / "electrical_graph.json").read_text(encoding="utf-8"))

    report = service.validator.check_power_integrity_estimate(graph, spec)

    assert report.status.value == "pass"
    assert "rail_decoupling_missing" not in {failure.code for failure in report.failures}
    assert report.metrics["coverage"]["USB_VBUS"]["bulk"]
    bulk_caps = [
        component
        for component in graph["components"]
        if component.get("category") == "bulk_cap"
        and {pin.get("net") for pin in component.get("pins", [])} == {"USB_VBUS", "GND"}
    ]
    assert bulk_caps


def test_bldc_esc_includes_reverse_polarity_and_can_termination_support(service):
    project = "bldc_esc_support_check"
    service.create_project(project, template="bldc_esc")
    result = service.generate_electronics_only(project)
    path = service.workspace.require_project(project)
    spec = service.read_spec(project)
    graph = json.loads((path / "electronics" / "generated" / "electrical_graph.json").read_text(encoding="utf-8"))

    assert result["resolution_report"]["status"] == "pass"
    support_report = service._support_circuit_completeness_report(spec, graph)
    interface_report = service.validator.check_interface_integrity(graph)
    power_tree_report = service.validator.check_power_tree(graph, spec)
    power_integrity_report = service.validator.check_power_integrity_estimate(graph, spec)

    assert support_report.status.value == "pass"
    assert interface_report.status.value == "pass"
    assert power_tree_report.status.value == "pass"
    assert "missing_required_protection_role" not in {failure.code for failure in support_report.failures}
    assert "can_termination_missing" not in {failure.code for failure in interface_report.failures}
    assert [
        failure.details["rail"]
        for failure in power_integrity_report.failures
        if failure.code == "rail_bulk_cap_missing"
    ] == ["V3V3"]

    components = {component["ref"]: component for component in graph["components"]}
    assert {pin["net"] for pin in components["Q4"]["pins"] if pin.get("net")} == {"VBAT_RAW", "VBAT", "GND"}
    assert {pin["net"] for pin in components["R3"]["pins"]} == {"CANH", "CANL"}
    roles = {
        (item["ref"], item["role"], item["component_id"], item["resolution"])
        for item in graph["component_resolution"]
    }
    assert ("Q4", "reverse_polarity", "lm74700qdbvrq1", "curated") in roles
    assert ("R3", "resistor_120r", "rc0603_120r", "curated") in roles


def test_rp2040_firmware_profile_and_stack_modules_are_graph_grounded(service):
    project = "rp2040_usb_device_firmware_check"
    service.create_project(project, template="rp2040_usb_device")
    service.generate_all(project)
    path = service.workspace.require_project(project)
    spec = service.read_spec(project)
    graph = json.loads((path / "electronics" / "generated" / "electrical_graph.json").read_text(encoding="utf-8"))
    pinmap = json.loads((path / "firmware" / "generated" / "pinmap.json").read_text(encoding="utf-8"))

    board_dir = path / "firmware" / "zephyr" / "boards" / "arm" / "rp2040_usb_device"
    dts = (board_dir / "rp2040_usb_device.dts").read_text(encoding="utf-8")
    defconfig = (board_dir / "rp2040_usb_device_defconfig").read_text(encoding="utf-8")
    board_yml = (board_dir / "board.yml").read_text(encoding="utf-8")
    board_metadata = (board_dir / "rp2040_usb_device.yaml").read_text(encoding="utf-8")
    board_kconfig = (board_dir / "Kconfig.rp2040_usb_device").read_text(encoding="utf-8")
    prj_conf = (path / "firmware" / "zephyr" / "app" / "prj.conf").read_text(encoding="utf-8")
    modules_cmake = (path / "firmware" / "modules" / "CMakeLists.txt").read_text(encoding="utf-8")
    pin_signals = {item["signal"] for item in pinmap}

    assert "#include <raspberrypi/rpi_pico/rp2040.dtsi>" in dts
    assert "#include <mem.h>" in dts
    assert "stm32h743" not in dts.lower()
    assert "zephyr,sram = &sram0" in dts
    assert "zephyr,flash = &flash0" in dts
    assert "zephyr,flash-controller = &ssi" in dts
    assert "zephyr,code-partition = &code_partition" in dts
    assert "reg = <0x10000000 DT_SIZE_M(2)>" in dts
    assert "code_partition: partition@100" in dts
    assert "reg = <0x100 (DT_SIZE_M(2) - 0x100)>" in dts
    assert all(f"&{node} {{\n\tstatus = \"okay\";" in dts for node in ("gpio0", "timer", "wdt0"))
    assert "zephyr_udc0: &usbd {\n\tstatus = \"okay\";" in dts
    assert "&vreg {\n\tregulator-always-on;" in dts
    assert "&xosc {\n\tstartup-delay-multiplier = <64>;" in dts

    assert "name: rp2040_usb_device" in board_yml
    assert "vendor: hw" in board_yml
    assert "- name: rp2040" in board_yml
    assert "identifier: rp2040_usb_device" in board_metadata
    assert "flash: 2048" in board_metadata
    assert "ram: 264" in board_metadata
    assert "  - usbd" in board_metadata
    assert "select SOC_RP2040" in board_kconfig
    assert "select RP2_FLASH_W25Q080" in board_kconfig

    assert "CONFIG_USE_DT_CODE_PARTITION=y" in defconfig
    assert "CONFIG_BUILD_OUTPUT_UF2=y" in defconfig
    assert "CONFIG_BUILD_OUTPUT_HEX=y" in defconfig
    assert "CONFIG_RESET=y" in defconfig
    assert "CONFIG_CLOCK_CONTROL=y" in defconfig
    assert "CONFIG_SPI=y" in prj_conf
    assert "CONFIG_USB_DEVICE_STACK=y" in prj_conf
    assert "${CMAKE_CURRENT_LIST_DIR}/usb_hid_stack.c" in modules_cmake
    assert "${CMAKE_CURRENT_LIST_DIR}/../generated" in modules_cmake
    assert {"USB_DP", "USB_DM", "QSPI_CLK", "QSPI_D2", "QSPI_D3"} <= pin_signals
    assert (path / "firmware" / "modules" / "usb_hid_stack.c").is_file()

    modules_report = service.validator.check_firmware_modules(
        spec["firmware"]["modules"],
        pinmap,
        spec=spec,
        graph=graph,
    )
    assert modules_report.status.value == "pass"
    assert modules_report.metrics["module_count"] == 4


def test_kicad_schematic_preserves_duplicate_power_pins(tmp_path):
    graph = {
        "components": [{
            "ref": "J1",
            "value": "DUPLICATE_POWER_PINS",
            "footprint": "Connector_Generic:Conn_01x04",
            "mpn": "TEST",
            "manufacturer": "test",
            "supplier_sku": "TEST",
            "pins": [
                {"number": "1", "name": "GND1", "net": "GND"},
                {"number": "2", "name": "GND2", "net": "GND"},
                {"number": "3", "name": "VDD1", "net": "V3V3"},
                {"number": "4", "name": "VDD2", "net": "V3V3"},
            ],
        }],
        "nets": [{"name": "GND"}, {"name": "V3V3"}],
    }
    output = tmp_path / "duplicate_power_pins.kicad_sch"

    generate_kicad_schematic("duplicate_power_pins", graph, output)

    text = output.read_text(encoding="utf-8")
    assert "Connector_Generic:Conn_01x04" in text
    assert text.count('"GND"') >= 2
    assert text.count('"V3V3"') >= 2


def test_freerouting_log_parser_distinguishes_complete_and_incomplete():
    assert FreeroutingBackend._final_unrouted("final score: 988.64 (1 unrouted)\n") == 1
    assert FreeroutingBackend._final_unrouted("final score: 861.22 (7 unrouted and 10 violations)\n") == 7
    assert FreeroutingBackend._final_routing_metrics("final score: 861.22 (7 unrouted and 10 violations)\n") == (7, 10)
    assert FreeroutingBackend._final_unrouted("final score: 992.25\nSaving board\n") == 0


def test_freerouting_cache_is_bound_to_board_content(tmp_path, monkeypatch):
    project = tmp_path / "cache_board"
    target = project / "electronics" / "generated" / "kicad"
    target.mkdir(parents=True)
    board = target / "cache_board.kicad_pcb"
    board.write_text("(kicad_pcb)\n", encoding="utf-8")
    routing = {
        "status": "pass",
        "signal_routing": "complete",
        "plane_connectivity": "copper_zones",
        "design_rules": None,
        "post_import_unconnected": 0,
        "board_sha256": hashlib.sha256(board.read_bytes()).hexdigest(),
    }
    (target / "routing.json").write_text(json.dumps(routing), encoding="utf-8")
    backend = FreeroutingBackend(tmp_path)
    monkeypatch.setattr(backend, "_tools", lambda: {"java": None, "jar": None, "kicad_python": None})

    cached = backend.route(project)
    assert cached.status.value == "pass"
    assert cached.metrics["cached"] is True

    board.write_text("(kicad_pcb (net 1 \"changed\"))\n", encoding="utf-8")
    stale = backend.route(project)
    assert stale.status.value == "blocked"
    assert stale.failures[0].code == "tool_unavailable"


def _write_failed_freerouting_cache(tmp_path):
    project = tmp_path / "failed_cache_board"
    target = project / "electronics" / "generated" / "kicad"
    target.mkdir(parents=True)
    board = target / "failed_cache_board.kicad_pcb"
    board.write_text(
        "(kicad_pcb\n  (zone\n    (filled_polygon\n    )\n  )\n)\n",
        encoding="utf-8",
    )
    (target / "failed_cache_board.kicad_pro").write_text(
        json.dumps(
            {
                "board": {
                    "design_settings": {
                        "rules": {"min_clearance": 0.15, "min_track_width": 0.18}
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    payload = {
        "status": "fail",
        "signal_routing": "complete",
        "plane_connectivity": "incomplete",
        "zone_fill": "persisted",
        "zone_count": 1,
        "filled_polygon_count": 1,
        "design_rules": {"min_clearance_mm": 0.15, "min_track_width_mm": 0.18},
        "post_import_unconnected": 7,
        "unrouted": 7,
        "violations": 0,
        "max_passes": 20,
        "freerouting_version": "2.2.4",
        "board_sha256": hashlib.sha256(board.read_bytes()).hexdigest(),
        "failures": [
            {
                "category": "EDA_ERROR",
                "code": "routing_incomplete_after_zone_fill",
                "details": {"unconnected": 7},
            }
        ],
    }
    routing_report = target / "routing.json"
    routing_report.write_text(json.dumps(payload), encoding="utf-8")
    return project, board, routing_report, payload


def test_freerouting_caches_authoritative_post_fill_connectivity_failure(
    tmp_path, monkeypatch
):
    project, board, routing_report, _ = _write_failed_freerouting_cache(tmp_path)
    backend = FreeroutingBackend(tmp_path)
    monkeypatch.setattr(
        backend,
        "_tools",
        lambda: pytest.fail("an authoritative failed route must not invoke tools"),
    )

    report = backend.route(project)

    assert report.status.value == "fail"
    assert report.failures[0].code == "routing_incomplete_after_zone_fill"
    assert report.failures[0].details == {"unconnected": 7}
    assert report.metrics == {
        "unrouted": 7,
        "max_passes": 20,
        "cached": True,
        "zone_count": 1,
        "filled_polygon_count": 1,
    }
    assert report.artifacts == [str(board), str(routing_report)]
    assert report.backend["cached"] is True


@pytest.mark.parametrize(
    "field",
    [
        "status",
        "signal_routing",
        "plane_connectivity",
        "zone_fill",
        "zone_count",
        "filled_polygon_count",
        "design_rules",
        "post_import_unconnected",
        "unrouted",
        "violations",
        "board_sha256",
        "failures",
    ],
)
def test_freerouting_failed_cache_reruns_when_authoritative_evidence_is_missing(
    tmp_path, monkeypatch, field
):
    project, _, routing_report, payload = _write_failed_freerouting_cache(tmp_path)
    payload.pop(field)
    routing_report.write_text(json.dumps(payload), encoding="utf-8")
    backend = FreeroutingBackend(tmp_path)
    monkeypatch.setattr(
        backend,
        "_tools",
        lambda: {"java": None, "jar": None, "kicad_python": None},
    )

    report = backend.route(project)

    assert report.status.value == "blocked"
    assert report.failures[0].code == "tool_unavailable"


@pytest.mark.parametrize("mutation", ["board", "rules", "status"])
def test_freerouting_failed_cache_reruns_when_board_rules_or_status_change(
    tmp_path, monkeypatch, mutation
):
    project, board, routing_report, payload = _write_failed_freerouting_cache(tmp_path)
    if mutation == "board":
        board.write_text(board.read_text(encoding="utf-8") + "(net 1 \"changed\")\n")
    elif mutation == "rules":
        project_file = board.with_suffix(".kicad_pro")
        project_payload = json.loads(project_file.read_text(encoding="utf-8"))
        project_payload["board"]["design_settings"]["rules"]["min_clearance"] = 0.2
        project_file.write_text(json.dumps(project_payload), encoding="utf-8")
    else:
        payload["status"] = "pass"
        routing_report.write_text(json.dumps(payload), encoding="utf-8")
    backend = FreeroutingBackend(tmp_path)
    monkeypatch.setattr(
        backend,
        "_tools",
        lambda: {"java": None, "jar": None, "kicad_python": None},
    )

    report = backend.route(project)

    assert report.status.value == "blocked"
    assert report.failures[0].code == "tool_unavailable"


def test_freerouting_applies_generated_project_rules_before_dsn_export(tmp_path, monkeypatch):
    project = tmp_path / "rules_board"
    target = project / "electronics" / "generated" / "kicad"
    target.mkdir(parents=True)
    board = target / "rules_board.kicad_pcb"
    board.write_text("(kicad_pcb)\n", encoding="utf-8")
    (target / "rules_board.kicad_pro").write_text(
        json.dumps(
            {
                "board": {
                    "design_settings": {
                        "rules": {"min_clearance": 0.15, "min_track_width": 0.18}
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    tools = {
        "java": tmp_path / "java",
        "jar": tmp_path / "freerouting.jar",
        "kicad_python": tmp_path / "python",
    }
    backend = FreeroutingBackend(tmp_path)
    observed = {}
    monkeypatch.setattr(backend, "_tools", lambda: tools)

    def fake_pcbnew(executable, code, *arguments):
        observed.update(executable=executable, code=code, arguments=arguments)
        return subprocess.CompletedProcess(args=arguments, returncode=2, stdout="", stderr="")

    monkeypatch.setattr(backend, "_pcbnew", fake_pcbnew)

    report = backend.route(project)

    assert report.failures[0].code == "dsn_export_failed"
    assert observed["arguments"] == (
        board,
        target / "rules_board.dsn",
        "0.15",
        "0.18",
    )
    assert "settings.m_MinClearance = clearance" in observed["code"]
    assert "settings.m_TrackMinWidth = track_width" in observed["code"]
    assert 'board.GetAllNetClasses()["Default"]' in observed["code"]
    assert "default_netclass.SetClearance(clearance)" in observed["code"]
    assert "default_netclass.SetTrackWidth(track_width)" in observed["code"]


@pytest.mark.parametrize(
    "project_payload",
    [
        "{not-json",
        json.dumps({"board": {"design_settings": {"rules": {"min_clearance": 0.15}}}}),
        json.dumps(
            {
                "board": {
                    "design_settings": {
                        "rules": {"min_clearance": 0.0, "min_track_width": 0.15}
                    }
                }
            }
        ),
        json.dumps(
            {
                "board": {
                    "design_settings": {
                        "rules": {"min_clearance": 0.15, "min_track_width": 1000.0}
                    }
                }
            }
        ),
    ],
)
def test_freerouting_blocks_malformed_or_unsafe_project_rules(
    tmp_path, monkeypatch, project_payload
):
    project = tmp_path / "bad_rules_board"
    target = project / "electronics" / "generated" / "kicad"
    target.mkdir(parents=True)
    (target / "bad_rules_board.kicad_pcb").write_text("(kicad_pcb)\n", encoding="utf-8")
    project_file = target / "bad_rules_board.kicad_pro"
    project_file.write_text(project_payload, encoding="utf-8")
    backend = FreeroutingBackend(tmp_path)
    monkeypatch.setattr(
        backend,
        "_tools",
        lambda: {"java": tmp_path / "java", "jar": tmp_path / "jar", "kicad_python": tmp_path / "python"},
    )
    monkeypatch.setattr(
        backend,
        "_pcbnew",
        lambda *_: pytest.fail("malformed rules must block before invoking KiCad"),
    )

    report = backend.route(project)

    assert report.status.value == "blocked"
    assert report.failures[0].code == "invalid_project_design_rules"
    assert report.failures[0].path == str(project_file)


def test_freerouting_keeps_legacy_export_fallback_without_project_file(tmp_path, monkeypatch):
    project = tmp_path / "legacy_board"
    target = project / "electronics" / "generated" / "kicad"
    target.mkdir(parents=True)
    board = target / "legacy_board.kicad_pcb"
    board.write_text("(kicad_pcb)\n", encoding="utf-8")
    backend = FreeroutingBackend(tmp_path)
    observed = {}
    monkeypatch.setattr(
        backend,
        "_tools",
        lambda: {"java": tmp_path / "java", "jar": tmp_path / "jar", "kicad_python": tmp_path / "python"},
    )

    def fake_pcbnew(executable, code, *arguments):
        observed["arguments"] = arguments
        return subprocess.CompletedProcess(args=arguments, returncode=2, stdout="", stderr="")

    monkeypatch.setattr(backend, "_pcbnew", fake_pcbnew)

    report = backend.route(project)

    assert report.failures[0].code == "dsn_export_failed"
    assert observed["arguments"] == (board, target / "legacy_board.dsn")


def test_generated_kicad_default_netclass_matches_manufacturing_rules(service, project):
    service.generate_electronics_only(project)
    path = service.workspace.require_project(project)
    project_file = path / "electronics" / "generated" / "kicad" / f"{project}.kicad_pro"
    payload = json.loads(project_file.read_text(encoding="utf-8"))
    rules = payload["board"]["design_settings"]["rules"]
    default_netclass = next(
        item for item in payload["net_settings"]["classes"] if item["name"] == "Default"
    )

    assert default_netclass["clearance"] == rules["min_clearance"]
    assert default_netclass["track_width"] == rules["min_track_width"]
    assert payload["net_settings"]["meta"]["version"] == 5


@pytest.mark.parametrize("raw_unrouted", [0, 3])
def test_freerouting_import_reapplies_rules_and_persists_zone_fill(
    tmp_path, monkeypatch, raw_unrouted
):
    project = tmp_path / "filled_board"
    target = project / "electronics" / "generated" / "kicad"
    target.mkdir(parents=True)
    board = target / "filled_board.kicad_pcb"
    board.write_text("(kicad_pcb\n  (zone\n  )\n)\n", encoding="utf-8")
    (target / "filled_board.kicad_pro").write_text(
        json.dumps(
            {
                "board": {
                    "design_settings": {
                        "rules": {"min_clearance": 0.15, "min_track_width": 0.18}
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    tools = {
        "java": tmp_path / "java",
        "jar": tmp_path / "freerouting.jar",
        "kicad_python": tmp_path / "python",
    }
    backend = FreeroutingBackend(tmp_path)
    pcbnew_calls = []
    monkeypatch.setattr(backend, "_tools", lambda: tools)

    def fake_pcbnew(executable, code, *arguments):
        pcbnew_calls.append((code, arguments))
        if len(pcbnew_calls) == 2:
            arguments[2].write_text(
                "(kicad_pcb\n  (zone\n    (filled_polygon\n    )\n  )\n)\n",
                encoding="utf-8",
            )
            arguments[2].with_suffix(".kicad_pro").write_text(
                json.dumps(
                    {
                        "board": {
                            "design_settings": {
                                "rules": {"min_clearance": 0.15, "min_track_width": 0.18}
                            }
                        },
                        "meta": {"filename": "filled_board.routed.kicad_pro", "version": 3},
                        "net_settings": {
                            "classes": [
                                {
                                    "name": "Default",
                                    "clearance": 0.15,
                                    "track_width": 0.18,
                                }
                            ]
                        },
                    }
                ),
                encoding="utf-8",
            )
        return subprocess.CompletedProcess(
            args=arguments,
            returncode=0,
            stdout="HW_UNCONNECTED=0\n" if len(pcbnew_calls) == 2 else "",
            stderr="",
        )

    def fake_freerouting(command, **kwargs):
        (target / "filled_board.ses").write_text("(session)\n", encoding="utf-8")
        return subprocess.CompletedProcess(
            args=command,
            returncode=0,
            stdout=f"final score: 1000 ({raw_unrouted} unrouted and 0 violations)\n",
            stderr="",
        )

    monkeypatch.setattr(backend, "_pcbnew", fake_pcbnew)
    monkeypatch.setattr("hw_codesign.backends.freerouting.run_process_group", fake_freerouting)

    report = backend.route(project)

    assert report.status.value == "pass"
    import_code, import_arguments = pcbnew_calls[1]
    assert import_arguments == (
        board,
        target / "filled_board.ses",
        target / "filled_board.routed.kicad_pcb",
        "0.15",
        "0.18",
    )
    assert "default_netclass.SetClearance(clearance)" in import_code
    assert "default_netclass.SetTrackWidth(track_width)" in import_code
    assert "filler = pcbnew.ZONE_FILLER(board)" in import_code
    assert "filler.Fill(board.Zones())" in import_code
    assert "board.BuildConnectivity()" in import_code
    assert "(filled_polygon" in board.read_text(encoding="utf-8")
    routing = json.loads((target / "routing.json").read_text(encoding="utf-8"))
    assert routing["design_rules"] == {
        "min_clearance_mm": 0.15,
        "min_track_width_mm": 0.18,
    }
    assert routing["zone_fill"] == "persisted"
    assert routing["filled_polygon_count"] == 1
    assert routing["freerouting_unrouted"] == raw_unrouted
    assert routing["post_import_unconnected"] == 0
    assert routing["project_sidecar_promoted"] is True
    canonical_project = json.loads((target / "filled_board.kicad_pro").read_text(encoding="utf-8"))
    assert canonical_project["meta"]["filename"] == "filled_board.kicad_pro"
    assert canonical_project["net_settings"]["classes"][0]["clearance"] == 0.15
    assert not (target / "filled_board.routed.kicad_pro").exists()


def test_freerouting_rejects_import_without_persisted_zone_fill(tmp_path, monkeypatch):
    project = tmp_path / "unfilled_board"
    target = project / "electronics" / "generated" / "kicad"
    target.mkdir(parents=True)
    board = target / "unfilled_board.kicad_pcb"
    board.write_text("(kicad_pcb\n  (zone\n  )\n)\n", encoding="utf-8")
    backend = FreeroutingBackend(tmp_path)
    monkeypatch.setattr(
        backend,
        "_tools",
        lambda: {"java": tmp_path / "java", "jar": tmp_path / "jar", "kicad_python": tmp_path / "python"},
    )
    pcbnew_calls = []

    def fake_pcbnew(executable, code, *arguments):
        pcbnew_calls.append(arguments)
        if len(pcbnew_calls) == 2:
            arguments[2].write_text("(kicad_pcb\n  (zone\n  )\n)\n", encoding="utf-8")
        return subprocess.CompletedProcess(
            args=arguments,
            returncode=0,
            stdout="HW_UNCONNECTED=0\n" if len(pcbnew_calls) == 2 else "",
            stderr="",
        )

    def fake_freerouting(command, **kwargs):
        (target / "unfilled_board.ses").write_text("(session)\n", encoding="utf-8")
        return subprocess.CompletedProcess(
            args=command,
            returncode=0,
            stdout="final score: 1000 (0 unrouted and 0 violations)\n",
            stderr="",
        )

    monkeypatch.setattr(backend, "_pcbnew", fake_pcbnew)
    monkeypatch.setattr("hw_codesign.backends.freerouting.run_process_group", fake_freerouting)

    report = backend.route(project)

    assert report.status.value == "fail"
    assert report.failures[0].code == "zone_fill_not_persisted"
    assert board.read_text(encoding="utf-8").count("filled_polygon") == 0


def test_freerouting_fails_when_kicad_connectivity_remains_incomplete(tmp_path, monkeypatch):
    project = tmp_path / "disconnected_board"
    target = project / "electronics" / "generated" / "kicad"
    target.mkdir(parents=True)
    board = target / "disconnected_board.kicad_pcb"
    board.write_text("(kicad_pcb\n  (zone\n  )\n)\n", encoding="utf-8")
    backend = FreeroutingBackend(tmp_path)
    monkeypatch.setattr(
        backend,
        "_tools",
        lambda: {"java": tmp_path / "java", "jar": tmp_path / "jar", "kicad_python": tmp_path / "python"},
    )
    pcbnew_calls = []

    def fake_pcbnew(executable, code, *arguments):
        pcbnew_calls.append(arguments)
        if len(pcbnew_calls) == 2:
            arguments[2].write_text(
                "(kicad_pcb\n  (zone\n    (filled_polygon\n    )\n  )\n)\n",
                encoding="utf-8",
            )
        return subprocess.CompletedProcess(
            args=arguments,
            returncode=0,
            stdout="HW_UNCONNECTED=7\n" if len(pcbnew_calls) == 2 else "",
            stderr="",
        )

    def fake_freerouting(command, **kwargs):
        (target / "disconnected_board.ses").write_text("(session)\n", encoding="utf-8")
        return subprocess.CompletedProcess(
            args=command,
            returncode=0,
            stdout="final score: 1000 (0 unrouted and 0 violations)\n",
            stderr="",
        )

    monkeypatch.setattr(backend, "_pcbnew", fake_pcbnew)
    monkeypatch.setattr("hw_codesign.backends.freerouting.run_process_group", fake_freerouting)

    report = backend.route(project)

    assert report.status.value == "fail"
    assert report.failures[0].code == "routing_incomplete_after_zone_fill"
    assert report.metrics["unrouted"] == 7
    routing = json.loads((target / "routing.json").read_text(encoding="utf-8"))
    assert routing["status"] == "fail"
    assert routing["post_import_unconnected"] == 7
    assert routing["plane_connectivity"] == "incomplete"
    assert "(filled_polygon" in board.read_text(encoding="utf-8")


def test_freerouting_timeout_is_bounded_and_reported(tmp_path, monkeypatch):
    project = tmp_path / "timeout_board"
    target = project / "electronics" / "generated" / "kicad"
    target.mkdir(parents=True)
    (target / "timeout_board.kicad_pcb").write_text("(kicad_pcb)\n", encoding="utf-8")
    tools = {
        "java": tmp_path / "java",
        "jar": tmp_path / "freerouting.jar",
        "kicad_python": tmp_path / "python",
    }
    for path in tools.values():
        path.write_text("", encoding="utf-8")
    backend = FreeroutingBackend(tmp_path)
    observed = {}

    monkeypatch.setattr(backend, "_tools", lambda: tools)
    monkeypatch.setattr(
        backend,
        "_pcbnew",
        lambda *args: subprocess.CompletedProcess(args=args, returncode=0, stdout="", stderr=""),
    )

    def fake_run(command, **kwargs):
        observed["timeout"] = kwargs["timeout"]
        raise subprocess.TimeoutExpired(command, kwargs["timeout"], output="partial", stderr="still running")

    monkeypatch.setattr("hw_codesign.backends.freerouting.run_process_group", fake_run)

    report = backend.route(project, timeout_seconds=3)

    assert observed["timeout"] == 3
    assert report.status.value == "fail"
    assert report.failures[0].code == "autoroute_timeout"
    assert report.failures[0].details["timeout_seconds"] == 3
    assert report.backend["timeout_seconds"] == 3


def test_iteration_records_reports_history_and_repair_plan(service, project):
    result = service.run_design_iteration(project, include_external=False)
    path = service.workspace.require_project(project)
    assert result["iteration_id"] == "0001"
    assert result["status"] == "blocked"
    assert "semantic_electrical" in result["failed_gates"]
    assert result["repair_plan"]["requires_user_decision"] is True
    assert (path / "history" / "iterations" / "0001" / "result.json").is_file()
    assert (path / "history" / "iterations" / "0001" / "electronics" / "intent" / "board.intent.md").is_file()
    assert (path / "history" / "iterations" / "0001" / "firmware" / "generated" / "pinmap.h").is_file()
    log = (path / "history" / "failure_log.jsonl").read_text(encoding="utf-8")
    assert "current_budget_exceeded" in log


def test_failure_log_is_recreated_if_legacy_project_lacks_it(service, project):
    project_path = service.workspace.require_project(project)
    log_path = project_path / "history" / "failure_log.jsonl"
    log_path.unlink()

    service._append_failures(
        project,
        "legacy-recovery",
        {
            "reports": [
                {
                    "gate": "fixture_gate",
                    "failures": [
                        {
                            "category": "RELEASE_ERROR",
                            "code": "fixture_failure",
                            "message": "fixture",
                        }
                    ],
                }
            ]
        },
    )

    assert log_path.is_file()
    record = json.loads(log_path.read_text(encoding="utf-8"))
    assert record["iteration_id"] == "legacy-recovery"
    assert record["gate"] == "fixture_gate"
    assert record["code"] == "fixture_failure"


def test_external_backends_report_real_availability_and_violations(service, project, monkeypatch):
    service.generate_all(project)
    monkeypatch.setattr("shutil.which", lambda _: None)
    checks = service.run_all_checks(project, include_external=True)
    external = [item for item in checks["reports"] if item["gate"] in {"native_erc", "native_drc", "native_zephyr_build"}]
    firmware = next(item for item in external if item["gate"] == "native_zephyr_build")
    assert firmware["status"] == "blocked"
    assert firmware["failures"][0]["code"] == "tool_unavailable"
    for item in (entry for entry in external if entry["gate"] in {"native_erc", "native_drc"} and entry["status"] == "pass"):
        assert item["metrics"]["violations"] == 0
        assert item["backend"]["available"] is True


def test_design_report_states_physical_gaps(service, project):
    service.generate_all(project)
    service.run_all_checks(project, include_external=False)
    output = Path(service.generate_design_report(project)["file"])
    text = output.read_text(encoding="utf-8")
    assert "EMI/EMC" in text
    assert "instrumented hardware testing" in text


def test_safety_spec_changes_require_explicit_approval(service, project):
    with pytest.raises(UnsafeChangeError):
        service.update_spec(project, "safety", {"emergency_stop": {"required": False}})
    result = service.update_spec(project, "safety", {"emergency_stop": {"required": True}}, user_approved=True)
    assert result["user_approved"] is True


def test_design_until_release_blocks_reference_pipeline(service, project):
    # Critical assumptions require explicit user approval; resolve them before the loop.
    spec = service.read_spec(project)
    for name, assumption in spec.get("assumptions", {}).items():
        if assumption.get("requires_user_review"):
            service.resolve_assumption(project, name, assumption.get("value") or "approved", approved=True)
    result = service.design_until_release(project, max_iterations=4, include_external=False)
    assert result["status"] == "blocked"
    assert not (service.workspace.require_project(project) / "exports" / "releases" / "r1").exists()


def test_natural_language_requirements_update_structured_spec(service, project):
    result = service.update_requirements(project, "16 channel 24V battery, peak 6A, STM32H7, IMU, emergency stop, Zephyr, 6-layer, external driver, forced cooling")
    spec = service.read_spec(project)
    assert result["status"] == "generated"
    assert spec["actuation"]["motor_channels"] == 16
    assert spec["actuation"]["motor_channel_peak_current_a"] == 6.0
    assert spec["system"]["supply"]["battery"]["pack_voltage_nominal"] == 24.0
    assert spec["actuation"]["motor_type"] == "external_driver_modules"
    assert spec["mechanical"]["cooling"] == "forced_air"
    assert spec["manufacturing"]["pcb"]["layers"] == 6
    assert spec["firmware"]["framework"] == "zephyr"
    assert spec.get("requirements", {}).get("active_unresolved", []) == []
    ir = result["compiler_ir"]
    assert ir["version"] == "requirements_ir_v1"
    lowered = {item["spec_path"]: item for item in ir["lowered_fields"]}
    assert lowered["actuation.motor_channels"]["value"] == 16
    assert lowered["actuation.motor_channels"]["field_type"] == "integer"
    assert lowered["actuation.motor_channels"]["source_range"] == {"start": 0, "end": 10}
    assert "power_integrity_estimate" in lowered["actuation.motor_channels"]["affected_gates"]
    assert "layout_thermal_integrity" in lowered["actuation.motor_channels"]["affected_gates"]
    assert lowered["actuation.motor_type"]["value"] == "external_driver_modules"
    assert lowered["mechanical.cooling"]["value"] == "forced_air"
    resolved = {item["assumption_key"]: item for item in ir["resolved_assumptions"]}
    assert {"motor_type", "cooling"} <= set(resolved)
    lowered_tokens = [item for item in ir["tokens"] if item["kind"] == "lowered_field"]
    assert any(item["spec_path"] == "actuation.motor_channels" and item["source_span"] == "16 channel" for item in lowered_tokens)
    assert ir["required_human_approvals"] == []


def test_requirements_lower_can_telemetry_into_firmware_module(service, project):
    result = service.update_requirements(
        project,
        "16 channel 24V battery external driver forced cooling CAN telemetry id 0x321 dlc 8 every 10 ms",
    )

    assert result["status"] == "generated"
    assert result["has_unresolved_constraints"] is False
    spec = service.read_spec(project)
    modules = {module["id"]: module for module in spec["firmware"]["modules"]}
    module = modules["can_telemetry_periodic"]
    assert module == {
        "id": "can_telemetry_periodic",
        "behavior": "periodic_transmit",
        "transport": "can",
        "interval_ms": 10,
        "frame": {"id": "0x321", "dlc": 8, "content": "telemetry"},
        "source": "requirements_ir_v1",
    }
    lowered = {item["spec_path"]: item for item in result["compiler_ir"]["lowered_fields"]}
    field = lowered["firmware.modules.can_telemetry_periodic"]
    assert field["field_type"] == "firmware_module"
    assert field["value"]["behavior"] == "periodic_transmit"
    assert "firmware_modules" in field["affected_gates"]

    service.generate_all(project)
    project_path = service.workspace.require_project(project)
    graph = json.loads((project_path / "electronics" / "generated" / "electrical_graph.json").read_text(encoding="utf-8"))
    pinmap = json.loads((project_path / "firmware" / "generated" / "pinmap.json").read_text(encoding="utf-8"))
    report = service.validator.check_firmware_modules(
        service.read_spec(project)["firmware"]["modules"],
        pinmap,
        spec=service.read_spec(project),
        graph=graph,
        module_dir=project_path / "firmware" / "modules",
    )
    assert report.status == "pass"


def test_requirements_do_not_lower_can_fd_telemetry_as_classical_can(service, project):
    result = service.update_requirements(
        project,
        "external driver forced cooling CAN-FD telemetry id 0x321 dlc 64 every 10 ms",
    )

    assert result["has_unresolved_constraints"] is True
    spec = service.read_spec(project)
    modules = {module["id"] for module in spec["firmware"].get("modules", [])}
    assert "can_telemetry_periodic" not in modules
    unresolved = spec["requirements"]["active_unresolved"]
    bus_protocol = next(item for item in unresolved if item["category"] == "bus_protocol")
    assert bus_protocol["field_type"] == "unsupported_constraint"
    assert "firmware_interface_contract" in bus_protocol["affected_gates"]


def test_requirements_relower_existing_firmware_module_into_active_ir(service, project):
    service.update_requirements(
        project,
        "external driver forced cooling CAN telemetry id 0x100 dlc 8 every 100 ms",
    )
    result = service.update_requirements(
        project,
        "external driver forced cooling CAN telemetry id 0x200 dlc 4 every 25 ms",
    )

    spec = service.read_spec(project)
    modules = [module for module in spec["firmware"]["modules"] if module["id"] == "can_telemetry_periodic"]
    assert len(modules) == 1
    assert modules[0]["interval_ms"] == 25
    assert modules[0]["frame"] == {"id": "0x200", "dlc": 4, "content": "telemetry"}
    lowered = {item["spec_path"]: item for item in result["compiler_ir"]["lowered_fields"]}
    assert lowered["firmware.modules.can_telemetry_periodic"]["value"]["interval_ms"] == 25


def test_requirements_ir_affected_gates_are_concrete_report_names(service, project):
    result = service.update_requirements(
        project,
        "16 channel 24V battery, IP67, CAN-FD, ASIL-B, 8A continuous, JLCPCB assembly, impedance-controlled",
    )
    service.generate_all(project)
    checks = service.run_all_checks(project, include_external=False)
    emitted_gates = {
        gate
        for item in [*result["compiler_ir"]["lowered_fields"], *result["compiler_ir"]["tokens"]]
        for gate in item.get("affected_gates", [])
    }
    report_gates = {report["gate"] for report in checks["reports"]}
    release_only_gates = {"artifact_integrity"}

    assert emitted_gates <= report_gates | release_only_gates
    assert not (emitted_gates & {"electrical_semantics", "power_budget", "thermal_integrity", "manufacturing_export", "safety_requirements"})


def test_requirements_update_result_matches_public_schema(service, project):
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource

    from hw_codesign.contracts import SHARED_SCHEMAS, TOOL_REGISTRY
    from hw_codesign.mcp_server import _enrich

    result = service.update_requirements(
        project,
        "16 channel 24V battery, IP67, CAN-FD, ASIL-B, 8A continuous, JLCPCB assembly, impedance-controlled",
    )
    registry = Registry().with_resources(
        (schema["$id"], Resource.from_contents(schema))
        for schema in SHARED_SCHEMAS.values()
    )

    Draft202012Validator(
        SHARED_SCHEMAS["requirements_update_result"],
        registry=registry,
    ).validate(result)
    Draft202012Validator(
        TOOL_REGISTRY["hw_update_requirements"].to_dict()["output_schema"],
        registry=registry,
    ).validate(_enrich(result))
    assert TOOL_REGISTRY["hw_update_requirements"].output_schema["$ref"].endswith("requirements_update_result")


def test_unsupported_constraints_persist_to_spec_and_block_validation(service, project):
    """update_requirements with high-risk constraints that cannot be lowered must:
    - return status='generated' with has_unresolved_constraints=true
    - persist constraints to spec so validate_spec fails with unlowered_constraint_in_spec
    - thereby block release promotion without requiring agent to inspect the return value."""
    result = service.update_requirements(
        project,
        "16 channel 24V battery, IP67, CAN-FD, ASIL-B, 8A continuous, JLCPCB assembly, impedance-controlled"
    )
    assert result["status"] == "generated"
    assert result["has_unresolved_constraints"] is True
    assert result["unsupported_constraints"]
    assert result["required_human_approvals"]
    assert "firmware_interface_contract" in result["affected_gates"]
    spec = service.read_spec(project)
    assert spec.get("requirements", {}).get("active_unresolved"), "Constraints must be persisted to spec/requirements.yaml"
    unresolved = spec["requirements"]["active_unresolved"]
    assert all(item["required_human_approvals"] for item in unresolved)
    assert all(item["affected_gates"] for item in unresolved)
    unsupported_unresolved = [item for item in unresolved if item["field_type"] == "unsupported_constraint"]
    assert all(item["source_range"]["end"] > item["source_range"]["start"] for item in unsupported_unresolved)
    assert unsupported_unresolved
    assert spec["requirements"]["compiler_ir"]["unsupported_constraints"]
    unresolved_tokens = [item for item in spec["requirements"]["compiler_ir"]["tokens"] if item["kind"] == "unsupported_constraint"]
    assert {item["category"] for item in unresolved_tokens} >= {"ip_protection", "bus_protocol", "functional_safety", "current_rating", "manufacturing_service", "pcb_stackup"}
    assert all(item["required_human_approvals"] for item in unresolved_tokens)
    checks = service.run_all_checks(project, include_external=False)
    assert checks["status"] != "pass"
    codes = {f["code"] for report in checks["reports"] for f in report["failures"]}
    assert "unlowered_requirement" in codes


def test_requirements_compiler_preserves_physical_qualification_constraints(service, project):
    result = service.update_requirements(
        project,
        "USB-C PD sink with EMI/EMC pre-compliance, MIL-STD-810 vibration, thermal limit 70C",
    )

    assert result["status"] == "generated"
    assert result["has_unresolved_constraints"] is True
    assert "physical_qualification" in result["affected_gates"]
    spec = service.read_spec(project)
    unsupported = spec["requirements"]["compiler_ir"]["unsupported_constraints"]
    by_category = {item["category"]: item for item in unsupported}

    assert {
        "usb_power_delivery",
        "emi_emc_compliance",
        "vibration_environment",
        "thermal_limit",
    } <= set(by_category)
    assert by_category["usb_power_delivery"]["source_span"] == "USB-C PD"
    assert "firmware_interface_contract" in by_category["usb_power_delivery"]["affected_gates"]
    assert "layout_signal_integrity" in by_category["emi_emc_compliance"]["affected_gates"]
    assert "mechanical_connector_retention" in by_category["vibration_environment"]["affected_gates"]
    assert "layout_thermal_integrity" in by_category["thermal_limit"]["affected_gates"]
    assert all(item["release_blocking"] for item in unsupported)
    assert all(item["required_human_approvals"] for item in unsupported)

    checks = service.run_all_checks(project, include_external=False)
    lowering = next(report for report in checks["reports"] if report["gate"] == "requirements_lowering")
    assert lowering["status"] != "pass"
    assert "unlowered_requirement" in {failure["code"] for failure in lowering["failures"]}


def test_update_requirements_replaces_active_unresolved_constraints(service, project):
    """update_requirements uses replace semantics for active_unresolved: a later call with no
    unsupported constraints clears active_unresolved even if the prior call had blockers.
    raw_inputs is append-only (audit log), so both calls are preserved there."""
    r1 = service.update_requirements(project, "IP67 impedance-controlled")
    assert r1["mode"] == "replace_active_requirements"
    assert service.read_spec(project).get("requirements", {}).get("active_unresolved")
    service.update_requirements(project, "16 channel 24V battery, Zephyr, external driver, forced cooling")
    spec = service.read_spec(project)
    assert spec.get("requirements", {}).get("active_unresolved", []) == []
    assert len(spec["requirements"]["raw_inputs"]) == 2, "raw_inputs must accumulate across calls"
    checks = service.run_all_checks(project, include_external=False)
    codes = {f["code"] for report in checks["reports"] for f in report["failures"]}
    assert "unlowered_requirement" not in codes


# ---------------------------------------------------------------------------
# Candidate lifecycle
# ---------------------------------------------------------------------------

def test_list_candidates_empty_before_iteration(service, project):
    result = service.list_candidates(project)
    assert result["status"] == "pass"
    assert result["candidates"] == []
    assert result["count"] == 0


def test_list_candidates_finds_candidates_after_iteration(service, project):
    service.run_design_iteration(project, include_external=False)
    result = service.list_candidates(project)
    assert result["count"] >= 1
    c = result["candidates"][0]
    assert "candidate_id" in c
    assert "backend" in c
    assert "gate_summary" in c
    # Scratch dirs (reference-fabrication, native-check) must NOT appear
    assert all(c["candidate_id"].isdigit() for c in result["candidates"])


def test_get_candidate_missing_returns_blocked(service, project):
    result = service.get_candidate(project, "9999")
    assert result["status"] == "blocked"
    assert result["code"] == "candidate_not_found"


def test_get_candidate_returns_frozen_data(service, project):
    service.run_design_iteration(project, include_external=False)
    candidates = service.list_candidates(project)
    cid = candidates["candidates"][0]["candidate_id"]
    result = service.get_candidate(project, cid)
    assert result["status"] == "pass"
    assert result["candidate_id"] == cid
    assert "checks" in result["candidate"]


def test_review_candidate_uses_frozen_checks_not_live_reports(service, project):
    service.run_design_iteration(project, include_external=False)
    cid = service.list_candidates(project)["candidates"][0]["candidate_id"]
    review = service.review_candidate(project, cid)
    assert review["status"] in {"pass", "fail", "blocked", "unknown"}
    assert "gate_summary" in review
    assert "blocking_gates" in review
    assert "recommendation" in review
    # Run fresh checks (changes live reports dir) — frozen review must be stable
    service.run_all_checks(project, include_external=False)
    review2 = service.review_candidate(project, cid)
    assert review2["gate_summary"] == review["gate_summary"]


def test_compare_candidates_detects_no_change(service, project):
    service.run_design_iteration(project, include_external=False)
    service.run_design_iteration(project, include_external=False)
    candidates = service.list_candidates(project)["candidates"]
    assert len(candidates) >= 2
    a, b = candidates[0]["candidate_id"], candidates[1]["candidate_id"]
    result = service.compare_candidates(project, a, b)
    assert result["status"] == "pass"
    assert "readiness_delta" in result
    assert "artifact_delta" in result
    assert "risk_delta" in result
    assert "recommendation" in result
    delta = result["readiness_delta"]
    assert isinstance(delta["blocking_gates_removed"], list)
    assert isinstance(delta["blocking_gates_added"], list)
    assert isinstance(delta["pass_count_delta"], int)


def test_compare_candidates_missing_returns_blocked(service, project):
    service.run_design_iteration(project, include_external=False)
    cid = service.list_candidates(project)["candidates"][0]["candidate_id"]
    result = service.compare_candidates(project, cid, "9999")
    assert result["status"] == "blocked"
    assert result["code"] == "candidate_not_found"


# ---------------------------------------------------------------------------
# Fabrication review preparation
# ---------------------------------------------------------------------------

def test_prepare_fabrication_review_before_any_candidate(service, project):
    result = service.prepare_fabrication_review(project)
    assert result["status"] == "pass"
    assert result["label"] == "do_not_fabricate"
    assert "artifact_presence" in result
    assert "fab_review_checklist" in result
    assert len(result["fab_review_checklist"]) >= 5


def test_prepare_fabrication_review_after_iteration(service, project):
    service.run_design_iteration(project, include_external=False)
    cid = service.list_candidates(project)["candidates"][0]["candidate_id"]
    result = service.prepare_fabrication_review(project, candidate_id=cid)
    assert result["status"] == "pass"
    assert result["label"] in {"do_not_fabricate", "review_only", "release_candidate"}
    assert result["candidate_id"] == cid
    assert "erc_status" in result
    assert "drc_status" in result
    assert isinstance(result["unresolved_assumptions"], list)
    assert isinstance(result["physical_qualification_gaps"], list)


# ---------------------------------------------------------------------------
# Environment diagnosis
# ---------------------------------------------------------------------------

def test_get_capabilities_partitions_release_tiers(service, project):
    result = service.get_capabilities()

    assert result["release_tiers"] == {
        "reference": "candidate",
        "python_netlist": "netlist",
        "atopile": "hdl_source",
        "tscircuit": "fabrication",
        "kicad": "fabrication",
    }
    assert set(result["release_eligible_backends"]) == {"tscircuit", "kicad", "python_netlist", "atopile"}
    assert result["canonical_fabrication_backends"] == ["tscircuit", "kicad"]
    assert result["canonical_fabrication_flow"] == {
        "tscircuit": "tscircuit -> Circuit JSON -> KiCad manufacturing bridge",
        "kicad": "native KiCad schematic/PCB -> KiCad CLI manufacturing export",
    }
    assert set(result["fabrication_release_backends"]) == {"tscircuit", "kicad"}
    assert result["netlist_release_backends"] == ["python_netlist"]
    assert result["source_release_backends"] == ["atopile"]
    assert result["candidate_only_backends"] == ["reference"]
    assert result["backends"]["python_netlist"]["fabrication_release_eligible"] is False
    assert result["backends"]["python_netlist"]["release_tier"] == "netlist"
    assert result["backends"]["atopile"]["fabrication_release_eligible"] is False
    assert result["backends"]["tscircuit"]["fabrication_release_eligible"] is True
    assert result["backends"]["kicad"]["release_tier"] == "fabrication"


def test_diagnose_environment_candidate_target_always_ready(service, project):
    result = service.diagnose_environment(target="candidate")
    assert result["status"] == "pass"
    assert result["ready"] is True
    assert result["missing_tools"] == []
    assert result["blocked_gates"] == []


def test_diagnose_environment_returns_structured_output(service, project):
    result = service.diagnose_environment(target="fabrication_release")
    assert result["target"] == "fabrication_release"
    assert isinstance(result["ready"], bool)
    assert isinstance(result["missing_tools"], list)
    assert isinstance(result["blocked_gates"], list)
    assert isinstance(result["install_hints"], dict)
    assert isinstance(result["tool_availability"], dict)
    assert isinstance(result["toolchain_probes"], dict)


def test_diagnose_environment_rejects_compiler_without_arm_newlib(service, monkeypatch):
    probe = ArmNewlibProbe(
        compiler="/opt/homebrew/bin/arm-none-eabi-gcc",
        toolchain_root="/opt/homebrew",
        source="PATH",
        explicit_root=False,
        files={"nosys.specs": "nosys.specs", "libc.a": "libc.a", "libnosys.a": "libnosys.a"},
        missing=("nosys.specs", "libc.a", "libnosys.a"),
    )
    monkeypatch.setattr("hw_codesign.service.probe_arm_newlib", lambda: probe)

    result = service.diagnose_environment(target="firmware_only")

    assert result["status"] == "fail"
    assert result["ready"] is False
    assert result["tool_availability"]["arm_none_eabi_gcc"] is False
    assert result["missing_tools"] == ["arm_none_eabi_gcc"]
    assert result["blocked_gates"] == ["native_zephyr_build"]
    assert result["toolchain_probes"]["arm_none_eabi_gcc"] == probe.to_dict()
    assert all("brew install arm-none-eabi-gcc" not in hint for hint in result["install_hints"]["macos"])
    assert "sudo apt-get install gcc-arm-none-eabi libnewlib-arm-none-eabi" in result["install_hints"]["linux"]


def test_get_capabilities_uses_complete_arm_newlib_probe(service, monkeypatch):
    probe = ArmNewlibProbe(
        compiler="/opt/arm/bin/arm-none-eabi-gcc",
        toolchain_root="/opt/arm",
        source="HW_ARM_TOOLCHAIN_ROOT",
        explicit_root=True,
        files={
            "nosys.specs": "/opt/arm/arm-none-eabi/lib/nosys.specs",
            "libc.a": "/opt/arm/arm-none-eabi/lib/libc.a",
            "libnosys.a": "/opt/arm/arm-none-eabi/lib/libnosys.a",
        },
        missing=(),
    )
    monkeypatch.setattr("hw_codesign.service.probe_arm_newlib", lambda: probe)

    result = service.get_capabilities()

    arm_tool = result["external_tools"]["arm_none_eabi_gcc"]
    assert arm_tool["available"] is True
    assert arm_tool["probe"] == probe.to_dict()
    assert "native_zephyr_build" not in result["missing_external_gates"]


def test_diagnose_environment_backend_adds_tool_requirement(service, project, monkeypatch):
    monkeypatch.setattr("shutil.which", lambda cmd: None if cmd == "node" else "/usr/bin/java")
    result = service.diagnose_environment(target="candidate", backend="tscircuit")
    assert "node" in result["missing_tools"]


def test_diagnose_environment_unknown_target_is_blocked(service, project):
    result = service.diagnose_environment(target="nonexistent_target")
    assert result["status"] == "blocked"
    assert result["code"] == "unknown_target"
