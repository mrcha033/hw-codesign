# hw-codesign: agentic hardware design with hard release gates

An AI co-design system for electronics, mechanical, firmware, and BOM that
cannot produce a passing release unless every check actually ran and passed.

Missing `kicad-cli` returns `blocked`. Missing OpenCASCADE returns `blocked`.
A compiled error element in tscircuit returns `fail`. An unresolved critical
assumption blocks release. Decoupling proximity not yet modelled is reported as
explicitly deferred, not silently green. **Nothing is assumed to have worked.**

```json
{
  "gate": "tscircuit_compile",
  "status": "blocked",
  "failures": [{"code": "tool_unavailable", "message": "tscircuit compiler not found"}]
}
```

vs.

```json
{
  "gate": "tscircuit_compile",
  "status": "pass",
  "metrics": {"error_elements": 0, "pad_count": 183, "route_count": 217}
}
```

The difference is observable in JSON and enforced by the release gate.

## What this is

A command-line and MCP-server platform that takes a structured YAML spec and
produces a release bundle — Gerbers, STEP, BOM, firmware source, Zephyr
devicetree — only after every configured gate reaches `pass`. Reference
designs produce `candidate` artifacts and are explicitly blocked from release.
Physical qualification risks (load thermals, EMI/EMC, vibration, abuse) are
stated as explicit gaps in every generated report and cannot be closed by
software.

The current reference design is a robotics motor controller (4-layer PCB,
STM32H7, 12 motor channels, CAN, 24 V VBAT).

## Capabilities

### Electronics
- Deterministic typed electrical graph with role-set resolver and curated
  component database; every resolved component has immutable provenance
- Shared six-gate backend contract (source → compile → netlist → graph parity →
  footprint parity → layout → manufacturing export) enforced across all adapters
- Offline pinned **tscircuit 0.1.1491** PCB compile: Circuit JSON netlist, pad,
  placement, routing, and error-element validation
- **KiCad-native** adapter: native XML netlist extraction, ERC/DRC, Freerouting
  2.2.4 autoroute (DSN/SES round-trip), and Gerber/drill/position/BOM/STEP export
- **Python-netlist** adapter: intentionally candidate-only; blocked from release
  because it has no PCB layout or manufacturing output — the block is explicit
- **Atopile** adapter: placeholder emitting marked intent only, blocked on every
  contract gate
- KiCad CLI and Zephyr `west` adapters with structured `tool_unavailable` reports
  when the tool is absent — they do not silently skip

### Placement
- Constraint-driven placement proposal: structured, provenance-tagged placements
  with keepout, mounting-hole, connector-edge, decoupling-proximity, and
  thermal-spacing constraints
- Hard-blocks on off-board components, coincident centers, and connectors placed
  on the wrong board half; advisory warnings on coarse courtyard overlap and
  thermal spacing
- Decoupling proximity is represented as explicitly unenforced — cap-to-IC
  association is not in the netlist; the gate says so rather than claiming it
  checked something it did not
- Not authoritative: native ERC/DRC and the mechanical interference gate remain
  the release-blocking arbiters

### Mechanical
- Spec-parameterized OpenCASCADE enclosure variants, mounting plates, frame
  brackets, connector cutouts, and board STEP assembly import/export
- Gates: valid solid, manifold STL, tolerance-aware board/component clearance,
  connector alignment, mounting-hole alignment, and measured BRep interference
  volume — nonzero interference returns `fail`
- Mechanical release requires the board STEP exported by the electronics backend;
  missing evidence returns `blocked`, not a fabricated pass

### Suppliers and BOM
- Normalized curated, LCSC/JLCPCB, Digi-Key, Mouser, and Octopart-style
  supplier adapters with datasheet evidence and availability gates
- Release checks consume only in-repository snapshots under `parts/suppliers`;
  no implicit network lookup at release time
- Known out-of-stock or discontinued parts fail; missing or stale evidence blocks
- Manufacturer datasheet review evidence hashed into resolved component provenance

### Release
- Release gate requires every configured gate at `pass`, all critical assumptions
  resolved by a human, and every declared artifact present on disk with a matching
  hash
- Only `tscircuit` and `kicad` backends are release-eligible; `reference`,
  `python_netlist`, and `atopile` are permanently candidate-only

## Quick start

```bash
python3 -m venv .venv
.venv/bin/pip install '.[dev,mcp]'
npm ci --ignore-scripts
.venv/bin/hw --root . create-project quadruped_robot_controller
.venv/bin/hw --root . iterate quadruped_robot_controller --no-external
```

Without native toolchains all external gates return `blocked`. That is the
expected and correct output when the tools are not installed.

Install the pinned native macOS backends and run the complete flow:

```bash
make toolchains
.venv/bin/hw --root . design-until-release quadruped_robot_controller --external
```

## MCP server

```bash
HW_PLATFORM_ROOT="$PWD" .venv/bin/hw-mcp
```

Tools: `hw_create_project`, `hw_read_spec`, `hw_validate_spec`, generation
tools, native ERC/DRC/build tools, semantic checks, `hw_run_all_checks`,
`hw_generate_repair_plan`, `hw_run_design_iteration`, `hw_check_release_gate`,
`hw_generate_design_report`. Generation is domain-explicit:
`hw_generate_reference_intent`, `hw_generate_electronics_source`,
`hw_generate_mechanical_source`, `hw_generate_firmware_source`.

## Gate semantics

| Status | Meaning |
|--------|---------|
| `pass` | check ran and found no blocking finding |
| `fail` | check ran and found a violation |
| `blocked` | required tooling or prior decision was absent |
| `candidate` | artifact was generated but is not release-eligible |

## Repository layout

```
src/hw_codesign/          # core platform and service layer
  backends/               # per-backend adapters (tscircuit, kicad, ...)
schemas/                  # JSON Schema for spec validation
parts/                    # curated component database and supplier snapshots
projects/<name>/          # generated project workspaces
  {spec,electronics,mechanical,firmware,validation,exports,history}/
```

Digital release evidence cannot certify load thermals, EMI/EMC, abuse safety,
vibration life, motor transients, ingress protection, or connector fatigue.
These remain explicit physical validation gaps in every generated report.
