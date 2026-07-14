"""Generated executable semantic schematic for agent review.

This file is intentionally compact and pin-name based. It can be executed
to reconstruct the normalized semantic_schematic model. Native EDA/CAD
artifacts are generated from typed artifacts; edit the spec or graph-producing
blocks when changing a generated design.
"""

from hw_codesign.semantic_schematic import SemanticBoard, pin

board = SemanticBoard(
    project='mini_biped_robot',
    revision='r1',
    purpose='LLM-suited schematic representation derived from typed graph; native EDA files are generated outputs.',
    source_graph='/Users/mrcha033/Documents/hw-cli/projects/mini_biped_robot/electronics/generated/electrical_graph.json',
    board_width_mm=50.0,
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
        pin('1', 'VCC', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin=None),
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
        pin('1', 'VCC', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'C20',
    role='bulk_cap',
    value='1000uF 10V LOW ESR',
    component_id='grm188_10u',
    mpn='GRM188R60J106ME47D',
    manufacturer='Murata',
    package='0603',
    footprint='Capacitor_SMD:C_0603_1608Metric',
    pin_contracts={'1': {'number': '1', 'name': 'VCC', 'electrical_type': 'passive'}, '2': {'number': '2', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}},
    pins=[
        pin('1', 'PLUS', net='V5', role='power_in', voltage_domain='V5', mcu_pin=None),
        pin('2', 'MINUS', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'C3',
    role='bulk_cap',
    value='10uF',
    component_id='grm188_10u',
    mpn='GRM188R60J106ME47D',
    manufacturer='Murata',
    package='0603',
    footprint='Capacitor_SMD:C_0603_1608Metric',
    pin_contracts={'1': {'number': '1', 'name': 'VCC', 'electrical_type': 'passive'}, '2': {'number': '2', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}},
    pins=[
        pin('1', 'VCC', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'C4',
    role='xtal_cap',
    value='12pF RTC XTAL',
    component_id='grm216_12p',
    mpn='GRM2165C1H120JA01D',
    manufacturer='Murata',
    package='0805',
    footprint='Capacitor_SMD:C_0805_2012Metric',
    pin_contracts={'1': {'number': '1', 'name': 'A', 'electrical_type': 'passive'}, '2': {'number': '2', 'name': 'B', 'electrical_type': 'passive'}},
    pins=[
        pin('1', 'A', net='XIN32', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'B', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'C5',
    role='xtal_cap',
    value='12pF RTC XTAL',
    component_id='grm216_12p',
    mpn='GRM2165C1H120JA01D',
    manufacturer='Murata',
    package='0805',
    footprint='Capacitor_SMD:C_0805_2012Metric',
    pin_contracts={'1': {'number': '1', 'name': 'A', 'electrical_type': 'passive'}, '2': {'number': '2', 'name': 'B', 'electrical_type': 'passive'}},
    pins=[
        pin('1', 'A', net='XOUT32', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'B', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'C6',
    role='capacitor_1uf',
    value='1uF VDDCORE',
    component_id='grm188_1uf',
    mpn='GRM188R61C105KA93D',
    manufacturer='Murata',
    package='0603',
    footprint='Capacitor_SMD:C_0603_1608Metric',
    pin_contracts={'1': {'number': '1', 'name': 'VCC', 'electrical_type': 'passive'}, '2': {'number': '2', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}},
    pins=[
        pin('1', 'VCC', net='VDDCORE', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'D1',
    role='tvs',
    value='USB ESD',
    component_id='usblc6_2sc6',
    mpn='USBLC6-2SC6',
    manufacturer='STMicroelectronics',
    package='SOT-23-6',
    footprint='Package_TO_SOT_SMD:SOT-23-6',
    pin_contracts={'1': {'number': '1', 'name': 'DP_IN', 'electrical_type': 'bidirectional'}, '2': {'number': '2', 'name': 'DP_OUT', 'electrical_type': 'bidirectional'}, '3': {'number': '3', 'name': 'DM_IN', 'electrical_type': 'bidirectional'}, '4': {'number': '4', 'name': 'DM_OUT', 'electrical_type': 'bidirectional'}, '5': {'number': '5', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}},
    pins=[
        pin('1', 'DP_IN', net='USB_DP_RAW', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('2', 'DP_OUT', net='USB_DP', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('3', 'DM_IN', net='USB_DM_RAW', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('4', 'DM_OUT', net='USB_DM', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('5', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('6', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'F20',
    role='fuse',
    value='10A SERVO FUSE',
    component_id=None,
    mpn='0451010.MRL',
    manufacturer='Littelfuse',
    package=None,
    footprint='Fuseholder_Blade_Mini',
    pin_contracts={},
    pins=[
        pin('1', 'IN', net='VBAT_RAW', role='power_in', voltage_domain='VBAT', mcu_pin=None),
        pin('2', 'OUT', net='VBAT_FUSED', role='bidirectional', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'J1',
    role='power_input',
    value='USB-C POWER',
    component_id='usb4105_gf_a',
    mpn='USB4105-GF-A',
    manufacturer='GCT',
    package='USB-C-16',
    footprint='Connector_USB:USB_C_GCT_USB4105',
    pin_contracts={'1': {'number': '1', 'name': 'VBUS', 'electrical_type': 'power_in', 'voltage_domain': 'USB_5V'}, '2': {'number': '2', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}, '3': {'number': '3', 'name': 'D+', 'electrical_type': 'bidirectional'}, '4': {'number': '4', 'name': 'D-', 'electrical_type': 'bidirectional'}, '5': {'number': '5', 'name': 'CC1', 'electrical_type': 'passive'}, '6': {'number': '6', 'name': 'CC2', 'electrical_type': 'passive'}},
    pins=[
        pin('1', 'VBUS', net='USB_VBUS', role='power_in', voltage_domain='USB_5V', mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('3', 'D+', net='USB_DP_RAW', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('4', 'D-', net='USB_DM_RAW', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('5', 'CC1', net='USB_CC1', role='passive', voltage_domain=None, mcu_pin=None),
        pin('6', 'CC2', net='USB_CC2', role='passive', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'J2',
    role='debug_header',
    value='SWD 10-pin',
    component_id='conn_2x05_2p54',
    mpn='61201021621',
    manufacturer='Würth Elektronik',
    package='PinHeader-2x5-2.54mm',
    footprint='Connector_PinHeader_2.54mm:PinHeader_2x05_P2.54mm_Vertical',
    pin_contracts={'1': {'number': '1', 'name': 'VCC', 'electrical_type': 'power_in'}, '2': {'number': '2', 'name': 'SWDIO', 'electrical_type': 'bidirectional'}, '3': {'number': '3', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}, '4': {'number': '4', 'name': 'SWDCLK', 'electrical_type': 'input'}, '5': {'number': '5', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}, '6': {'number': '6', 'name': 'SWO', 'electrical_type': 'output'}, '7': {'number': '7', 'name': 'KEY', 'electrical_type': 'no_connect'}, '8': {'number': '8', 'name': 'NC', 'electrical_type': 'no_connect'}, '9': {'number': '9', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}, '10': {'number': '10', 'name': 'RESET', 'electrical_type': 'input'}},
    pins=[
        pin('1', 'VCC', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin=None),
        pin('2', 'SWDIO', net='SWDIO', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('3', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('4', 'SWDCLK', net='SWCLK', role='input', voltage_domain=None, mcu_pin=None),
        pin('5', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('6', 'SWO', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('7', 'KEY', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('8', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('9', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('10', 'RESET', net='MCU_NRST', role='input', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'J20',
    role='battery_input',
    value='2S LIPO INPUT',
    component_id=None,
    mpn='XT30PW-M',
    manufacturer='AMASS',
    package=None,
    footprint='XT30PW_M',
    pin_contracts={},
    pins=[
        pin('1', 'VBAT', net='VBAT_RAW', role='power_in', voltage_domain='VBAT', mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'J21',
    role='servo_output',
    value='SERVO_1_3PIN',
    component_id=None,
    mpn='M20-9990345',
    manufacturer='Harwin',
    package=None,
    footprint='PinHeader_1x03_P2.54mm_Vertical',
    pin_contracts={},
    pins=[
        pin('1', 'SIGNAL', net='SERVO1_PWM', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('2', 'VPLUS', net='V5', role='power_in', voltage_domain='V5', mcu_pin=None),
        pin('3', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'J22',
    role='servo_output',
    value='SERVO_2_3PIN',
    component_id=None,
    mpn='M20-9990345',
    manufacturer='Harwin',
    package=None,
    footprint='PinHeader_1x03_P2.54mm_Vertical',
    pin_contracts={},
    pins=[
        pin('1', 'SIGNAL', net='SERVO2_PWM', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('2', 'VPLUS', net='V5', role='power_in', voltage_domain='V5', mcu_pin=None),
        pin('3', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'J23',
    role='servo_output',
    value='SERVO_3_3PIN',
    component_id=None,
    mpn='M20-9990345',
    manufacturer='Harwin',
    package=None,
    footprint='PinHeader_1x03_P2.54mm_Vertical',
    pin_contracts={},
    pins=[
        pin('1', 'SIGNAL', net='SERVO3_PWM', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('2', 'VPLUS', net='V5', role='power_in', voltage_domain='V5', mcu_pin=None),
        pin('3', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'J24',
    role='servo_output',
    value='SERVO_4_3PIN',
    component_id=None,
    mpn='M20-9990345',
    manufacturer='Harwin',
    package=None,
    footprint='PinHeader_1x03_P2.54mm_Vertical',
    pin_contracts={},
    pins=[
        pin('1', 'SIGNAL', net='SERVO4_PWM', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('2', 'VPLUS', net='V5', role='power_in', voltage_domain='V5', mcu_pin=None),
        pin('3', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'J25',
    role='servo_output',
    value='SERVO_5_3PIN',
    component_id=None,
    mpn='M20-9990345',
    manufacturer='Harwin',
    package=None,
    footprint='PinHeader_1x03_P2.54mm_Vertical',
    pin_contracts={},
    pins=[
        pin('1', 'SIGNAL', net='SERVO5_PWM', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('2', 'VPLUS', net='V5', role='power_in', voltage_domain='V5', mcu_pin=None),
        pin('3', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'J26',
    role='servo_output',
    value='SERVO_6_3PIN',
    component_id=None,
    mpn='M20-9990345',
    manufacturer='Harwin',
    package=None,
    footprint='PinHeader_1x03_P2.54mm_Vertical',
    pin_contracts={},
    pins=[
        pin('1', 'SIGNAL', net='SERVO6_PWM', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('2', 'VPLUS', net='V5', role='power_in', voltage_domain='V5', mcu_pin=None),
        pin('3', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'J27',
    role='estop',
    value='NC E-STOP LOOP',
    component_id=None,
    mpn='1935161',
    manufacturer='Phoenix Contact',
    package=None,
    footprint='TerminalBlock_1x03_P5.08mm',
    pin_contracts={},
    pins=[
        pin('1', 'VCC', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin=None),
        pin('2', 'ESTOP_OK', net='ESTOP_OK', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('3', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'R1',
    role='resistor_4k7',
    value='4K7 SCL PU',
    component_id='rc0603_4k7',
    mpn='RC0603FR-074K7L',
    manufacturer='Yageo',
    package='0603',
    footprint='Resistor_SMD:R_0603_1608Metric',
    pin_contracts={'1': {'number': '1', 'name': 'VCC', 'electrical_type': 'passive'}, '2': {'number': '2', 'name': 'SIGNAL', 'electrical_type': 'passive'}},
    pins=[
        pin('1', 'A', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin=None),
        pin('2', 'B', net='I2C_SCL', role='passive', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'R2',
    role='resistor_4k7',
    value='4K7 SDA PU',
    component_id='rc0603_4k7',
    mpn='RC0603FR-074K7L',
    manufacturer='Yageo',
    package='0603',
    footprint='Resistor_SMD:R_0603_1608Metric',
    pin_contracts={'1': {'number': '1', 'name': 'VCC', 'electrical_type': 'passive'}, '2': {'number': '2', 'name': 'SIGNAL', 'electrical_type': 'passive'}},
    pins=[
        pin('1', 'A', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin=None),
        pin('2', 'B', net='I2C_SDA', role='passive', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'R20',
    role='pulldown',
    value='10K E-STOP FAIL-SAFE PULLDOWN',
    component_id=None,
    mpn='RC0603FR-0710KL',
    manufacturer='Yageo',
    package=None,
    footprint='R0603',
    pin_contracts={},
    pins=[
        pin('1', 'A', net='ESTOP_OK', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('2', 'B', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'R3',
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
    'R4',
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
    value='SAMD21G18A',
    component_id='atsamd21g18a_au',
    mpn='ATSAMD21G18A-AU',
    manufacturer='Microchip Technology',
    package='TQFP-48',
    footprint='Package_QFP:TQFP-48_7x7mm_P0.5mm',
    pin_contracts={'1': {'number': '1', 'name': 'PA00_XIN32', 'electrical_type': 'bidirectional'}, '2': {'number': '2', 'name': 'PA01_XOUT32', 'electrical_type': 'bidirectional'}, '3': {'number': '3', 'name': 'PB08_ADC0_2_AIN2', 'electrical_type': 'bidirectional'}, '4': {'number': '4', 'name': 'PB09_ADC0_3_AIN3', 'electrical_type': 'bidirectional'}, '5': {'number': '5', 'name': 'PA04_SERCOM0_0', 'electrical_type': 'bidirectional'}, '6': {'number': '6', 'name': 'PA05_SERCOM0_1', 'electrical_type': 'bidirectional'}, '7': {'number': '7', 'name': 'PA06_SERCOM0_2', 'electrical_type': 'bidirectional'}, '8': {'number': '8', 'name': 'PA07_SERCOM0_3', 'electrical_type': 'bidirectional'}, '9': {'number': '9', 'name': 'VDDANA', 'electrical_type': 'power_in', 'voltage_domain': 'V3V3'}, '10': {'number': '10', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}, '11': {'number': '11', 'name': 'PB02_SERCOM5_0', 'electrical_type': 'bidirectional'}, '12': {'number': '12', 'name': 'PB03_SERCOM5_1', 'electrical_type': 'bidirectional'}, '13': {'number': '13', 'name': 'PA08_SERCOM2_0', 'electrical_type': 'bidirectional'}, '14': {'number': '14', 'name': 'PA09_SERCOM2_1', 'electrical_type': 'bidirectional'}, '15': {'number': '15', 'name': 'PA10_SERCOM2_2', 'electrical_type': 'bidirectional'}, '16': {'number': '16', 'name': 'PA11_SERCOM2_3', 'electrical_type': 'bidirectional'}, '17': {'number': '17', 'name': 'VDDIO', 'electrical_type': 'power_in', 'voltage_domain': 'V3V3'}, '18': {'number': '18', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}, '19': {'number': '19', 'name': 'PB10_SERCOM4_2', 'electrical_type': 'bidirectional'}, '20': {'number': '20', 'name': 'PB11_SERCOM4_3', 'electrical_type': 'bidirectional'}, '21': {'number': '21', 'name': 'PA12_SERCOM4_0', 'electrical_type': 'bidirectional'}, '22': {'number': '22', 'name': 'PA13_SERCOM4_1', 'electrical_type': 'bidirectional'}, '23': {'number': '23', 'name': 'PA14', 'electrical_type': 'bidirectional'}, '24': {'number': '24', 'name': 'PA15', 'electrical_type': 'bidirectional'}, '25': {'number': '25', 'name': 'PA16_SERCOM3_0', 'electrical_type': 'bidirectional'}, '26': {'number': '26', 'name': 'PA17_SERCOM3_1', 'electrical_type': 'bidirectional'}, '27': {'number': '27', 'name': 'PA18_SERCOM3_2', 'electrical_type': 'bidirectional'}, '28': {'number': '28', 'name': 'PA19_SERCOM3_3', 'electrical_type': 'bidirectional'}, '29': {'number': '29', 'name': 'PA20_SERCOM5_2', 'electrical_type': 'bidirectional'}, '30': {'number': '30', 'name': 'PA21_SERCOM5_3', 'electrical_type': 'bidirectional'}, '31': {'number': '31', 'name': 'PA22_SERCOM3_SDA', 'electrical_type': 'bidirectional'}, '32': {'number': '32', 'name': 'PA23_SERCOM3_SCL', 'electrical_type': 'bidirectional'}, '33': {'number': '33', 'name': 'PA24_USBDM', 'electrical_type': 'bidirectional'}, '34': {'number': '34', 'name': 'PA25_USBDP', 'electrical_type': 'bidirectional'}, '35': {'number': '35', 'name': 'VDDIO', 'electrical_type': 'power_in', 'voltage_domain': 'V3V3'}, '36': {'number': '36', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}, '37': {'number': '37', 'name': 'PB22_SERCOM5_2', 'electrical_type': 'bidirectional'}, '38': {'number': '38', 'name': 'PB23_SERCOM5_3', 'electrical_type': 'bidirectional'}, '39': {'number': '39', 'name': 'PA27', 'electrical_type': 'bidirectional'}, '40': {'number': '40', 'name': '~RESETN', 'electrical_type': 'input'}, '41': {'number': '41', 'name': 'PA28', 'electrical_type': 'bidirectional'}, '42': {'number': '42', 'name': 'VDDCORE', 'electrical_type': 'power_out'}, '43': {'number': '43', 'name': 'VDDIN', 'electrical_type': 'power_in', 'voltage_domain': 'V3V3'}, '44': {'number': '44', 'name': 'PB02_ADC', 'electrical_type': 'bidirectional'}, '45': {'number': '45', 'name': 'PB03_ADC', 'electrical_type': 'bidirectional'}, '46': {'number': '46', 'name': 'PA30_SWCLK', 'electrical_type': 'bidirectional'}, '47': {'number': '47', 'name': 'PA31_SWDIO', 'electrical_type': 'bidirectional'}, '48': {'number': '48', 'name': 'PB30', 'electrical_type': 'bidirectional'}},
    pins=[
        pin('1', 'PA00_XIN32', net='XIN32', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'PA01_XOUT32', net='XOUT32', role='passive', voltage_domain=None, mcu_pin=None),
        pin('9', 'VDDANA', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin=None),
        pin('10', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('17', 'VDDIO', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin=None),
        pin('18', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('27', 'PA18_SERCOM3_2', net='IMU_INT1', role='input', voltage_domain=None, mcu_pin=None),
        pin('31', 'PA22_SDA', net='I2C_SDA', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('32', 'PA23_SCL', net='I2C_SCL', role='input', voltage_domain=None, mcu_pin=None),
        pin('33', 'PA24_USBDM', net='USB_DM', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('34', 'PA25_USBDP', net='USB_DP', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('35', 'VDDIO', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin=None),
        pin('36', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('40', '~RESETN', net='MCU_NRST', role='input', voltage_domain=None, mcu_pin=None),
        pin('42', 'VDDCORE', net='VDDCORE', role='power_out', voltage_domain='V3V3', mcu_pin=None),
        pin('43', 'VDDIN', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin=None),
        pin('46', 'PA30_SWCLK', net='SWCLK', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('47', 'PA31_SWDIO', net='SWDIO', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('3', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('4', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('5', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('6', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('7', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('8', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('11', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('12', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('13', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('14', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('15', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('16', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('19', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('20', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('21', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('22', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('23', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('24', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('25', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('26', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('28', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('29', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('30', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('37', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('38', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('39', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('41', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('44', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('45', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('48', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'U20',
    role='external_buck_module',
    value='5V 9A STEP-DOWN MODULE',
    component_id=None,
    mpn='D24V90F5',
    manufacturer='Pololu',
    package=None,
    footprint='MODULE_POLOLU_D24V90F5',
    pin_contracts={},
    pins=[
        pin('1', 'VIN', net='VBAT_FUSED', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('3', 'VOUT', net='V5', role='power_in', voltage_domain='V5', mcu_pin=None),
        pin('4', 'EN', net='ESTOP_OK', role='bidirectional', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'U21',
    role='pwm_driver',
    value='16-CHANNEL I2C PWM',
    component_id=None,
    mpn='PCA9685PW',
    manufacturer='NXP',
    package=None,
    footprint='TSSOP-28_4.4x9.7mm_P0.65mm',
    pin_contracts={},
    pins=[
        pin('1', 'VCC', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('3', 'SCL', net='I2C_SCL', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('4', 'SDA', net='I2C_SDA', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('5', 'OE', net='SERVO_PWM_OE', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('6', 'LED0', net='SERVO1_PWM', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('7', 'LED1', net='SERVO2_PWM', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('8', 'LED2', net='SERVO3_PWM', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('9', 'LED3', net='SERVO4_PWM', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('10', 'LED4', net='SERVO5_PWM', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('11', 'LED5', net='SERVO6_PWM', role='bidirectional', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'U22',
    role='safety_gate',
    value='E-STOP PWM INVERTER',
    component_id=None,
    mpn='SN74LVC1G04DBVR',
    manufacturer='Texas Instruments',
    package=None,
    footprint='SOT-23-5',
    pin_contracts={},
    pins=[
        pin('1', 'VCC', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('3', 'A', net='ESTOP_OK', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('4', 'Y', net='SERVO_PWM_OE', role='bidirectional', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'U3',
    role='imu',
    value='LSM6DSOX',
    component_id='lsm6dsoxtr',
    mpn='LSM6DSOXTR',
    manufacturer='STMicroelectronics',
    package='LGA-14L',
    footprint='Package_LGA:LGA-14_3x2.5mm_P0.5mm',
    pin_contracts={'1': {'number': '1', 'name': 'SDO_SA0', 'electrical_type': 'bidirectional'}, '2': {'number': '2', 'name': 'SDX', 'electrical_type': 'bidirectional'}, '3': {'number': '3', 'name': 'SCX', 'electrical_type': 'input'}, '4': {'number': '4', 'name': 'INT1', 'electrical_type': 'output'}, '5': {'number': '5', 'name': 'INT2', 'electrical_type': 'output'}, '6': {'number': '6', 'name': 'VDD_IO', 'electrical_type': 'power_in'}, '7': {'number': '7', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}, '8': {'number': '8', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}, '9': {'number': '9', 'name': 'VDD', 'electrical_type': 'power_in'}, '10': {'number': '10', 'name': 'OCS_AUX', 'electrical_type': 'input'}, '11': {'number': '11', 'name': 'SDO_AUX', 'electrical_type': 'bidirectional'}, '12': {'number': '12', 'name': 'SDA_AUX', 'electrical_type': 'bidirectional'}, '13': {'number': '13', 'name': 'SCX_AUX', 'electrical_type': 'input'}, '14': {'number': '14', 'name': 'CS', 'electrical_type': 'input'}},
    pins=[
        pin('1', 'SDO_SA0', net='GND', role='input', voltage_domain=None, mcu_pin=None),
        pin('2', 'SDX', net='I2C_SDA', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('3', 'SCX', net='I2C_SCL', role='input', voltage_domain=None, mcu_pin=None),
        pin('4', 'INT1', net='IMU_INT1', role='output', voltage_domain=None, mcu_pin=None),
        pin('5', 'INT2', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('6', 'VDD_IO', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin=None),
        pin('7', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('8', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('9', 'VDD', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin=None),
        pin('14', 'CS', net='V3V3', role='input', voltage_domain=None, mcu_pin=None),
        pin('10', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('11', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('12', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
        pin('13', 'NC', net=None, role='no_connect', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'U4',
    role='env_sensor',
    value='BME280',
    component_id='bme280',
    mpn='BME280',
    manufacturer='Bosch Sensortec',
    package='LGA-8',
    footprint='Package_LGA:Bosch_LGA-8_2.5x2.5mm_P0.65mm',
    pin_contracts={'1': {'number': '1', 'name': 'VDD', 'electrical_type': 'power_in', 'voltage_domain': 'V3V3'}, '2': {'number': '2', 'name': 'VDDIO', 'electrical_type': 'power_in', 'voltage_domain': 'V3V3'}, '3': {'number': '3', 'name': 'GND', 'electrical_type': 'ground', 'voltage_domain': 'GND'}, '4': {'number': '4', 'name': 'SDI_SDA', 'electrical_type': 'open_drain'}, '5': {'number': '5', 'name': 'SCK_SCL', 'electrical_type': 'open_drain'}, '6': {'number': '6', 'name': 'SDO_ADDR', 'electrical_type': 'input'}, '7': {'number': '7', 'name': 'CSB', 'electrical_type': 'input'}, '8': {'number': '8', 'name': 'GND2', 'electrical_type': 'ground', 'voltage_domain': 'GND'}},
    pins=[
        pin('1', 'VDD', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin=None),
        pin('2', 'VDDIO', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin=None),
        pin('3', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('4', 'SDI_SDA', net='I2C_SDA', role='open_drain', voltage_domain=None, mcu_pin=None),
        pin('5', 'SCK_SCL', net='I2C_SCL', role='open_drain', voltage_domain=None, mcu_pin=None),
        pin('6', 'SDO_ADDR', net='GND', role='input', voltage_domain=None, mcu_pin=None),
        pin('7', 'CSB', net='V3V3', role='input', voltage_domain=None, mcu_pin=None),
        pin('8', 'GND2', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'X1',
    role='rtc_crystal',
    value='32.768kHz XTAL',
    component_id='mc_306_32khz',
    mpn='MC-306 32.768KHZ',
    manufacturer='Epson',
    package='SMD-2Pin-Crystal',
    footprint='Crystal:Crystal_SMD_Epson_MC-306_3.2x1.5mm',
    pin_contracts={'1': {'number': '1', 'name': 'XIN', 'electrical_type': 'passive'}, '2': {'number': '2', 'name': 'XOUT', 'electrical_type': 'passive'}},
    pins=[
        pin('1', 'XIN32', net='XIN32', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'XOUT32', net='XOUT32', role='passive', voltage_domain=None, mcu_pin=None),
    ],
)


net('ESTOP_OK', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J27', pin='ESTOP_OK', number='2', net='ESTOP_OK', role='bidirectional', mcu_pin=None)
connect('R20', pin='A', number='1', net='ESTOP_OK', role='bidirectional', mcu_pin=None)
connect('U20', pin='EN', number='4', net='ESTOP_OK', role='bidirectional', mcu_pin=None)
connect('U22', pin='A', number='3', net='ESTOP_OK', role='bidirectional', mcu_pin=None)

net('GND', signal_class='ground', voltage_domain='GND', required_track_width_mm=0.2)
connect('C1', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('C2', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('C20', pin='MINUS', number='2', net='GND', role='ground', mcu_pin=None)
connect('C3', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('C4', pin='B', number='2', net='GND', role='ground', mcu_pin=None)
connect('C5', pin='B', number='2', net='GND', role='ground', mcu_pin=None)
connect('C6', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('D1', pin='GND', number='5', net='GND', role='ground', mcu_pin=None)
connect('J1', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('J2', pin='GND', number='3', net='GND', role='ground', mcu_pin=None)
connect('J2', pin='GND', number='5', net='GND', role='ground', mcu_pin=None)
connect('J2', pin='GND', number='9', net='GND', role='ground', mcu_pin=None)
connect('J20', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('J21', pin='GND', number='3', net='GND', role='ground', mcu_pin=None)
connect('J22', pin='GND', number='3', net='GND', role='ground', mcu_pin=None)
connect('J23', pin='GND', number='3', net='GND', role='ground', mcu_pin=None)
connect('J24', pin='GND', number='3', net='GND', role='ground', mcu_pin=None)
connect('J25', pin='GND', number='3', net='GND', role='ground', mcu_pin=None)
connect('J26', pin='GND', number='3', net='GND', role='ground', mcu_pin=None)
connect('J27', pin='GND', number='3', net='GND', role='ground', mcu_pin=None)
connect('R20', pin='B', number='2', net='GND', role='ground', mcu_pin=None)
connect('R3', pin='B', number='2', net='GND', role='ground', mcu_pin=None)
connect('R4', pin='B', number='2', net='GND', role='ground', mcu_pin=None)
connect('U1', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('U2', pin='GND', number='10', net='GND', role='ground', mcu_pin=None)
connect('U2', pin='GND', number='18', net='GND', role='ground', mcu_pin=None)
connect('U2', pin='GND', number='36', net='GND', role='ground', mcu_pin=None)
connect('U20', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('U21', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('U22', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('U3', pin='SDO_SA0', number='1', net='GND', role='input', mcu_pin=None)
connect('U3', pin='GND', number='7', net='GND', role='ground', mcu_pin=None)
connect('U3', pin='GND', number='8', net='GND', role='ground', mcu_pin=None)
connect('U4', pin='GND', number='3', net='GND', role='ground', mcu_pin=None)
connect('U4', pin='SDO_ADDR', number='6', net='GND', role='input', mcu_pin=None)
connect('U4', pin='GND2', number='8', net='GND', role='ground', mcu_pin=None)

net('I2C_SCL', signal_class='i2c', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('R1', pin='B', number='2', net='I2C_SCL', role='passive', mcu_pin=None)
connect('U2', pin='PA23_SCL', number='32', net='I2C_SCL', role='input', mcu_pin=None)
connect('U21', pin='SCL', number='3', net='I2C_SCL', role='bidirectional', mcu_pin=None)
connect('U3', pin='SCX', number='3', net='I2C_SCL', role='input', mcu_pin=None)
connect('U4', pin='SCK_SCL', number='5', net='I2C_SCL', role='open_drain', mcu_pin=None)

net('I2C_SDA', signal_class='i2c', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('R2', pin='B', number='2', net='I2C_SDA', role='passive', mcu_pin=None)
connect('U2', pin='PA22_SDA', number='31', net='I2C_SDA', role='bidirectional', mcu_pin=None)
connect('U21', pin='SDA', number='4', net='I2C_SDA', role='bidirectional', mcu_pin=None)
connect('U3', pin='SDX', number='2', net='I2C_SDA', role='bidirectional', mcu_pin=None)
connect('U4', pin='SDI_SDA', number='4', net='I2C_SDA', role='open_drain', mcu_pin=None)

net('IMU_INT1', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('U2', pin='PA18_SERCOM3_2', number='27', net='IMU_INT1', role='input', mcu_pin=None)
connect('U3', pin='INT1', number='4', net='IMU_INT1', role='output', mcu_pin=None)

net('MCU_NRST', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J2', pin='RESET', number='10', net='MCU_NRST', role='input', mcu_pin=None)
connect('U2', pin='~RESETN', number='40', net='MCU_NRST', role='input', mcu_pin=None)

net('SERVO1_PWM', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J21', pin='SIGNAL', number='1', net='SERVO1_PWM', role='bidirectional', mcu_pin=None)
connect('U21', pin='LED0', number='6', net='SERVO1_PWM', role='bidirectional', mcu_pin=None)

net('SERVO2_PWM', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J22', pin='SIGNAL', number='1', net='SERVO2_PWM', role='bidirectional', mcu_pin=None)
connect('U21', pin='LED1', number='7', net='SERVO2_PWM', role='bidirectional', mcu_pin=None)

net('SERVO3_PWM', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J23', pin='SIGNAL', number='1', net='SERVO3_PWM', role='bidirectional', mcu_pin=None)
connect('U21', pin='LED2', number='8', net='SERVO3_PWM', role='bidirectional', mcu_pin=None)

net('SERVO4_PWM', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J24', pin='SIGNAL', number='1', net='SERVO4_PWM', role='bidirectional', mcu_pin=None)
connect('U21', pin='LED3', number='9', net='SERVO4_PWM', role='bidirectional', mcu_pin=None)

net('SERVO5_PWM', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J25', pin='SIGNAL', number='1', net='SERVO5_PWM', role='bidirectional', mcu_pin=None)
connect('U21', pin='LED4', number='10', net='SERVO5_PWM', role='bidirectional', mcu_pin=None)

net('SERVO6_PWM', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J26', pin='SIGNAL', number='1', net='SERVO6_PWM', role='bidirectional', mcu_pin=None)
connect('U21', pin='LED5', number='11', net='SERVO6_PWM', role='bidirectional', mcu_pin=None)

net('SERVO_PWM_OE', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('U21', pin='OE', number='5', net='SERVO_PWM_OE', role='bidirectional', mcu_pin=None)
connect('U22', pin='Y', number='4', net='SERVO_PWM_OE', role='bidirectional', mcu_pin=None)

net('SWCLK', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J2', pin='SWDCLK', number='4', net='SWCLK', role='input', mcu_pin=None)
connect('U2', pin='PA30_SWCLK', number='46', net='SWCLK', role='bidirectional', mcu_pin=None)

net('SWDIO', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J2', pin='SWDIO', number='2', net='SWDIO', role='bidirectional', mcu_pin=None)
connect('U2', pin='PA31_SWDIO', number='47', net='SWDIO', role='bidirectional', mcu_pin=None)

net('USB_CC1', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J1', pin='CC1', number='5', net='USB_CC1', role='passive', mcu_pin=None)
connect('R3', pin='A', number='1', net='USB_CC1', role='passive', mcu_pin=None)

net('USB_CC2', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J1', pin='CC2', number='6', net='USB_CC2', role='passive', mcu_pin=None)
connect('R4', pin='A', number='1', net='USB_CC2', role='passive', mcu_pin=None)

net('USB_DM', signal_class='usb', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('D1', pin='DM_OUT', number='4', net='USB_DM', role='bidirectional', mcu_pin=None)
connect('U2', pin='PA24_USBDM', number='33', net='USB_DM', role='bidirectional', mcu_pin=None)

net('USB_DM_RAW', signal_class='usb', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('D1', pin='DM_IN', number='3', net='USB_DM_RAW', role='bidirectional', mcu_pin=None)
connect('J1', pin='D-', number='4', net='USB_DM_RAW', role='bidirectional', mcu_pin=None)

net('USB_DP', signal_class='usb', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('D1', pin='DP_OUT', number='2', net='USB_DP', role='bidirectional', mcu_pin=None)
connect('U2', pin='PA25_USBDP', number='34', net='USB_DP', role='bidirectional', mcu_pin=None)

net('USB_DP_RAW', signal_class='usb', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('D1', pin='DP_IN', number='1', net='USB_DP_RAW', role='bidirectional', mcu_pin=None)
connect('J1', pin='D+', number='3', net='USB_DP_RAW', role='bidirectional', mcu_pin=None)

net('USB_VBUS', signal_class='power', voltage_domain='USB_5V', required_track_width_mm=0.5)
connect('J1', pin='VBUS', number='1', net='USB_VBUS', role='power_in', mcu_pin=None)
connect('U1', pin='EN', number='1', net='USB_VBUS', role='input', mcu_pin=None)
connect('U1', pin='VIN', number='3', net='USB_VBUS', role='power_in', mcu_pin=None)

net('V3V3', signal_class='power', voltage_domain='V3V3', required_track_width_mm=0.5)
connect('C1', pin='VCC', number='1', net='V3V3', role='power_in', mcu_pin=None)
connect('C2', pin='VCC', number='1', net='V3V3', role='power_in', mcu_pin=None)
connect('C3', pin='VCC', number='1', net='V3V3', role='power_in', mcu_pin=None)
connect('J2', pin='VCC', number='1', net='V3V3', role='power_in', mcu_pin=None)
connect('J27', pin='VCC', number='1', net='V3V3', role='power_in', mcu_pin=None)
connect('R1', pin='A', number='1', net='V3V3', role='power_in', mcu_pin=None)
connect('R2', pin='A', number='1', net='V3V3', role='power_in', mcu_pin=None)
connect('U1', pin='VOUT', number='5', net='V3V3', role='power_out', mcu_pin=None)
connect('U2', pin='VDDIO', number='17', net='V3V3', role='power_in', mcu_pin=None)
connect('U2', pin='VDDIO', number='35', net='V3V3', role='power_in', mcu_pin=None)
connect('U2', pin='VDDIN', number='43', net='V3V3', role='power_in', mcu_pin=None)
connect('U2', pin='VDDANA', number='9', net='V3V3', role='power_in', mcu_pin=None)
connect('U21', pin='VCC', number='1', net='V3V3', role='power_in', mcu_pin=None)
connect('U22', pin='VCC', number='1', net='V3V3', role='power_in', mcu_pin=None)
connect('U3', pin='CS', number='14', net='V3V3', role='input', mcu_pin=None)
connect('U3', pin='VDD_IO', number='6', net='V3V3', role='power_in', mcu_pin=None)
connect('U3', pin='VDD', number='9', net='V3V3', role='power_in', mcu_pin=None)
connect('U4', pin='VDD', number='1', net='V3V3', role='power_in', mcu_pin=None)
connect('U4', pin='VDDIO', number='2', net='V3V3', role='power_in', mcu_pin=None)
connect('U4', pin='CSB', number='7', net='V3V3', role='input', mcu_pin=None)

net('V5', signal_class='power', voltage_domain='V5', required_track_width_mm=0.5)
connect('C20', pin='PLUS', number='1', net='V5', role='power_in', mcu_pin=None)
connect('J21', pin='VPLUS', number='2', net='V5', role='power_in', mcu_pin=None)
connect('J22', pin='VPLUS', number='2', net='V5', role='power_in', mcu_pin=None)
connect('J23', pin='VPLUS', number='2', net='V5', role='power_in', mcu_pin=None)
connect('J24', pin='VPLUS', number='2', net='V5', role='power_in', mcu_pin=None)
connect('J25', pin='VPLUS', number='2', net='V5', role='power_in', mcu_pin=None)
connect('J26', pin='VPLUS', number='2', net='V5', role='power_in', mcu_pin=None)
connect('U20', pin='VOUT', number='3', net='V5', role='power_in', mcu_pin=None)

net('VBAT_FUSED', signal_class='power', voltage_domain='VBAT', required_track_width_mm=2.0)
connect('F20', pin='OUT', number='2', net='VBAT_FUSED', role='bidirectional', mcu_pin=None)
connect('U20', pin='VIN', number='1', net='VBAT_FUSED', role='bidirectional', mcu_pin=None)

net('VBAT_RAW', signal_class='power', voltage_domain='VBAT', required_track_width_mm=2.0)
connect('F20', pin='IN', number='1', net='VBAT_RAW', role='power_in', mcu_pin=None)
connect('J20', pin='VBAT', number='1', net='VBAT_RAW', role='power_in', mcu_pin=None)

net('VDDCORE', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('C6', pin='VCC', number='1', net='VDDCORE', role='passive', mcu_pin=None)
connect('U2', pin='VDDCORE', number='42', net='VDDCORE', role='power_out', mcu_pin=None)

net('XIN32', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('C4', pin='A', number='1', net='XIN32', role='passive', mcu_pin=None)
connect('U2', pin='PA00_XIN32', number='1', net='XIN32', role='passive', mcu_pin=None)
connect('X1', pin='XIN32', number='1', net='XIN32', role='passive', mcu_pin=None)

net('XOUT32', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('C5', pin='A', number='1', net='XOUT32', role='passive', mcu_pin=None)
connect('U2', pin='PA01_XOUT32', number='2', net='XOUT32', role='passive', mcu_pin=None)
connect('X1', pin='XOUT32', number='2', net='XOUT32', role='passive', mcu_pin=None)


place('C1', data={'ref': 'C1', 'x_mm': 20.0, 'y_mm': 14.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 1.7, 'courtyard_h_mm': 0.7, 'source': 'samd21_sensor_hub_anchor', 'rationale': 'Board-family anchor for the SAMD21 USB sensor hub layout contract.', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('C2', data={'ref': 'C2', 'x_mm': 34.0, 'y_mm': 16.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 1.7, 'courtyard_h_mm': 0.7, 'source': 'samd21_sensor_hub_anchor', 'rationale': 'Board-family anchor for the SAMD21 USB sensor hub layout contract.', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('C20', data={'ref': 'C20', 'x_mm': 42.35, 'y_mm': 11.6, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 1.7, 'courtyard_h_mm': 0.8, 'source': 'shelf_pack_seed', 'rationale': 'Footprint-aware shelf pack; no curated anchor for this reference.', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('C3', data={'ref': 'C3', 'x_mm': 34.0, 'y_mm': 5.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 1.7, 'courtyard_h_mm': 0.8, 'source': 'samd21_sensor_hub_anchor', 'rationale': 'Board-family anchor for the SAMD21 USB sensor hub layout contract.', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('C4', data={'ref': 'C4', 'x_mm': 21.0, 'y_mm': 17.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 2.0, 'courtyard_h_mm': 1.2, 'source': 'samd21_sensor_hub_anchor', 'rationale': 'Board-family anchor for the SAMD21 USB sensor hub layout contract.', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('C5', data={'ref': 'C5', 'x_mm': 21.0, 'y_mm': 23.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 2.0, 'courtyard_h_mm': 1.2, 'source': 'samd21_sensor_hub_anchor', 'rationale': 'Board-family anchor for the SAMD21 USB sensor hub layout contract.', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('C6', data={'ref': 'C6', 'x_mm': 18.0, 'y_mm': 24.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 1.7, 'courtyard_h_mm': 0.8, 'source': 'samd21_sensor_hub_anchor', 'rationale': 'Board-family anchor for the SAMD21 USB sensor hub layout contract.', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('D1', data={'ref': 'D1', 'x_mm': 18.0, 'y_mm': 3.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 3.189, 'courtyard_h_mm': 1.939, 'source': 'samd21_sensor_hub_anchor', 'rationale': 'Board-family anchor for the SAMD21 USB sensor hub layout contract.', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('F20', data={'ref': 'F20', 'x_mm': 33.0, 'y_mm': 12.7, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 3.0, 'courtyard_h_mm': 3.0, 'source': 'solver_agent_adjacent_to', 'rationale': 'Cost solver satisfied adjacent_to relation with J20.', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('J1', data={'ref': 'J1', 'x_mm': 12.0, 'y_mm': 3.769, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 9.189, 'courtyard_h_mm': 7.444, 'source': 'samd21_sensor_hub_anchor', 'rationale': 'Board-family anchor for the SAMD21 USB sensor hub layout contract.', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': -0.047})
place('J2', data={'ref': 'J2', 'x_mm': 47.0, 'y_mm': 21.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 5.08, 'courtyard_h_mm': 12.7, 'source': 'samd21_sensor_hub_anchor', 'rationale': 'Board-family anchor for the SAMD21 USB sensor hub layout contract.', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('J20', data={'ref': 'J20', 'x_mm': 29.5, 'y_mm': 12.7, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 3.0, 'courtyard_h_mm': 3.0, 'source': 'shelf_pack_seed', 'rationale': 'Footprint-aware shelf pack; no curated anchor for this reference.', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('J21', data={'ref': 'J21', 'x_mm': 29.5, 'y_mm': 9.2, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 2.54, 'courtyard_h_mm': 7.62, 'source': 'solver_agent_adjacent_to', 'rationale': 'Cost solver satisfied adjacent_to relation with J20.', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('J22', data={'ref': 'J22', 'x_mm': 26.5, 'y_mm': 12.7, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 2.54, 'courtyard_h_mm': 7.62, 'source': 'agent_constraint_thermal_separation', 'rationale': 'Position derived from thermal_separation constraint relative to J21.', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('J23', data={'ref': 'J23', 'x_mm': 31.5, 'y_mm': 12.7, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 2.54, 'courtyard_h_mm': 7.62, 'source': 'agent_constraint_thermal_separation', 'rationale': 'Position derived from thermal_separation constraint relative to J22.', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('J24', data={'ref': 'J24', 'x_mm': 34.5, 'y_mm': 9.2, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 2.54, 'courtyard_h_mm': 7.62, 'source': 'solver_agent_thermal_separation', 'rationale': 'Cost solver separated J24 from thermal target J21.', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('J25', data={'ref': 'J25', 'x_mm': 39.5, 'y_mm': 9.2, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 2.54, 'courtyard_h_mm': 7.62, 'source': 'solver_agent_thermal_separation', 'rationale': 'Cost solver separated J25 from thermal target J24.', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('J26', data={'ref': 'J26', 'x_mm': 46.5, 'y_mm': 12.7, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 2.54, 'courtyard_h_mm': 7.62, 'source': 'agent_constraint_thermal_separation', 'rationale': 'Position derived from thermal_separation constraint relative to J25.', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('J27', data={'ref': 'J27', 'x_mm': 10.028, 'y_mm': 12.85, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 3.3, 'courtyard_h_mm': 3.15, 'source': 'shelf_pack_seed', 'rationale': 'Footprint-aware shelf pack; no curated anchor for this reference.', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': -0.075})
place('R1', data={'ref': 'R1', 'x_mm': 29.0, 'y_mm': 22.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 1.7, 'courtyard_h_mm': 0.8, 'source': 'samd21_sensor_hub_anchor', 'rationale': 'Board-family anchor for the SAMD21 USB sensor hub layout contract.', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('R2', data={'ref': 'R2', 'x_mm': 29.0, 'y_mm': 26.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 1.7, 'courtyard_h_mm': 0.8, 'source': 'samd21_sensor_hub_anchor', 'rationale': 'Board-family anchor for the SAMD21 USB sensor hub layout contract.', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('R20', data={'ref': 'R20', 'x_mm': 39.5, 'y_mm': 12.7, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 3.0, 'courtyard_h_mm': 3.0, 'source': 'shelf_pack_seed', 'rationale': 'Footprint-aware shelf pack; no curated anchor for this reference.', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('R3', data={'ref': 'R3', 'x_mm': 16.0, 'y_mm': 6.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 1.7, 'courtyard_h_mm': 0.8, 'source': 'usb_c_rd_connector_seed', 'rationale': 'USB-C Rd resistor position derived from the connector CC pins.', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('R4', data={'ref': 'R4', 'x_mm': 20.0, 'y_mm': 6.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 1.7, 'courtyard_h_mm': 0.8, 'source': 'usb_c_rd_connector_seed', 'rationale': 'USB-C Rd resistor position derived from the connector CC pins.', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('U1', data={'ref': 'U1', 'x_mm': 28.0, 'y_mm': 5.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 3.189, 'courtyard_h_mm': 1.939, 'source': 'samd21_sensor_hub_anchor', 'rationale': 'Board-family anchor for the SAMD21 USB sensor hub layout contract.', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('U2', data={'ref': 'U2', 'x_mm': 24.0, 'y_mm': 17.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 7.0, 'courtyard_h_mm': 7.0, 'source': 'samd21_sensor_hub_anchor', 'rationale': 'Board-family anchor for the SAMD21 USB sensor hub layout contract.', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('U20', data={'ref': 'U20', 'x_mm': 23.0, 'y_mm': 12.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 3.189, 'courtyard_h_mm': 3.189, 'source': 'agent_constraint_thermal_separation', 'rationale': 'Position derived from thermal_separation constraint relative to U3.', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('U21', data={'ref': 'U21', 'x_mm': 34.0, 'y_mm': 22.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 4.4, 'courtyard_h_mm': 9.7, 'source': 'agent_constraint_adjacent_to', 'rationale': 'Position derived from adjacent_to constraint relative to R1.', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('U22', data={'ref': 'U22', 'x_mm': 13.528, 'y_mm': 12.85, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 3.189, 'courtyard_h_mm': 3.189, 'source': 'agent_constraint_adjacent_to', 'rationale': 'Position derived from adjacent_to constraint relative to J27.', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('U3', data={'ref': 'U3', 'x_mm': 36.0, 'y_mm': 12.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 3.0, 'courtyard_h_mm': 2.5, 'source': 'samd21_sensor_hub_anchor', 'rationale': 'Board-family anchor for the SAMD21 USB sensor hub layout contract.', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('U4', data={'ref': 'U4', 'x_mm': 36.0, 'y_mm': 21.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 2.5, 'courtyard_h_mm': 2.5, 'source': 'samd21_sensor_hub_anchor', 'rationale': 'Board-family anchor for the SAMD21 USB sensor hub layout contract.', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})
place('X1', data={'ref': 'X1', 'x_mm': 18.0, 'y_mm': 20.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 3.2, 'courtyard_h_mm': 1.5, 'source': 'samd21_sensor_hub_anchor', 'rationale': 'Board-family anchor for the SAMD21 USB sensor hub layout contract.', 'courtyard_offset_x_mm': 0.0, 'courtyard_offset_y_mm': 0.0})

constraint(data={'kind': 'board_keepout', 'target_ref': None, 'params': {'width_mm': 50.0, 'height_mm': 30.0, 'edge_margin_mm': 0.15}, 'derived_from': 'mechanical.envelope + manufacturing.pcb.min_clearance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'mounting_hole_keepout', 'target_ref': None, 'params': {'x_mm': 2.5, 'y_mm': 2.5, 'keepout_radius_mm': 1.7}, 'derived_from': 'mechanical.mounting_holes[0] + mechanical.assembly_clearance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'mounting_hole_keepout', 'target_ref': None, 'params': {'x_mm': 47.5, 'y_mm': 2.5, 'keepout_radius_mm': 1.7}, 'derived_from': 'mechanical.mounting_holes[1] + mechanical.assembly_clearance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'mounting_hole_keepout', 'target_ref': None, 'params': {'x_mm': 2.5, 'y_mm': 27.5, 'keepout_radius_mm': 1.7}, 'derived_from': 'mechanical.mounting_holes[2] + mechanical.assembly_clearance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'mounting_hole_keepout', 'target_ref': None, 'params': {'x_mm': 37.5, 'y_mm': 27.5, 'keepout_radius_mm': 1.7}, 'derived_from': 'mechanical.mounting_holes[3] + mechanical.assembly_clearance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'connector_edge', 'target_ref': 'J1', 'params': {'side': 'front', 'max_edge_distance_mm': 6.0}, 'derived_from': 'mechanical.connector_interfaces + mechanical.max_connector_edge_distance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'connector_edge', 'target_ref': 'J2', 'params': {'side': 'right', 'max_edge_distance_mm': 6.0}, 'derived_from': 'mechanical.connector_interfaces + mechanical.max_connector_edge_distance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'decoupling_proximity', 'target_ref': 'C1', 'params': {'power_nets': ['GND', 'V3V3'], 'target_ref': 'U2', 'target_source': 'inferred_power_rail_consumer', 'max_distance_mm': 12.0}, 'derived_from': 'graph decoupling component pins + decoupling target inference', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'decoupling_proximity', 'target_ref': 'C2', 'params': {'power_nets': ['GND', 'V3V3'], 'target_ref': 'U3', 'target_source': 'inferred_power_rail_consumer', 'max_distance_mm': 12.0}, 'derived_from': 'graph decoupling component pins + decoupling target inference', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'thermal_spacing', 'target_ref': 'U1', 'params': {'min_spacing_mm': 8.0}, 'derived_from': 'graph power-category component', 'enforced': False, 'rationale': 'Advisory spacing only; thermal qualification requires load testing.'})
constraint(data={'kind': 'thermal_spacing', 'target_ref': 'U22', 'params': {'min_spacing_mm': 8.0}, 'derived_from': 'graph power-category component', 'enforced': False, 'rationale': 'Advisory spacing only; thermal qualification requires load testing.'})
constraint(data={'kind': 'agent_adjacent_to', 'target_ref': 'F20', 'params': {'relationship': 'adjacent_to', 'target': 'J20', 'max_distance_mm': 5.0}, 'derived_from': 'spec.placement.constraints', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'agent_thermal_separation', 'target_ref': 'U20', 'params': {'relationship': 'thermal_separation', 'target': 'U3', 'min_distance_mm': 12.0}, 'derived_from': 'spec.placement.constraints', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'agent_adjacent_to', 'target_ref': 'U21', 'params': {'relationship': 'adjacent_to', 'target': 'R1', 'max_distance_mm': 8.0}, 'derived_from': 'spec.placement.constraints', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'agent_adjacent_to', 'target_ref': 'U22', 'params': {'relationship': 'adjacent_to', 'target': 'J27', 'max_distance_mm': 5.0}, 'derived_from': 'spec.placement.constraints', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'agent_near_connector', 'target_ref': 'J21', 'params': {'relationship': 'near_connector', 'target': 'J20', 'side': 'same_half'}, 'derived_from': 'spec.placement.constraints', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'agent_near_connector', 'target_ref': 'J22', 'params': {'relationship': 'near_connector', 'target': 'J20', 'side': 'same_half'}, 'derived_from': 'spec.placement.constraints', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'agent_near_connector', 'target_ref': 'J23', 'params': {'relationship': 'near_connector', 'target': 'J20', 'side': 'same_half'}, 'derived_from': 'spec.placement.constraints', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'agent_near_connector', 'target_ref': 'J24', 'params': {'relationship': 'near_connector', 'target': 'J20', 'side': 'same_half'}, 'derived_from': 'spec.placement.constraints', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'agent_near_connector', 'target_ref': 'J25', 'params': {'relationship': 'near_connector', 'target': 'J20', 'side': 'same_half'}, 'derived_from': 'spec.placement.constraints', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'agent_near_connector', 'target_ref': 'J26', 'params': {'relationship': 'near_connector', 'target': 'J20', 'side': 'same_half'}, 'derived_from': 'spec.placement.constraints', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'agent_thermal_separation', 'target_ref': 'J22', 'params': {'relationship': 'thermal_separation', 'target': 'J21', 'min_distance_mm': 4.0}, 'derived_from': 'spec.placement.constraints', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'agent_thermal_separation', 'target_ref': 'J23', 'params': {'relationship': 'thermal_separation', 'target': 'J21', 'min_distance_mm': 4.0}, 'derived_from': 'spec.placement.constraints', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'agent_thermal_separation', 'target_ref': 'J24', 'params': {'relationship': 'thermal_separation', 'target': 'J21', 'min_distance_mm': 4.0}, 'derived_from': 'spec.placement.constraints', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'agent_thermal_separation', 'target_ref': 'J25', 'params': {'relationship': 'thermal_separation', 'target': 'J21', 'min_distance_mm': 4.0}, 'derived_from': 'spec.placement.constraints', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'agent_thermal_separation', 'target_ref': 'J26', 'params': {'relationship': 'thermal_separation', 'target': 'J21', 'min_distance_mm': 4.0}, 'derived_from': 'spec.placement.constraints', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'agent_thermal_separation', 'target_ref': 'J23', 'params': {'relationship': 'thermal_separation', 'target': 'J22', 'min_distance_mm': 4.0}, 'derived_from': 'spec.placement.constraints', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'agent_thermal_separation', 'target_ref': 'J24', 'params': {'relationship': 'thermal_separation', 'target': 'J22', 'min_distance_mm': 4.0}, 'derived_from': 'spec.placement.constraints', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'agent_thermal_separation', 'target_ref': 'J25', 'params': {'relationship': 'thermal_separation', 'target': 'J22', 'min_distance_mm': 4.0}, 'derived_from': 'spec.placement.constraints', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'agent_thermal_separation', 'target_ref': 'J26', 'params': {'relationship': 'thermal_separation', 'target': 'J22', 'min_distance_mm': 4.0}, 'derived_from': 'spec.placement.constraints', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'agent_thermal_separation', 'target_ref': 'J24', 'params': {'relationship': 'thermal_separation', 'target': 'J23', 'min_distance_mm': 4.0}, 'derived_from': 'spec.placement.constraints', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'agent_thermal_separation', 'target_ref': 'J25', 'params': {'relationship': 'thermal_separation', 'target': 'J23', 'min_distance_mm': 4.0}, 'derived_from': 'spec.placement.constraints', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'agent_thermal_separation', 'target_ref': 'J26', 'params': {'relationship': 'thermal_separation', 'target': 'J23', 'min_distance_mm': 4.0}, 'derived_from': 'spec.placement.constraints', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'agent_thermal_separation', 'target_ref': 'J25', 'params': {'relationship': 'thermal_separation', 'target': 'J24', 'min_distance_mm': 4.0}, 'derived_from': 'spec.placement.constraints', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'agent_thermal_separation', 'target_ref': 'J26', 'params': {'relationship': 'thermal_separation', 'target': 'J24', 'min_distance_mm': 4.0}, 'derived_from': 'spec.placement.constraints', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'agent_thermal_separation', 'target_ref': 'J26', 'params': {'relationship': 'thermal_separation', 'target': 'J25', 'min_distance_mm': 4.0}, 'derived_from': 'spec.placement.constraints', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'agent_adjacent_to', 'target_ref': 'J21', 'params': {'relationship': 'adjacent_to', 'target': 'J20', 'max_distance_mm': 5.0}, 'derived_from': 'spec.placement.constraints', 'enforced': True, 'rationale': ''})

semantic_schematic = board.to_dict()
