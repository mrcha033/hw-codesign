# Physical Qualification Plan

Project: `bench_sensor_logger_usb_5eab0a5d`
Revision: `r1`

This plan defines external evidence required before physical qualification can be claimed.

## Required Tests

### assembly_inspection
- Category: `assembly_quality`
- Objective: Verify fabricated board and assembly match the released BOM, orientation, polarity, and connector plan.
- Evidence: photos, assembly_checklist, bom_lot_trace
- Acceptance: No reversed polarized parts; Connector orientation matches assembly drawing; No visible solder bridges or tombstoning

### current_limited_power_up
- Category: `bringup`
- Objective: Power the board with current limiting and verify expected rails before enabling loads.
- Evidence: bench_supply_log, rail_voltage_measurements, thermal_image_optional
- Acceptance: No input current runaway; All required rails within tolerance; No component exceeds safe touch temperature during idle bring-up

### firmware_interface_bringup
- Category: `firmware_co_design`
- Objective: Flash firmware and verify pinmap-controlled interfaces against the assembled board.
- Evidence: flash_log, interface_probe_log, firmware_revision_hash
- Acceptance: Firmware image matches released source hash; Pinmap self-test passes; Required buses enumerate expected devices

### thermal_load_profile
- Category: `thermal`
- Objective: Measure thermal behavior under representative load and ambient assumptions.
- Evidence: thermal_camera_capture, load_profile_log, ambient_temperature_log
- Acceptance: No component exceeds datasheet or enclosure thermal limit; Board remains stable for the required dwell time

### emi_emc_prescan
- Category: `emi_emc`
- Objective: Run conducted/radiated emissions pre-scan or document certified exemption scope.
- Evidence: emi_prescan_report, test_setup_photos, cable_configuration
- Acceptance: No unmitigated emissions finding in intended operating mode; Cable and enclosure configuration matches release use case

### signal_power_integrity_probe
- Category: `si_pi`
- Objective: Probe high-risk signal and power nets under representative switching and load conditions.
- Evidence: oscilloscope_captures, probe_points, load_state_log
- Acceptance: No excessive rail droop or ringing on required rails; Digital bus eye/timing margin is acceptable for the selected interfaces

### vibration_connector_retention
- Category: `mechanical_reliability`
- Objective: Verify connectors, mounts, and enclosure remain secure under expected vibration and handling.
- Evidence: vibration_test_log, post_test_inspection_photos, connector_retention_measurements
- Acceptance: No connector disengagement; No mounting hardware loosening; No enclosure or PCB crack

### ingress_esd_abuse_check
- Category: `environmental_safety`
- Objective: Verify exposed connectors and enclosure openings match the intended ingress, ESD, and abuse assumptions.
- Evidence: ingress_test_report_or_waiver, esd_test_log_or_waiver, enclosure_photos
- Acceptance: No unreviewed exposed conductor path; Ingress/IP assumption is tested or explicitly waived; ESD handling risk is documented

## Oracle Boundary

- Digital validators cannot certify thermal load behavior, EMI/EMC, SI/PI, vibration, ingress, connector fatigue, assembly quality, or board bring-up.
- Each required test needs approved external evidence before the physical_qualification gate can pass.
