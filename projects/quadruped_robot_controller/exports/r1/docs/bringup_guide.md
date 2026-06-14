# Bring-up Guide

1. Inspect assembly and verify no shorts with power removed.
2. Current-limit the bench supply below 0.5 A and apply 24 V through the protected input.
3. Verify 5 V and 3.3 V rails before fitting the MCU.
4. Keep motor enable disabled; flash the Zephyr image over SWD.
5. Verify console, IMU identity, CAN loopback, E-stop latch, then each PWM/encoder/current channel.
6. Increase load only under instrumented thermal and transient monitoring.
