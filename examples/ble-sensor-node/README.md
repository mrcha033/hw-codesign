# BLE sensor node reference design

nRF52840-QIAA, LiPo battery (BQ24079 + BQ27441 + AP2112K-3.3), SHT31
temperature/humidity sensor, USB-C charging, BLE, 50×35 mm two-layer PCB.

Source specification: [`projects/ble_sensor_node/spec/`](../../projects/ble_sensor_node/spec/)

## Inspect without installing

| Evidence | File | What it establishes |
|---|---|---|
| Candidate bundle | [ble_sensor_node-0001-candidate.zip](../../projects/ble_sensor_node/exports/candidates/0001/ble_sensor_node-0001-candidate.zip) | Inspectable generated directory set |
| BOM | [bom.csv](../../projects/ble_sensor_node/electronics/generated/bom.csv) | Generated component list |
| Current review | [portable review bundle](proof/review_bundle.json) | Current gate reports with machine-local paths normalized |
| Electrical graph | [electrical_graph.json](../../projects/ble_sensor_node/electronics/generated/electrical_graph.json) | Resolved component graph |
| Firmware pinmap | [pinmap.json](../../projects/ble_sensor_node/firmware/generated/pinmap.json) | Pin assignments |
| Mechanical contract | [mechanical_contract.json](../../projects/ble_sensor_node/mechanical/source/mechanical_contract.json) | Board envelope and clearances |

## Current gate summary

| Status | Count |
|---|---:|
| `pass` | 24 |
| `fail` | 3 |
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

Failing gates reflect missing curated support-circuit evidence and provenance
gaps for components resolved from the shared catalog. These prevent release but
do not affect candidate generation.

The committed portable review bundle has hash:

```text
b0d23f054aca463f4e4f2bd4cd0a4fa32d21fbda8797048a419b237000ec314f
```

Regenerate locally with:

```bash
PYTHONPATH=src python3 -m hw_codesign.cli --root . export-review ble_sensor_node
```

## Evidence not yet present

There is no published fabrication, board bring-up, thermal, transient, EMI/EMC,
vibration, ingress, or connector-life evidence for this design. Do not infer
those results from the generated artifacts or digital gate reports.
