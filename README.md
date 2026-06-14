# Verifiable Agentic Hardware Co-Design Platform

An agent-first, repository-backed platform for jointly generating and validating electronics intent, mechanical source, firmware board support, and manufacturing release evidence.

The platform treats structured specifications as the source of truth. It never reports native EDA, CAD, firmware, sourcing, or physical validation as passed unless the corresponding check actually ran and passed.

## Current implementation

- Persistent project workspaces and numbered iteration snapshots
- Full robotics controller template with explicit critical assumptions
- JSON Schema validation and structured failure taxonomy
- Built-in electrical budget/safety, mechanical envelope, and firmware pin-map checks
- Deterministic typed electrical graph, editable KiCad schematic/PCB, mechanical source, Zephyr source, and BOM generation
- Plane-preseeded Freerouting 2.2.4 autoroute with DSN/SES round-trip through KiCad's native Python API
- KiCad CLI and Zephyr `west` adapters with honest blocked reports when unavailable
- Release gate requiring all gates, resolved critical assumptions, and actual release artifacts
- Shared CLI/MCP service layer and JSON-only operation results
- Docker toolchain definition and pytest coverage

The included reference robotics backend now emits a native KiCad 4-layer project with typed pin/net connectivity, deterministic power-plane trees, externally autorouted signal layers, KiCad-validated Gerber/drill/board STEP outputs, parametric enclosure STEP/STL, Zephyr BSP/application sources, a cross-compiled STM32H743 ELF, and a checksum-verified release archive. Physical qualification risks remain explicit and cannot be closed by software.

## Quick start

```bash
python3 -m venv .venv
.venv/bin/pip install '.[dev,mcp]'
.venv/bin/hw --root . create-project quadruped_robot_controller
.venv/bin/hw --root . iterate quadruped_robot_controller --no-external
```

Install the pinned native macOS backends and run the complete flow:

```bash
make toolchains
.venv/bin/hw --root . design-until-release quadruped_robot_controller --external
```

Run with native backends enabled:

```bash
.venv/bin/hw --root . iterate quadruped_robot_controller
```

Missing `kicad-cli`, KiCad Python, the pinned Freerouting JAR/JRE, or `west` produces a structured `tool_unavailable` result. It does not silently skip the gate.

## MCP server

```bash
HW_PLATFORM_ROOT="$PWD" .venv/bin/hw-mcp
```

Core tools include `hw_create_project`, `hw_read_spec`, `hw_validate_spec`, generation tools, native ERC/DRC/build tools, semantic checks, `hw_run_all_checks`, `hw_generate_repair_plan`, `hw_run_design_iteration`, `hw_check_release_gate`, and `hw_generate_design_report`.

## Gate semantics

- `pass`: the check ran and found no blocking finding.
- `fail`: the check ran or had sufficient local evidence and found a violation.
- `blocked`: required tooling or decision input was unavailable.

Digital release evidence cannot certify load thermals, EMI/EMC, abuse safety, vibration life, motor transients, ingress protection, or connector fatigue. These remain explicit physical validation gaps in generated reports.

## Repository layout

Generated projects follow the requested `projects/<name>/{spec,electronics,mechanical,firmware,validation,exports,history}` structure. Product code lives in `src/hw_codesign`; schemas are in `schemas`; adapters are isolated under `src/hw_codesign/backends`.
