EESchema Schematic File Version 4
LIBS:power
EELAYER 29 0
EELAYER END
$Descr A4 11693 8268
Sheet 1 1
Title "Robot Controller"
$EndDescr
$Comp
L Connector_Generic:Conn_01x02 J1
U 1 1 3E8
P 1500 1200
F 0 "J1" H 1580 1400 50  0000 C CNN
F 1 "USB-C 2.0" H 1580 1000 50  0000 C CNN
F 2 "Connector_USB:USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal" H 1500 1200 50  0001 C CNN
	1    0    0    -1
$EndComp
$Comp
L Connector_Generic:Conn_01x02 D1
U 1 1 3E9
P 3500 1200
F 0 "D1" H 3580 1400 50  0000 C CNN
F 1 "USB 2.0 ESD" H 3580 1000 50  0000 C CNN
F 2 "Package_TO_SOT_SMD:SOT-23-6" H 3500 1200 50  0001 C CNN
	1    0    0    -1
$EndComp
$Comp
L Connector_Generic:Conn_01x02 R1
U 1 1 3EA
P 5500 1200
F 0 "R1" H 5580 1400 50  0000 C CNN
F 1 "27R USB D+" H 5580 1000 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric" H 5500 1200 50  0001 C CNN
	1    0    0    -1
$EndComp
$Comp
L Connector_Generic:Conn_01x02 R2
U 1 1 3EB
P 7500 1200
F 0 "R2" H 7580 1400 50  0000 C CNN
F 1 "27R USB D-" H 7580 1000 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric" H 7500 1200 50  0001 C CNN
	1    0    0    -1
$EndComp
$Comp
L Connector_Generic:Conn_01x02 U1
U 1 1 3EC
P 1500 2100
F 0 "U1" H 1580 2300 50  0000 C CNN
F 1 "3V3 LDO" H 1580 1900 50  0000 C CNN
F 2 "Package_TO_SOT_SMD:SOT-23-5" H 1500 2100 50  0001 C CNN
	1    0    0    -1
$EndComp
$Comp
L Connector_Generic:Conn_01x02 U2
U 1 1 3ED
P 3500 2100
F 0 "U2" H 3580 2300 50  0000 C CNN
F 1 "RP2040" H 3580 1900 50  0000 C CNN
F 2 "Package_DFN_QFN:QFN-56-1EP_7x7mm_P0.4mm_EP3.2x3.2mm" H 3500 2100 50  0001 C CNN
	1    0    0    -1
$EndComp
$Comp
L Connector_Generic:Conn_01x02 U3
U 1 1 3EE
P 5500 2100
F 0 "U3" H 5580 2300 50  0000 C CNN
F 1 "16Mbit QSPI Flash" H 5580 1900 50  0000 C CNN
F 2 "Package_SO:SOIC-8_5.3x5.3mm_P1.27mm" H 5500 2100 50  0001 C CNN
	1    0    0    -1
$EndComp
$Comp
L Connector_Generic:Conn_01x02 X1
U 1 1 3EF
P 7500 2100
F 0 "X1" H 7580 2300 50  0000 C CNN
F 1 "12MHz RP2040 crystal" H 7580 1900 50  0000 C CNN
F 2 "Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm" H 7500 2100 50  0001 C CNN
	1    0    0    -1
$EndComp
$Comp
L Connector_Generic:Conn_01x02 R3
U 1 1 3F0
P 1500 3000
F 0 "R3" H 1580 3200 50  0000 C CNN
F 1 "1K XTAL damping" H 1580 2800 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric" H 1500 3000 50  0001 C CNN
	1    0    0    -1
$EndComp
$Comp
L Connector_Generic:Conn_01x02 R4
U 1 1 3F1
P 3500 3000
F 0 "R4" H 3580 3200 50  0000 C CNN
F 1 "10K QSPI CS pull-up" H 3580 2800 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric" H 3500 3000 50  0001 C CNN
	1    0    0    -1
$EndComp
$Comp
L Connector_Generic:Conn_01x02 R5
U 1 1 3F2
P 5500 3000
F 0 "R5" H 5580 3200 50  0000 C CNN
F 1 "5K1 USB-C Rd" H 5580 2800 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric" H 5500 3000 50  0001 C CNN
	1    0    0    -1
$EndComp
$Comp
L Connector_Generic:Conn_01x02 R6
U 1 1 3F3
P 7500 3000
F 0 "R6" H 7580 3200 50  0000 C CNN
F 1 "5K1 USB-C Rd" H 7580 2800 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric" H 7500 3000 50  0001 C CNN
	1    0    0    -1
$EndComp
$Comp
L Connector_Generic:Conn_01x02 J2
U 1 1 3F4
P 1500 3900
F 0 "J2" H 1580 4100 50  0000 C CNN
F 1 "Cortex 10-pin SWD" H 1580 3700 50  0000 C CNN
F 2 "Connector_IDC:IDC-Header_2x05_P2.54mm_Vertical" H 1500 3900 50  0001 C CNN
	1    0    0    -1
$EndComp
$Comp
L Connector_Generic:Conn_01x02 C1
U 1 1 3F5
P 3500 3900
F 0 "C1" H 3580 4100 50  0000 C CNN
F 1 "100nF" H 3580 3700 50  0000 C CNN
F 2 "Capacitor_SMD:C_0402_1005Metric" H 3500 3900 50  0001 C CNN
	1    0    0    -1
$EndComp
$Comp
L Connector_Generic:Conn_01x02 C2
U 1 1 3F6
P 5500 3900
F 0 "C2" H 5580 4100 50  0000 C CNN
F 1 "100nF" H 5580 3700 50  0000 C CNN
F 2 "Capacitor_SMD:C_0402_1005Metric" H 5500 3900 50  0001 C CNN
	1    0    0    -1
$EndComp
$Comp
L Connector_Generic:Conn_01x02 C3
U 1 1 3F7
P 7500 3900
F 0 "C3" H 7580 4100 50  0000 C CNN
F 1 "100nF" H 7580 3700 50  0000 C CNN
F 2 "Capacitor_SMD:C_0402_1005Metric" H 7500 3900 50  0001 C CNN
	1    0    0    -1
$EndComp
$Comp
L Connector_Generic:Conn_01x02 C4
U 1 1 3F8
P 1500 4800
F 0 "C4" H 1580 5000 50  0000 C CNN
F 1 "100nF" H 1580 4600 50  0000 C CNN
F 2 "Capacitor_SMD:C_0402_1005Metric" H 1500 4800 50  0001 C CNN
	1    0    0    -1
$EndComp
$Comp
L Connector_Generic:Conn_01x02 C5
U 1 1 3F9
P 3500 4800
F 0 "C5" H 3580 5000 50  0000 C CNN
F 1 "100nF" H 3580 4600 50  0000 C CNN
F 2 "Capacitor_SMD:C_0402_1005Metric" H 3500 4800 50  0001 C CNN
	1    0    0    -1
$EndComp
$Comp
L Connector_Generic:Conn_01x02 C6
U 1 1 3FA
P 5500 4800
F 0 "C6" H 5580 5000 50  0000 C CNN
F 1 "100nF" H 5580 4600 50  0000 C CNN
F 2 "Capacitor_SMD:C_0402_1005Metric" H 5500 4800 50  0001 C CNN
	1    0    0    -1
$EndComp
$Comp
L Connector_Generic:Conn_01x02 C7
U 1 1 3FB
P 7500 4800
F 0 "C7" H 7580 5000 50  0000 C CNN
F 1 "100nF" H 7580 4600 50  0000 C CNN
F 2 "Capacitor_SMD:C_0402_1005Metric" H 7500 4800 50  0001 C CNN
	1    0    0    -1
$EndComp
$Comp
L Connector_Generic:Conn_01x02 C8
U 1 1 3FC
P 1500 5700
F 0 "C8" H 1580 5900 50  0000 C CNN
F 1 "100nF" H 1580 5500 50  0000 C CNN
F 2 "Capacitor_SMD:C_0402_1005Metric" H 1500 5700 50  0001 C CNN
	1    0    0    -1
$EndComp
$Comp
L Connector_Generic:Conn_01x02 C9
U 1 1 3FD
P 3500 5700
F 0 "C9" H 3580 5900 50  0000 C CNN
F 1 "100nF" H 3580 5500 50  0000 C CNN
F 2 "Capacitor_SMD:C_0402_1005Metric" H 3500 5700 50  0001 C CNN
	1    0    0    -1
$EndComp
$Comp
L Connector_Generic:Conn_01x02 C10
U 1 1 3FE
P 5500 5700
F 0 "C10" H 5580 5900 50  0000 C CNN
F 1 "100nF" H 5580 5500 50  0000 C CNN
F 2 "Capacitor_SMD:C_0402_1005Metric" H 5500 5700 50  0001 C CNN
	1    0    0    -1
$EndComp
$Comp
L Connector_Generic:Conn_01x02 C11
U 1 1 3FF
P 7500 5700
F 0 "C11" H 7580 5900 50  0000 C CNN
F 1 "1uF VREG_VIN" H 7580 5500 50  0000 C CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 7500 5700 50  0001 C CNN
	1    0    0    -1
$EndComp
$Comp
L Connector_Generic:Conn_01x02 C12
U 1 1 400
P 1500 6600
F 0 "C12" H 1580 6800 50  0000 C CNN
F 1 "1uF VREG_VOUT" H 1580 6400 50  0000 C CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 1500 6600 50  0001 C CNN
	1    0    0    -1
$EndComp
$Comp
L Connector_Generic:Conn_01x02 C13
U 1 1 401
P 3500 6600
F 0 "C13" H 3580 6800 50  0000 C CNN
F 1 "100nF FLASH" H 3580 6400 50  0000 C CNN
F 2 "Capacitor_SMD:C_0402_1005Metric" H 3500 6600 50  0001 C CNN
	1    0    0    -1
$EndComp
$Comp
L Connector_Generic:Conn_01x02 C14
U 1 1 402
P 5500 6600
F 0 "C14" H 5580 6800 50  0000 C CNN
F 1 "100nF USB ESD VBUS" H 5580 6400 50  0000 C CNN
F 2 "Capacitor_SMD:C_0402_1005Metric" H 5500 6600 50  0001 C CNN
	1    0    0    -1
$EndComp
$Comp
L Connector_Generic:Conn_01x02 C15
U 1 1 403
P 7500 6600
F 0 "C15" H 7580 6800 50  0000 C CNN
F 1 "1uF LDO input" H 7580 6400 50  0000 C CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 7500 6600 50  0001 C CNN
	1    0    0    -1
$EndComp
$Comp
L Connector_Generic:Conn_01x02 C16
U 1 1 404
P 1500 7500
F 0 "C16" H 1580 7700 50  0000 C CNN
F 1 "1uF LDO output" H 1580 7300 50  0000 C CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 1500 7500 50  0001 C CNN
	1    0    0    -1
$EndComp
$Comp
L Connector_Generic:Conn_01x02 C17
U 1 1 405
P 3500 7500
F 0 "C17" H 3580 7700 50  0000 C CNN
F 1 "15pF XTAL" H 3580 7300 50  0000 C CNN
F 2 "Capacitor_SMD:C_0402_1005Metric" H 3500 7500 50  0001 C CNN
	1    0    0    -1
$EndComp
$Comp
L Connector_Generic:Conn_01x02 C18
U 1 1 406
P 5500 7500
F 0 "C18" H 5580 7700 50  0000 C CNN
F 1 "15pF XTAL" H 5580 7300 50  0000 C CNN
F 2 "Capacitor_SMD:C_0402_1005Metric" H 5500 7500 50  0001 C CNN
	1    0    0    -1
$EndComp
$EndSCHEMATC
