# Platform architecture

hw-codesign is a command-line and MCP-server design system for AI agents. From a structured YAML spec
and agent-authored design actions, it generates PCB topology, parametric mechanical source, firmware
pinmaps and interfaces, sourcing decisions, manufacturing outputs, and review bundles. Release
bundles are produced only after every configured gate reaches `pass`. Physical qualification risks
are stated as explicit gaps and cannot be closed by software.

The primary authoring surface is semantic-first: requirements, electrical graph, executable
pin-name semantic schematic, relative placement constraints, mechanical contract, and firmware
pinmap remain machine-readable before native EDA/CAD outputs are emitted.

## Board families

Thirteen maintained board templates are shipped. Three representative families
are summarized here:

| Template | MCU | Layers | Key features |
|---|---|---|---|
| `robotics_controller_full` | STM32H743VIT6, LQFP-100 | 4 | 12 motor channels, CAN, 24 V battery, e-stop, 6-layer option |
| `sensor_data_logger` | ESP32-S3-WROOM-1 | 2 | USB-C power, I2C IMU, sensor logging |
| `ble_sensor_node` | nRF52840-QIAA | 2 | LiPo (BQ24079 + BQ27441 + AP2112K), SHT31, BLE, 50×35 mm |

Supporting a materially different topology requires extending role sets, component catalogs,
templates, and sometimes generators. See [adapting-a-spec.md](adapting-a-spec.md).

## Backend maturity

| Backend | What works | Release tier |
|---|---|---|
| `kicad` | Native netlist, ERC/DRC, Freerouting autoroute, Gerber/drill/BOM/STEP export | Fabrication |
| `tscircuit` | Pinned offline compile (0.1.1491), solver-coordinate and Circuit JSON placement parity, graph/footprint parity, KiCad manufacturing bridge | Fabrication |
| `python_netlist` | Deterministic `compiled_netlist.json` + firmware; layout and manufacturing gates are N/A | Netlist |
| `atopile` | Real `.ato` source, `ato build`; compile/netlist_extract/graph_parity via source-AST parity; footprint/layout/manufacturing blocked pending KiCad plugin path | HDL source |
| `reference` | Design intent and candidate artifacts for inspection and tutorials | Candidate-only |

All release paths require every configured gate to pass. All backends emit `blocked` (not silence)
when a required tool is absent.

## Repository layout

```
src/hw_codesign/          core platform and service layer
  backends/               per-backend adapters (tscircuit, kicad, atopile, ...)
    firmware_modules/     parametric firmware behavior renderers
    parts/                parametric 3D part designers
  templates/              project spec templates (one YAML per board family)
  contracts/              MCP tool schemas and response contracts
schemas/                  JSON Schema for spec validation
parts/
  components/             curated component definitions with pin, footprint, and datasheet evidence
  role_sets/              functional role assignments + alternatives + single-source justifications
  schemas/                JSON Schema for role set files
  suppliers/              supplier snapshot records (curated, LCSC/JLCPCB, Digi-Key, Mouser)
projects/<name>/          generated project workspaces
  spec/
    system.yaml           board topology, backend, supply rails
    agent_blocks.yaml     agent-authored circuit blocks + placement constraints
  electronics/
    intent/               generated design intent
    generated/
      electrical_graph.json
      semantic/           semantic_schematic.json + semantic_schematic.py
  mechanical/source/      parameterized CAD source + mechanical contract
  firmware/
    generated/            pinmap.json, devicetree overlay, Zephyr scaffold
    modules/              agent-authored firmware module .c files
  validation/
    reports/*.json        one structured result per gate
    physical/             qualification plan JSON and evidence records
  history/
    decisions.jsonl       structured design decision log
    iterations/           immutable iteration snapshots
    design_space/         design-space exploration results
  exports/
    candidates/           candidate bundles and ZIPs
    r<n>/                 release bundles (Gerbers, STEP, BOM, firmware, docs)
```

## Key modules

| Module | Responsibility |
|---|---|
| `service.py` | Orchestrates design candidate generation, gate checks, repair loops, release packaging |
| `validation.py` | Gate checks: spec, BOM, power-tree, interface integrity, firmware modules, pin resolution |
| `placement.py` | Constraint-driven placement proposal; thermal and signal-integrity layout checks |
| `generators.py` | Electrical graph, semantic schematic (JSON + Python), BOM, firmware source |
| `semantic_schematic.py` | Semantic schematic authoring model and pin-name wiring representation |
| `resolver.py` | Role-set component resolution with alternative enforcement and role-override support |
| `reference_backend.py` | Reference graph builder, ERC, DRC, fabrication export for the reference backend |
| `mcp_server.py` | FastMCP server wiring: registers all tools and resources |
| `cli.py` | Click CLI: wraps every service method as a subcommand |
| `workspace.py` | Project directory management, spec merge, iteration snapshots |
| `board_layout.py` | Component-position derivation from placement constraints |
| `policy.py` | Change policy and assumption resolution |
| `provenance.py` | Artifact provenance hashing and recording |
