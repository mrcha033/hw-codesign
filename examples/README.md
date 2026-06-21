# Reference designs

Three board families are maintained with generated candidate artifacts, portable
review bundles, and digital gate reports:

- [Robotics motor controller](robotics-motor-controller/README.md): STM32H7,
  12 motor channels, CAN, 24 V VBAT, four-layer PCB, enclosure, firmware, and
  manufacturing outputs.
- [IoT sensor data logger](sensor-data-logger/README.md): ESP32-S3-WROOM-1,
  USB-C power, I2C IMU, temperature sensor, two-layer PCB, Zephyr firmware.
- [BLE sensor node](ble-sensor-node/README.md): nRF52840-QIAA, LiPo charging
  (BQ24079 + BQ27441 + AP2112K-3.3), SHT31 temperature/humidity, BLE, 50×35 mm.

Each family has its own role set, component catalog entries, template, and
service-layer generators. Each has been run end-to-end to produce a candidate
bundle and a portable review bundle with machine-normalized paths.

## Evidence scope

All three are digital candidates, not fabricated boards. Generated Gerbers, BOM,
STEP files, firmware, and gate reports are included. None carries fabrication,
board bring-up, thermal, EMI/EMC, vibration, ingress, or connector-life evidence.
