"""Generated executable semantic schematic for agent review.

This file is intentionally compact and pin-name based. It can be executed
to reconstruct the normalized semantic_schematic model. Native EDA/CAD
artifacts are generated from typed artifacts; edit the spec or graph-producing
blocks when changing a generated design.
"""

from hw_codesign.semantic_schematic import SemanticBoard, pin

board = SemanticBoard(
    project='bench_robotics_controller_5eab0a5d',
    revision='r1',
    purpose='LLM-suited schematic representation derived from typed graph; native EDA files are generated outputs.',
    source_graph='/Users/mrcha033/Documents/hw-cli/projects/bench_robotics_controller_5eab0a5d/electronics/generated/electrical_graph.json',
    board_width_mm=160.0,
    board_height_mm=100.0,
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
    component_id='grm188_100n',
    mpn='GRM188R71C104KA01D',
    manufacturer='Murata',
    package='0603',
    footprint='Capacitor_SMD:C_0603_1608Metric',
    pins=[
        pin('1', 'VCC', net='V3V3', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'C10',
    role='bulk_cap',
    value='10uF 50V',
    component_id='grm32_10u_50v',
    mpn='GRM32ER71H106KA12L',
    manufacturer='Murata',
    package='1210',
    footprint='Capacitor_SMD:C_1210_3225Metric',
    pins=[
        pin('1', 'VCC', net='VSYS', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'C2',
    role='decoupling',
    value='100nF',
    component_id='grm188_100n',
    mpn='GRM188R71C104KA01D',
    manufacturer='Murata',
    package='0603',
    footprint='Capacitor_SMD:C_0603_1608Metric',
    pins=[
        pin('1', 'VCC', net='V3V3', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'C3',
    role='decoupling',
    value='100nF',
    component_id='grm188_100n',
    mpn='GRM188R71C104KA01D',
    manufacturer='Murata',
    package='0603',
    footprint='Capacitor_SMD:C_0603_1608Metric',
    pins=[
        pin('1', 'VCC', net='V3V3', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'C4',
    role='decoupling',
    value='100nF',
    component_id='grm188_100n',
    mpn='GRM188R71C104KA01D',
    manufacturer='Murata',
    package='0603',
    footprint='Capacitor_SMD:C_0603_1608Metric',
    pins=[
        pin('1', 'VCC', net='V3V3', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'C5',
    role='decoupling',
    value='100nF',
    component_id='grm188_100n',
    mpn='GRM188R71C104KA01D',
    manufacturer='Murata',
    package='0603',
    footprint='Capacitor_SMD:C_0603_1608Metric',
    pins=[
        pin('1', 'VCC', net='V3V3', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'C6',
    role='decoupling',
    value='100nF',
    component_id='grm188_100n',
    mpn='GRM188R71C104KA01D',
    manufacturer='Murata',
    package='0603',
    footprint='Capacitor_SMD:C_0603_1608Metric',
    pins=[
        pin('1', 'VCC', net='V3V3', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'C7',
    role='decoupling',
    value='100nF',
    component_id='grm188_100n',
    mpn='GRM188R71C104KA01D',
    manufacturer='Murata',
    package='0603',
    footprint='Capacitor_SMD:C_0603_1608Metric',
    pins=[
        pin('1', 'VCC', net='V3V3', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'C8',
    role='decoupling',
    value='100nF',
    component_id='grm188_100n',
    mpn='GRM188R71C104KA01D',
    manufacturer='Murata',
    package='0603',
    footprint='Capacitor_SMD:C_0603_1608Metric',
    pins=[
        pin('1', 'VCC', net='V3V3', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'C9',
    role='bulk_cap',
    value='22uF',
    component_id='grm31_22u',
    mpn='GRM31CR61E226ME15L',
    manufacturer='Murata',
    package='1206',
    footprint='Capacitor_SMD:C_1206_3216Metric',
    pins=[
        pin('1', 'VCC', net='V5', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'D1',
    role='tvs',
    value='33V TVS',
    component_id='smcj33a',
    mpn='SMCJ33A',
    manufacturer='Littelfuse',
    package='SMC',
    footprint='Diode_SMD:D_SMC',
    pins=[
        pin('1', 'K', net='VBAT', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'A', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'D2',
    role='usb_esd',
    value='USB ESD',
    component_id='usblc6_2sc6',
    mpn='USBLC6-2SC6',
    manufacturer='STMicroelectronics',
    package='SOT-23-6',
    footprint='Package_TO_SOT_SMD:SOT-23-6',
    pins=[
        pin('1', 'DP_IN', net='USB_DP_RAW', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('2', 'DP_OUT', net='USB_DP', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('3', 'DM_IN', net='USB_DM_RAW', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('4', 'DM_OUT', net='USB_DM', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('5', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'F1',
    role='fuse',
    value='80A SERVICE FUSE',
    component_id='littelfuse_0498080',
    mpn='Littelfuse-0498080.M',
    manufacturer='Littelfuse',
    package='MIDI',
    footprint='HW_Curated:MIDI_Fuse',
    pins=[
        pin('1', 'IN', net='VBAT_RAW', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'OUT', net='VBAT_FUSED', role='passive', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'J1',
    role='power_input',
    value='24V INPUT',
    component_id='molex_42820_2212',
    mpn='Molex-42820-2212',
    manufacturer='Molex',
    package='Micro-Fit',
    footprint='HW_Curated:MicroFit_2Pin',
    pins=[
        pin('1', 'VBAT', net='VBAT_RAW', role='power_in', voltage_domain='VBAT', mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'J11',
    role='motor_io',
    value='MOTOR_IO_1',
    component_id='molex_43045_0800',
    mpn='Molex-43045-0800',
    manufacturer='Molex',
    package='Micro-Fit-8',
    footprint='HW_Curated:MicroFit_8Pin',
    pins=[
        pin('1', 'V5', net='V5', role='power_out', voltage_domain='V5', mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('3', 'PWM', net='MOTOR1_PWM', role='output', voltage_domain=None, mcu_pin=None),
        pin('4', 'CURRENT', net='MOTOR1_CURRENT', role='analog', voltage_domain=None, mcu_pin=None),
        pin('5', 'ENC', net='MOTOR1_ENC', role='input', voltage_domain=None, mcu_pin=None),
        pin('6', 'ESTOP', net='ESTOP_GATE', role='output', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'J12',
    role='motor_io',
    value='MOTOR_IO_2',
    component_id='molex_43045_0800',
    mpn='Molex-43045-0800',
    manufacturer='Molex',
    package='Micro-Fit-8',
    footprint='HW_Curated:MicroFit_8Pin',
    pins=[
        pin('1', 'V5', net='V5', role='power_out', voltage_domain='V5', mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('3', 'PWM', net='MOTOR2_PWM', role='output', voltage_domain=None, mcu_pin=None),
        pin('4', 'CURRENT', net='MOTOR2_CURRENT', role='analog', voltage_domain=None, mcu_pin=None),
        pin('5', 'ENC', net='MOTOR2_ENC', role='input', voltage_domain=None, mcu_pin=None),
        pin('6', 'ESTOP', net='ESTOP_GATE', role='output', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'J13',
    role='motor_io',
    value='MOTOR_IO_3',
    component_id='molex_43045_0800',
    mpn='Molex-43045-0800',
    manufacturer='Molex',
    package='Micro-Fit-8',
    footprint='HW_Curated:MicroFit_8Pin',
    pins=[
        pin('1', 'V5', net='V5', role='power_out', voltage_domain='V5', mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('3', 'PWM', net='MOTOR3_PWM', role='output', voltage_domain=None, mcu_pin=None),
        pin('4', 'CURRENT', net='MOTOR3_CURRENT', role='analog', voltage_domain=None, mcu_pin=None),
        pin('5', 'ENC', net='MOTOR3_ENC', role='input', voltage_domain=None, mcu_pin=None),
        pin('6', 'ESTOP', net='ESTOP_GATE', role='output', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'J14',
    role='motor_io',
    value='MOTOR_IO_4',
    component_id='molex_43045_0800',
    mpn='Molex-43045-0800',
    manufacturer='Molex',
    package='Micro-Fit-8',
    footprint='HW_Curated:MicroFit_8Pin',
    pins=[
        pin('1', 'V5', net='V5', role='power_out', voltage_domain='V5', mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('3', 'PWM', net='MOTOR4_PWM', role='output', voltage_domain=None, mcu_pin=None),
        pin('4', 'CURRENT', net='MOTOR4_CURRENT', role='analog', voltage_domain=None, mcu_pin=None),
        pin('5', 'ENC', net='MOTOR4_ENC', role='input', voltage_domain=None, mcu_pin=None),
        pin('6', 'ESTOP', net='ESTOP_GATE', role='output', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'J15',
    role='motor_io',
    value='MOTOR_IO_5',
    component_id='molex_43045_0800',
    mpn='Molex-43045-0800',
    manufacturer='Molex',
    package='Micro-Fit-8',
    footprint='HW_Curated:MicroFit_8Pin',
    pins=[
        pin('1', 'V5', net='V5', role='power_out', voltage_domain='V5', mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('3', 'PWM', net='MOTOR5_PWM', role='output', voltage_domain=None, mcu_pin=None),
        pin('4', 'CURRENT', net='MOTOR5_CURRENT', role='analog', voltage_domain=None, mcu_pin=None),
        pin('5', 'ENC', net='MOTOR5_ENC', role='input', voltage_domain=None, mcu_pin=None),
        pin('6', 'ESTOP', net='ESTOP_GATE', role='output', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'J16',
    role='motor_io',
    value='MOTOR_IO_6',
    component_id='molex_43045_0800',
    mpn='Molex-43045-0800',
    manufacturer='Molex',
    package='Micro-Fit-8',
    footprint='HW_Curated:MicroFit_8Pin',
    pins=[
        pin('1', 'V5', net='V5', role='power_out', voltage_domain='V5', mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('3', 'PWM', net='MOTOR6_PWM', role='output', voltage_domain=None, mcu_pin=None),
        pin('4', 'CURRENT', net='MOTOR6_CURRENT', role='analog', voltage_domain=None, mcu_pin=None),
        pin('5', 'ENC', net='MOTOR6_ENC', role='input', voltage_domain=None, mcu_pin=None),
        pin('6', 'ESTOP', net='ESTOP_GATE', role='output', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'J17',
    role='motor_io',
    value='MOTOR_IO_7',
    component_id='molex_43045_0800',
    mpn='Molex-43045-0800',
    manufacturer='Molex',
    package='Micro-Fit-8',
    footprint='HW_Curated:MicroFit_8Pin',
    pins=[
        pin('1', 'V5', net='V5', role='power_out', voltage_domain='V5', mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('3', 'PWM', net='MOTOR7_PWM', role='output', voltage_domain=None, mcu_pin=None),
        pin('4', 'CURRENT', net='MOTOR7_CURRENT', role='analog', voltage_domain=None, mcu_pin=None),
        pin('5', 'ENC', net='MOTOR7_ENC', role='input', voltage_domain=None, mcu_pin=None),
        pin('6', 'ESTOP', net='ESTOP_GATE', role='output', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'J18',
    role='motor_io',
    value='MOTOR_IO_8',
    component_id='molex_43045_0800',
    mpn='Molex-43045-0800',
    manufacturer='Molex',
    package='Micro-Fit-8',
    footprint='HW_Curated:MicroFit_8Pin',
    pins=[
        pin('1', 'V5', net='V5', role='power_out', voltage_domain='V5', mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('3', 'PWM', net='MOTOR8_PWM', role='output', voltage_domain=None, mcu_pin=None),
        pin('4', 'CURRENT', net='MOTOR8_CURRENT', role='analog', voltage_domain=None, mcu_pin=None),
        pin('5', 'ENC', net='MOTOR8_ENC', role='input', voltage_domain=None, mcu_pin=None),
        pin('6', 'ESTOP', net='ESTOP_GATE', role='output', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'J19',
    role='motor_io',
    value='MOTOR_IO_9',
    component_id='molex_43045_0800',
    mpn='Molex-43045-0800',
    manufacturer='Molex',
    package='Micro-Fit-8',
    footprint='HW_Curated:MicroFit_8Pin',
    pins=[
        pin('1', 'V5', net='V5', role='power_out', voltage_domain='V5', mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('3', 'PWM', net='MOTOR9_PWM', role='output', voltage_domain=None, mcu_pin=None),
        pin('4', 'CURRENT', net='MOTOR9_CURRENT', role='analog', voltage_domain=None, mcu_pin=None),
        pin('5', 'ENC', net='MOTOR9_ENC', role='input', voltage_domain=None, mcu_pin=None),
        pin('6', 'ESTOP', net='ESTOP_GATE', role='output', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'J2',
    role='estop',
    value='E-STOP',
    component_id='phoenix_1935161',
    mpn='Phoenix-1935161',
    manufacturer='Phoenix Contact',
    package='Terminal-3',
    footprint='TerminalBlock:Phoenix_3Pin',
    pins=[
        pin('1', 'V3V3', net='V3V3', role='power_out', voltage_domain='V3V3', mcu_pin=None),
        pin('2', 'ESTOP', net='ESTOP_IN', role='input', voltage_domain=None, mcu_pin=None),
        pin('3', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'J20',
    role='motor_io',
    value='MOTOR_IO_10',
    component_id='molex_43045_0800',
    mpn='Molex-43045-0800',
    manufacturer='Molex',
    package='Micro-Fit-8',
    footprint='HW_Curated:MicroFit_8Pin',
    pins=[
        pin('1', 'V5', net='V5', role='power_out', voltage_domain='V5', mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('3', 'PWM', net='MOTOR10_PWM', role='output', voltage_domain=None, mcu_pin=None),
        pin('4', 'CURRENT', net='MOTOR10_CURRENT', role='analog', voltage_domain=None, mcu_pin=None),
        pin('5', 'ENC', net='MOTOR10_ENC', role='input', voltage_domain=None, mcu_pin=None),
        pin('6', 'ESTOP', net='ESTOP_GATE', role='output', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'J21',
    role='motor_io',
    value='MOTOR_IO_11',
    component_id='molex_43045_0800',
    mpn='Molex-43045-0800',
    manufacturer='Molex',
    package='Micro-Fit-8',
    footprint='HW_Curated:MicroFit_8Pin',
    pins=[
        pin('1', 'V5', net='V5', role='power_out', voltage_domain='V5', mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('3', 'PWM', net='MOTOR11_PWM', role='output', voltage_domain=None, mcu_pin=None),
        pin('4', 'CURRENT', net='MOTOR11_CURRENT', role='analog', voltage_domain=None, mcu_pin=None),
        pin('5', 'ENC', net='MOTOR11_ENC', role='input', voltage_domain=None, mcu_pin=None),
        pin('6', 'ESTOP', net='ESTOP_GATE', role='output', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'J22',
    role='motor_io',
    value='MOTOR_IO_12',
    component_id='molex_43045_0800',
    mpn='Molex-43045-0800',
    manufacturer='Molex',
    package='Micro-Fit-8',
    footprint='HW_Curated:MicroFit_8Pin',
    pins=[
        pin('1', 'V5', net='V5', role='power_out', voltage_domain='V5', mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('3', 'PWM', net='MOTOR12_PWM', role='output', voltage_domain=None, mcu_pin=None),
        pin('4', 'CURRENT', net='MOTOR12_CURRENT', role='analog', voltage_domain=None, mcu_pin=None),
        pin('5', 'ENC', net='MOTOR12_ENC', role='input', voltage_domain=None, mcu_pin=None),
        pin('6', 'ESTOP', net='ESTOP_GATE', role='output', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'J3',
    role='can_connector',
    value='CAN',
    component_id='molex_43650_0300',
    mpn='Molex-43650-0300',
    manufacturer='Molex',
    package='Micro-Fit-3',
    footprint='HW_Curated:MicroFit_3Pin',
    pins=[
        pin('1', 'CANH', net='CANH', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('2', 'CANL', net='CANL', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('3', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'J4',
    role='debug',
    value='SWD',
    component_id='samtec_ftsh_105',
    mpn='Samtec-FTSH-105-01-L-DV-K',
    manufacturer='Samtec',
    package='FTSH-10',
    footprint='Connector_Samtec:FTSH-105',
    pins=[
        pin('1', 'VREF', net='V3V3', role='power_out', voltage_domain='V3V3', mcu_pin=None),
        pin('2', 'SWDIO', net='SWDIO', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('3', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('4', 'SWCLK', net='SWCLK', role='input', voltage_domain=None, mcu_pin=None),
        pin('5', 'NRST', net='NRST', role='bidirectional', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'J5',
    role='usb',
    value='USB-C',
    component_id='usb4105_gf_a',
    mpn='USB4105-GF-A',
    manufacturer='GCT',
    package='USB-C-16',
    footprint='Connector_USB:USB_C_GCT_USB4105',
    pins=[
        pin('1', 'VBUS', net='USB_VBUS', role='power_in', voltage_domain='USB_5V', mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('3', 'D+', net='USB_DP_RAW', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('4', 'D-', net='USB_DM_RAW', role='bidirectional', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'Q1',
    role='reverse_polarity',
    value='IDEAL DIODE',
    component_id='lm74700qdbvrq1',
    mpn='LM74700QDBVRQ1',
    manufacturer='Texas Instruments',
    package='SOT-23-6',
    footprint='Package_TO_SOT_SMD:SOT-23-6',
    pins=[
        pin('1', 'ANODE', net='VBAT_FUSED', role='power_in', voltage_domain='VBAT', mcu_pin=None),
        pin('2', 'CATHODE', net='VBAT', role='power_out', voltage_domain='VBAT', mcu_pin=None),
        pin('3', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'Q2',
    role='safety_gate',
    value='E-STOP GATE',
    component_id='sn74lvc1g97dbvr',
    mpn='SN74LVC1G97DBVR',
    manufacturer='Texas Instruments',
    package='SOT-23-6',
    footprint='Package_TO_SOT_SMD:SOT-23-6',
    pins=[
        pin('1', 'VCC', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin=None),
        pin('2', 'IN', net='ESTOP_IN', role='input', voltage_domain=None, mcu_pin=None),
        pin('3', 'OUT', net='ESTOP_GATE', role='output', voltage_domain=None, mcu_pin=None),
        pin('4', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'R1',
    role='termination',
    value='120R',
    component_id='rc0603_120r',
    mpn='RC0603FR-07120RL',
    manufacturer='Yageo',
    package='0603',
    footprint='Resistor_SMD:R_0603_1608Metric',
    pins=[
        pin('1', 'A', net='CANH', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'B', net='CANL', role='passive', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'R2',
    role='pullup',
    value='4K7',
    component_id='rc0603_4k7',
    mpn='RC0603FR-074K7L',
    manufacturer='Yageo',
    package='0603',
    footprint='Resistor_SMD:R_0603_1608Metric',
    pins=[
        pin('1', 'VCC', net='V3V3', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'SCL', net='I2C_IMU_SCL', role='passive', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'R3',
    role='pullup',
    value='4K7',
    component_id='rc0603_4k7',
    mpn='RC0603FR-074K7L',
    manufacturer='Yageo',
    package='0603',
    footprint='Resistor_SMD:R_0603_1608Metric',
    pins=[
        pin('1', 'VCC', net='V3V3', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'SDA', net='I2C_IMU_SDA', role='passive', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'R4',
    role='discharge',
    value='100K',
    component_id='rc0603_100k',
    mpn='RC0603FR-07100KL',
    manufacturer='Yageo',
    package='0603',
    footprint='Resistor_SMD:R_0603_1608Metric',
    pins=[
        pin('1', 'VBUS', net='USB_VBUS', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'U1',
    role='mcu',
    value='STM32H743',
    component_id='stm32h743vit6',
    mpn='STM32H743VIT6',
    manufacturer='STMicroelectronics',
    package='LQFP-100',
    footprint='Package_QFP:LQFP-100_14x14mm_P0.5mm',
    pins=[
        pin('1', 'VDD', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin=None),
        pin('2', 'VSS', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('3', 'ESTOP_IN', net='ESTOP_IN', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('4', 'CAN_RX', net='CAN_RX', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('5', 'CAN_TX', net='CAN_TX', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('6', 'I2C_IMU_SCL', net='I2C_IMU_SCL', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('7', 'I2C_IMU_SDA', net='I2C_IMU_SDA', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('8', 'IMU_INT', net='IMU_INT', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('9', 'SWDIO', net='SWDIO', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('10', 'SWCLK', net='SWCLK', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('11', 'NRST', net='NRST', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('12', 'USB_DP', net='USB_DP', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('13', 'USB_DM', net='USB_DM', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('14', 'MOTOR1_PWM', net='MOTOR1_PWM', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('15', 'MOTOR1_CURRENT', net='MOTOR1_CURRENT', role='analog', voltage_domain=None, mcu_pin=None),
        pin('16', 'MOTOR1_ENC', net='MOTOR1_ENC', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('17', 'MOTOR2_PWM', net='MOTOR2_PWM', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('18', 'MOTOR2_CURRENT', net='MOTOR2_CURRENT', role='analog', voltage_domain=None, mcu_pin=None),
        pin('19', 'MOTOR2_ENC', net='MOTOR2_ENC', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('20', 'MOTOR3_PWM', net='MOTOR3_PWM', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('21', 'MOTOR3_CURRENT', net='MOTOR3_CURRENT', role='analog', voltage_domain=None, mcu_pin=None),
        pin('22', 'MOTOR3_ENC', net='MOTOR3_ENC', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('23', 'MOTOR4_PWM', net='MOTOR4_PWM', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('24', 'MOTOR4_CURRENT', net='MOTOR4_CURRENT', role='analog', voltage_domain=None, mcu_pin=None),
        pin('25', 'MOTOR4_ENC', net='MOTOR4_ENC', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('26', 'MOTOR5_PWM', net='MOTOR5_PWM', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('27', 'MOTOR5_CURRENT', net='MOTOR5_CURRENT', role='analog', voltage_domain=None, mcu_pin=None),
        pin('28', 'MOTOR5_ENC', net='MOTOR5_ENC', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('29', 'MOTOR6_PWM', net='MOTOR6_PWM', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('30', 'MOTOR6_CURRENT', net='MOTOR6_CURRENT', role='analog', voltage_domain=None, mcu_pin=None),
        pin('31', 'MOTOR6_ENC', net='MOTOR6_ENC', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('32', 'MOTOR7_PWM', net='MOTOR7_PWM', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('33', 'MOTOR7_CURRENT', net='MOTOR7_CURRENT', role='analog', voltage_domain=None, mcu_pin=None),
        pin('34', 'MOTOR7_ENC', net='MOTOR7_ENC', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('35', 'MOTOR8_PWM', net='MOTOR8_PWM', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('36', 'MOTOR8_CURRENT', net='MOTOR8_CURRENT', role='analog', voltage_domain=None, mcu_pin=None),
        pin('37', 'MOTOR8_ENC', net='MOTOR8_ENC', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('38', 'MOTOR9_PWM', net='MOTOR9_PWM', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('39', 'MOTOR9_CURRENT', net='MOTOR9_CURRENT', role='analog', voltage_domain=None, mcu_pin=None),
        pin('40', 'MOTOR9_ENC', net='MOTOR9_ENC', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('41', 'MOTOR10_PWM', net='MOTOR10_PWM', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('42', 'MOTOR10_CURRENT', net='MOTOR10_CURRENT', role='analog', voltage_domain=None, mcu_pin=None),
        pin('43', 'MOTOR10_ENC', net='MOTOR10_ENC', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('44', 'MOTOR11_PWM', net='MOTOR11_PWM', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('45', 'MOTOR11_CURRENT', net='MOTOR11_CURRENT', role='analog', voltage_domain=None, mcu_pin=None),
        pin('46', 'MOTOR11_ENC', net='MOTOR11_ENC', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('47', 'MOTOR12_PWM', net='MOTOR12_PWM', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('48', 'MOTOR12_CURRENT', net='MOTOR12_CURRENT', role='analog', voltage_domain=None, mcu_pin=None),
        pin('49', 'MOTOR12_ENC', net='MOTOR12_ENC', role='bidirectional', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'U2',
    role='imu',
    value='ICM-42688-P',
    component_id='icm_42688_p',
    mpn='ICM-42688-P',
    manufacturer='TDK InvenSense',
    package='LGA-14',
    footprint='Package_LGA:LGA-14',
    pins=[
        pin('1', 'VDD', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('3', 'SCL', net='I2C_IMU_SCL', role='open_drain', voltage_domain=None, mcu_pin=None),
        pin('4', 'SDA', net='I2C_IMU_SDA', role='open_drain', voltage_domain=None, mcu_pin=None),
        pin('5', 'INT1', net='IMU_INT', role='output', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'U3',
    role='efuse',
    value='eFuse',
    component_id='tps26630rget',
    mpn='TPS26630RGET',
    manufacturer='Texas Instruments',
    package='VQFN-24',
    footprint='Package_DFN_QFN:VQFN-24-1EP',
    pins=[
        pin('1', 'IN', net='VBAT', role='power_in', voltage_domain='VBAT', mcu_pin=None),
        pin('2', 'OUT', net='VSYS', role='power_out', voltage_domain='VBAT', mcu_pin=None),
        pin('3', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('4', 'SHDN', net='ESTOP_GATE', role='input', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'U4',
    role='regulator',
    value='5V Buck',
    component_id='lm76005rnpr',
    mpn='LM76005RNPR',
    manufacturer='Texas Instruments',
    package='WQFN-30',
    footprint='Package_DFN_QFN:WQFN-30',
    pins=[
        pin('1', 'VIN', net='VSYS', role='power_in', voltage_domain='VBAT', mcu_pin=None),
        pin('2', 'VOUT', net='V5', role='power_out', voltage_domain='V5', mcu_pin=None),
        pin('3', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'U5',
    role='regulator',
    value='3V3 Buck',
    component_id='tps62133rgtr',
    mpn='TPS62133RGTR',
    manufacturer='Texas Instruments',
    package='VQFN-16',
    footprint='Package_DFN_QFN:VQFN-16',
    pins=[
        pin('1', 'VIN', net='V5', role='power_in', voltage_domain='V5', mcu_pin=None),
        pin('2', 'VOUT', net='V3V3', role='power_out', voltage_domain='V3V3', mcu_pin=None),
        pin('3', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'U6',
    role='can',
    value='CAN PHY',
    component_id='tcan1042hgvdrq1',
    mpn='TCAN1042HGVDRQ1',
    manufacturer='Texas Instruments',
    package='SOIC-8',
    footprint='Package_SO:SOIC-8_3.9x4.9mm_P1.27mm',
    pins=[
        pin('1', 'VCC', net='V5', role='power_in', voltage_domain='V5', mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('3', 'RXD', net='CAN_RX', role='output', voltage_domain=None, mcu_pin=None),
        pin('4', 'TXD', net='CAN_TX', role='input', voltage_domain=None, mcu_pin=None),
        pin('5', 'CANH', net='CANH', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('6', 'CANL', net='CANL', role='bidirectional', voltage_domain=None, mcu_pin=None),
    ],
)


net('CANH', signal_class='can', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J3', pin='CANH', number='1', net='CANH', role='bidirectional', mcu_pin=None)
connect('R1', pin='A', number='1', net='CANH', role='passive', mcu_pin=None)
connect('U6', pin='CANH', number='5', net='CANH', role='bidirectional', mcu_pin=None)

net('CANL', signal_class='can', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J3', pin='CANL', number='2', net='CANL', role='bidirectional', mcu_pin=None)
connect('R1', pin='B', number='2', net='CANL', role='passive', mcu_pin=None)
connect('U6', pin='CANL', number='6', net='CANL', role='bidirectional', mcu_pin=None)

net('CAN_RX', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('U1', pin='CAN_RX', number='4', net='CAN_RX', role='bidirectional', mcu_pin=None)
connect('U6', pin='RXD', number='3', net='CAN_RX', role='output', mcu_pin=None)

net('CAN_TX', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('U1', pin='CAN_TX', number='5', net='CAN_TX', role='bidirectional', mcu_pin=None)
connect('U6', pin='TXD', number='4', net='CAN_TX', role='input', mcu_pin=None)

net('ESTOP_GATE', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J11', pin='ESTOP', number='6', net='ESTOP_GATE', role='output', mcu_pin=None)
connect('J12', pin='ESTOP', number='6', net='ESTOP_GATE', role='output', mcu_pin=None)
connect('J13', pin='ESTOP', number='6', net='ESTOP_GATE', role='output', mcu_pin=None)
connect('J14', pin='ESTOP', number='6', net='ESTOP_GATE', role='output', mcu_pin=None)
connect('J15', pin='ESTOP', number='6', net='ESTOP_GATE', role='output', mcu_pin=None)
connect('J16', pin='ESTOP', number='6', net='ESTOP_GATE', role='output', mcu_pin=None)
connect('J17', pin='ESTOP', number='6', net='ESTOP_GATE', role='output', mcu_pin=None)
connect('J18', pin='ESTOP', number='6', net='ESTOP_GATE', role='output', mcu_pin=None)
connect('J19', pin='ESTOP', number='6', net='ESTOP_GATE', role='output', mcu_pin=None)
connect('J20', pin='ESTOP', number='6', net='ESTOP_GATE', role='output', mcu_pin=None)
connect('J21', pin='ESTOP', number='6', net='ESTOP_GATE', role='output', mcu_pin=None)
connect('J22', pin='ESTOP', number='6', net='ESTOP_GATE', role='output', mcu_pin=None)
connect('Q2', pin='OUT', number='3', net='ESTOP_GATE', role='output', mcu_pin=None)
connect('U3', pin='SHDN', number='4', net='ESTOP_GATE', role='input', mcu_pin=None)

net('ESTOP_IN', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J2', pin='ESTOP', number='2', net='ESTOP_IN', role='input', mcu_pin=None)
connect('Q2', pin='IN', number='2', net='ESTOP_IN', role='input', mcu_pin=None)
connect('U1', pin='ESTOP_IN', number='3', net='ESTOP_IN', role='bidirectional', mcu_pin=None)

net('GND', signal_class='ground', voltage_domain='GND', required_track_width_mm=0.2)
connect('C1', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('C10', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('C2', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('C3', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('C4', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('C5', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('C6', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('C7', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('C8', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('C9', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('D1', pin='A', number='2', net='GND', role='ground', mcu_pin=None)
connect('D2', pin='GND', number='5', net='GND', role='ground', mcu_pin=None)
connect('J1', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('J11', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('J12', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('J13', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('J14', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('J15', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('J16', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('J17', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('J18', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('J19', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('J2', pin='GND', number='3', net='GND', role='ground', mcu_pin=None)
connect('J20', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('J21', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('J22', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('J3', pin='GND', number='3', net='GND', role='ground', mcu_pin=None)
connect('J4', pin='GND', number='3', net='GND', role='ground', mcu_pin=None)
connect('J5', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('Q1', pin='GND', number='3', net='GND', role='ground', mcu_pin=None)
connect('Q2', pin='GND', number='4', net='GND', role='ground', mcu_pin=None)
connect('R4', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('U1', pin='VSS', number='2', net='GND', role='ground', mcu_pin=None)
connect('U2', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('U3', pin='GND', number='3', net='GND', role='ground', mcu_pin=None)
connect('U4', pin='GND', number='3', net='GND', role='ground', mcu_pin=None)
connect('U5', pin='GND', number='3', net='GND', role='ground', mcu_pin=None)
connect('U6', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)

net('I2C_IMU_SCL', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('R2', pin='SCL', number='2', net='I2C_IMU_SCL', role='passive', mcu_pin=None)
connect('U1', pin='I2C_IMU_SCL', number='6', net='I2C_IMU_SCL', role='bidirectional', mcu_pin=None)
connect('U2', pin='SCL', number='3', net='I2C_IMU_SCL', role='open_drain', mcu_pin=None)

net('I2C_IMU_SDA', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('R3', pin='SDA', number='2', net='I2C_IMU_SDA', role='passive', mcu_pin=None)
connect('U1', pin='I2C_IMU_SDA', number='7', net='I2C_IMU_SDA', role='bidirectional', mcu_pin=None)
connect('U2', pin='SDA', number='4', net='I2C_IMU_SDA', role='open_drain', mcu_pin=None)

net('IMU_INT', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('U1', pin='IMU_INT', number='8', net='IMU_INT', role='bidirectional', mcu_pin=None)
connect('U2', pin='INT1', number='5', net='IMU_INT', role='output', mcu_pin=None)

net('MOTOR10_CURRENT', signal_class='analog', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J20', pin='CURRENT', number='4', net='MOTOR10_CURRENT', role='analog', mcu_pin=None)
connect('U1', pin='MOTOR10_CURRENT', number='42', net='MOTOR10_CURRENT', role='analog', mcu_pin=None)

net('MOTOR10_ENC', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J20', pin='ENC', number='5', net='MOTOR10_ENC', role='input', mcu_pin=None)
connect('U1', pin='MOTOR10_ENC', number='43', net='MOTOR10_ENC', role='bidirectional', mcu_pin=None)

net('MOTOR10_PWM', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J20', pin='PWM', number='3', net='MOTOR10_PWM', role='output', mcu_pin=None)
connect('U1', pin='MOTOR10_PWM', number='41', net='MOTOR10_PWM', role='bidirectional', mcu_pin=None)

net('MOTOR11_CURRENT', signal_class='analog', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J21', pin='CURRENT', number='4', net='MOTOR11_CURRENT', role='analog', mcu_pin=None)
connect('U1', pin='MOTOR11_CURRENT', number='45', net='MOTOR11_CURRENT', role='analog', mcu_pin=None)

net('MOTOR11_ENC', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J21', pin='ENC', number='5', net='MOTOR11_ENC', role='input', mcu_pin=None)
connect('U1', pin='MOTOR11_ENC', number='46', net='MOTOR11_ENC', role='bidirectional', mcu_pin=None)

net('MOTOR11_PWM', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J21', pin='PWM', number='3', net='MOTOR11_PWM', role='output', mcu_pin=None)
connect('U1', pin='MOTOR11_PWM', number='44', net='MOTOR11_PWM', role='bidirectional', mcu_pin=None)

net('MOTOR12_CURRENT', signal_class='analog', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J22', pin='CURRENT', number='4', net='MOTOR12_CURRENT', role='analog', mcu_pin=None)
connect('U1', pin='MOTOR12_CURRENT', number='48', net='MOTOR12_CURRENT', role='analog', mcu_pin=None)

net('MOTOR12_ENC', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J22', pin='ENC', number='5', net='MOTOR12_ENC', role='input', mcu_pin=None)
connect('U1', pin='MOTOR12_ENC', number='49', net='MOTOR12_ENC', role='bidirectional', mcu_pin=None)

net('MOTOR12_PWM', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J22', pin='PWM', number='3', net='MOTOR12_PWM', role='output', mcu_pin=None)
connect('U1', pin='MOTOR12_PWM', number='47', net='MOTOR12_PWM', role='bidirectional', mcu_pin=None)

net('MOTOR1_CURRENT', signal_class='analog', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J11', pin='CURRENT', number='4', net='MOTOR1_CURRENT', role='analog', mcu_pin=None)
connect('U1', pin='MOTOR1_CURRENT', number='15', net='MOTOR1_CURRENT', role='analog', mcu_pin=None)

net('MOTOR1_ENC', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J11', pin='ENC', number='5', net='MOTOR1_ENC', role='input', mcu_pin=None)
connect('U1', pin='MOTOR1_ENC', number='16', net='MOTOR1_ENC', role='bidirectional', mcu_pin=None)

net('MOTOR1_PWM', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J11', pin='PWM', number='3', net='MOTOR1_PWM', role='output', mcu_pin=None)
connect('U1', pin='MOTOR1_PWM', number='14', net='MOTOR1_PWM', role='bidirectional', mcu_pin=None)

net('MOTOR2_CURRENT', signal_class='analog', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J12', pin='CURRENT', number='4', net='MOTOR2_CURRENT', role='analog', mcu_pin=None)
connect('U1', pin='MOTOR2_CURRENT', number='18', net='MOTOR2_CURRENT', role='analog', mcu_pin=None)

net('MOTOR2_ENC', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J12', pin='ENC', number='5', net='MOTOR2_ENC', role='input', mcu_pin=None)
connect('U1', pin='MOTOR2_ENC', number='19', net='MOTOR2_ENC', role='bidirectional', mcu_pin=None)

net('MOTOR2_PWM', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J12', pin='PWM', number='3', net='MOTOR2_PWM', role='output', mcu_pin=None)
connect('U1', pin='MOTOR2_PWM', number='17', net='MOTOR2_PWM', role='bidirectional', mcu_pin=None)

net('MOTOR3_CURRENT', signal_class='analog', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J13', pin='CURRENT', number='4', net='MOTOR3_CURRENT', role='analog', mcu_pin=None)
connect('U1', pin='MOTOR3_CURRENT', number='21', net='MOTOR3_CURRENT', role='analog', mcu_pin=None)

net('MOTOR3_ENC', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J13', pin='ENC', number='5', net='MOTOR3_ENC', role='input', mcu_pin=None)
connect('U1', pin='MOTOR3_ENC', number='22', net='MOTOR3_ENC', role='bidirectional', mcu_pin=None)

net('MOTOR3_PWM', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J13', pin='PWM', number='3', net='MOTOR3_PWM', role='output', mcu_pin=None)
connect('U1', pin='MOTOR3_PWM', number='20', net='MOTOR3_PWM', role='bidirectional', mcu_pin=None)

net('MOTOR4_CURRENT', signal_class='analog', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J14', pin='CURRENT', number='4', net='MOTOR4_CURRENT', role='analog', mcu_pin=None)
connect('U1', pin='MOTOR4_CURRENT', number='24', net='MOTOR4_CURRENT', role='analog', mcu_pin=None)

net('MOTOR4_ENC', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J14', pin='ENC', number='5', net='MOTOR4_ENC', role='input', mcu_pin=None)
connect('U1', pin='MOTOR4_ENC', number='25', net='MOTOR4_ENC', role='bidirectional', mcu_pin=None)

net('MOTOR4_PWM', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J14', pin='PWM', number='3', net='MOTOR4_PWM', role='output', mcu_pin=None)
connect('U1', pin='MOTOR4_PWM', number='23', net='MOTOR4_PWM', role='bidirectional', mcu_pin=None)

net('MOTOR5_CURRENT', signal_class='analog', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J15', pin='CURRENT', number='4', net='MOTOR5_CURRENT', role='analog', mcu_pin=None)
connect('U1', pin='MOTOR5_CURRENT', number='27', net='MOTOR5_CURRENT', role='analog', mcu_pin=None)

net('MOTOR5_ENC', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J15', pin='ENC', number='5', net='MOTOR5_ENC', role='input', mcu_pin=None)
connect('U1', pin='MOTOR5_ENC', number='28', net='MOTOR5_ENC', role='bidirectional', mcu_pin=None)

net('MOTOR5_PWM', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J15', pin='PWM', number='3', net='MOTOR5_PWM', role='output', mcu_pin=None)
connect('U1', pin='MOTOR5_PWM', number='26', net='MOTOR5_PWM', role='bidirectional', mcu_pin=None)

net('MOTOR6_CURRENT', signal_class='analog', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J16', pin='CURRENT', number='4', net='MOTOR6_CURRENT', role='analog', mcu_pin=None)
connect('U1', pin='MOTOR6_CURRENT', number='30', net='MOTOR6_CURRENT', role='analog', mcu_pin=None)

net('MOTOR6_ENC', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J16', pin='ENC', number='5', net='MOTOR6_ENC', role='input', mcu_pin=None)
connect('U1', pin='MOTOR6_ENC', number='31', net='MOTOR6_ENC', role='bidirectional', mcu_pin=None)

net('MOTOR6_PWM', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J16', pin='PWM', number='3', net='MOTOR6_PWM', role='output', mcu_pin=None)
connect('U1', pin='MOTOR6_PWM', number='29', net='MOTOR6_PWM', role='bidirectional', mcu_pin=None)

net('MOTOR7_CURRENT', signal_class='analog', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J17', pin='CURRENT', number='4', net='MOTOR7_CURRENT', role='analog', mcu_pin=None)
connect('U1', pin='MOTOR7_CURRENT', number='33', net='MOTOR7_CURRENT', role='analog', mcu_pin=None)

net('MOTOR7_ENC', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J17', pin='ENC', number='5', net='MOTOR7_ENC', role='input', mcu_pin=None)
connect('U1', pin='MOTOR7_ENC', number='34', net='MOTOR7_ENC', role='bidirectional', mcu_pin=None)

net('MOTOR7_PWM', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J17', pin='PWM', number='3', net='MOTOR7_PWM', role='output', mcu_pin=None)
connect('U1', pin='MOTOR7_PWM', number='32', net='MOTOR7_PWM', role='bidirectional', mcu_pin=None)

net('MOTOR8_CURRENT', signal_class='analog', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J18', pin='CURRENT', number='4', net='MOTOR8_CURRENT', role='analog', mcu_pin=None)
connect('U1', pin='MOTOR8_CURRENT', number='36', net='MOTOR8_CURRENT', role='analog', mcu_pin=None)

net('MOTOR8_ENC', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J18', pin='ENC', number='5', net='MOTOR8_ENC', role='input', mcu_pin=None)
connect('U1', pin='MOTOR8_ENC', number='37', net='MOTOR8_ENC', role='bidirectional', mcu_pin=None)

net('MOTOR8_PWM', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J18', pin='PWM', number='3', net='MOTOR8_PWM', role='output', mcu_pin=None)
connect('U1', pin='MOTOR8_PWM', number='35', net='MOTOR8_PWM', role='bidirectional', mcu_pin=None)

net('MOTOR9_CURRENT', signal_class='analog', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J19', pin='CURRENT', number='4', net='MOTOR9_CURRENT', role='analog', mcu_pin=None)
connect('U1', pin='MOTOR9_CURRENT', number='39', net='MOTOR9_CURRENT', role='analog', mcu_pin=None)

net('MOTOR9_ENC', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J19', pin='ENC', number='5', net='MOTOR9_ENC', role='input', mcu_pin=None)
connect('U1', pin='MOTOR9_ENC', number='40', net='MOTOR9_ENC', role='bidirectional', mcu_pin=None)

net('MOTOR9_PWM', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J19', pin='PWM', number='3', net='MOTOR9_PWM', role='output', mcu_pin=None)
connect('U1', pin='MOTOR9_PWM', number='38', net='MOTOR9_PWM', role='bidirectional', mcu_pin=None)

net('NRST', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J4', pin='NRST', number='5', net='NRST', role='bidirectional', mcu_pin=None)
connect('U1', pin='NRST', number='11', net='NRST', role='bidirectional', mcu_pin=None)

net('SWCLK', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J4', pin='SWCLK', number='4', net='SWCLK', role='input', mcu_pin=None)
connect('U1', pin='SWCLK', number='10', net='SWCLK', role='bidirectional', mcu_pin=None)

net('SWDIO', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('J4', pin='SWDIO', number='2', net='SWDIO', role='bidirectional', mcu_pin=None)
connect('U1', pin='SWDIO', number='9', net='SWDIO', role='bidirectional', mcu_pin=None)

net('USB_DM', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('D2', pin='DM_OUT', number='4', net='USB_DM', role='bidirectional', mcu_pin=None)
connect('U1', pin='USB_DM', number='13', net='USB_DM', role='bidirectional', mcu_pin=None)

net('USB_DM_RAW', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('D2', pin='DM_IN', number='3', net='USB_DM_RAW', role='bidirectional', mcu_pin=None)
connect('J5', pin='D-', number='4', net='USB_DM_RAW', role='bidirectional', mcu_pin=None)

net('USB_DP', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('D2', pin='DP_OUT', number='2', net='USB_DP', role='bidirectional', mcu_pin=None)
connect('U1', pin='USB_DP', number='12', net='USB_DP', role='bidirectional', mcu_pin=None)

net('USB_DP_RAW', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.2)
connect('D2', pin='DP_IN', number='1', net='USB_DP_RAW', role='bidirectional', mcu_pin=None)
connect('J5', pin='D+', number='3', net='USB_DP_RAW', role='bidirectional', mcu_pin=None)

net('USB_VBUS', signal_class='power', voltage_domain='USB_5V', required_track_width_mm=0.5)
connect('J5', pin='VBUS', number='1', net='USB_VBUS', role='power_in', mcu_pin=None)
connect('R4', pin='VBUS', number='1', net='USB_VBUS', role='passive', mcu_pin=None)

net('V3V3', signal_class='power', voltage_domain='V3V3', required_track_width_mm=0.5)
connect('C1', pin='VCC', number='1', net='V3V3', role='passive', mcu_pin=None)
connect('C2', pin='VCC', number='1', net='V3V3', role='passive', mcu_pin=None)
connect('C3', pin='VCC', number='1', net='V3V3', role='passive', mcu_pin=None)
connect('C4', pin='VCC', number='1', net='V3V3', role='passive', mcu_pin=None)
connect('C5', pin='VCC', number='1', net='V3V3', role='passive', mcu_pin=None)
connect('C6', pin='VCC', number='1', net='V3V3', role='passive', mcu_pin=None)
connect('C7', pin='VCC', number='1', net='V3V3', role='passive', mcu_pin=None)
connect('C8', pin='VCC', number='1', net='V3V3', role='passive', mcu_pin=None)
connect('J2', pin='V3V3', number='1', net='V3V3', role='power_out', mcu_pin=None)
connect('J4', pin='VREF', number='1', net='V3V3', role='power_out', mcu_pin=None)
connect('Q2', pin='VCC', number='1', net='V3V3', role='power_in', mcu_pin=None)
connect('R2', pin='VCC', number='1', net='V3V3', role='passive', mcu_pin=None)
connect('R3', pin='VCC', number='1', net='V3V3', role='passive', mcu_pin=None)
connect('U1', pin='VDD', number='1', net='V3V3', role='power_in', mcu_pin=None)
connect('U2', pin='VDD', number='1', net='V3V3', role='power_in', mcu_pin=None)
connect('U5', pin='VOUT', number='2', net='V3V3', role='power_out', mcu_pin=None)

net('V5', signal_class='power', voltage_domain='V5', required_track_width_mm=0.5)
connect('C9', pin='VCC', number='1', net='V5', role='passive', mcu_pin=None)
connect('J11', pin='V5', number='1', net='V5', role='power_out', mcu_pin=None)
connect('J12', pin='V5', number='1', net='V5', role='power_out', mcu_pin=None)
connect('J13', pin='V5', number='1', net='V5', role='power_out', mcu_pin=None)
connect('J14', pin='V5', number='1', net='V5', role='power_out', mcu_pin=None)
connect('J15', pin='V5', number='1', net='V5', role='power_out', mcu_pin=None)
connect('J16', pin='V5', number='1', net='V5', role='power_out', mcu_pin=None)
connect('J17', pin='V5', number='1', net='V5', role='power_out', mcu_pin=None)
connect('J18', pin='V5', number='1', net='V5', role='power_out', mcu_pin=None)
connect('J19', pin='V5', number='1', net='V5', role='power_out', mcu_pin=None)
connect('J20', pin='V5', number='1', net='V5', role='power_out', mcu_pin=None)
connect('J21', pin='V5', number='1', net='V5', role='power_out', mcu_pin=None)
connect('J22', pin='V5', number='1', net='V5', role='power_out', mcu_pin=None)
connect('U4', pin='VOUT', number='2', net='V5', role='power_out', mcu_pin=None)
connect('U5', pin='VIN', number='1', net='V5', role='power_in', mcu_pin=None)
connect('U6', pin='VCC', number='1', net='V5', role='power_in', mcu_pin=None)

net('VBAT', signal_class='power', voltage_domain='VBAT', required_track_width_mm=2.0)
connect('D1', pin='K', number='1', net='VBAT', role='passive', mcu_pin=None)
connect('Q1', pin='CATHODE', number='2', net='VBAT', role='power_out', mcu_pin=None)
connect('U3', pin='IN', number='1', net='VBAT', role='power_in', mcu_pin=None)

net('VBAT_FUSED', signal_class='power', voltage_domain='VBAT', required_track_width_mm=2.0)
connect('F1', pin='OUT', number='2', net='VBAT_FUSED', role='passive', mcu_pin=None)
connect('Q1', pin='ANODE', number='1', net='VBAT_FUSED', role='power_in', mcu_pin=None)

net('VBAT_RAW', signal_class='power', voltage_domain='VBAT', required_track_width_mm=2.0)
connect('F1', pin='IN', number='1', net='VBAT_RAW', role='passive', mcu_pin=None)
connect('J1', pin='VBAT', number='1', net='VBAT_RAW', role='power_in', mcu_pin=None)

net('VSYS', signal_class='power', voltage_domain='VBAT', required_track_width_mm=0.5)
connect('C10', pin='VCC', number='1', net='VSYS', role='passive', mcu_pin=None)
connect('U3', pin='OUT', number='2', net='VSYS', role='power_out', mcu_pin=None)
connect('U4', pin='VIN', number='1', net='VSYS', role='power_in', mcu_pin=None)


place('C1', data={'ref': 'C1', 'x_mm': 24.0, 'y_mm': 76.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 4.243, 'courtyard_h_mm': 4.243, 'source': 'decoupling_row_seed', 'rationale': 'Seed row reserved for decoupling capacitors.'})
place('C10', data={'ref': 'C10', 'x_mm': 112.0, 'y_mm': 89.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 4.243, 'courtyard_h_mm': 4.243, 'source': 'decoupling_row_seed', 'rationale': 'Seed row reserved for decoupling capacitors.'})
place('C2', data={'ref': 'C2', 'x_mm': 46.0, 'y_mm': 76.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 4.243, 'courtyard_h_mm': 4.243, 'source': 'decoupling_row_seed', 'rationale': 'Seed row reserved for decoupling capacitors.'})
place('C3', data={'ref': 'C3', 'x_mm': 68.0, 'y_mm': 76.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 4.243, 'courtyard_h_mm': 4.243, 'source': 'decoupling_row_seed', 'rationale': 'Seed row reserved for decoupling capacitors.'})
place('C4', data={'ref': 'C4', 'x_mm': 90.0, 'y_mm': 76.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 4.243, 'courtyard_h_mm': 4.243, 'source': 'decoupling_row_seed', 'rationale': 'Seed row reserved for decoupling capacitors.'})
place('C5', data={'ref': 'C5', 'x_mm': 112.0, 'y_mm': 76.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 4.243, 'courtyard_h_mm': 4.243, 'source': 'decoupling_row_seed', 'rationale': 'Seed row reserved for decoupling capacitors.'})
place('C6', data={'ref': 'C6', 'x_mm': 24.0, 'y_mm': 89.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 4.243, 'courtyard_h_mm': 4.243, 'source': 'decoupling_row_seed', 'rationale': 'Seed row reserved for decoupling capacitors.'})
place('C7', data={'ref': 'C7', 'x_mm': 46.0, 'y_mm': 89.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 4.243, 'courtyard_h_mm': 4.243, 'source': 'decoupling_row_seed', 'rationale': 'Seed row reserved for decoupling capacitors.'})
place('C8', data={'ref': 'C8', 'x_mm': 68.0, 'y_mm': 89.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 4.243, 'courtyard_h_mm': 4.243, 'source': 'decoupling_row_seed', 'rationale': 'Seed row reserved for decoupling capacitors.'})
place('C9', data={'ref': 'C9', 'x_mm': 90.0, 'y_mm': 89.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 4.243, 'courtyard_h_mm': 4.243, 'source': 'decoupling_row_seed', 'rationale': 'Seed row reserved for decoupling capacitors.'})
place('D1', data={'ref': 'D1', 'x_mm': 74.0, 'y_mm': 5.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 4.243, 'courtyard_h_mm': 4.243, 'source': 'curated_anchor', 'rationale': 'Hand-tuned anchor from the reference layout seed.'})
place('D2', data={'ref': 'D2', 'x_mm': 120.0, 'y_mm': 86.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 6.708, 'courtyard_h_mm': 6.708, 'source': 'curated_anchor', 'rationale': 'Hand-tuned anchor from the reference layout seed.'})
place('F1', data={'ref': 'F1', 'x_mm': 38.0, 'y_mm': 5.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 4.243, 'courtyard_h_mm': 4.243, 'source': 'curated_anchor', 'rationale': 'Hand-tuned anchor from the reference layout seed.'})
place('J1', data={'ref': 'J1', 'x_mm': 20.0, 'y_mm': 5.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 4.243, 'courtyard_h_mm': 4.243, 'source': 'curated_anchor', 'rationale': 'Hand-tuned anchor from the reference layout seed.'})
place('J11', data={'ref': 'J11', 'x_mm': 9.0, 'y_mm': 7.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 7.348, 'courtyard_h_mm': 7.348, 'source': 'connector_edge_seed', 'rationale': 'Seed pushed to a board edge for connector access.'})
place('J12', data={'ref': 'J12', 'x_mm': 9.0, 'y_mm': 22.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 7.348, 'courtyard_h_mm': 7.348, 'source': 'connector_edge_seed', 'rationale': 'Seed pushed to a board edge for connector access.'})
place('J13', data={'ref': 'J13', 'x_mm': 9.0, 'y_mm': 37.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 7.348, 'courtyard_h_mm': 7.348, 'source': 'connector_edge_seed', 'rationale': 'Seed pushed to a board edge for connector access.'})
place('J14', data={'ref': 'J14', 'x_mm': 9.0, 'y_mm': 52.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 7.348, 'courtyard_h_mm': 7.348, 'source': 'connector_edge_seed', 'rationale': 'Seed pushed to a board edge for connector access.'})
place('J15', data={'ref': 'J15', 'x_mm': 9.0, 'y_mm': 67.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 7.348, 'courtyard_h_mm': 7.348, 'source': 'connector_edge_seed', 'rationale': 'Seed pushed to a board edge for connector access.'})
place('J16', data={'ref': 'J16', 'x_mm': 9.0, 'y_mm': 82.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 7.348, 'courtyard_h_mm': 7.348, 'source': 'connector_edge_seed', 'rationale': 'Seed pushed to a board edge for connector access.'})
place('J17', data={'ref': 'J17', 'x_mm': 151.0, 'y_mm': 7.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 7.348, 'courtyard_h_mm': 7.348, 'source': 'connector_edge_seed', 'rationale': 'Seed pushed to a board edge for connector access.'})
place('J18', data={'ref': 'J18', 'x_mm': 151.0, 'y_mm': 22.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 7.348, 'courtyard_h_mm': 7.348, 'source': 'connector_edge_seed', 'rationale': 'Seed pushed to a board edge for connector access.'})
place('J19', data={'ref': 'J19', 'x_mm': 151.0, 'y_mm': 37.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 7.348, 'courtyard_h_mm': 7.348, 'source': 'connector_edge_seed', 'rationale': 'Seed pushed to a board edge for connector access.'})
place('J2', data={'ref': 'J2', 'x_mm': 140.0, 'y_mm': 95.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 5.196, 'courtyard_h_mm': 5.196, 'source': 'curated_anchor', 'rationale': 'Hand-tuned anchor from the reference layout seed.'})
place('J20', data={'ref': 'J20', 'x_mm': 151.0, 'y_mm': 52.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 7.348, 'courtyard_h_mm': 7.348, 'source': 'connector_edge_seed', 'rationale': 'Seed pushed to a board edge for connector access.'})
place('J21', data={'ref': 'J21', 'x_mm': 151.0, 'y_mm': 67.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 7.348, 'courtyard_h_mm': 7.348, 'source': 'connector_edge_seed', 'rationale': 'Seed pushed to a board edge for connector access.'})
place('J22', data={'ref': 'J22', 'x_mm': 151.0, 'y_mm': 82.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 7.348, 'courtyard_h_mm': 7.348, 'source': 'connector_edge_seed', 'rationale': 'Seed pushed to a board edge for connector access.'})
place('J3', data={'ref': 'J3', 'x_mm': 80.0, 'y_mm': 5.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 5.196, 'courtyard_h_mm': 5.196, 'source': 'curated_anchor', 'rationale': 'Hand-tuned anchor from the reference layout seed.'})
place('J4', data={'ref': 'J4', 'x_mm': 104.0, 'y_mm': 69.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 6.708, 'courtyard_h_mm': 6.708, 'source': 'curated_anchor', 'rationale': 'Hand-tuned anchor from the reference layout seed.'})
place('J5', data={'ref': 'J5', 'x_mm': 120.0, 'y_mm': 95.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 6.0, 'courtyard_h_mm': 6.0, 'source': 'curated_anchor', 'rationale': 'Hand-tuned anchor from the reference layout seed.'})
place('Q1', data={'ref': 'Q1', 'x_mm': 56.0, 'y_mm': 5.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 5.196, 'courtyard_h_mm': 5.196, 'source': 'curated_anchor', 'rationale': 'Hand-tuned anchor from the reference layout seed.'})
place('Q2', data={'ref': 'Q2', 'x_mm': 124.0, 'y_mm': 48.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 6.0, 'courtyard_h_mm': 6.0, 'source': 'curated_anchor', 'rationale': 'Hand-tuned anchor from the reference layout seed.'})
place('R1', data={'ref': 'R1', 'x_mm': 104.0, 'y_mm': 20.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 4.243, 'courtyard_h_mm': 4.243, 'source': 'curated_anchor', 'rationale': 'Hand-tuned anchor from the reference layout seed.'})
place('R2', data={'ref': 'R2', 'x_mm': 42.0, 'y_mm': 48.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 4.243, 'courtyard_h_mm': 4.243, 'source': 'curated_anchor', 'rationale': 'Hand-tuned anchor from the reference layout seed.'})
place('R3', data={'ref': 'R3', 'x_mm': 58.0, 'y_mm': 48.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 4.243, 'courtyard_h_mm': 4.243, 'source': 'curated_anchor', 'rationale': 'Hand-tuned anchor from the reference layout seed.'})
place('R4', data={'ref': 'R4', 'x_mm': 60.0, 'y_mm': 27.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 4.243, 'courtyard_h_mm': 4.243, 'source': 'curated_anchor', 'rationale': 'Hand-tuned anchor from the reference layout seed.'})
place('U1', data={'ref': 'U1', 'x_mm': 70.0, 'y_mm': 37.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 21.0, 'courtyard_h_mm': 21.0, 'source': 'curated_anchor', 'rationale': 'Hand-tuned anchor from the reference layout seed.'})
place('U2', data={'ref': 'U2', 'x_mm': 22.0, 'y_mm': 48.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 6.708, 'courtyard_h_mm': 6.708, 'source': 'curated_anchor', 'rationale': 'Hand-tuned anchor from the reference layout seed.'})
place('U3', data={'ref': 'U3', 'x_mm': 92.0, 'y_mm': 5.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 6.0, 'courtyard_h_mm': 6.0, 'source': 'curated_anchor', 'rationale': 'Hand-tuned anchor from the reference layout seed.'})
place('U4', data={'ref': 'U4', 'x_mm': 112.0, 'y_mm': 18.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 5.196, 'courtyard_h_mm': 5.196, 'source': 'curated_anchor', 'rationale': 'Hand-tuned anchor from the reference layout seed.'})
place('U5', data={'ref': 'U5', 'x_mm': 132.0, 'y_mm': 18.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 5.196, 'courtyard_h_mm': 5.196, 'source': 'curated_anchor', 'rationale': 'Hand-tuned anchor from the reference layout seed.'})
place('U6', data={'ref': 'U6', 'x_mm': 90.0, 'y_mm': 27.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 7.348, 'courtyard_h_mm': 7.348, 'source': 'curated_anchor', 'rationale': 'Hand-tuned anchor from the reference layout seed.'})

constraint(data={'kind': 'board_keepout', 'target_ref': None, 'params': {'width_mm': 160.0, 'height_mm': 100.0, 'edge_margin_mm': 0.15}, 'derived_from': 'mechanical.envelope + manufacturing.pcb.min_clearance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'mounting_hole_keepout', 'target_ref': None, 'params': {'x_mm': 6.0, 'y_mm': 6.0, 'keepout_radius_mm': 2.6}, 'derived_from': 'mechanical.mounting_holes[0] + mechanical.assembly_clearance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'mounting_hole_keepout', 'target_ref': None, 'params': {'x_mm': 154.0, 'y_mm': 6.0, 'keepout_radius_mm': 2.6}, 'derived_from': 'mechanical.mounting_holes[1] + mechanical.assembly_clearance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'mounting_hole_keepout', 'target_ref': None, 'params': {'x_mm': 6.0, 'y_mm': 94.0, 'keepout_radius_mm': 2.6}, 'derived_from': 'mechanical.mounting_holes[2] + mechanical.assembly_clearance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'mounting_hole_keepout', 'target_ref': None, 'params': {'x_mm': 154.0, 'y_mm': 94.0, 'keepout_radius_mm': 2.6}, 'derived_from': 'mechanical.mounting_holes[3] + mechanical.assembly_clearance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'connector_edge', 'target_ref': 'J1', 'params': {'side': 'front', 'max_edge_distance_mm': 10.0}, 'derived_from': 'mechanical.connector_interfaces + mechanical.max_connector_edge_distance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'connector_edge', 'target_ref': 'J3', 'params': {'side': 'front', 'max_edge_distance_mm': 10.0}, 'derived_from': 'mechanical.connector_interfaces + mechanical.max_connector_edge_distance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'connector_edge', 'target_ref': 'J5', 'params': {'side': 'rear', 'max_edge_distance_mm': 10.0}, 'derived_from': 'mechanical.connector_interfaces + mechanical.max_connector_edge_distance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'connector_edge', 'target_ref': 'J2', 'params': {'side': 'rear', 'max_edge_distance_mm': 10.0}, 'derived_from': 'mechanical.connector_interfaces + mechanical.max_connector_edge_distance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'connector_edge', 'target_ref': 'J11', 'params': {'side': 'left', 'max_edge_distance_mm': 10.0}, 'derived_from': 'mechanical.connector_interfaces + mechanical.max_connector_edge_distance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'connector_edge', 'target_ref': 'J12', 'params': {'side': 'left', 'max_edge_distance_mm': 10.0}, 'derived_from': 'mechanical.connector_interfaces + mechanical.max_connector_edge_distance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'connector_edge', 'target_ref': 'J13', 'params': {'side': 'left', 'max_edge_distance_mm': 10.0}, 'derived_from': 'mechanical.connector_interfaces + mechanical.max_connector_edge_distance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'connector_edge', 'target_ref': 'J14', 'params': {'side': 'left', 'max_edge_distance_mm': 10.0}, 'derived_from': 'mechanical.connector_interfaces + mechanical.max_connector_edge_distance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'connector_edge', 'target_ref': 'J15', 'params': {'side': 'left', 'max_edge_distance_mm': 10.0}, 'derived_from': 'mechanical.connector_interfaces + mechanical.max_connector_edge_distance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'connector_edge', 'target_ref': 'J16', 'params': {'side': 'left', 'max_edge_distance_mm': 10.0}, 'derived_from': 'mechanical.connector_interfaces + mechanical.max_connector_edge_distance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'connector_edge', 'target_ref': 'J17', 'params': {'side': 'right', 'max_edge_distance_mm': 10.0}, 'derived_from': 'mechanical.connector_interfaces + mechanical.max_connector_edge_distance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'connector_edge', 'target_ref': 'J18', 'params': {'side': 'right', 'max_edge_distance_mm': 10.0}, 'derived_from': 'mechanical.connector_interfaces + mechanical.max_connector_edge_distance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'connector_edge', 'target_ref': 'J19', 'params': {'side': 'right', 'max_edge_distance_mm': 10.0}, 'derived_from': 'mechanical.connector_interfaces + mechanical.max_connector_edge_distance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'connector_edge', 'target_ref': 'J20', 'params': {'side': 'right', 'max_edge_distance_mm': 10.0}, 'derived_from': 'mechanical.connector_interfaces + mechanical.max_connector_edge_distance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'connector_edge', 'target_ref': 'J21', 'params': {'side': 'right', 'max_edge_distance_mm': 10.0}, 'derived_from': 'mechanical.connector_interfaces + mechanical.max_connector_edge_distance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'connector_edge', 'target_ref': 'J22', 'params': {'side': 'right', 'max_edge_distance_mm': 10.0}, 'derived_from': 'mechanical.connector_interfaces + mechanical.max_connector_edge_distance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'decoupling_proximity', 'target_ref': 'C1', 'params': {'power_nets': ['GND', 'V3V3'], 'target_ref': None, 'max_distance_mm': 12.0}, 'derived_from': 'graph decoupling component pins + decoupling_target_ref', 'enforced': False, 'rationale': 'Cap-to-IC association is not modelled in the netlist; proximity enforcement is deferred.'})
constraint(data={'kind': 'decoupling_proximity', 'target_ref': 'C2', 'params': {'power_nets': ['GND', 'V3V3'], 'target_ref': None, 'max_distance_mm': 12.0}, 'derived_from': 'graph decoupling component pins + decoupling_target_ref', 'enforced': False, 'rationale': 'Cap-to-IC association is not modelled in the netlist; proximity enforcement is deferred.'})
constraint(data={'kind': 'decoupling_proximity', 'target_ref': 'C3', 'params': {'power_nets': ['GND', 'V3V3'], 'target_ref': None, 'max_distance_mm': 12.0}, 'derived_from': 'graph decoupling component pins + decoupling_target_ref', 'enforced': False, 'rationale': 'Cap-to-IC association is not modelled in the netlist; proximity enforcement is deferred.'})
constraint(data={'kind': 'decoupling_proximity', 'target_ref': 'C4', 'params': {'power_nets': ['GND', 'V3V3'], 'target_ref': None, 'max_distance_mm': 12.0}, 'derived_from': 'graph decoupling component pins + decoupling_target_ref', 'enforced': False, 'rationale': 'Cap-to-IC association is not modelled in the netlist; proximity enforcement is deferred.'})
constraint(data={'kind': 'decoupling_proximity', 'target_ref': 'C5', 'params': {'power_nets': ['GND', 'V3V3'], 'target_ref': None, 'max_distance_mm': 12.0}, 'derived_from': 'graph decoupling component pins + decoupling_target_ref', 'enforced': False, 'rationale': 'Cap-to-IC association is not modelled in the netlist; proximity enforcement is deferred.'})
constraint(data={'kind': 'decoupling_proximity', 'target_ref': 'C6', 'params': {'power_nets': ['GND', 'V3V3'], 'target_ref': None, 'max_distance_mm': 12.0}, 'derived_from': 'graph decoupling component pins + decoupling_target_ref', 'enforced': False, 'rationale': 'Cap-to-IC association is not modelled in the netlist; proximity enforcement is deferred.'})
constraint(data={'kind': 'decoupling_proximity', 'target_ref': 'C7', 'params': {'power_nets': ['GND', 'V3V3'], 'target_ref': None, 'max_distance_mm': 12.0}, 'derived_from': 'graph decoupling component pins + decoupling_target_ref', 'enforced': False, 'rationale': 'Cap-to-IC association is not modelled in the netlist; proximity enforcement is deferred.'})
constraint(data={'kind': 'decoupling_proximity', 'target_ref': 'C8', 'params': {'power_nets': ['GND', 'V3V3'], 'target_ref': None, 'max_distance_mm': 12.0}, 'derived_from': 'graph decoupling component pins + decoupling_target_ref', 'enforced': False, 'rationale': 'Cap-to-IC association is not modelled in the netlist; proximity enforcement is deferred.'})
constraint(data={'kind': 'thermal_spacing', 'target_ref': 'Q1', 'params': {'min_spacing_mm': 8.0}, 'derived_from': 'graph power-category component', 'enforced': False, 'rationale': 'Advisory spacing only; thermal qualification requires load testing.'})
constraint(data={'kind': 'thermal_spacing', 'target_ref': 'U3', 'params': {'min_spacing_mm': 8.0}, 'derived_from': 'graph power-category component', 'enforced': False, 'rationale': 'Advisory spacing only; thermal qualification requires load testing.'})
constraint(data={'kind': 'thermal_spacing', 'target_ref': 'U4', 'params': {'min_spacing_mm': 8.0}, 'derived_from': 'graph power-category component', 'enforced': False, 'rationale': 'Advisory spacing only; thermal qualification requires load testing.'})
constraint(data={'kind': 'thermal_spacing', 'target_ref': 'U5', 'params': {'min_spacing_mm': 8.0}, 'derived_from': 'graph power-category component', 'enforced': False, 'rationale': 'Advisory spacing only; thermal qualification requires load testing.'})
constraint(data={'kind': 'thermal_spacing', 'target_ref': 'Q2', 'params': {'min_spacing_mm': 8.0}, 'derived_from': 'graph power-category component', 'enforced': False, 'rationale': 'Advisory spacing only; thermal qualification requires load testing.'})
constraint(data={'kind': 'thermal_spacing', 'target_ref': 'J11', 'params': {'min_spacing_mm': 8.0}, 'derived_from': 'graph power-category component', 'enforced': False, 'rationale': 'Advisory spacing only; thermal qualification requires load testing.'})
constraint(data={'kind': 'thermal_spacing', 'target_ref': 'J12', 'params': {'min_spacing_mm': 8.0}, 'derived_from': 'graph power-category component', 'enforced': False, 'rationale': 'Advisory spacing only; thermal qualification requires load testing.'})
constraint(data={'kind': 'thermal_spacing', 'target_ref': 'J13', 'params': {'min_spacing_mm': 8.0}, 'derived_from': 'graph power-category component', 'enforced': False, 'rationale': 'Advisory spacing only; thermal qualification requires load testing.'})
constraint(data={'kind': 'thermal_spacing', 'target_ref': 'J14', 'params': {'min_spacing_mm': 8.0}, 'derived_from': 'graph power-category component', 'enforced': False, 'rationale': 'Advisory spacing only; thermal qualification requires load testing.'})
constraint(data={'kind': 'thermal_spacing', 'target_ref': 'J15', 'params': {'min_spacing_mm': 8.0}, 'derived_from': 'graph power-category component', 'enforced': False, 'rationale': 'Advisory spacing only; thermal qualification requires load testing.'})
constraint(data={'kind': 'thermal_spacing', 'target_ref': 'J16', 'params': {'min_spacing_mm': 8.0}, 'derived_from': 'graph power-category component', 'enforced': False, 'rationale': 'Advisory spacing only; thermal qualification requires load testing.'})
constraint(data={'kind': 'thermal_spacing', 'target_ref': 'J17', 'params': {'min_spacing_mm': 8.0}, 'derived_from': 'graph power-category component', 'enforced': False, 'rationale': 'Advisory spacing only; thermal qualification requires load testing.'})
constraint(data={'kind': 'thermal_spacing', 'target_ref': 'J18', 'params': {'min_spacing_mm': 8.0}, 'derived_from': 'graph power-category component', 'enforced': False, 'rationale': 'Advisory spacing only; thermal qualification requires load testing.'})
constraint(data={'kind': 'thermal_spacing', 'target_ref': 'J19', 'params': {'min_spacing_mm': 8.0}, 'derived_from': 'graph power-category component', 'enforced': False, 'rationale': 'Advisory spacing only; thermal qualification requires load testing.'})
constraint(data={'kind': 'thermal_spacing', 'target_ref': 'J20', 'params': {'min_spacing_mm': 8.0}, 'derived_from': 'graph power-category component', 'enforced': False, 'rationale': 'Advisory spacing only; thermal qualification requires load testing.'})
constraint(data={'kind': 'thermal_spacing', 'target_ref': 'J21', 'params': {'min_spacing_mm': 8.0}, 'derived_from': 'graph power-category component', 'enforced': False, 'rationale': 'Advisory spacing only; thermal qualification requires load testing.'})
constraint(data={'kind': 'thermal_spacing', 'target_ref': 'J22', 'params': {'min_spacing_mm': 8.0}, 'derived_from': 'graph power-category component', 'enforced': False, 'rationale': 'Advisory spacing only; thermal qualification requires load testing.'})

semantic_schematic = board.to_dict()
