# Verifiable Agentic Hardware Co-Design Platform

An agent-first, repository-backed platform for jointly generating and validating electronics intent, mechanical source, firmware board support, and manufacturing release evidence.

The platform treats structured specifications as the source of truth. It never reports native EDA, CAD, firmware, sourcing, or physical validation as passed unless the corresponding check actually ran and passed.

## Current implementation

- Persistent project workspaces and numbered iteration snapshots
- Full robotics controller template with explicit critical assumptions
- JSON Schema validation and structured failure taxonomy
- Built-in electrical budget/safety, mechanical envelope, and firmware pin-map checks
- Deterministic typed electrical graph, editable KiCad schematic/PCB, mechanical source, Zephyr source, and BOM generation
- Curated in-repository component database, role-set resolver, pin/symbol/footprint contracts, and immutable resolution provenance
- Normalized curated, LCSC/JLCPCB, Digi-Key, Mouser, and Octopart-style supplier adapters with datasheet evidence and availability gates
- Shared electronics backend contract covering source, compile, netlist extraction, graph parity, footprint parity, layout evidence, and manufacturing export
- Offline pinned tscircuit 0.1.1491 PCB compile with Circuit JSON netlist, pad, placement, routing, and error-element validation
- KiCad-native source adapter with native XML netlist extraction and Gerber/drill/position/BOM/STEP export evidence
- Executable Python-netlist adapter that is intentionally blocked from release because it has no PCB layout or manufacturing output
- Atopile adapter placeholder that emits only marked intent and returns `backend_not_implemented` for every contract gate
- Constraint-driven placement proposal: structured, provenance-tagged component placements with derived keepout, mounting-hole, connector-edge, decoupling-proximity, and thermal-spacing constraints, checked by a non-authoritative `placement_constraints` gate (blocks on off-board/coincident/wrong-side-connector; advisory courtyard/thermal warnings; decoupling proximity represented but deferred because cap-to-IC association is not modelled). It proposes and checks placement only; native ERC/DRC and the mechanical interference gate remain authoritative
- Plane-preseeded Freerouting 2.2.4 autoroute with DSN/SES round-trip through KiCad's native Python API
- KiCad CLI and Zephyr `west` adapters with honest blocked reports when unavailable
- Spec-parameterized OpenCASCADE enclosure variants, mounting plates, frame brackets, connector cutouts, and board STEP assembly import/export
- Mechanical gates for valid solids, manifold STL, tolerance-aware board/component clearance, electrical connector alignment, mounting-hole alignment, and measured BRep interference volumes
- Release gate requiring all gates, resolved critical assumptions, and actual release artifacts
- Shared CLI/MCP service layer and JSON-only operation results
- Docker toolchain definition and pytest coverage

The reference robotics backend emits design-intent and candidate artifacts only. It is never release eligible. Release requires a complete tscircuit or KiCad-native backend contract plus curated component, KiCad, mechanical, Zephyr, parity, assumption, and integrity gates. Python-netlist and Atopile projects remain candidate-only. Physical qualification risks remain explicit and cannot be closed by software.

## Quick start

```bash
python3 -m venv .venv
.venv/bin/pip install '.[dev,mcp]'
npm ci --ignore-scripts
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

Mechanical release requires the native board STEP exported by the electronics backend. Missing OpenCASCADE or board STEP evidence returns `blocked`; malformed solids, non-manifold STL, connector drift, insufficient tolerance/clearance, or nonzero assembly intersection volumes return `fail`. All configured enclosure variants and enabled fixtures are required release artifacts and are covered by both the mechanical manifest and release manifest integrity gates.

Electronics backends are selected with `electronics.backend`: `reference`, `tscircuit`, `kicad`, `python_netlist`, or `atopile`. Every non-reference adapter emits `electronics/source/<backend>/source_manifest.json` with the same six contract gates. A missing compiler blocks the contract; a nonzero compiler or compiled error element fails it. No backend can pass release policy without manufacturing artifacts.

Supplier selection is configured with `sourcing.provider`. Release checks consume only in-repository supplier snapshots under `parts/suppliers`; they do not perform an implicit network lookup. An `available` record requires a supplier identifier and observation timestamp, known out-of-stock or discontinued parts fail, and missing or stale evidence blocks. Manufacturer datasheet review evidence is maintained under `parts/evidence` and is hashed into each resolved component's provenance.

## MCP server

```bash
HW_PLATFORM_ROOT="$PWD" .venv/bin/hw-mcp
```

Core tools include `hw_create_project`, `hw_read_spec`, `hw_validate_spec`, generation tools, native ERC/DRC/build tools, semantic checks, `hw_run_all_checks`, `hw_generate_repair_plan`, `hw_run_design_iteration`, `hw_check_release_gate`, and `hw_generate_design_report`.

Domain generation is explicit: `hw_generate_reference_intent`, `hw_generate_electronics_source`, `hw_generate_mechanical_source`, and `hw_generate_firmware_source`. Only `hw_generate_all` invokes all domains.

## Gate semantics

- `pass`: the check ran and found no blocking finding.
- `fail`: the check ran or had sufficient local evidence and found a violation.
- `blocked`: required tooling or decision input was unavailable.

Digital release evidence cannot certify load thermals, EMI/EMC, abuse safety, vibration life, motor transients, ingress protection, or connector fatigue. These remain explicit physical validation gaps in generated reports.

## Repository layout

Generated projects follow the requested `projects/<name>/{spec,electronics,mechanical,firmware,validation,exports,history}` structure. Product code lives in `src/hw_codesign`; schemas are in `schemas`; adapters are isolated under `src/hw_codesign/backends`.

Candidate bundles live under `exports/candidates/<iteration_id>`. Release artifacts and bundles live under `exports/releases/<revision>` and are created only after every release gate passes.
