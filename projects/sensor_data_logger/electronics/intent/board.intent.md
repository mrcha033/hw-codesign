---
artifact_type: design_intent
compiled: false
release_eligible: false
source_of_truth: false
backend: reference
---

# Generated high-level hardware intent. Edit spec, then regenerate.
module ESP32S3Board:
  mcu = new ESP32S3
  power_input = new UsbCPowerInput
  imu = new IMU
