# IoT sensor data logger reference design

ESP32-S3-WROOM-1, USB-C power (USB-PD, 5 V), I2C IMU, temperature sensor,
two-layer PCB, Zephyr firmware scaffold.

Source specification: [`projects/sensor_data_logger/spec/`](../../projects/sensor_data_logger/spec/)

## Inspect without installing

| Evidence | File | What it establishes |
|---|---|---|
| Candidate bundle | [sensor_data_logger-0001-candidate.zip](../../projects/sensor_data_logger/exports/candidates/0001/sensor_data_logger-0001-candidate.zip) | Inspectable generated directory set |
| BOM | [bom.csv](../../projects/sensor_data_logger/electronics/generated/bom.csv) | Generated component list |
| Current review | [portable review bundle](proof/review_bundle.json) | Current gate reports with machine-local paths normalized |
| Electrical graph | [electrical_graph.json](../../projects/sensor_data_logger/electronics/generated/electrical_graph.json) | Resolved component graph |
| Firmware pinmap | [pinmap.json](../../projects/sensor_data_logger/firmware/generated/pinmap.json) | Pin assignments |
| Mechanical contract | [mechanical_contract.json](../../projects/sensor_data_logger/mechanical/source/mechanical_contract.json) | Board envelope and clearances |

## Current gate summary

| Status | Count |
|---|---:|
| `pass` | 26 |
| `fail` | 1 |
| `blocked` | 14 |
| total | 41 |

Representative blocked gates (no toolchain present):

| Gate | Reason |
|---|---|
| `tscircuit_compile` | tscircuit compiler not requested for current run |
| `autoroute` | Freerouting not requested |
| `native_erc` | KiCad ERC not requested |
| `native_drc` | KiCad DRC not requested |
| `native_mechanical_validation` | Native CAD validation not requested |
| `native_zephyr_build` | Native Zephyr build not requested |
| `supplier_availability` | Curated snapshot entries lack live stock data |
| `physical_qualification` | No bench evidence attached |

The single failing gate (`support_circuit_completeness`) reflects a missing
curated support-circuit entry for the ESP32-S3-WROOM-1 antenna keep-out
assertion. It prevents release but does not affect candidate generation.

The committed portable review bundle has hash:

```text
033692421dfa846b6f7d0260fcaad048f110fd2e9659571f316285b7b17e1683
```

Regenerate locally with:

```bash
PYTHONPATH=src python3 -m hw_codesign.cli --root . export-review sensor_data_logger
```

## Evidence not yet present

There is no published fabrication, board bring-up, thermal, transient, EMI/EMC,
vibration, ingress, or connector-life evidence for this design. Do not infer
those results from the generated artifacts or digital gate reports.
