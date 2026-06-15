# Zero to first candidate report

This walkthrough demonstrates the public workflow without requiring KiCad,
OpenCASCADE, Freerouting, or Zephyr locally. The expected endpoint is a
reviewable candidate with explicit blocked gates, not a manufacturing release.

## 1. Create a workspace

Run these commands from an empty writable directory:

```bash
uvx --from hw-codesign-platform hw --root . create-project first_board
uvx --from hw-codesign-platform hw --root . iterate first_board --no-external
```

`create-project` currently instantiates the `robotics_controller_full` template.
The name changes the workspace identity; it does not select a different board
topology.

The first iteration should return `status: blocked` and a candidate object
similar to:

```json
{
  "status": "blocked",
  "iteration_id": "0001",
  "passed_gates": [
    "spec_schema",
    "mechanical_fit",
    "firmware_pinmap",
    "component_resolution",
    "bom",
    "hw_sw_parity"
  ],
  "failed_gates": [
    "semantic_electrical",
    "compiled_electronics_backend",
    "native_erc",
    "native_drc",
    "native_mechanical_validation",
    "native_zephyr_build"
  ],
  "candidate": {
    "status": "candidate",
    "candidate_only": true,
    "path": ".../projects/first_board/exports/candidates/0001"
  }
}
```

The exact gate list can change as checks are added. The invariant is that absent
tools, unsupported constraints, unresolved decisions, or a candidate-only
backend remain visible and prevent release.

## 2. Inspect what changed

The workflow creates:

```text
projects/first_board/
  project.yaml                    project identity and revision
  spec/*.yaml                     editable design requirements
  electronics/intent/             generated design intent
  electronics/generated/          typed graph and BOM
  mechanical/source/              parameterized CAD source
  firmware/generated/             pin map and devicetree inputs
  validation/reports/*.json       one structured result per gate
  history/iterations/0001/        immutable iteration snapshot
  exports/candidates/0001/        candidate metadata and ZIP
```

Start with these files:

```bash
jq '{gate,status,failures}' projects/first_board/validation/reports/compiled_electronics_backend.json
jq '{gate,status,failures}' projects/first_board/validation/reports/semantic_electrical.json
```

A gate status means:

| Status | Interpretation |
|---|---|
| `pass` | The check ran and found no release-blocking issue. |
| `fail` | The check ran and found a violation. |
| `blocked` | Required tooling, evidence, or a decision was unavailable. |
| `candidate` | Output exists but is not eligible for release. |

## 3. Compare a candidate and release failure

The candidate is retained for review even though release is refused:

```bash
uvx --from hw-codesign-platform hw --root . release-gate first_board
```

The expected result is `status: blocked`. Typical release failures include:

```json
{
  "gate": "release",
  "status": "blocked",
  "failures": [
    {
      "code": "compiled_electronics_backend_required",
      "message": "Required gate did not pass: backend_release_policy"
    },
    {
      "code": "failed_gate",
      "message": "Required gate did not pass: native_drc"
    }
  ]
}
```

This is the central behavior: generated output is not promoted when required
evidence is absent.

## 4. Generate a review bundle

```bash
uvx --from hw-codesign-platform hw --root . export-review first_board
uvx --from hw-codesign-platform hw --root . serve-review first_board
```

`export-review` writes normalized JSON and HTML under:

```text
projects/first_board/exports/working/review/bundle.json
projects/first_board/exports/working/review/report.html
```

`serve-review` opens the local report at `http://127.0.0.1:7474` and stores
comments in a sidecar JSONL file without mutating the evidence bundle.

## 5. Run native gates

Use the full-toolchain image for the supported Linux path:

```bash
docker run --rm -v "$PWD:/workspace" ghcr.io/mrcha033/hw-cli:latest \
  iterate first_board
```

Native tools do not guarantee a release. The selected electronics backend must
be release-eligible, all required gates must pass, critical assumptions must be
resolved, and every declared output must exist with the recorded hash.

## 6. Know the boundary

This walkthrough proves that the pipeline creates artifacts and refuses to hide
missing evidence. It does not prove that a generated design is safe to
fabricate. Load thermals, EMI/EMC, vibration, abuse, ingress, transients, and
connector life require physical engineering validation.
