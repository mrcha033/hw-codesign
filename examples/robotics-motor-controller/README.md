# Robotics motor controller reference design

This is the currently maintained end-to-end design family. Its source
specification is under
[`projects/quadruped_robot_controller/spec/`](../../projects/quadruped_robot_controller/spec/).

## Inspect without installing

| Evidence | File | What it establishes |
|---|---|---|
| Complete export | [candidate bundle](../../projects/quadruped_robot_controller/exports/quadruped_robot_controller-r1.zip) | Inspectable generated directory set |
| Manufacturing | [Gerbers](../../projects/quadruped_robot_controller/exports/r1/fabrication/gerbers.zip) | Generated fabrication layers |
| Procurement | [BOM CSV](../../projects/quadruped_robot_controller/exports/r1/fabrication/bom.csv) | Generated component list |
| Mechanical | [Assembly STEP](../../projects/quadruped_robot_controller/exports/r1/mechanical/assembly.step) | Generated assembly geometry |
| Validation | [historical validation JSON](../../projects/quadruped_robot_controller/exports/r1/docs/validation_report.json) | Digital checks recorded for the tracked export |
| Integrity | [release manifest](../../projects/quadruped_robot_controller/exports/r1/manifest.json) | Artifact paths, sizes, and SHA-256 hashes |
| Risk boundary | [known risks](../../projects/quadruped_robot_controller/exports/r1/docs/known_risks.md) | Physical checks not established by software |

The historical validation JSON reflects the gate set used when that export was
generated. It is not a statement that the current checked-in configuration
passes the current release contract.

## Current gate summary

The current review bundle for the checked-in `reference` backend reports:

| Status | Count |
|---|---:|
| `pass` | 13 |
| `blocked` | 8 |
| `fail` | 0 |
| total | 21 |

Representative blocked gates are:

| Gate | Reason |
|---|---|
| `compiled_electronics_backend` | The reference backend produces candidate artifacts only. |
| `autoroute` | Freerouting was not requested for the current review run. |
| `native_erc` | KiCad ERC was not requested for the current review run. |
| `native_drc` | KiCad DRC was not requested for the current review run. |
| `native_mechanical_validation` | Native CAD validation was not requested. |
| `native_zephyr_build` | A native Zephyr build was not requested. |
| `release` | Required upstream gates did not pass. |

Regenerate the machine-readable review bundle locally with:

```bash
uvx --from hw-codesign-platform hw --root . export-review quadruped_robot_controller
```

The output is
`projects/quadruped_robot_controller/exports/working/review/bundle.json`.
Generated working exports are intentionally ignored; tagged GitHub releases
attach the canonical bundle and its JSON Schema.

A committed sample `bundle.json` remains open because the current exporter
retains absolute local paths in gate artifacts and backend metadata. Publishing
that file as portable canonical evidence requires path normalization first. The
[bundle schema](../../schemas/review_bundle.schema.json) is tracked today.

## Evidence not yet present

There is no published fabrication, board bring-up, thermal, transient, EMI/EMC,
vibration, ingress, or connector-life evidence for this design. Do not infer
those results from the generated Gerbers, STEP files, or digital gate reports.
