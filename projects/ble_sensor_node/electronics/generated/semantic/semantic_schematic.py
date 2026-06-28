"""Generated executable semantic schematic for agent review.

This file is intentionally compact and pin-name based. It can be executed
to reconstruct the normalized semantic_schematic model. Native EDA/CAD
artifacts are generated from typed artifacts; edit the spec or graph-producing
blocks when changing a generated design.
"""

from hw_codesign.semantic_schematic import SemanticBoard, pin

board = SemanticBoard(
    project='ble_sensor_node',
    revision='r1',
    purpose='LLM-suited schematic representation derived from typed graph; native EDA files are generated outputs.',
    source_graph='/Users/mrcha033/Documents/hw-cli/projects/ble_sensor_node/electronics/generated/electrical_graph.json',
    board_width_mm=50.0,
    board_height_mm=35.0,
)
component = board.component
net = board.net
connect = board.connect
place = board.place
constraint = board.constraint

component(
    'BT1',
    role='battery',
    value='LiPo 400mAh',
    component_id='jst_ph_2pin',
    mpn='S2B-PH-K-S',
    manufacturer='JST',
    package='TH-2Pin',
    footprint='Connector_JST:JST_PH_S2B-PH-K_1x02_P2.00mm_Horizontal',
    pins=[
        pin('1', 'VBAT', net='VBAT', role='power_in', voltage_domain='VBAT', mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

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
    role='bulk_cap',
    value='10uF',
    component_id='grm32_10u_50v',
    mpn='GRM32ER71H106KA12L',
    manufacturer='Murata',
    package='1210',
    footprint='Capacitor_SMD:C_1210_3225Metric',
    pins=[
        pin('1', 'VCC', net='VBAT', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'C4',
    role='bulk_cap',
    value='10uF',
    component_id='grm32_10u_50v',
    mpn='GRM32ER71H106KA12L',
    manufacturer='Murata',
    package='1210',
    footprint='Capacitor_SMD:C_1210_3225Metric',
    pins=[
        pin('1', 'VCC', net='V3V3', role='passive', voltage_domain=None, mcu_pin=None),
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
    value='500mA Fuse',
    component_id='littelfuse_0498080',
    mpn='Littelfuse-0498080.M',
    manufacturer='Littelfuse',
    package='MIDI',
    footprint='HW_Curated:MIDI_Fuse',
    pins=[
        pin('1', 'IN', net='USB_VBUS', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'OUT', net='USB_FUSED', role='passive', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'J1',
    role='power_input',
    value='USB-C CHARGE',
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
    'J2',
    role='debug',
    value='SWD DEBUG',
    component_id='samtec_ftsh_105',
    mpn='Samtec-FTSH-105-01-L-DV-K',
    manufacturer='Samtec',
    package='FTSH-10',
    footprint='Connector_Samtec:FTSH-105',
    pins=[
        pin('1', 'GND_IN', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('2', 'SWDIO', net='SWDIO', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('3', 'SWO', net='SWO', role='output', voltage_domain=None, mcu_pin=None),
        pin('4', 'NRST', net='NRST', role='bidirectional', voltage_domain=None, mcu_pin=None),
        pin('5', 'TX', net='UART_TX', role='output', voltage_domain=None, mcu_pin=None),
        pin('6', 'VREF', net='V3V3', role='power_out', voltage_domain='V3V3', mcu_pin=None),
        pin('7', 'SWDCLK', net='SWDCLK', role='input', voltage_domain=None, mcu_pin=None),
        pin('8', 'RX', net='UART_RX', role='input', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'LD1',
    role='regulator',
    value='3V3 LDO',
    component_id='ap2112k_33trg1',
    mpn='AP2112K-3.3TRG1',
    manufacturer='Diodes Incorporated',
    package='SOT-23-5',
    footprint='Package_TO_SOT_SMD:SOT-23-5',
    pins=[
        pin('1', 'EN', net='V3V3', role='input', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('3', 'VIN', net='VBAT', role='power_in', voltage_domain='VBAT', mcu_pin=None),
        pin('4', 'NC', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('5', 'VOUT', net='V3V3', role='power_out', voltage_domain='V3V3', mcu_pin=None),
    ],
)

component(
    'Q1',
    role='reverse_polarity',
    value='Ideal Diode',
    component_id='lm74700qdbvrq1',
    mpn='LM74700QDBVRQ1',
    manufacturer='Texas Instruments',
    package='SOT-23-6',
    footprint='Package_TO_SOT_SMD:SOT-23-6',
    pins=[
        pin('1', 'ANODE', net='USB_FUSED', role='power_in', voltage_domain='V3V3', mcu_pin=None),
        pin('2', 'CATHODE', net='USB_PROT', role='power_out', voltage_domain='V3V3', mcu_pin=None),
        pin('3', 'GND', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)

component(
    'R1',
    role='pullup',
    value='4K7',
    component_id='rc0603_4k7',
    mpn='RC0603FR-074K7L',
    manufacturer='Yageo',
    package='0603',
    footprint='Resistor_SMD:R_0603_1608Metric',
    pins=[
        pin('1', 'VCC', net='V3V3', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'SCL', net='I2C_SCL', role='passive', voltage_domain=None, mcu_pin=None),
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
        pin('2', 'SDA', net='I2C_SDA', role='passive', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'R3',
    role='led_resistor',
    value='1K',
    component_id='rc0603_1k',
    mpn='RC0603FR-071KL',
    manufacturer='Yageo',
    package='R0603',
    footprint='Resistor_SMD:R_0603_1608Metric',
    pins=[
        pin('1', 'A', net='V3V3', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'K', net='LED_BLE', role='passive', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'R4',
    role='charge_set',
    value='10K',
    component_id='rc0603_10k',
    mpn='RC0603FR-0710KL',
    manufacturer='Yageo',
    package='R0603',
    footprint='Resistor_SMD:R_0603_1608Metric',
    pins=[
        pin('1', 'A', net='CHG_ISET', role='passive', voltage_domain=None, mcu_pin=None),
        pin('2', 'GND', net='GND', role='passive', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'U1',
    role='mcu',
    value='nRF52840',
    component_id='nrf52840_qiaa',
    mpn='nRF52840-QIAA',
    manufacturer='Nordic Semiconductor',
    package='aQFN-73',
    footprint='Nordic_nRF52840:nRF52840-QIAA',
    pins=[
        pin('1', 'VDD', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin=None),
        pin('2', 'VSS', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('3', 'VDDPA', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin=None),
        pin('4', 'VDDMAIN', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin=None),
        pin('5', 'P0.02', net='I2C_SCL', role='open_drain', voltage_domain=None, mcu_pin='P0.02'),
        pin('6', 'P0.03', net='I2C_SDA', role='open_drain', voltage_domain=None, mcu_pin='P0.03'),
        pin('7', 'P0.04', net='CHG_STAT', role='input', voltage_domain=None, mcu_pin='P0.04'),
        pin('8', 'P0.05', net='TEMP_INT', role='input', voltage_domain=None, mcu_pin='P0.05'),
        pin('9', 'P0.06', net='FUEL_ALRT', role='input', voltage_domain=None, mcu_pin='P0.06'),
        pin('10', 'P0.08', net='LED_BLE', role='output', voltage_domain=None, mcu_pin='P0.08'),
        pin('11', 'NRESET', net='NRST', role='bidirectional', voltage_domain=None, mcu_pin='NRESET'),
        pin('12', 'P0.28', net='UART_TX', role='output', voltage_domain=None, mcu_pin='P0.28'),
        pin('13', 'P0.29', net='UART_RX', role='input', voltage_domain=None, mcu_pin='P0.29'),
        pin('14', 'SWDCLK', net='SWDCLK', role='input', voltage_domain=None, mcu_pin='SWDCLK'),
        pin('15', 'SWDIO', net='SWDIO', role='bidirectional', voltage_domain=None, mcu_pin='SWDIO'),
        pin('16', 'SWO', net='SWO', role='output', voltage_domain=None, mcu_pin='SWO'),
        pin('17', 'USB_DP', net='USB_DP', role='bidirectional', voltage_domain=None, mcu_pin='D+'),
        pin('18', 'USB_DM', net='USB_DM', role='bidirectional', voltage_domain=None, mcu_pin='D-'),
    ],
)

component(
    'U2',
    role='charger',
    value='LiPo Charger',
    component_id='bq24079rgtt',
    mpn='BQ24079RGTT',
    manufacturer='Texas Instruments',
    package='SOT-23-8',
    footprint='Package_TO_SOT_SMD:SOT-23-8',
    pins=[
        pin('1', 'IN', net='USB_PROT', role='power_in', voltage_domain='V3V3', mcu_pin=None),
        pin('2', 'VSS', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('3', 'EN1', net='V3V3', role='input', voltage_domain=None, mcu_pin=None),
        pin('4', 'EN2', net='GND', role='input', voltage_domain=None, mcu_pin=None),
        pin('5', 'OUT', net='VBAT', role='power_out', voltage_domain='VBAT', mcu_pin=None),
        pin('6', 'STAT', net='CHG_STAT', role='output', voltage_domain=None, mcu_pin=None),
        pin('7', 'TE', net='V3V3', role='input', voltage_domain=None, mcu_pin=None),
        pin('8', 'ISET', net='CHG_ISET', role='passive', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'U3',
    role='fuel_gauge',
    value='Fuel Gauge',
    component_id='bq27441drzr_g1a',
    mpn='BQ27441DRZR-G1A',
    manufacturer='Texas Instruments',
    package='VSON-9',
    footprint='Package_SON:VSON-9_2x3mm_P0.5mm',
    pins=[
        pin('1', 'SDA', net='I2C_SDA', role='open_drain', voltage_domain=None, mcu_pin=None),
        pin('2', 'SCL', net='I2C_SCL', role='open_drain', voltage_domain=None, mcu_pin=None),
        pin('3', 'GPO', net='FUEL_ALRT', role='output', voltage_domain=None, mcu_pin=None),
        pin('4', 'VSS', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
        pin('5', 'SRN', net='VBAT', role='passive', voltage_domain=None, mcu_pin=None),
        pin('6', 'SRP', net='VBAT', role='passive', voltage_domain=None, mcu_pin=None),
        pin('7', 'BAT', net='VBAT', role='power_in', voltage_domain='VBAT', mcu_pin=None),
        pin('8', 'VCC', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin=None),
        pin('9', 'REGIN', net='VBAT', role='passive', voltage_domain=None, mcu_pin=None),
    ],
)

component(
    'U5',
    role='env_sensor',
    value='Temp/Humidity',
    component_id='sht31_dis_b',
    mpn='SHT31-DIS-B2.5KS',
    manufacturer='Sensirion',
    package='DFN-8',
    footprint='Package_DFN_QFN:DFN-8-1EP_2x2.5mm_P0.5mm',
    pins=[
        pin('1', 'SDA', net='I2C_SDA', role='open_drain', voltage_domain=None, mcu_pin=None),
        pin('2', 'ADDR', net='GND', role='input', voltage_domain=None, mcu_pin=None),
        pin('3', 'ALERT', net='TEMP_INT', role='output', voltage_domain=None, mcu_pin=None),
        pin('4', 'SCL', net='I2C_SCL', role='open_drain', voltage_domain=None, mcu_pin=None),
        pin('5', 'VDD', net='V3V3', role='power_in', voltage_domain='V3V3', mcu_pin=None),
        pin('6', 'nRESET', net='V3V3', role='input', voltage_domain=None, mcu_pin=None),
        pin('7', 'R', net='GND', role='passive', voltage_domain=None, mcu_pin=None),
        pin('8', 'VSS', net='GND', role='ground', voltage_domain='GND', mcu_pin=None),
    ],
)


net('CHG_ISET', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.15)
connect('R4', pin='A', number='1', net='CHG_ISET', role='passive', mcu_pin=None)
connect('U2', pin='ISET', number='8', net='CHG_ISET', role='passive', mcu_pin=None)

net('CHG_STAT', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.15)
connect('U1', pin='P0.04', number='7', net='CHG_STAT', role='input', mcu_pin='P0.04')
connect('U2', pin='STAT', number='6', net='CHG_STAT', role='output', mcu_pin=None)

net('FUEL_ALRT', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.15)
connect('U1', pin='P0.06', number='9', net='FUEL_ALRT', role='input', mcu_pin='P0.06')
connect('U3', pin='GPO', number='3', net='FUEL_ALRT', role='output', mcu_pin=None)

net('GND', signal_class='ground', voltage_domain='GND', required_track_width_mm=0.15)
connect('BT1', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('C1', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('C2', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('C3', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('C4', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('D1', pin='GND', number='5', net='GND', role='ground', mcu_pin=None)
connect('J1', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('J2', pin='GND_IN', number='1', net='GND', role='ground', mcu_pin=None)
connect('LD1', pin='GND', number='2', net='GND', role='ground', mcu_pin=None)
connect('LD1', pin='NC', number='4', net='GND', role='ground', mcu_pin=None)
connect('Q1', pin='GND', number='3', net='GND', role='ground', mcu_pin=None)
connect('R4', pin='GND', number='2', net='GND', role='passive', mcu_pin=None)
connect('U1', pin='VSS', number='2', net='GND', role='ground', mcu_pin=None)
connect('U2', pin='VSS', number='2', net='GND', role='ground', mcu_pin=None)
connect('U2', pin='EN2', number='4', net='GND', role='input', mcu_pin=None)
connect('U3', pin='VSS', number='4', net='GND', role='ground', mcu_pin=None)
connect('U5', pin='ADDR', number='2', net='GND', role='input', mcu_pin=None)
connect('U5', pin='R', number='7', net='GND', role='passive', mcu_pin=None)
connect('U5', pin='VSS', number='8', net='GND', role='ground', mcu_pin=None)

net('I2C_SCL', signal_class='i2c', voltage_domain='V3V3', required_track_width_mm=0.15)
connect('R1', pin='SCL', number='2', net='I2C_SCL', role='passive', mcu_pin=None)
connect('U1', pin='P0.02', number='5', net='I2C_SCL', role='open_drain', mcu_pin='P0.02')
connect('U3', pin='SCL', number='2', net='I2C_SCL', role='open_drain', mcu_pin=None)
connect('U5', pin='SCL', number='4', net='I2C_SCL', role='open_drain', mcu_pin=None)

net('I2C_SDA', signal_class='i2c', voltage_domain='V3V3', required_track_width_mm=0.15)
connect('R2', pin='SDA', number='2', net='I2C_SDA', role='passive', mcu_pin=None)
connect('U1', pin='P0.03', number='6', net='I2C_SDA', role='open_drain', mcu_pin='P0.03')
connect('U3', pin='SDA', number='1', net='I2C_SDA', role='open_drain', mcu_pin=None)
connect('U5', pin='SDA', number='1', net='I2C_SDA', role='open_drain', mcu_pin=None)

net('LED_BLE', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.15)
connect('R3', pin='K', number='2', net='LED_BLE', role='passive', mcu_pin=None)
connect('U1', pin='P0.08', number='10', net='LED_BLE', role='output', mcu_pin='P0.08')

net('NRST', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.15)
connect('J2', pin='NRST', number='4', net='NRST', role='bidirectional', mcu_pin=None)
connect('U1', pin='NRESET', number='11', net='NRST', role='bidirectional', mcu_pin='NRESET')

net('SWDCLK', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.15)
connect('J2', pin='SWDCLK', number='7', net='SWDCLK', role='input', mcu_pin=None)
connect('U1', pin='SWDCLK', number='14', net='SWDCLK', role='input', mcu_pin='SWDCLK')

net('SWDIO', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.15)
connect('J2', pin='SWDIO', number='2', net='SWDIO', role='bidirectional', mcu_pin=None)
connect('U1', pin='SWDIO', number='15', net='SWDIO', role='bidirectional', mcu_pin='SWDIO')

net('SWO', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.15)
connect('J2', pin='SWO', number='3', net='SWO', role='output', mcu_pin=None)
connect('U1', pin='SWO', number='16', net='SWO', role='output', mcu_pin='SWO')

net('TEMP_INT', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.15)
connect('U1', pin='P0.05', number='8', net='TEMP_INT', role='input', mcu_pin='P0.05')
connect('U5', pin='ALERT', number='3', net='TEMP_INT', role='output', mcu_pin=None)

net('UART_RX', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.15)
connect('J2', pin='RX', number='8', net='UART_RX', role='input', mcu_pin=None)
connect('U1', pin='P0.29', number='13', net='UART_RX', role='input', mcu_pin='P0.29')

net('UART_TX', signal_class='signal', voltage_domain='V3V3', required_track_width_mm=0.15)
connect('J2', pin='TX', number='5', net='UART_TX', role='output', mcu_pin=None)
connect('U1', pin='P0.28', number='12', net='UART_TX', role='output', mcu_pin='P0.28')

net('USB_DM', signal_class='usb', voltage_domain='V3V3', required_track_width_mm=0.15)
connect('D1', pin='DM_OUT', number='4', net='USB_DM', role='bidirectional', mcu_pin=None)
connect('U1', pin='USB_DM', number='18', net='USB_DM', role='bidirectional', mcu_pin='D-')

net('USB_DM_RAW', signal_class='usb', voltage_domain='V3V3', required_track_width_mm=0.15)
connect('D1', pin='DM_IN', number='3', net='USB_DM_RAW', role='bidirectional', mcu_pin=None)
connect('J1', pin='D-', number='4', net='USB_DM_RAW', role='bidirectional', mcu_pin=None)

net('USB_DP', signal_class='usb', voltage_domain='V3V3', required_track_width_mm=0.15)
connect('D1', pin='DP_OUT', number='2', net='USB_DP', role='bidirectional', mcu_pin=None)
connect('U1', pin='USB_DP', number='17', net='USB_DP', role='bidirectional', mcu_pin='D+')

net('USB_DP_RAW', signal_class='usb', voltage_domain='V3V3', required_track_width_mm=0.15)
connect('D1', pin='DP_IN', number='1', net='USB_DP_RAW', role='bidirectional', mcu_pin=None)
connect('J1', pin='D+', number='3', net='USB_DP_RAW', role='bidirectional', mcu_pin=None)

net('USB_FUSED', signal_class='power', voltage_domain='V3V3', required_track_width_mm=0.5)
connect('F1', pin='OUT', number='2', net='USB_FUSED', role='passive', mcu_pin=None)
connect('Q1', pin='ANODE', number='1', net='USB_FUSED', role='power_in', mcu_pin=None)

net('USB_PROT', signal_class='power', voltage_domain='V3V3', required_track_width_mm=0.5)
connect('Q1', pin='CATHODE', number='2', net='USB_PROT', role='power_out', mcu_pin=None)
connect('U2', pin='IN', number='1', net='USB_PROT', role='power_in', mcu_pin=None)

net('USB_VBUS', signal_class='power', voltage_domain='USB_5V', required_track_width_mm=0.5)
connect('F1', pin='IN', number='1', net='USB_VBUS', role='passive', mcu_pin=None)
connect('J1', pin='VBUS', number='1', net='USB_VBUS', role='power_in', mcu_pin=None)

net('V3V3', signal_class='power', voltage_domain='V3V3', required_track_width_mm=0.5)
connect('C1', pin='VCC', number='1', net='V3V3', role='passive', mcu_pin=None)
connect('C2', pin='VCC', number='1', net='V3V3', role='passive', mcu_pin=None)
connect('C4', pin='VCC', number='1', net='V3V3', role='passive', mcu_pin=None)
connect('J2', pin='VREF', number='6', net='V3V3', role='power_out', mcu_pin=None)
connect('LD1', pin='EN', number='1', net='V3V3', role='input', mcu_pin=None)
connect('LD1', pin='VOUT', number='5', net='V3V3', role='power_out', mcu_pin=None)
connect('R1', pin='VCC', number='1', net='V3V3', role='passive', mcu_pin=None)
connect('R2', pin='VCC', number='1', net='V3V3', role='passive', mcu_pin=None)
connect('R3', pin='A', number='1', net='V3V3', role='passive', mcu_pin=None)
connect('U1', pin='VDD', number='1', net='V3V3', role='power_in', mcu_pin=None)
connect('U1', pin='VDDPA', number='3', net='V3V3', role='power_in', mcu_pin=None)
connect('U1', pin='VDDMAIN', number='4', net='V3V3', role='power_in', mcu_pin=None)
connect('U2', pin='EN1', number='3', net='V3V3', role='input', mcu_pin=None)
connect('U2', pin='TE', number='7', net='V3V3', role='input', mcu_pin=None)
connect('U3', pin='VCC', number='8', net='V3V3', role='power_in', mcu_pin=None)
connect('U5', pin='VDD', number='5', net='V3V3', role='power_in', mcu_pin=None)
connect('U5', pin='nRESET', number='6', net='V3V3', role='input', mcu_pin=None)

net('VBAT', signal_class='power', voltage_domain='VBAT', required_track_width_mm=0.5)
connect('BT1', pin='VBAT', number='1', net='VBAT', role='power_in', mcu_pin=None)
connect('C3', pin='VCC', number='1', net='VBAT', role='passive', mcu_pin=None)
connect('LD1', pin='VIN', number='3', net='VBAT', role='power_in', mcu_pin=None)
connect('U2', pin='OUT', number='5', net='VBAT', role='power_out', mcu_pin=None)
connect('U3', pin='SRN', number='5', net='VBAT', role='passive', mcu_pin=None)
connect('U3', pin='SRP', number='6', net='VBAT', role='passive', mcu_pin=None)
connect('U3', pin='BAT', number='7', net='VBAT', role='power_in', mcu_pin=None)
connect('U3', pin='REGIN', number='9', net='VBAT', role='passive', mcu_pin=None)


place('BT1', data={'ref': 'BT1', 'x_mm': 43.0, 'y_mm': 4.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 4.243, 'courtyard_h_mm': 4.243, 'source': 'ble_sensor_node_anchor', 'rationale': ''})
place('C1', data={'ref': 'C1', 'x_mm': 25.0, 'y_mm': 12.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 4.243, 'courtyard_h_mm': 4.243, 'source': 'ble_sensor_node_anchor', 'rationale': ''})
place('C2', data={'ref': 'C2', 'x_mm': 27.0, 'y_mm': 19.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 4.243, 'courtyard_h_mm': 4.243, 'source': 'ble_sensor_node_anchor', 'rationale': ''})
place('C3', data={'ref': 'C3', 'x_mm': 44.0, 'y_mm': 10.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 4.243, 'courtyard_h_mm': 4.243, 'source': 'ble_sensor_node_anchor', 'rationale': ''})
place('C4', data={'ref': 'C4', 'x_mm': 19.0, 'y_mm': 19.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 4.243, 'courtyard_h_mm': 4.243, 'source': 'ble_sensor_node_anchor', 'rationale': ''})
place('D1', data={'ref': 'D1', 'x_mm': 12.0, 'y_mm': 10.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 6.708, 'courtyard_h_mm': 6.708, 'source': 'ble_sensor_node_anchor', 'rationale': ''})
place('F1', data={'ref': 'F1', 'x_mm': 17.0, 'y_mm': 4.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 4.243, 'courtyard_h_mm': 4.243, 'source': 'ble_sensor_node_anchor', 'rationale': ''})
place('J1', data={'ref': 'J1', 'x_mm': 12.0, 'y_mm': 4.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 6.0, 'courtyard_h_mm': 6.0, 'source': 'ble_sensor_node_anchor', 'rationale': ''})
place('J2', data={'ref': 'J2', 'x_mm': 6.0, 'y_mm': 28.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 8.485, 'courtyard_h_mm': 8.485, 'source': 'ble_sensor_node_anchor', 'rationale': ''})
place('LD1', data={'ref': 'LD1', 'x_mm': 32.0, 'y_mm': 11.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 6.708, 'courtyard_h_mm': 6.708, 'source': 'ble_sensor_node_anchor', 'rationale': ''})
place('Q1', data={'ref': 'Q1', 'x_mm': 24.0, 'y_mm': 4.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 5.196, 'courtyard_h_mm': 5.196, 'source': 'ble_sensor_node_anchor', 'rationale': ''})
place('R1', data={'ref': 'R1', 'x_mm': 10.0, 'y_mm': 13.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 4.243, 'courtyard_h_mm': 4.243, 'source': 'ble_sensor_node_anchor', 'rationale': ''})
place('R2', data={'ref': 'R2', 'x_mm': 15.0, 'y_mm': 13.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 4.243, 'courtyard_h_mm': 4.243, 'source': 'ble_sensor_node_anchor', 'rationale': ''})
place('R3', data={'ref': 'R3', 'x_mm': 38.0, 'y_mm': 25.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 4.243, 'courtyard_h_mm': 4.243, 'source': 'ble_sensor_node_anchor', 'rationale': ''})
place('R4', data={'ref': 'R4', 'x_mm': 37.0, 'y_mm': 4.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 4.243, 'courtyard_h_mm': 4.243, 'source': 'ble_sensor_node_anchor', 'rationale': ''})
place('U1', data={'ref': 'U1', 'x_mm': 25.0, 'y_mm': 28.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 12.728, 'courtyard_h_mm': 12.728, 'source': 'ble_sensor_node_anchor', 'rationale': ''})
place('U2', data={'ref': 'U2', 'x_mm': 30.0, 'y_mm': 4.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 8.485, 'courtyard_h_mm': 8.485, 'source': 'ble_sensor_node_anchor', 'rationale': ''})
place('U3', data={'ref': 'U3', 'x_mm': 40.0, 'y_mm': 6.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 9.0, 'courtyard_h_mm': 9.0, 'source': 'ble_sensor_node_anchor', 'rationale': ''})
place('U5', data={'ref': 'U5', 'x_mm': 10.0, 'y_mm': 24.0, 'rotation_deg': 0.0, 'side': 'top', 'courtyard_w_mm': 8.485, 'courtyard_h_mm': 8.485, 'source': 'ble_sensor_node_anchor', 'rationale': ''})

constraint(data={'kind': 'board_keepout', 'target_ref': None, 'params': {'width_mm': 50.0, 'height_mm': 35.0, 'edge_margin_mm': 0.15}, 'derived_from': 'mechanical.envelope + manufacturing.pcb.min_clearance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'mounting_hole_keepout', 'target_ref': None, 'params': {'x_mm': 3.5, 'y_mm': 3.5, 'keepout_radius_mm': 2.4}, 'derived_from': 'mechanical.mounting_holes[0] + mechanical.assembly_clearance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'mounting_hole_keepout', 'target_ref': None, 'params': {'x_mm': 46.5, 'y_mm': 3.5, 'keepout_radius_mm': 2.4}, 'derived_from': 'mechanical.mounting_holes[1] + mechanical.assembly_clearance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'mounting_hole_keepout', 'target_ref': None, 'params': {'x_mm': 3.5, 'y_mm': 31.5, 'keepout_radius_mm': 2.4}, 'derived_from': 'mechanical.mounting_holes[2] + mechanical.assembly_clearance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'mounting_hole_keepout', 'target_ref': None, 'params': {'x_mm': 46.5, 'y_mm': 31.5, 'keepout_radius_mm': 2.4}, 'derived_from': 'mechanical.mounting_holes[3] + mechanical.assembly_clearance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'connector_edge', 'target_ref': 'J1', 'params': {'side': 'front', 'max_edge_distance_mm': 5.0}, 'derived_from': 'mechanical.connector_interfaces + mechanical.max_connector_edge_distance_mm', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'decoupling_proximity', 'target_ref': 'C1', 'params': {'power_nets': ['GND', 'V3V3'], 'target_ref': None, 'max_distance_mm': 12.0}, 'derived_from': 'graph decoupling component pins + decoupling_target_ref', 'enforced': False, 'rationale': 'Cap-to-IC association is not modelled in the netlist; proximity enforcement is deferred.'})
constraint(data={'kind': 'decoupling_proximity', 'target_ref': 'C2', 'params': {'power_nets': ['GND', 'V3V3'], 'target_ref': 'U1', 'max_distance_mm': 12.0}, 'derived_from': 'graph decoupling component pins + decoupling_target_ref', 'enforced': True, 'rationale': ''})
constraint(data={'kind': 'thermal_spacing', 'target_ref': 'Q1', 'params': {'min_spacing_mm': 8.0}, 'derived_from': 'graph power-category component', 'enforced': False, 'rationale': 'Advisory spacing only; thermal qualification requires load testing.'})
constraint(data={'kind': 'thermal_spacing', 'target_ref': 'LD1', 'params': {'min_spacing_mm': 8.0}, 'derived_from': 'graph power-category component', 'enforced': False, 'rationale': 'Advisory spacing only; thermal qualification requires load testing.'})

semantic_schematic = board.to_dict()
