# hw-codesign: agentic hardware design system

[![CI](https://github.com/mrcha033/hw-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/mrcha033/hw-cli/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/hw-codesign-platform)](https://pypi.org/project/hw-codesign-platform/)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://pypi.org/project/hw-codesign-platform/)
[![Platforms](https://img.shields.io/badge/platforms-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey)](#install)
[![MCP](https://img.shields.io/badge/MCP-FastMCP%203.4-purple)](docs/mcp-tools.md)

An agent-facing CLI and MCP server that lets AI coding agents — such as Claude Code or Codex —
design PCB electronics, mechanical parts, firmware interfaces, sourcing choices, manufacturing
outputs, and reviewable release artifacts. It generates cross-domain hardware candidates backed
by typed specs and deterministic gates, then promotes only evidence-backed candidates.

Three maintained board families are included: an STM32H7 robotics motor controller, an
ESP32-S3 IoT sensor data logger, and an nRF52840 BLE sensor node.

> **Evidence status:** the repository includes generated Gerbers, STEP files, BOM, firmware,
> reports, and a downloadable candidate bundle. It does not yet claim a fabricated,
> electrically brought-up, thermally qualified, or EMC-tested board.

---

## Install

**Standalone binary** — download from the [latest release](../../releases/latest), no Python needed:

| Platform | File |
|---|---|
| Linux x86-64 | `hw-{version}-linux-x86_64.tar.gz` |
| macOS arm64 | `hw-{version}-macos-arm64.tar.gz` |
| Windows x86-64 | `hw-{version}-windows-x86_64.zip` |

macOS: clear Gatekeeper quarantine after download with `xattr -d com.apple.quarantine ./hw ./hw-mcp`.

**Run directly with uv** (no install):

```bash
uvx --from hw-codesign-platform hw --root . create-project my_board
uvx --from 'hw-codesign-platform[mcp]' hw-mcp  # MCP server
```

**Full toolchain container** (KiCad, OpenCASCADE, Freerouting, Zephyr):

```bash
docker run --rm -v "$PWD:/workspace" ghcr.io/mrcha033/hw-cli:latest \
  design-until-release my_board --external
```

---

## Quickstart

```bash
uvx --from hw-codesign-platform hw --root . create-project first_board
uvx --from hw-codesign-platform hw --root . design-candidate first_board \
  --brief "16 channel 24V battery, peak 6A, STM32H7, IMU, emergency stop, Zephyr, 6-layer"
```

Expected result (abbreviated):

```json
{
  "status": "candidate",
  "release_eligible": false,
  "gate_summary": {"pass": 7, "fail": 2, "blocked": 5},
  "semantic_representation": {
    "layers": {
      "requirements": ["…/spec/system.yaml"],
      "electronics_graph": "…/electrical_graph.json",
      "semantic_schematic": "…/semantic/semantic_schematic.json",
      "semantic_schematic_code": "…/semantic/semantic_schematic.py",
      "relative_placement": {"style": "constraint-derived positions with provenance"},
      "mechanical_contract": "…/mechanical_contract.json",
      "firmware_pinmap": "…/pinmap.json"
    }
  },
  "reviewable_artifacts": {
    "candidate_bundle": "…/first_board-0001-candidate.zip",
    "review_bundle": "…/review/bundle.json"
  }
}
```

`release_eligible: false` means the design system preserved the generated candidate but refused
to promote it. Gate failures and blocked native tools are explicit in the report, never silently
green. Read [Zero to first candidate report](docs/first-run.md) for the full walkthrough.

---

## Documentation

| Doc | Contents |
|---|---|
| [Zero to first candidate report](docs/first-run.md) | Step-by-step walkthrough without native toolchains |
| [Adapting the design system](docs/adapting-a-spec.md) | Spec parameters, topology extension, backend selection |
| [Capabilities reference](docs/capabilities.md) | Electronics, placement, mechanical, firmware, sourcing, release |
| [MCP tool reference](docs/mcp-tools.md) | Agent workflow, all tools, response envelope, resources |
| [Platform architecture](docs/architecture.md) | Board families, backend maturity, repo layout, module map |
| [Validation contract](docs/validation-contract.md) | Gate statuses, release rules, physical evidence boundary |

---

## Development setup

```bash
python3 -m venv .venv
.venv/bin/pip install '.[dev,mcp]'
npm ci --ignore-scripts
.venv/bin/hw --root . create-project quadruped_robot_controller
.venv/bin/hw --root . iterate quadruped_robot_controller --no-external
```

Without native toolchains all external gates return `blocked`. Install native macOS backends
and run the complete flow:

```bash
make toolchains
.venv/bin/hw --root . design-until-release quadruped_robot_controller --external
```

---

## Known limits

- The `reference` backend is candidate-only. `tscircuit` and `kicad` are fabrication-release-eligible;
  `python_netlist` is netlist-release-eligible; `atopile` is HDL-source-release-eligible. All
  release paths require every configured gate to pass.
- Digital gates cannot certify load thermals, EMI/EMC, vibration, abuse safety, ingress
  protection, transients, or connector life. These gaps are stated explicitly in every generated
  report and cannot be closed by software.
- The complete cross-domain flow depends on native KiCad, OpenCASCADE, Freerouting, tscircuit,
  and Zephyr. Validated paths: Linux container (CI), macOS (`make toolchains`), and Windows
  (Python test suite — native toolchains not yet installed on Windows runners).
- The tracked `r1` export is historical digital evidence. The current checked-in `reference`
  configuration is candidate-only and its release gate is expected to remain blocked unless a
  compiled backend is selected and all native gates pass.

---

## Generated example

The tracked robotics-controller example provides inspectable output without a local toolchain run:

- [Example and proof index](examples/robotics-motor-controller/README.md)
- [Complete generated bundle](projects/quadruped_robot_controller/exports/quadruped_robot_controller-r1.zip)
- [Validation report](projects/quadruped_robot_controller/exports/r1/docs/validation_report.json)
- [Known physical risks](projects/quadruped_robot_controller/exports/r1/docs/known_risks.md)

These are generated design artifacts and digital evidence, not proof of fabrication or physical
qualification.
