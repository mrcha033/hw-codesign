# hw-codesign: agentic hardware design system

[![CI](https://github.com/mrcha033/hw-cli/actions/workflows/ci.yml/badge.svg)](https://github.com/mrcha033/hw-cli/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/hw-codesign-platform)](https://pypi.org/project/hw-codesign-platform/)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://pypi.org/project/hw-codesign-platform/)
[![Platforms](https://img.shields.io/badge/platforms-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey)](#development-setup)
[![MCP](https://img.shields.io/badge/MCP-FastMCP%203.4-purple)](docs/mcp-tools.md)

![hw-cli logo](docs/assets/hero.png)

An MCP server and CLI that lets AI agents — Claude Code, Claude Desktop, Codex, or any
MCP-capable agent — design PCB electronics, mechanical parts, firmware interfaces, sourcing
decisions, and manufacturing outputs. Agents author cross-domain hardware candidates through
structured tool calls; the platform promotes only evidence-backed candidates through tiered
release gates.

Three board family templates ship ready to use: an STM32H7 robotics motor controller, an
ESP32-S3 IoT sensor data logger, and an nRF52840 BLE sensor node. Each has a generated
candidate bundle, review bundle, and digital gate report an agent can inspect without running
a local toolchain.

> **Evidence status:** generated Gerbers, STEP files, BOM, firmware, and digital gate reports
> are included. These are not fabricated, electrically brought-up, thermally qualified, or
> EMC-tested boards.

---

## Connect an agent

### Codex

Install the repository-owned plugin from a local clone:

```bash
codex plugin marketplace add "$PWD"
codex plugin add hw-codesign@hw-cli
```

Start a new Codex task, then invoke `$design-hardware` or ask Codex to create, inspect,
validate, compare, or prepare a hardware candidate for release. The plugin runs the MCP
server from the checked-out source with Python 3.11+ and uses the repository root as
`HW_PLATFORM_ROOT`.

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "hw-codesign": {
      "command": "uvx",
      "args": ["--from", "hw-codesign-platform[mcp]", "hw-mcp"],
      "env": {
        "HW_PLATFORM_ROOT": "/absolute/path/to/hardware-workspace"
      }
    }
  }
}
```

### Claude Code

```bash
claude mcp add hw-codesign \
  -e HW_PLATFORM_ROOT="$PWD" \
  -- uvx --from 'hw-codesign-platform[mcp]' hw-mcp
```

### Full toolchain container (KiCad, OpenCASCADE, Freerouting, Zephyr)

```bash
docker run --rm -v "$PWD:/workspace" ghcr.io/mrcha033/hw-cli:latest hw-mcp
```

Point the MCP client at `stdio` transport from the container. Toolchain-dependent gates
(`native_erc`, `native_drc`, `autoroute`, `native_zephyr_build`) become available only when
the corresponding native tool is reachable from the server process.

The workspace path must be writable; the server creates projects, validation reports, review
bundles, and release artifacts beneath it.

---

## What an agent does with this server

The canonical agent workflow, from the [MCP tool reference](docs/mcp-tools.md):

```
hw_get_capabilities            ← which backends and native tools are installed
hw_create_project              ← instantiate a board family template
hw_update_requirements         ← lower requirements into typed fields plus resolved/unresolved assumption IR

# Author topology, placement, and firmware
hw_propose_circuit_block       ← search the component catalog before committing
hw_add_circuit_block           ← add a circuit block; ERC runs and result is returned immediately
hw_set_placement_constraint    ← express adjacent_to / near_connector; gate runs and coordinates refresh
hw_design_firmware_module      ← author a firmware behavior (timeout_shutdown, periodic_transmit, …)
hw_check_cross_domain_consistency

hw_design_candidate            ← generate all domains, run gates, return semantic representation
                                  and review bundle; always release_eligible=false until gates pass
hw_explore_design_space        ← score backend, component, mechanical, and supplier alternatives
hw_run_grounding_benchmark     ← adversarial check: injected defects must be caught by gates
hw_run_design_benchmark        ← held-out intents: gate pass-rate plus physical evidence gaps
hw_generate_physical_qualification_plan
hw_record_physical_evidence    ← attach bench measurements; physical_qualification gate requires them

hw_check_release_gate          ← the only tool that sets release_eligible=true
hw_export_release_bundle       ← ZIP the release directory; release_eligible=true on status=released
```

Every tool response carries `release_eligible`, `candidate_only`, and
`release_blocking_failures`. `release_eligible: true` is set only by `hw_check_release_gate`
(status `pass`) and `hw_export_release_bundle` (status `released`). An agent cannot self-report
a release. See [MCP tool reference](docs/mcp-tools.md) for the full response envelope.

---

## Board families

Three templates are maintained and have generated candidate artifacts an agent can open
immediately with `hw_open_project`:

| Template | MCU | Layers | Generated artifacts |
|---|---|---|---|
| `robotics_controller_full` | STM32H743VIT6 LQFP-100 | 4 (6-layer option) | [proof index](examples/robotics-motor-controller/README.md) |
| `sensor_data_logger` | ESP32-S3-WROOM-1 | 2 | [proof index](examples/sensor-data-logger/README.md) |
| `ble_sensor_node` | nRF52840-QIAA | 2 | [proof index](examples/ble-sensor-node/README.md) |

An agent starts a new project with:

```
hw_create_project(name="my_board", template="sensor_data_logger")
```

To use a materially different topology, see [Adapting the design system](docs/adapting-a-spec.md).

---

## Documentation

| Doc | Contents |
|---|---|
| [MCP tool reference](docs/mcp-tools.md) | Setup, canonical agent workflow, all tools, response envelope, resources |
| [Zero to first candidate report](docs/first-run.md) | CLI walkthrough: candidate generation without native toolchains |
| [Capabilities reference](docs/capabilities.md) | Electronics, placement, mechanical, firmware, sourcing, release |
| [Adapting the design system](docs/adapting-a-spec.md) | Spec parameters, topology extension, backend selection, new board families |
| [Platform architecture](docs/architecture.md) | Board families, backend maturity, repo layout, module map |
| [Validation contract](docs/validation-contract.md) | Gate statuses, release tiers, adapter contract, physical evidence boundary |

---

## Development setup

```bash
python3 -m venv .venv
.venv/bin/pip install '.[dev,mcp]'
npm ci --ignore-scripts
PYTHONPATH=src python3 -m hw_codesign.cli --root . design-candidate quadruped_robot_controller
```

Without native toolchains all external gates return `blocked`. Install native macOS backends
and run the complete flow:

```bash
make toolchains
PYTHONPATH=src python3 -m hw_codesign.cli --root . design-until-release quadruped_robot_controller --external
```

---

## Known limits

- The `reference` backend is candidate-only. The canonical fabrication backends are
  `tscircuit` (Circuit JSON -> KiCad bridge) and native `kicad`; `python_netlist`
  is netlist-release-eligible (`netlist/compiled_netlist.json`); `atopile` is
  HDL-source-release-eligible (`source/atopile/design.ato`). All release paths
  require every configured gate to pass.
- Digital gates cannot certify load thermals, EMI/EMC, vibration, abuse safety, ingress
  protection, transients, or connector life. These gaps are stated explicitly in every generated
  report and cannot be closed by software.
- The complete cross-domain flow depends on native KiCad, OpenCASCADE, Freerouting, tscircuit,
  and Zephyr. Validated paths: Linux container (CI), macOS (`make toolchains`), and Windows
  (Python test suite — native toolchains not yet installed on Windows runners).
- Hosted MCP registry publication is deferred until the public tool interface and versioning policy are stable; the repository-owned Codex plugin is installable from a local clone.
