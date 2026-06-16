# Validation contract

The platform's primary contract is refusal: an artifact may be generated and
reviewed without being represented as a release. This document defines the
statuses, adapter obligations, artifact integrity rules, and evidence boundary
used by the current implementation.

## Gate statuses

| Status | Contract meaning |
|---|---|
| `pass` | The named check ran and produced no release-blocking finding. |
| `fail` | The check ran and found a violation. |
| `blocked` | The check could not establish a result because tooling, evidence, prior output, or a human decision was missing. |
| `generated` | An artifact was written; no release claim follows from generation alone. |
| `candidate` | Reviewable output exists but is not release-eligible. |
| `released` | Export completed only after the release gate passed. |

`blocked` is not equivalent to `pass`, and a missing gate is not silently
skipped. A required adapter stage that did not run is injected as a blocked
`gate_not_run` report.

## Release eligibility

A release is eligible only when all of the following are true:

1. The electronics backend is release-capable (`tscircuit`, `kicad`, or
   `python_netlist`).
2. Every supplied and required gate report has status `pass`.
3. Every critical assumption marked `requires_user_review` has been resolved.
4. Every required release artifact exists.
5. The release manifest covers every required artifact.
6. Every covered artifact has the recorded byte count and SHA-256 digest.

Any `fail` prevents release. Any `blocked` result makes the aggregate release
gate `blocked`. Missing exports and integrity failures prevent release even if
the design checks themselves passed.

Three release tiers are defined:

- **Fabrication** (`tscircuit`, `kicad`): Gerber + drill + STEP + BOM.
  All six contract gates must pass, including layout and manufacturing export.
- **Netlist** (`python_netlist`): `compiled_netlist.json` + firmware.
  Compile, netlist_extract, graph_parity, and footprint_parity must pass;
  layout_completeness and manufacturing_export are N/A for this tier.
- **Candidate-only** (`reference`, `atopile`): no release path exists.
  These backends cannot become release-eligible through a manual status override.

## Adapter contract

Compiled electronics adapters generate source, then report these six gate
stages:

1. compile
2. netlist extraction
3. graph parity
4. footprint parity
5. layout completeness
6. manufacturing export

The selected release-eligible backend must report every stage. Unsupported or
unexecuted stages return `blocked`; compiler or design violations return `fail`.
Manufacturing output from a source-only or netlist-only adapter is not inferred.

Native gates, including KiCad ERC/DRC, mechanical validation, autorouting, and
Zephyr builds, must include backend metadata and artifacts where applicable.
Tool absence is represented as structured `tool_unavailable` or
`external_gate_not_run` evidence.

## Artifact integrity

Release manifests use SHA-256. For each manifest entry the integrity gate checks:

- the path exists beneath the release directory;
- the byte count matches;
- the SHA-256 digest matches; and
- every required release output is represented in the manifest.

A missing manifest, missing file, checksum mismatch, or uncovered required
artifact fails `artifact_integrity`.

Review bundles are separately canonicalized. `bundle_hash` is the SHA-256 of
the stable JSON fields with sorted keys and compact separators;
`generated_at` is excluded so identical evidence has an identical hash.
Review comments are stored separately and do not mutate `bundle.json`.

## Evidence boundary

Software gates can establish that a command ran, an output was parsed, digital
constraints were checked, and declared artifacts match their hashes. They
cannot certify physical behavior that was not measured.

The following require external physical evidence and remain release risks until
that evidence is attached to an explicit contract:

- fabrication yield and assembly quality;
- current-path temperature rise and load transients;
- EMI/EMC and signal integrity under representative operation;
- vibration, shock, ingress, abuse, and connector-cycle life; and
- successful board bring-up against the released artifact hashes.

No generated report should describe these properties as passed solely because
the digital release gate passed.

## Public evidence interpretation

The tracked `projects/quadruped_robot_controller/exports/r1/` directory is a
historical generated export and digital validation record. It is useful for
inspecting output shape, but it is not fabrication or qualification evidence.

The current checked-in project uses the candidate-only `reference` backend. Its
current review bundle is therefore expected to show blocked release gates. See
the [example proof index](../examples/robotics-motor-controller/README.md) for
both sets of evidence and their scope.
