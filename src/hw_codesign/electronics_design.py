from __future__ import annotations

from collections import defaultdict
from typing import Any


def pin(number: str | int, name: str, net: str, role: str) -> dict[str, Any]:
    return {"number": str(number), "name": name, "net": net, "role": role, "voltage_domain": _domain(net) if role in {"power_in", "power_out", "ground"} else None}


def component(ref: str, category: str, value: str, mpn: str, footprint: str, pins: list[dict[str, Any]], **metadata: Any) -> dict[str, Any]:
    return {
        "ref": ref,
        "category": category,
        "value": value,
        "mpn": mpn,
        "footprint": footprint,
        "pins": pins,
        "lifecycle": metadata.pop("lifecycle", "active"),
        "manufacturer": metadata.pop("manufacturer", "specified"),
        "supplier_sku": metadata.pop("supplier_sku", mpn),
        "substitute_mpn": metadata.pop("substitute_mpn", None),
        **metadata,
    }


def build_controller_graph(spec: dict[str, Any]) -> dict[str, Any]:
    channels = int(spec["actuation"]["motor_channels"])
    signal_nets = ["ESTOP_IN", "CAN_RX", "CAN_TX", "I2C_IMU_SCL", "I2C_IMU_SDA", "IMU_INT", "SWDIO", "SWCLK", "NRST", "USB_DP", "USB_DM"]
    for index in range(1, channels + 1):
        signal_nets.extend((f"MOTOR{index}_PWM", f"MOTOR{index}_CURRENT", f"MOTOR{index}_ENC"))
    mcu_pins = [pin(1, "VDD", "V3V3", "power_in"), pin(2, "VSS", "GND", "ground")]
    for number, net in enumerate(signal_nets, 3):
        role = "analog" if net.endswith("CURRENT") else "bidirectional"
        mcu_pins.append(pin(number, net, net, role))
    components = [
        component("J1", "power_input", "24V INPUT", "Molex-42820-2212", "MicroFit_2Pin", [pin(1, "VBAT", "VBAT_RAW", "power_in"), pin(2, "GND", "GND", "ground")], manufacturer="Molex", substitute_mpn="Molex-43650-0200"),
        component("F1", "fuse", "80A SERVICE FUSE", "Littelfuse-0498080.M", "MIDI_Fuse", [pin(1, "IN", "VBAT_RAW", "passive"), pin(2, "OUT", "VBAT_FUSED", "passive")], manufacturer="Littelfuse", substitute_mpn="Eaton-BK-AMG-80"),
        component("Q1", "reverse_polarity", "IDEAL DIODE", "LM74700QDBVRQ1", "SOT23-6", [pin(1, "ANODE", "VBAT_FUSED", "power_in"), pin(2, "CATHODE", "VBAT", "power_out"), pin(3, "GND", "GND", "ground")], manufacturer="Texas Instruments", substitute_mpn="LTC4359IMS8"),
        component("D1", "tvs", "33V TVS", "SMCJ33A", "SMCJ", [pin(1, "K", "VBAT", "passive"), pin(2, "A", "GND", "ground")], manufacturer="Littelfuse", substitute_mpn="SMCJ33A-E3/57T"),
        component("U3", "efuse", "eFuse", "TPS26630RGET", "VQFN24", [pin(1, "IN", "VBAT", "power_in"), pin(2, "OUT", "VSYS", "power_out"), pin(3, "GND", "GND", "ground"), pin(4, "SHDN", "ESTOP_GATE", "input")], manufacturer="Texas Instruments", substitute_mpn="LTC4368IDD-2"),
        component("U4", "regulator", "5V Buck", "LM76005RNPR", "WQFN30", [pin(1, "VIN", "VSYS", "power_in"), pin(2, "VOUT", "V5", "power_out"), pin(3, "GND", "GND", "ground")], manufacturer="Texas Instruments", substitute_mpn="LT8645SIV"),
        component("U5", "regulator", "3V3 Buck", "TPS62133RGTR", "VQFN16", [pin(1, "VIN", "V5", "power_in"), pin(2, "VOUT", "V3V3", "power_out"), pin(3, "GND", "GND", "ground")], manufacturer="Texas Instruments", substitute_mpn="AP63203WU-7"),
        component("U1", "mcu", "STM32H743", "STM32H743VIT6", "LQFP100", mcu_pins, manufacturer="STMicroelectronics", substitute_mpn="STM32H753VIT6"),
        component("U2", "imu", "ICM-42688-P", "ICM-42688-P", "LGA14", [pin(1, "VDD", "V3V3", "power_in"), pin(2, "GND", "GND", "ground"), pin(3, "SCL", "I2C_IMU_SCL", "open_drain"), pin(4, "SDA", "I2C_IMU_SDA", "open_drain"), pin(5, "INT1", "IMU_INT", "output")], manufacturer="TDK InvenSense", substitute_mpn="BMI088"),
        component("U6", "can", "CAN PHY", "TCAN1042HGVDRQ1", "SOIC8", [pin(1, "VCC", "V5", "power_in"), pin(2, "GND", "GND", "ground"), pin(3, "RXD", "CAN_RX", "output"), pin(4, "TXD", "CAN_TX", "input"), pin(5, "CANH", "CANH", "bidirectional"), pin(6, "CANL", "CANL", "bidirectional")], manufacturer="Texas Instruments", substitute_mpn="TJA1042TK/3"),
        component("J2", "estop", "E-STOP", "Phoenix-1935161", "Terminal_3Pin", [pin(1, "V3V3", "V3V3", "power_out"), pin(2, "ESTOP", "ESTOP_IN", "input"), pin(3, "GND", "GND", "ground")], manufacturer="Phoenix Contact", substitute_mpn="WAGO-250-203"),
        component("Q2", "safety_gate", "E-STOP GATE", "SN74LVC1G97DBVR", "SOT23-6", [pin(1, "VCC", "V3V3", "power_in"), pin(2, "IN", "ESTOP_IN", "input"), pin(3, "OUT", "ESTOP_GATE", "output"), pin(4, "GND", "GND", "ground")], manufacturer="Texas Instruments", substitute_mpn="74LVC1G97GV"),
        component("J3", "can_connector", "CAN", "Molex-43650-0300", "MicroFit_3Pin", [pin(1, "CANH", "CANH", "bidirectional"), pin(2, "CANL", "CANL", "bidirectional"), pin(3, "GND", "GND", "ground")], manufacturer="Molex", substitute_mpn="Phoenix-1935174"),
        component("R1", "termination", "120R", "RC0603FR-07120RL", "R0603", [pin(1, "A", "CANH", "passive"), pin(2, "B", "CANL", "passive")], manufacturer="Yageo", substitute_mpn="CRCW0603120RFKEA"),
        component("J4", "debug", "SWD", "Samtec-FTSH-105-01-L-DV-K", "Cortex_Debug_10Pin", [pin(1, "VREF", "V3V3", "power_out"), pin(2, "SWDIO", "SWDIO", "bidirectional"), pin(3, "GND", "GND", "ground"), pin(4, "SWCLK", "SWCLK", "input"), pin(5, "NRST", "NRST", "bidirectional")], manufacturer="Samtec", substitute_mpn="Harwin-M50-3600542"),
        component("J5", "usb", "USB-C", "USB4105-GF-A", "USB_C_16Pin", [pin(1, "VBUS", "USB_VBUS", "power_in"), pin(2, "GND", "GND", "ground"), pin(3, "D+", "USB_DP_RAW", "bidirectional"), pin(4, "D-", "USB_DM_RAW", "bidirectional")], manufacturer="GCT", substitute_mpn="USB4085-GF-A"),
        component("D2", "usb_esd", "USB ESD", "USBLC6-2SC6", "SOT23-6", [pin(1, "DP_IN", "USB_DP_RAW", "bidirectional"), pin(2, "DP_OUT", "USB_DP", "bidirectional"), pin(3, "DM_IN", "USB_DM_RAW", "bidirectional"), pin(4, "DM_OUT", "USB_DM", "bidirectional"), pin(5, "GND", "GND", "ground")], manufacturer="STMicroelectronics", substitute_mpn="TPD2EUSB30DRTR"),
        component("R4", "discharge", "100K", "RC0603FR-07100KL", "R0603", [pin(1, "VBUS", "USB_VBUS", "passive"), pin(2, "GND", "GND", "ground")], manufacturer="Yageo", substitute_mpn="CRCW0603100KFKEA"),
        component("R2", "pullup", "4K7", "RC0603FR-074K7L", "R0603", [pin(1, "VCC", "V3V3", "passive"), pin(2, "SCL", "I2C_IMU_SCL", "passive")], manufacturer="Yageo", substitute_mpn="CRCW06034K70FKEA"),
        component("R3", "pullup", "4K7", "RC0603FR-074K7L", "R0603", [pin(1, "VCC", "V3V3", "passive"), pin(2, "SDA", "I2C_IMU_SDA", "passive")], manufacturer="Yageo", substitute_mpn="CRCW06034K70FKEA"),
    ]
    for index in range(1, channels + 1):
        components.append(component(f"J{index + 10}", "motor_io", f"MOTOR_IO_{index}", "Molex-43045-0800", "MicroFit_8Pin", [
            pin(1, "V5", "V5", "power_out"), pin(2, "GND", "GND", "ground"), pin(3, "PWM", f"MOTOR{index}_PWM", "output"),
            pin(4, "CURRENT", f"MOTOR{index}_CURRENT", "analog"), pin(5, "ENC", f"MOTOR{index}_ENC", "input"), pin(6, "ESTOP", "ESTOP_GATE", "output"),
        ], manufacturer="Molex", substitute_mpn="Molex-43025-0800"))
    for index in range(1, 9):
        components.append(component(f"C{index}", "decoupling", "100nF", "GRM188R71C104KA01D", "C0603", [pin(1, "VCC", "V3V3", "passive"), pin(2, "GND", "GND", "ground")], manufacturer="Murata", substitute_mpn="CC0603KRX7R9BB104"))
    components.extend((
        component("C9", "bulk_cap", "22uF", "GRM31CR61E226ME15L", "C1206", [pin(1, "VCC", "V5", "passive"), pin(2, "GND", "GND", "ground")], manufacturer="Murata", substitute_mpn="CL31A226KAHNNNE"),
        component("C10", "bulk_cap", "10uF 50V", "GRM32ER71H106KA12L", "C1210", [pin(1, "VCC", "VSYS", "passive"), pin(2, "GND", "GND", "ground")], manufacturer="Murata", substitute_mpn="C3225X7R1H106K250AB"),
    ))
    net_classes = {"GND": "ground", "VBAT_RAW": "power", "VBAT_FUSED": "power", "VBAT": "power", "VSYS": "power", "V5": "power", "V3V3": "power", "USB_VBUS": "power", "CANH": "can", "CANL": "can"}
    endpoints: dict[str, list[str]] = defaultdict(list)
    for item in components:
        for item_pin in item["pins"]:
            endpoints[item_pin["net"]].append(f"{item['ref']}.{item_pin['number']}")
    nets = []
    for name in sorted(endpoints):
        signal_class = net_classes.get(name, "analog" if name.endswith("CURRENT") else "signal")
        nets.append({"name": name, "signal_class": signal_class, "voltage_domain": _domain(name), "connected_pins": endpoints[name], "required_track_width_mm": 2.0 if signal_class == "power" and name.startswith("VBAT") else (0.5 if signal_class == "power" else 0.2)})
    return {"components": components, "nets": nets, "design_basis": {"motor_topology": "external_driver_modules", "board_carries_motor_power": False, "max_simultaneous_peak_channels": min(channels, 10), "architecture": "protected_controller_and_external_driver_io"}}


def _domain(name: str) -> str | None:
    if name == "GND": return "GND"
    if name.startswith("VBAT") or name == "VSYS": return "VBAT"
    if name == "V5": return "V5"
    if name == "USB_VBUS": return "USB_5V"
    return "V3V3"
