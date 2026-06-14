---
artifact_type: design_intent
compiled: false
release_eligible: false
source_of_truth: false
backend: reference
---

# Generated high-level hardware intent. Edit spec, then regenerate.
module RobotController:
  mcu = new STM32H7
  power_input = new ProtectedPowerInput
  imu = new IMU
  motor_channels = new MotorChannel[12]
  emergency_stop = new FailSafeEmergencyStop
