---
artifact_type: design_intent
compiled: false
release_eligible: false
source_of_truth: false
backend: reference
---

# Generated high-level hardware intent. Edit spec, then regenerate.
module SAMD21Board:
  mcu = new SAMD21
  power_input = new ProtectedPowerInput
  imu = new IMU
  emergency_stop = new FailSafeEmergencyStop
