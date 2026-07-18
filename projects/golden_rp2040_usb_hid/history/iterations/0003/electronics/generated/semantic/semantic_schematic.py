"""Generated executable semantic schematic for agent review.

This file is intentionally compact and pin-name based. It can be executed
to reconstruct the normalized semantic_schematic model. Native EDA/CAD
artifacts are generated from typed artifacts; edit the spec or graph-producing
blocks when changing a generated design.
"""

from hw_codesign.semantic_schematic import SemanticBoard, pin

board = SemanticBoard(
    project='golden_rp2040_usb_hid',
    revision='r1',
    purpose='LLM-suited schematic representation derived from typed graph; native EDA files are generated outputs.',
    source_graph='/Users/mrcha033/Documents/hw-cli/projects/golden_rp2040_usb_hid/electronics/generated/electrical_graph.json',
    board_width_mm=65.0,
    board_height_mm=30.0,
)
component = board.component
net = board.net
connect = board.connect
place = board.place
constraint = board.constraint

component(
    'C1',
    role='decoupling',
    value='100nF',
    component_id='grm155_100n',
    mpn='GRM155R71C104KA88D',
    manufacturer='Murata',
    package='0402',
    footprint='Capacitor_SMD:C_0402_1005Metric',
    pin_contracts={'1': {'number': '1', 'name': 'VCC', 'electrical_type': 'passive'}, '2': {'number': '2', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}},
    pins=[
        pin('1', 'VCC', net='V3V3', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'C10',
    role='decoupling',
    value='100nF',
    component_id='grm155_100n',
    mpn='GRM155R71C104KA88D',
    manufacturer='Murata',
    package='0402',
    footprint='Capacitor_SMD:C_0402_1005Metric',
    pin_contracts={'1': {'number': '1', 'name': 'VCC', 'electrical_type': 'passive'}, '2': {'number': '2', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}},
    pins=[
        pin('1', 'VCC', net='V1V1', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'C11',
    role='decoupling',
    value='1uF VREG_VIN',
    component_id='grm188_1uf',
    mpn='GRM188R61C105KA93D',
    manufacturer='Murata',
    package='0603',
    footprint='Capacitor_SMD:C_0603_1608Metric',
    pin_contracts={'1': {'number': '1', 'name': 'VCC', 'electrical_type': 'passive'}, '2': {'number': '2', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}},
    pins=[
        pin('1', 'VCC', net='V3V3', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'C12',
    role='decoupling',
    value='1uF VREG_VOUT',
    component_id='grm188_1uf',
    mpn='GRM188R61C105KA93D',
    manufacturer='Murata',
    package='0603',
    footprint='Capacitor_SMD:C_0603_1608Metric',
    pin_contracts={'1': {'number': '1', 'name': 'VCC', 'electrical_type': 'passive'}, '2': {'number': '2', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}},
    pins=[
        pin('1', 'VCC', net='V1V1', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'C13',
    role='decoupling',
    value='100nF FLASH',
    component_id='grm155_100n',
    mpn='GRM155R71C104KA88D',
    manufacturer='Murata',
    package='0402',
    footprint='Capacitor_SMD:C_0402_1005Metric',
    pin_contracts={'1': {'number': '1', 'name': 'VCC', 'electrical_type': 'passive'}, '2': {'number': '2', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}},
    pins=[
        pin('1', 'VCC', net='V3V3', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'C14',
    role='decoupling',
    value='100nF USB ESD VBUS',
    component_id='grm155_100n',
    mpn='GRM155R71C104KA88D',
    manufacturer='Murata',
    package='0402',
    footprint='Capacitor_SMD:C_0402_1005Metric',
    pin_contracts={'1': {'number': '1', 'name': 'VCC', 'electrical_type': 'passive'}, '2': {'number': '2', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}},
    pins=[
        pin('1', 'VBUS', net='USB_VBUS', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'C15',
    role='decoupling',
    value='1uF LDO input',
    component_id='grm188_1uf',
    mpn='GRM188R61C105KA93D',
    manufacturer='Murata',
    package='0603',
    footprint='Capacitor_SMD:C_0603_1608Metric',
    pin_contracts={'1': {'number': '1', 'name': 'VCC', 'electrical_type': 'passive'}, '2': {'number': '2', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}},
    pins=[
        pin('1', 'VIN', net='USB_VBUS', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'C16',
    role='decoupling',
    value='1uF LDO output',
    component_id='grm188_1uf',
    mpn='GRM188R61C105KA93D',
    manufacturer='Murata',
    package='0603',
    footprint='Capacitor_SMD:C_0603_1608Metric',
    pin_contracts={'1': {'number': '1', 'name': 'VCC', 'electrical_type': 'passive'}, '2': {'number': '2', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}},
    pins=[
        pin('1', 'VOUT', net='V3V3', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'C17',
    role='xtal_cap',
    value='15pF XTAL',
    component_id='grm1555_15p',
    mpn='GRM1555C1H150JA01D',
    manufacturer='Murata',
    package='0402',
    footprint='Capacitor_SMD:C_0402_1005Metric',
    pin_contracts={'1': {'number': '1', 'name': 'A', 'electrical_type': 'passive'}, '2': {'number': '2', 'name': 'B', 'electrical_type': 'passive'}},
    pins=[
        pin('1', 'XTAL', net='XIN', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'C18',
    role='xtal_cap',
    value='15pF XTAL',
    component_id='grm1555_15p',
    mpn='GRM1555C1H150JA01D',
    manufacturer='Murata',
    package='0402',
    footprint='Capacitor_SMD:C_0402_1005Metric',
    pin_contracts={'1': {'number': '1', 'name': 'A', 'electrical_type': 'passive'}, '2': {'number': '2', 'name': 'B', 'electrical_type': 'passive'}},
    pins=[
        pin('1', 'XTAL', net='XTAL_RETURN', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'C2',
    role='decoupling',
    value='100nF',
    component_id='grm155_100n',
    mpn='GRM155R71C104KA88D',
    manufacturer='Murata',
    package='0402',
    footprint='Capacitor_SMD:C_0402_1005Metric',
    pin_contracts={'1': {'number': '1', 'name': 'VCC', 'electrical_type': 'passive'}, '2': {'number': '2', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}},
    pins=[
        pin('1', 'VCC', net='V3V3', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'C3',
    role='decoupling',
    value='100nF',
    component_id='grm155_100n',
    mpn='GRM155R71C104KA88D',
    manufacturer='Murata',
    package='0402',
    footprint='Capacitor_SMD:C_0402_1005Metric',
    pin_contracts={'1': {'number': '1', 'name': 'VCC', 'electrical_type': 'passive'}, '2': {'number': '2', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}},
    pins=[
        pin('1', 'VCC', net='V3V3', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'C4',
    role='decoupling',
    value='100nF',
    component_id='grm155_100n',
    mpn='GRM155R71C104KA88D',
    manufacturer='Murata',
    package='0402',
    footprint='Capacitor_SMD:C_0402_1005Metric',
    pin_contracts={'1': {'number': '1', 'name': 'VCC', 'electrical_type': 'passive'}, '2': {'number': '2', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}},
    pins=[
        pin('1', 'VCC', net='V1V1', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'C5',
    role='decoupling',
    value='100nF',
    component_id='grm155_100n',
    mpn='GRM155R71C104KA88D',
    manufacturer='Murata',
    package='0402',
    footprint='Capacitor_SMD:C_0402_1005Metric',
    pin_contracts={'1': {'number': '1', 'name': 'VCC', 'electrical_type': 'passive'}, '2': {'number': '2', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}},
    pins=[
        pin('1', 'VCC', net='V3V3', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'C6',
    role='decoupling',
    value='100nF',
    component_id='grm155_100n',
    mpn='GRM155R71C104KA88D',
    manufacturer='Murata',
    package='0402',
    footprint='Capacitor_SMD:C_0402_1005Metric',
    pin_contracts={'1': {'number': '1', 'name': 'VCC', 'electrical_type': 'passive'}, '2': {'number': '2', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}},
    pins=[
        pin('1', 'VCC', net='V3V3', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'C7',
    role='decoupling',
    value='100nF',
    component_id='grm155_100n',
    mpn='GRM155R71C104KA88D',
    manufacturer='Murata',
    package='0402',
    footprint='Capacitor_SMD:C_0402_1005Metric',
    pin_contracts={'1': {'number': '1', 'name': 'VCC', 'electrical_type': 'passive'}, '2': {'number': '2', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}},
    pins=[
        pin('1', 'VCC', net='V3V3', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'C8',
    role='decoupling',
    value='100nF',
    component_id='grm155_100n',
    mpn='GRM155R71C104KA88D',
    manufacturer='Murata',
    package='0402',
    footprint='Capacitor_SMD:C_0402_1005Metric',
    pin_contracts={'1': {'number': '1', 'name': 'VCC', 'electrical_type': 'passive'}, '2': {'number': '2', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}},
    pins=[
        pin('1', 'VCC', net='V3V3', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'C9',
    role='decoupling',
    value='100nF',
    component_id='grm155_100n',
    mpn='GRM155R71C104KA88D',
    manufacturer='Murata',
    package='0402',
    footprint='Capacitor_SMD:C_0402_1005Metric',
    pin_contracts={'1': {'number': '1', 'name': 'VCC', 'electrical_type': 'passive'}, '2': {'number': '2', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}},
    pins=[
        pin('1', 'VCC', net='V3V3', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'D1',
    role='tvs',
    value='USB 2.0 ESD',
    component_id='usblc6_2sc6',
    mpn='USBLC6-2SC6',
    manufacturer='STMicroelectronics',
    package='SOT-23-6',
    footprint='Package_TO_SOT_SMD:SOT-23-6',
    pin_contracts={'1': {'number': '1', 'name': 'I/O1_IN', 'electrical_type': 'bidirectional'}, '2': {'number': '2', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}, '3': {'number': '3', 'name': 'I/O2_IN', 'electrical_type': 'bidirectional'}, '4': {'number': '4', 'name': 'I/O2_OUT', 'electrical_type': 'bidirectional'}, '5': {'number': '5', 'name': 'VBUS', 'electrical_type': 'power_in', 'voltage_domain': 'USB_5V'}, '6': {'number': '6', 'name': 'I/O1_OUT', 'electrical_type': 'bidirectional'}},
    pins=[
        pin('1', 'DP_IN', net='USB_DP_RAW', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('3', 'DM_IN', net='USB_DM_RAW', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('4', 'DM_OUT', net='USB_DM_ESD', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('5', 'VBUS', net='USB_VBUS', role='power_in', voltage_domain='USB_5V', mcu_pin=None),
        pin('6', 'DP_OUT', net='USB_DP_ESD', role='bidirectional', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'J1',
    role='power_input',
    value='USB-C 2.0',
    component_id='usb4105_gf_a',
    mpn='USB4105-GF-A',
    manufacturer='GCT',
    package='USB-C-16',
    footprint='Connector_USB:USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal',
    pin_contracts={'A1': {'number': 'A1', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}, 'A4': {'number': 'A4', 'name': 'VBUS', 'electrical_type': 'power_in', 'voltage_domain': 'USB_5V'}, 'A5': {'number': 'A5', 'name': 'CC1', 'electrical_type': 'passive'}, 'A6': {'number': 'A6', 'name': 'D+', 'electrical_type': 'bidirectional'}, 'A7': {'number': 'A7', 'name': 'D-', 'electrical_type': 'bidirectional'}, 'A8': {'number': 'A8', 'name': 'SBU1', 'electrical_type': 'no_connect'}, 'A9': {'number': 'A9', 'name': 'VBUS', 'electrical_type': 'power_in', 'voltage_domain': 'USB_5V'}, 'A12': {'number': 'A12', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}, 'B1': {'number': 'B1', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}, 'B4': {'number': 'B4', 'name': 'VBUS', 'electrical_type': 'power_in', 'voltage_domain': 'USB_5V'}, 'B5': {'number': 'B5', 'name': 'CC2', 'electrical_type': 'passive'}, 'B6': {'number': 'B6', 'name': 'D+', 'electrical_type': 'bidirectional'}, 'B7': {'number': 'B7', 'name': 'D-', 'electrical_type': 'bidirectional'}, 'B8': {'number': 'B8', 'name': 'SBU2', 'electrical_type': 'no_connect'}, 'B9': {'number': 'B9', 'name': 'VBUS', 'electrical_type': 'power_in', 'voltage_domain': 'USB_5V'}, 'B12': {'number': 'B12', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}, 'SH': {'number': 'SH', 'name': 'SHIELD', 'electrical_type': 'ground', 'voltage_domain': 'GND'}},
    pins=[
        pin('A1', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('A4', 'VBUS', net='USB_VBUS', role='power_in', voltage_domain='USB_5V', mcu_pin=None),
        pin('A5', 'CC1', net='USB_CC1', role='passive', voltage_domain=None, mcu_pin=None),
        pin('A6', 'D+', net='USB_DP_RAW', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('A7', 'D-', net='USB_DM_RAW', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('A8', 'SBU1', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('A9', 'VBUS', net='USB_VBUS', role='power_in', voltage_domain='USB_5V', mcu_pin=None),
        pin('A12', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('B1', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('B4', 'VBUS', net='USB_VBUS', role='power_in', voltage_domain='USB_5V', mcu_pin=None),
        pin('B5', 'CC2', net='USB_CC2', role='passive', voltage_domain=None, mcu_pin=None),
        pin('B6', 'D+', net='USB_DP_RAW', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('B7', 'D-', net='USB_DM_RAW', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('B8', 'SBU2', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('B9', 'VBUS', net='USB_VBUS', role='power_in', voltage_domain='USB_5V', mcu_pin=None),
        pin('B12', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('SH', 'SHIELD', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'J2',
    role='debug_header',
    value='Cortex 10-pin SWD',
    component_id='conn_2x05_2p54',
    mpn='61201021621',
    manufacturer='Würth Elektronik',
    package='BoxHeader-2x5-2.54mm',
    footprint='Connector_IDC:IDC-Header_2x05_P2.54mm_Vertical',
    pin_contracts={'1': {'number': '1', 'name': 'VCC', 'electrical_type': 'power_in'}, '2': {'number': '2', 'name': 'SWDIO', 'electrical_type': 'bidirectional'}, '3': {'number': '3', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}, '4': {'number': '4', 'name': 'SWDCLK', 'electrical_type': 'input'}, '5': {'number': '5', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}, '6': {'number': '6', 'name': 'SWO', 'electrical_type': 'output'}, '7': {'number': '7', 'name': 'KEY', 'electrical_type': 'no_connect'}, '8': {'number': '8', 'name': 'NC', 'electrical_type': 'no_connect'}, '9': {'number': '9', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}, '10': {'number': '10', 'name': 'RESET', 'electrical_type': 'input'}},
    pins=[
        pin('1', 'VTREF', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin=None),
        pin('2', 'SWDIO', net='SWDIO', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('3', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('4', 'SWCLK', net='SWCLK', role='input', voltage_domain=None, mcu_pin=None),
        pin('5', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('6', 'SWO', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('7', 'KEY', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('8', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('9', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('10', 'RUN', net='MCU_RUN', role='bidirectional', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'R1',
    role='usb_series_resistor',
    value='27R USB D+',
    component_id='rc0603_27r',
    mpn='RC0603FR-0727RL',
    manufacturer='Yageo',
    package='0603',
    footprint='Resistor_SMD:R_0603_1608Metric',
    pin_contracts={'1': {'number': '1', 'name': 'A', 'electrical_type': 'passive'}, '2': {'number': '2', 'name': 'B', 'electrical_type': 'passive'}},
    pins=[
        pin('1', 'ESD', net='USB_DP_ESD', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'MCU', net='USB_DP', role='passive', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'R2',
    role='usb_series_resistor',
    value='27R USB D-',
    component_id='rc0603_27r',
    mpn='RC0603FR-0727RL',
    manufacturer='Yageo',
    package='0603',
    footprint='Resistor_SMD:R_0603_1608Metric',
    pin_contracts={'1': {'number': '1', 'name': 'A', 'electrical_type': 'passive'}, '2': {'number': '2', 'name': 'B', 'electrical_type': 'passive'}},
    pins=[
        pin('1', 'ESD', net='USB_DM_ESD', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'MCU', net='USB_DM', role='passive', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'R3',
    role='xtal_series_resistor',
    value='1K XTAL damping',
    component_id='rc0603_1k',
    mpn='RC0603FR-071KL',
    manufacturer='Yageo',
    package='R0603',
    footprint='Resistor_SMD:R_0603_1608Metric',
    pin_contracts={'1': {'number': '1', 'name': 'A', 'electrical_type': 'passive'}, '2': {'number': '2', 'name': 'B', 'electrical_type': 'passive'}},
    pins=[
        pin('1', 'XOUT', net='XOUT', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'XTAL', net='XTAL_RETURN', role='passive', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'R4',
    role='flash_cs_pullup',
    value='10K QSPI CS pull-up',
    component_id='rc0603_10k',
    mpn='RC0603FR-0710KL',
    manufacturer='Yageo',
    package='R0603',
    footprint='Resistor_SMD:R_0603_1608Metric',
    pin_contracts={'1': {'number': '1', 'name': 'A', 'electrical_type': 'passive'}, '2': {'number': '2', 'name': 'B', 'electrical_type': 'passive'}},
    pins=[
        pin('1', 'VCC', net='V3V3', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'CS', net='QSPI_CS', role='passive', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'R5',
    role='usb_cc_pulldown',
    value='5K1 USB-C Rd',
    component_id='rc0603_5k1',
    mpn='RC0603FR-075K1L',
    manufacturer='Yageo',
    package='0603',
    footprint='Resistor_SMD:R_0603_1608Metric',
    pin_contracts={'1': {'number': '1', 'name': 'A', 'electrical_type': 'passive'}, '2': {'number': '2', 'name': 'B', 'electrical_type': 'passive'}},
    pins=[
        pin('1', 'A', net='USB_CC1', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'B', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'R6',
    role='usb_cc_pulldown',
    value='5K1 USB-C Rd',
    component_id='rc0603_5k1',
    mpn='RC0603FR-075K1L',
    manufacturer='Yageo',
    package='0603',
    footprint='Resistor_SMD:R_0603_1608Metric',
    pin_contracts={'1': {'number': '1', 'name': 'A', 'electrical_type': 'passive'}, '2': {'number': '2', 'name': 'B', 'electrical_type': 'passive'}},
    pins=[
        pin('1', 'A', net='USB_CC2', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'B', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'U1',
    role='regulator_3v3',
    value='3V3 LDO',
    component_id='ap2112k_33trg1',
    mpn='AP2112K-3.3TRG1',
    manufacturer='Diodes Incorporated',
    package='SOT-23-5',
    footprint='Package_TO_SOT_SMD:SOT-23-5',
    pin_contracts={'1': {'number': '1', 'name': 'EN', 'electrical_type': 'input'}, '2': {'number': '2', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}, '3': {'number': '3', 'name': 'VIN', 'electrical_type': 'power_in'}, '4': {'number': '4', 'name': 'NC', 'electrical_type': 'no_connect'}, '5': {'number': '5', 'name': 'VOUT', 'electrical_type': 'power_out'}},
    pins=[
        pin('1', 'EN', net='USB_VBUS', role='input', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('3', 'VIN', net='USB_VBUS', role='power_in', voltage_domain='USB_5V', mcu_pin=None),
        pin('4', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('5', 'VOUT', net='V3V3', role='power_out', voltage_domain='V3V3', mcu_pin=None),
    ],
)

component(
    'U2',
    role='mcu',
    value='RP2040',
    component_id='rp2040',
    mpn='RP2040',
    manufacturer='Raspberry Pi Ltd',
    package='QFN-56-1EP',
    footprint='Package_DFN_QFN:QFN-56-1EP_7x7mm_P0.4mm_EP3.2x3.2mm',
    pin_contracts={'1': {'number': '1', 'name': 'IOVDD', 'electrical_type': 'power_in', 'voltage_domain': 'V3V3'}, '2': {'number': '2', 'name': 'GPIO0', 'electrical_type': 'bidirectional'}, '3': {'number': '3', 'name': 'GPIO1', 'electrical_type': 'bidirectional'}, '4': {'number': '4', 'name': 'GPIO2', 'electrical_type': 'bidirectional'}, '5': {'number': '5', 'name': 'GPIO3', 'electrical_type': 'bidirectional'}, '6': {'number': '6', 'name': 'GPIO4', 'electrical_type': 'bidirectional'}, '7': {'number': '7', 'name': 'GPIO5', 'electrical_type': 'bidirectional'}, '8': {'number': '8', 'name': 'GPIO6', 'electrical_type': 'bidirectional'}, '9': {'number': '9', 'name': 'GPIO7', 'electrical_type': 'bidirectional'}, '10': {'number': '10', 'name': 'IOVDD', 'electrical_type': 'power_in', 'voltage_domain': 'V3V3'}, '11': {'number': '11', 'name': 'GPIO8', 'electrical_type': 'bidirectional'}, '12': {'number': '12', 'name': 'GPIO9', 'electrical_type': 'bidirectional'}, '13': {'number': '13', 'name': 'GPIO10', 'electrical_type': 'bidirectional'}, '14': {'number': '14', 'name': 'GPIO11', 'electrical_type': 'bidirectional'}, '15': {'number': '15', 'name': 'GPIO12', 'electrical_type': 'bidirectional'}, '16': {'number': '16', 'name': 'GPIO13', 'electrical_type': 'bidirectional'}, '17': {'number': '17', 'name': 'GPIO14', 'electrical_type': 'bidirectional'}, '18': {'number': '18', 'name': 'GPIO15', 'electrical_type': 'bidirectional'}, '19': {'number': '19', 'name': 'TESTEN', 'electrical_type': 'ground', 'voltage_domain': 'GND'}, '20': {'number': '20', 'name': 'XIN', 'electrical_type': 'passive'}, '21': {'number': '21', 'name': 'XOUT', 'electrical_type': 'passive'}, '22': {'number': '22', 'name': 'IOVDD', 'electrical_type': 'power_in', 'voltage_domain': 'V3V3'}, '23': {'number': '23', 'name': 'DVDD', 'electrical_type': 'power_in', 'voltage_domain': 'V1V1'}, '24': {'number': '24', 'name': 'SWCLK', 'electrical_type': 'input'}, '25': {'number': '25', 'name': 'SWDIO', 'electrical_type': 'bidirectional'}, '26': {'number': '26', 'name': 'RUN', 'electrical_type': 'input'}, '27': {'number': '27', 'name': 'GPIO16', 'electrical_type': 'bidirectional'}, '28': {'number': '28', 'name': 'GPIO17', 'electrical_type': 'bidirectional'}, '29': {'number': '29', 'name': 'GPIO18', 'electrical_type': 'bidirectional'}, '30': {'number': '30', 'name': 'GPIO19', 'electrical_type': 'bidirectional'}, '31': {'number': '31', 'name': 'GPIO20', 'electrical_type': 'bidirectional'}, '32': {'number': '32', 'name': 'GPIO21', 'electrical_type': 'bidirectional'}, '33': {'number': '33', 'name': 'IOVDD', 'electrical_type': 'power_in', 'voltage_domain': 'V3V3'}, '34': {'number': '34', 'name': 'GPIO22', 'electrical_type': 'bidirectional'}, '35': {'number': '35', 'name': 'GPIO23', 'electrical_type': 'bidirectional'}, '36': {'number': '36', 'name': 'GPIO24', 'electrical_type': 'bidirectional'}, '37': {'number': '37', 'name': 'GPIO25', 'electrical_type': 'bidirectional'}, '38': {'number': '38', 'name': 'GPIO26_ADC0', 'electrical_type': 'bidirectional'}, '39': {'number': '39', 'name': 'GPIO27_ADC1', 'electrical_type': 'bidirectional'}, '40': {'number': '40', 'name': 'GPIO28_ADC2', 'electrical_type': 'bidirectional'}, '41': {'number': '41', 'name': 'GPIO29_ADC3', 'electrical_type': 'bidirectional'}, '42': {'number': '42', 'name': 'IOVDD', 'electrical_type': 'power_in', 'voltage_domain': 'V3V3'}, '43': {'number': '43', 'name': 'ADC_AVDD', 'electrical_type': 'power_in', 'voltage_domain': 'V3V3'}, '44': {'number': '44', 'name': 'VREG_VIN', 'electrical_type': 'power_in', 'voltage_domain': 'V3V3'}, '45': {'number': '45', 'name': 'VREG_VOUT', 'electrical_type': 'power_out', 'voltage_domain': 'V1V1'}, '46': {'number': '46', 'name': 'USB_DM', 'electrical_type': 'bidirectional'}, '47': {'number': '47', 'name': 'USB_DP', 'electrical_type': 'bidirectional'}, '48': {'number': '48', 'name': 'USB_VDD', 'electrical_type': 'power_in', 'voltage_domain': 'V3V3'}, '49': {'number': '49', 'name': 'IOVDD', 'electrical_type': 'power_in', 'voltage_domain': 'V3V3'}, '50': {'number': '50', 'name': 'DVDD', 'electrical_type': 'power_in', 'voltage_domain': 'V1V1'}, '51': {'number': '51', 'name': 'QSPI_SD3', 'electrical_type': 'bidirectional'}, '52': {'number': '52', 'name': 'QSPI_SCLK', 'electrical_type': 'output'}, '53': {'number': '53', 'name': 'QSPI_SD0', 'electrical_type': 'bidirectional'}, '54': {'number': '54', 'name': 'QSPI_SD2', 'electrical_type': 'bidirectional'}, '55': {'number': '55', 'name': 'QSPI_SD1', 'electrical_type': 'bidirectional'}, '56': {'number': '56', 'name': 'QSPI_CSn', 'electrical_type': 'output'}, '57': {'number': '57', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}},
    pins=[
        pin('1', 'IOVDD', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin='IOVDD'),
        pin('2', 'GPIO0', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('3', 'GPIO1', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('4', 'GPIO2', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('5', 'GPIO3', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('6', 'GPIO4', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('7', 'GPIO5', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('8', 'GPIO6', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('9', 'GPIO7', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('10', 'IOVDD', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin='IOVDD'),
        pin('11', 'GPIO8', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('12', 'GPIO9', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('13', 'GPIO10', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('14', 'GPIO11', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('15', 'GPIO12', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('16', 'GPIO13', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('17', 'GPIO14', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('18', 'GPIO15', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('19', 'TESTEN', net='GND', role='ground', voltage_domain='GND', mcu_pin='TESTEN'),
        pin('20', 'XIN', net='XIN', role='passive', voltage_domain=None, mcu_pin='XIN'),
        pin('21', 'XOUT', net='XOUT', role='passive', voltage_domain=None, mcu_pin='XOUT'),
        pin('22', 'IOVDD', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin='IOVDD'),
        pin('23', 'DVDD', net='V1V1', role='power_in', voltage_domain='V1V1', mcu_pin='DVDD'),
        pin('24', 'SWCLK', net='SWCLK', role='input', voltage_domain=None, mcu_pin='SWCLK'),
        pin('25', 'SWDIO', net='SWDIO', role='bidirectional', voltage_domain=None, mcu_pin='SWDIO'),
        pin('26', 'RUN', net='MCU_RUN', role='input', voltage_domain=None, mcu_pin='RUN'),
        pin('27', 'GPIO16', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('28', 'GPIO17', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('29', 'GPIO18', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('30', 'GPIO19', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('31', 'GPIO20', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('32', 'GPIO21', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('33', 'IOVDD', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin='IOVDD'),
        pin('34', 'GPIO22', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('35', 'GPIO23', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('36', 'GPIO24', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('37', 'GPIO25', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('38', 'GPIO26_ADC0', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('39', 'GPIO27_ADC1', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('40', 'GPIO28_ADC2', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('41', 'GPIO29_ADC3', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('42', 'IOVDD', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin='IOVDD'),
        pin('43', 'ADC_AVDD', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin='ADC_AVDD'),
        pin('44', 'VREG_VIN', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin='VREG_VIN'),
        pin('45', 'VREG_VOUT', net='V1V1', role='power_out', voltage_domain='V1V1', mcu_pin='VREG_VOUT'),
        pin('46', 'USB_DM', net='USB_DM', role='bidirectional', voltage_domain=None, mcu_pin='USB_DM'),
        pin('47', 'USB_DP', net='USB_DP', role='bidirectional', voltage_domain=None, mcu_pin='USB_DP'),
        pin('48', 'USB_VDD', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin='USB_VDD'),
        pin('49', 'IOVDD', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin='IOVDD'),
        pin('50', 'DVDD', net='V1V1', role='power_in', voltage_domain='V1V1', mcu_pin='DVDD'),
        pin('51', 'QSPI_SD3', net='QSPI_D3', role='bidirectional', voltage_domain=None, mcu_pin='QSPI_SD3'),
        pin('52', 'QSPI_SCLK', net='QSPI_CLK', role='output', voltage_domain=None, mcu_pin='QSPI_SCLK'),
        pin('53', 'QSPI_SD0', net='QSPI_MOSI', role='bidirectional', voltage_domain=None, mcu_pin='QSPI_SD0'),
        pin('54', 'QSPI_SD2', net='QSPI_D2', role='bidirectional', voltage_domain=None, mcu_pin='QSPI_SD2'),
        pin('55', 'QSPI_SD1', net='QSPI_MISO', role='bidirectional', voltage_domain=None, mcu_pin='QSPI_SD1'),
        pin('56', 'QSPI_CSn', net='QSPI_CS', role='output', voltage_domain=None, mcu_pin='QSPI_CSn'),
        pin('57', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin='GND'),
    ],
)

component(
    'U3',
    role='flash',
    value='16Mbit QSPI Flash',
    component_id='w25q16jv',
    mpn='W25Q16JVSSIQ',
    manufacturer='Winbond Electronics',
    package='SOP-8-208mil',
    footprint='Package_SO:SOIC-8_5.3x5.3mm_P1.27mm',
    pin_contracts={'1': {'number': '1', 'name': 'CS', 'electrical_type': 'input'}, '2': {'number': '2', 'name': 'IO1', 'electrical_type': 'bidirectional'}, '3': {'number': '3', 'name': 'IO2_WP', 'electrical_type': 'bidirectional'}, '4': {'number': '4', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}, '5': {'number': '5', 'name': 'IO0', 'electrical_type': 'bidirectional'}, '6': {'number': '6', 'name': 'CLK', 'electrical_type': 'input'}, '7': {'number': '7', 'name': 'IO3_HOLD', 'electrical_type': 'bidirectional'}, '8': {'number': '8', 'name': 'VCC', 'electrical_type': 'power_in', 'voltage_domain': 'V3V3'}},
    pins=[
        pin('1', '~CS', net='QSPI_CS', role='input', voltage_domain=None, mcu_pin=None),
        pin('2', 'IO1', net='QSPI_MISO', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('3', 'IO2/~WP', net='QSPI_D2', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('4', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('5', 'IO0', net='QSPI_MOSI', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('6', 'CLK', net='QSPI_CLK', role='input', voltage_domain=None, mcu_pin=None),
        pin('7', 'IO3/~HOLD', net='QSPI_D3', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('8', 'VCC', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin=None),
    ],
)

component(
    'X1',
    role='crystal_12m',
    value='12MHz RP2040 crystal',
    component_id='abm8_272_t3',
    mpn='ABM8-272-T3',
    manufacturer='Abracon',
    package='3225-4-SMD',
    footprint='Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm',
    pin_contracts={'1': {'number': '1', 'name': 'XIN', 'electrical_type': 'passive'}, '2': {'number': '2', 'name': 'CASE_GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}, '3': {'number': '3', 'name': 'XTAL_RETURN', 'electrical_type': 'passive'}, '4': {'number': '4', 'name': 'CASE_GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}},
    pins=[
        pin('1', 'XIN', net='XIN', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'CASE_GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('3', 'XTAL_RETURN', net='XTAL_RETURN', role='passive', voltage_domain=None, mcu_pin=None),
        pin('4', 'CASE_GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)


net('GND', signal_class='ground', voltage_domain='GND', required_track_width_mm=0.2)
connect('C1', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('C10', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('C11', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('C12', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('C13', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('C14', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('C15', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('C16', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('C17', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('C18', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('C2', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('C3', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('C4', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('C5', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('C6', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('C7', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('C8', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('C9', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('D1', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('J1', pin='GND', number='A1', net='GND', role='ground', mcu_pin=None)
connect('J1', pin='GND', number='A12', net='GND', role='ground', mcu_pin=None)
connect('J1', pin='GND', number='B1', net='GND', role='ground', mcu_pin=None)
connect('J1', pin='GND', number='B12', net='GND', role='ground', mcu_pin=None)
connect('J1', pin='SHIELD', number='SH', net='GND', role='ground', mcu_pin=None)
connect('J2', pin='GND', number='3', net='GND', role='ground', mcu_pin=None)
connect('J2', pin='GND', number='5', net='GND', role='ground', mcu_pin=None)
connect('J2', pin='GND', number='9', net='GND', role='ground', mcu_pin=None)
connect('R5', pin='B', number='2', net='GND', role='ground', mcu_pin=None)
connect('R6', pin='B', number='2', net='GND', role='ground', mcu_pin=None)
connect('U1', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('U2', pin='TESTEN', number='19', net='GND', role='ground', mcu_pin='TESTEN')
connect('U2', pin='GND', number='57', net='GND', role='ground', mcu_pin='GND')
connect('U3', pin='GND', number='4', net='GND', role='ground', mcu_pin=None)
connect('X1', pin='CASE_GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('X1', pin='CASE_GND', number='4', net='GND', role='ground', mcu_pin=None)

net('MCU_RUN', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.15)
connect('J2', pin='RUN', number='10', net='MCU_RUN', role='bidirectional', mcu_pin=None)
connect('U2', pin='RUN', number='26', net='MCU_RUN', role='input', mcu_pin='RUN')

net('QSPI_CLK', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.15)
connect('U2', pin='QSPI_SCLK', number='52', net='QSPI_CLK', role='output', mcu_pin='QSPI_SCLK')
connect('U3', pin='CLK', number='6', net='QSPI_CLK', role='input', mcu_pin=None)

net('QSPI_CS', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.15)
connect('R4', pin='CS', number='2', net='QSPI_CS', role='passive', mcu_pin=None)
connect('U2', pin='QSPI_CSn', number='56', net='QSPI_CS', role='output', mcu_pin='QSPI_CSn')
connect('U3', pin='~CS', number='1', net='QSPI_CS', role='input', mcu_pin=None)

net('QSPI_D2', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.15)
connect('U2', pin='QSPI_SD2', number='54', net='QSPI_D2', role='bidirectional', mcu_pin='QSPI_SD2')
connect('U3', pin='IO2/~WP', number='3', net='QSPI_D2', role='bidirectional', mcu_pin=None)

net('QSPI_D3', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.15)
connect('U2', pin='QSPI_SD3', number='51', net='QSPI_D3', role='bidirectional', mcu_pin='QSPI_SD3')
connect('U3', pin='IO3/~HOLD', number='7', net='QSPI_D3', role='bidirectional', mcu_pin=None)

net('QSPI_MISO', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.15)
connect('U2', pin='QSPI_SD1', number='55', net='QSPI_MISO', role='bidirectional', mcu_pin='QSPI_SD1')
connect('U3', pin='IO1', number='2', net='QSPI_MISO', role='bidirectional', mcu_pin=None)

net('QSPI_MOSI', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.15)
connect('U2', pin='QSPI_SD0', number='53', net='QSPI_MOSI', role='bidirectional', mcu_pin='QSPI_SD0')
connect('U3', pin='IO0', number='5', net='QSPI_MOSI', role='bidirectional', mcu_pin=None)

net('SWCLK', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.15)
connect('J2', pin='SWCLK', number='4', net='SWCLK', role='input', mcu_pin=None)
connect('U2', pin='SWCLK', number='24', net='SWCLK', role='input', mcu_pin='SWCLK')

net('SWDIO', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.15)
connect('J2', pin='SWDIO', number='2', net='SWDIO', role='bidirectional', mcu_pin=None)
connect('U2', pin='SWDIO', number='25', net='SWDIO', role='bidirectional', mcu_pin='SWDIO')

net('USB_CC1', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.15)
connect('J1', pin='CC1', number='A5', net='USB_CC1', role='passive', mcu_pin=None)
connect('R5', pin='A', number='1', net='USB_CC1', role='passive', mcu_pin=None)

net('USB_CC2', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.15)
connect('J1', pin='CC2', number='B5', net='USB_CC2', role='passive', mcu_pin=None)
connect('R6', pin='A', number='1', net='USB_CC2', role='passive', mcu_pin=None)

net('USB_DM', signal_class='usb', voltage_domain='V3V3', required_track_width_mm=0.8)
connect('R2', pin='MCU', number='2', net='USB_DM', role='passive', mcu_pin=None)
connect('U2', pin='USB_DM', number='46', net='USB_DM', role='bidirectional', mcu_pin='USB_DM')

net('USB_DM_ESD', signal_class='usb', voltage_domain='V3V3', required_track_width_mm=0.8)
connect('D1', pin='DM_OUT', number='4', net='USB_DM_ESD', role='bidirectional', mcu_pin=None)
connect('R2', pin='ESD', number='1', net='USB_DM_ESD', role='passive', mcu_pin=None)

net('USB_DM_RAW', signal_class='usb', voltage_domain='V3V3', required_track_width_mm=0.8)
connect('D1', pin='DM_IN', number='3', net='USB_DM_RAW', role='bidirectional', mcu_pin=None)
connect('J1', pin='D-', number='A7', net='USB_DM_RAW', role='bidirectional', mcu_pin=None)
connect('J1', pin='D-', number='B7', net='USB_DM_RAW', role='bidirectional', mcu_pin=None)

net('USB_DP', signal_class='usb', voltage_domain='V3V3', required_track_width_mm=0.8)
connect('R1', pin='MCU', number='2', net='USB_DP', role='passive', mcu_pin=None)
connect('U2', pin='USB_DP', number='47', net='USB_DP', role='bidirectional', mcu_pin='USB_DP')

net('USB_DP_ESD', signal_class='usb', voltage_domain='V3V3', required_track_width_mm=0.8)
connect('D1', pin='DP_OUT', number='6', net='USB_DP_ESD', role='bidirectional', mcu_pin=None)
connect('R1', pin='ESD', number='1', net='USB_DP_ESD', role='passive', mcu_pin=None)

net('USB_DP_RAW', signal_class='usb', voltage_domain='V3V3', required_track_width_mm=0.8)
connect('D1', pin='DP_IN', number='1', net='USB_DP_RAW', role='bidirectional', mcu_pin=None)
connect('J1', pin='D+', number='A6', net='USB_DP_RAW', role='bidirectional', mcu_pin=None)
connect('J1', pin='D+', number='B6', net='USB_DP_RAW', role='bidirectional', mcu_pin=None)

net('USB_VBUS', signal_class='power', voltage_domain='USB_5V', required_track_width_mm=0.5)
connect('C14', pin='VBUS', number='1', net='USB_VBUS', role='passive', mcu_pin=None)
connect('C15', pin='VIN', number='1', net='USB_VBUS', role='passive', mcu_pin=None)
connect('D1', pin='VBUS', number='5', net='USB_VBUS', role='power_in', mcu_pin=None)
connect('J1', pin='VBUS', number='A4', net='USB_VBUS', role='power_in', mcu_pin=None)
connect('J1', pin='VBUS', number='A9', net='USB_VBUS', role='power_in', mcu_pin=None)
connect('J1', pin='VBUS', number='B4', net='USB_VBUS', role='power_in', mcu_pin=None)
connect('J1', pin='VBUS', number='B9', net='USB_VBUS', role='power_in', mcu_pin=None)
connect('U1', pin='EN', number='1', net='USB_VBUS', role='input', mcu_pin=None)
connect('U1', pin='VIN', number='3', net='USB_VBUS', role='power_in', mcu_pin=None)

net('V1V1', signal_class='power', voltage_domain='V1V1', required_track_width_mm=0.5)
connect('C10', pin='VCC', number='1', net='V1V1', role='passive', mcu_pin=None)
connect('C12', pin='VCC', number='1', net='V1V1', role='passive', mcu_pin=None)
connect('C4', pin='VCC', number='1', net='V1V1', role='passive', mcu_pin=None)
connect('U2', pin='DVDD', number='23', net='V1V1', role='power_in', mcu_pin='DVDD')
connect('U2', pin='VREG_VOUT', number='45', net='V1V1', role='power_out', mcu_pin='VREG_VOUT')
connect('U2', pin='DVDD', number='50', net='V1V1', role='power_in', mcu_pin='DVDD')

net('V3V3', signal_class='power', voltage_domain='V3V3', required_track_width_mm=0.5)
connect('C1', pin='VCC', number='1', net='V3V3', role='passive', mcu_pin=None)
connect('C11', pin='VCC', number='1', net='V3V3', role='passive', mcu_pin=None)
connect('C13', pin='VCC', number='1', net='V3V3', role='passive', mcu_pin=None)
connect('C16', pin='VOUT', number='1', net='V3V3', role='passive', mcu_pin=None)
connect('C2', pin='VCC', number='1', net='V3V3', role='passive', mcu_pin=None)
connect('C3', pin='VCC', number='1', net='V3V3', role='passive', mcu_pin=None)
connect('C5', pin='VCC', number='1', net='V3V3', role='passive', mcu_pin=None)
connect('C6', pin='VCC', number='1', net='V3V3', role='passive', mcu_pin=None)
connect('C7', pin='VCC', number='1', net='V3V3', role='passive', mcu_pin=None)
connect('C8', pin='VCC', number='1', net='V3V3', role='passive', mcu_pin=None)
connect('C9', pin='VCC', number='1', net='V3V3', role='passive', mcu_pin=None)
connect('J2', pin='VTREF', number='1', net='V3V3', role='power_in', mcu_pin=None)
connect('R4', pin='VCC', number='1', net='V3V3', role='passive', mcu_pin=None)
connect('U1', pin='VOUT', number='5', net='V3V3', role='power_out', mcu_pin=None)
connect('U2', pin='IOVDD', number='1', net='V3V3', role='power_in', mcu_pin='IOVDD')
connect('U2', pin='IOVDD', number='10', net='V3V3', role='power_in', mcu_pin='IOVDD')
connect('U2', pin='IOVDD', number='22', net='V3V3', role='power_in', mcu_pin='IOVDD')
connect('U2', pin='IOVDD', number='33', net='V3V3', role='power_in', mcu_pin='IOVDD')
connect('U2', pin='IOVDD', number='42', net='V3V3', role='power_in', mcu_pin='IOVDD')
connect('U2', pin='ADC_AVDD', number='43', net='V3V3', role='power_in', mcu_pin='ADC_AVDD')
connect('U2', pin='VREG_VIN', number='44', net='V3V3', role='power_in', mcu_pin='VREG_VIN')
connect('U2', pin='USB_VDD', number='48', net='V3V3', role='power_in', mcu_pin='USB_VDD')
connect('U2', pin='IOVDD', number='49', net='V3V3', role='power_in', mcu_pin='IOVDD')
connect('U3', pin='VCC', number='8', net='V3V3', role='power_in', mcu_pin=None)

net('XIN', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.15)
connect('C17', pin='XTAL', number='1', net='XIN', role='passive', mcu_pin=None)
connect('U2', pin='XIN', number='20', net='XIN', role='passive', mcu_pin='XIN')
connect('X1', pin='XIN', number='1', net='XIN', role='passive', mcu_pin=None)

net('XOUT', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.15)
connect('R3', pin='XOUT', number='1', net='XOUT', role='passive', mcu_pin=None)
connect('U2', pin='XOUT', number='21', net='XOUT', role='passive', mcu_pin='XOUT')

net('XTAL_RETURN', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.15)
connect('C18', pin='XTAL', number='1', net='XTAL_RETURN', role='passive', mcu_pin=None)
connect('R3', pin='XTAL', number='2', net='XTAL_RETURN', role='passive', mcu_pin=None)
connect('X1', pin='XTAL_RETURN', number='3', net='XTAL_RETURN', role='passive', mcu_pin=None)


place('C1', data={'ref': 'C1', 'x_mm': 24.8, 'y_mm': 13.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 1.52, 'courtyard_h_mm': 0.62, 'source': 'rp2040_usb_hid_anchor', 'rationale': '', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('C10', data={'ref': 'C10', 'x_mm': 25.5, 'y_mm': 8.5, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 1.52, 'courtyard_h_mm': 0.62, 'source': 'rp2040_usb_hid_anchor', 'rationale': '', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('C11', data={'ref': 'C11', 'x_mm': 35.97, 'y_mm': 8.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 2.45, 'courtyard_h_mm': 0.95, 'source': 'rp2040_usb_hid_anchor', 'rationale': '', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('C12', data={'ref': 'C12', 'x_mm': 33.0, 'y_mm': 8.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 2.45, 'courtyard_h_mm': 0.95, 'source': 'rp2040_usb_hid_anchor', 'rationale': '', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('C13', data={'ref': 'C13', 'x_mm': 43.0, 'y_mm': 11.5, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 1.52, 'courtyard_h_mm': 0.62, 'source': 'rp2040_usb_hid_anchor', 'rationale': '', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('C14', data={'ref': 'C14', 'x_mm': 15.5, 'y_mm': 18.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 1.52, 'courtyard_h_mm': 0.62, 'source': 'rp2040_usb_hid_anchor', 'rationale': '', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('C15', data={'ref': 'C15', 'x_mm': 10.8, 'y_mm': 24.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 2.45, 'courtyard_h_mm': 0.95, 'source': 'rp2040_usb_hid_anchor', 'rationale': '', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('C16', data={'ref': 'C16', 'x_mm': 24.4, 'y_mm': 19.7, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 2.45, 'courtyard_h_mm': 0.95, 'source': 'solver_decoupling_proximity', 'rationale': 'Cost solver placed C16 beside, not inside, decoupling target U2.', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('C17', data={'ref': 'C17', 'x_mm': 43.0, 'y_mm': 17.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 1.52, 'courtyard_h_mm': 0.62, 'source': 'crystal_load_cap_seed', 'rationale': 'Crystal load capacitor position derived from the crystal reference.', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('C18', data={'ref': 'C18', 'x_mm': 43.0, 'y_mm': 23.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 1.52, 'courtyard_h_mm': 0.62, 'source': 'crystal_load_cap_seed', 'rationale': 'Crystal load capacitor position derived from the crystal reference.', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('C2', data={'ref': 'C2', 'x_mm': 24.8, 'y_mm': 16.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 1.52, 'courtyard_h_mm': 0.62, 'source': 'rp2040_usb_hid_anchor', 'rationale': '', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('C3', data={'ref': 'C3', 'x_mm': 29.7, 'y_mm': 20.5, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 1.52, 'courtyard_h_mm': 0.62, 'source': 'rp2040_usb_hid_anchor', 'rationale': '', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('C4', data={'ref': 'C4', 'x_mm': 31.7, 'y_mm': 20.5, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 1.52, 'courtyard_h_mm': 0.62, 'source': 'rp2040_usb_hid_anchor', 'rationale': '', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('C5', data={'ref': 'C5', 'x_mm': 35.1, 'y_mm': 16.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 1.52, 'courtyard_h_mm': 0.62, 'source': 'rp2040_usb_hid_anchor', 'rationale': '', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('C6', data={'ref': 'C6', 'x_mm': 35.1, 'y_mm': 12.5, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 1.52, 'courtyard_h_mm': 0.62, 'source': 'rp2040_usb_hid_anchor', 'rationale': '', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('C7', data={'ref': 'C7', 'x_mm': 34.5, 'y_mm': 10.5, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 1.52, 'courtyard_h_mm': 0.62, 'source': 'rp2040_usb_hid_anchor', 'rationale': '', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('C8', data={'ref': 'C8', 'x_mm': 30.5, 'y_mm': 8.5, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 1.52, 'courtyard_h_mm': 0.62, 'source': 'rp2040_usb_hid_anchor', 'rationale': '', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('C9', data={'ref': 'C9', 'x_mm': 28.0, 'y_mm': 8.5, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 1.52, 'courtyard_h_mm': 0.62, 'source': 'rp2040_usb_hid_anchor', 'rationale': '', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('D1', data={'ref': 'D1', 'x_mm': 15.5, 'y_mm': 15.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 3.6, 'courtyard_h_mm': 2.9, 'source': 'rp2040_usb_hid_anchor', 'rationale': '', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('J1', data={'ref': 'J1', 'x_mm': 3.1, 'y_mm': 15.0, 'rotation_deg': 270.0, 'side': 'top', 'courtyard_w_mm': 9.64, 'courtyard_h_mm': 7.93, 'source': 'rp2040_usb_hid_anchor', 'rationale': '', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': -0.29})
place('J2', data={'ref': 'J2', 'x_mm': 55.0, 'y_mm': 11.1, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 8.9, 'courtyard_h_mm': 20.36, 'source': 'rp2040_usb_hid_anchor', 'rationale': '', 'courtyard_offset_x_mm': 1.27, 'courtyard_offset_y_mm': 5.08})
place('R1', data={'ref': 'R1', 'x_mm': 20.0, 'y_mm': 13.5, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 2.45, 'courtyard_h_mm': 0.95, 'source': 'rp2040_usb_hid_anchor', 'rationale': '', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('R2', data={'ref': 'R2', 'x_mm': 20.0, 'y_mm': 16.5, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 2.45, 'courtyard_h_mm': 0.95, 'source': 'rp2040_usb_hid_anchor', 'rationale': '', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('R3', data={'ref': 'R3', 'x_mm': 36.0, 'y_mm': 20.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 2.45, 'courtyard_h_mm': 0.95, 'source': 'rp2040_usb_hid_anchor', 'rationale': '', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('R4', data={'ref': 'R4', 'x_mm': 43.0, 'y_mm': 13.5, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 2.45, 'courtyard_h_mm': 0.95, 'source': 'rp2040_usb_hid_anchor', 'rationale': '', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('R5', data={'ref': 'R5', 'x_mm': 11.0, 'y_mm': 8.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 2.45, 'courtyard_h_mm': 0.95, 'source': 'rp2040_usb_hid_anchor', 'rationale': '', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('R6', data={'ref': 'R6', 'x_mm': 11.0, 'y_mm': 22.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 2.45, 'courtyard_h_mm': 0.95, 'source': 'rp2040_usb_hid_anchor', 'rationale': '', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('U1', data={'ref': 'U1', 'x_mm': 15.5, 'y_mm': 24.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 3.6, 'courtyard_h_mm': 2.9, 'source': 'rp2040_usb_hid_anchor', 'rationale': '', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('U2', data={'ref': 'U2', 'x_mm': 30.0, 'y_mm': 15.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 7.75, 'courtyard_h_mm': 7.75, 'source': 'rp2040_usb_hid_anchor', 'rationale': '', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('U3', data={'ref': 'U3', 'x_mm': 43.0, 'y_mm': 8.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 8.8, 'courtyard_h_mm': 5.3, 'source': 'rp2040_usb_hid_anchor', 'rationale': '', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('X1', data={'ref': 'X1', 'x_mm': 40.0, 'y_mm': 20.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 3.6, 'courtyard_h_mm': 2.9, 'source': 'rp2040_usb_hid_anchor', 'rationale': '', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})

constraint(data={'kind': 'board_keepout', 'target_ref': None, 'params': {'width_mm': 65.0, 'height_mm': 30.0, 'edge_margin_mm': 0.5}, 'derived_from': 'mechanical.envelope + manufacturing.pcb.min_copper_edge_clearance_mm (KiCad default 0.5 mm)', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'mounting_hole_keepout', 'target_ref': None, 'params': {'x_mm': 2.5, 'y_mm': 2.5, 'keepout_radius_mm': 1.6}, 'derived_from': 'mechanical.mounting_holes[0] + mechanical.assembly_clearance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'mounting_hole_keepout', 'target_ref': None, 'params': {'x_mm': 62.5, 'y_mm': 2.5, 'keepout_radius_mm': 1.6}, 'derived_from': 'mechanical.mounting_holes[1] + mechanical.assembly_clearance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'mounting_hole_keepout', 'target_ref': None, 'params': {'x_mm': 2.5, 'y_mm': 27.5, 'keepout_radius_mm': 1.6}, 'derived_from': 'mechanical.mounting_holes[2] + mechanical.assembly_clearance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'mounting_hole_keepout', 'target_ref': None, 'params': {'x_mm': 62.5, 'y_mm': 27.5, 'keepout_radius_mm': 1.6}, 'derived_from': 'mechanical.mounting_holes[3] + mechanical.assembly_clearance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'connector_edge', 'target_ref': 'J1', 'params': {'side': 'left', 'max_edge_distance_mm': 10.0}, 'derived_from': 'mechanical.connector_interfaces + mechanical.max_connector_edge_distance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'decoupling_proximity', 'target_ref': 'C1', 'params': {'power_nets': ['GND', 'V3V3'], 'target_ref': 'U2', 'target_source': 'inferred_power_rail_consumer', 'max_distance_mm': 12.0}, 'derived_from': 'graph decoupling component pins + decoupling target inference', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'decoupling_proximity', 'target_ref': 'C2', 'params': {'power_nets': ['GND', 'V3V3'], 'target_ref': 'U2', 'target_source': 'inferred_power_rail_consumer', 'max_distance_mm': 12.0}, 'derived_from': 'graph decoupling component pins + decoupling target inference', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'decoupling_proximity', 'target_ref': 'C3', 'params': {'power_nets': ['GND', 'V3V3'], 'target_ref': 'U2', 'target_source': 'inferred_power_rail_consumer', 'max_distance_mm': 12.0}, 'derived_from': 'graph decoupling component pins + decoupling target inference', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'decoupling_proximity', 'target_ref': 'C4', 'params': {'power_nets': ['GND', 'V1V1'], 'target_ref': 'U2', 'target_source': 'inferred_power_rail_consumer', 'max_distance_mm': 12.0}, 'derived_from': 'graph decoupling component pins + decoupling target inference', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'decoupling_proximity', 'target_ref': 'C5', 'params': {'power_nets': ['GND', 'V3V3'], 'target_ref': 'U2', 'target_source': 'inferred_power_rail_consumer', 'max_distance_mm': 12.0}, 'derived_from': 'graph decoupling component pins + decoupling target inference', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'decoupling_proximity', 'target_ref': 'C6', 'params': {'power_nets': ['GND', 'V3V3'], 'target_ref': 'U2', 'target_source': 'inferred_power_rail_consumer', 'max_distance_mm': 12.0}, 'derived_from': 'graph decoupling component pins + decoupling target inference', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'decoupling_proximity', 'target_ref': 'C7', 'params': {'power_nets': ['GND', 'V3V3'], 'target_ref': 'U2', 'target_source': 'inferred_power_rail_consumer', 'max_distance_mm': 12.0}, 'derived_from': 'graph decoupling component pins + decoupling target inference', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'decoupling_proximity', 'target_ref': 'C8', 'params': {'power_nets': ['GND', 'V3V3'], 'target_ref': 'U2', 'target_source': 'inferred_power_rail_consumer', 'max_distance_mm': 12.0}, 'derived_from': 'graph decoupling component pins + decoupling target inference', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'decoupling_proximity', 'target_ref': 'C9', 'params': {'power_nets': ['GND', 'V3V3'], 'target_ref': 'U2', 'target_source': 'inferred_power_rail_consumer', 'max_distance_mm': 12.0}, 'derived_from': 'graph decoupling component pins + decoupling target inference', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'decoupling_proximity', 'target_ref': 'C10', 'params': {'power_nets': ['GND', 'V1V1'], 'target_ref': 'U2', 'target_source': 'inferred_power_rail_consumer', 'max_distance_mm': 12.0}, 'derived_from': 'graph decoupling component pins + decoupling target inference', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'decoupling_proximity', 'target_ref': 'C11', 'params': {'power_nets': ['GND', 'V3V3'], 'target_ref': 'U3', 'target_source': 'inferred_power_rail_consumer', 'max_distance_mm': 12.0}, 'derived_from': 'graph decoupling component pins + decoupling target inference', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'decoupling_proximity', 'target_ref': 'C12', 'params': {'power_nets': ['GND', 'V1V1'], 'target_ref': 'U2', 'target_source': 'inferred_power_rail_consumer', 'max_distance_mm': 12.0}, 'derived_from': 'graph decoupling component pins + decoupling target inference', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'decoupling_proximity', 'target_ref': 'C13', 'params': {'power_nets': ['GND', 'V3V3'], 'target_ref': 'U3', 'target_source': 'inferred_power_rail_consumer', 'max_distance_mm': 12.0}, 'derived_from': 'graph decoupling component pins + decoupling target inference', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'decoupling_proximity', 'target_ref': 'C14', 'params': {'power_nets': ['GND', 'USB_VBUS'], 'target_ref': 'D1', 'target_source': 'inferred_power_rail_consumer', 'max_distance_mm': 12.0}, 'derived_from': 'graph decoupling component pins + decoupling target inference', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'decoupling_proximity', 'target_ref': 'C15', 'params': {'power_nets': ['GND', 'USB_VBUS'], 'target_ref': 'U1', 'target_source': 'inferred_power_rail_consumer', 'max_distance_mm': 12.0}, 'derived_from': 'graph decoupling component pins + decoupling target inference', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'decoupling_proximity', 'target_ref': 'C16', 'params': {'power_nets': ['GND', 'V3V3'], 'target_ref': 'U2', 'target_source': 'inferred_power_rail_consumer', 'max_distance_mm': 12.0}, 'derived_from': 'graph decoupling component pins + decoupling target inference', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'thermal_spacing', 'target_ref': 'U1', 'params': {'min_spacing_mm': 8.0}, 'derived_from': 'graph power-category component', 'enforced': False, 'rationale': 'Advisory spacing only; thermal qualification requires load testing.'})

semantic_schematic = board.to_dict()
