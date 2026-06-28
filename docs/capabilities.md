# Capabilities reference

## Electronics topology authoring

- Agents author circuit blocks via `hw_add_circuit_block`: specify a ref, category, and connection
  map; the block is merged into the base topology, nets are re-derived, and ERC runs immediately
- `hw_propose_circuit_block` searches the curated component catalog by category and returns
  candidates with BOM-resolution status before any block is committed
- Agent-authored blocks stored under `agent_electronics.blocks` in `spec/agent_blocks.yaml`;
  distinct key prevents collision with `system.yaml` during spec merge
- ERC tolerates single-pin nets when every endpoint belongs to an agent block

## Electronics backends

- Deterministic typed electrical graph with role-set resolver and curated component database;
  every resolved component has immutable provenance
- Shared source-generation step plus six-gate backend contract (compile → netlist → graph parity
  → footprint parity → layout → manufacturing export) enforced across all adapters
- Offline pinned **tscircuit 0.1.1491**: Circuit JSON netlist, pad, placement, routing, and
  error-element validation
- **KiCad-native**: native XML netlist, ERC/DRC, Freerouting 2.2.4 autoroute (DSN/SES
  round-trip), and Gerber/drill/position/BOM/STEP export
- **python_netlist**: netlist-release-eligible; produces `compiled_netlist.json` + firmware;
  layout and manufacturing gates are N/A rather than blocking
- **Atopile**: emits `.ato` source and runs `ato build`; when compile passes, `netlist_extract`
  and `graph_parity` resolve via source-AST parity; footprint/layout/manufacturing blocked pending
  a KiCad plugin path
- KiCad CLI and Zephyr `west` adapters emit structured `tool_unavailable` reports when absent

## Placement

- Agent-authored placement constraints via `hw_set_placement_constraint`: express relationships
  (`adjacent_to`, `near_connector`) rather than absolute XY coordinates; the placer derives
  positions and the `placement_constraints` gate validates compliance immediately on write
- Constraint-driven placement proposal: structured, provenance-tagged placements with keepout,
  mounting-hole, connector-edge, decoupling-proximity, and thermal-spacing constraints
- Hard-blocks on off-board components, coincident centers, and connectors placed on the wrong
  board half; advisory warnings on coarse courtyard overlap estimation
- `layout_thermal_integrity` and `layout_signal_integrity` are gated checks that block
  high-current designs on under-layered stackups, thermal-risk components placed next to
  sensitive devices, and misplaced RF antenna or USB ESD components
- Decoupling proximity is explicitly unenforced — cap-to-IC association is not in the netlist;
  the gate says so rather than claiming it checked something it did not
- Not authoritative: native ERC/DRC and the mechanical interference gate remain the
  release-blocking arbiters

## Mechanical

- Parametric 3D part design via `hw_design_part`: five part types (`pcb_mount_bracket`,
  `standoff_tower`, `cable_clip`, `din_rail_adapter`, `custom_enclosure_variant`), each with
  typed intent fields; parts exported as STEP + STL with an FDM printability report
- Spec-parameterized OpenCASCADE enclosure variants, mounting plates, frame brackets, connector
  cutouts, and board STEP assembly import/export
- Gates: valid solid, manifold STL, tolerance-aware board/component clearance, connector
  alignment, mounting-hole alignment, and measured BRep interference volume — nonzero
  interference returns `fail`
- `mechanical_connector_retention` requires high-vibration exposed connector designs to declare
  a retention fixture, method, and covered connector refs before the candidate can promote
- Mechanical release requires the board STEP exported by the electronics backend; missing
  evidence returns `blocked`, not a fabricated pass

## Firmware module authoring

- Agents author firmware behavior modules via `hw_design_firmware_module`: four parametric
  behaviors (`timeout_shutdown`, `periodic_transmit`, `state_machine`, `sensor_poll`); each
  emits a `.c` file under `firmware/modules/` with matching Zephyr config entries
- `firmware_modules` gate validates that every referenced signal exists in the pinmap and that
  motor/e-stop specs include a `timeout_shutdown` behavior that disables motor outputs
- `firmware_interface_contract` verifies generated Zephyr config and bring-up stubs cover
  required board interfaces (I2C, CAN, USB, e-stop fail-safe, motor PWM, BLE) before firmware
  build gates can promote the candidate
- Signal-level cross-domain consistency checked by `hw_check_cross_domain_consistency`:
  placement constraint refs verified against BOM, firmware module signals verified against pinmap

## Suppliers and BOM

- Normalized curated, LCSC/JLCPCB, Digi-Key, Mouser, and Octopart-style supplier adapters with
  datasheet evidence and availability gates
- Release checks consume only in-repository snapshots under `parts/suppliers`; no implicit
  network lookup at release time
- Known out-of-stock or discontinued parts fail; missing or stale evidence blocks
- `sourcing_resilience` gate: critical roles must have a curated alternative listed in the role
  set or an explicit single-source justification; roles with neither return `fail`
- Manufacturer datasheet review evidence hashed into resolved component provenance
- `role_overrides` in `system.yaml` lets a project select a curated alternative for any role;
  the resolver enforces that the override names a listed alternative

## Design space exploration and grounding

- `hw_explore_design_space` enumerates backend, component, mechanical variant, and supplier axes
  and scores each against the current gates; result written to `history/design_space/exploration.json`
- `hw_run_grounding_benchmark` adversarially mutates generated artifacts (pinout, footprint,
  power tree, interface wiring, layout, RF, connector retention, sourcing, firmware) and confirms
  every relevant gate catches the injected defect; a missed case fails the benchmark
- `hw_generate_physical_qualification_plan` writes a machine-readable evidence contract (thermal,
  EMI/EMC, SI/PI, vibration, ingress, connector fatigue, bring-up); `hw_record_physical_evidence`
  attaches approved test evidence; `physical_qualification` remains `blocked` until every
  required test has an approved passing record

## Release

- Release gate requires every configured gate at `pass`, all critical assumptions resolved,
  and every declared artifact present with a matching hash
- Fabrication release: `tscircuit` and `kicad` backends (Gerber + drill + STEP + BOM)
- Netlist release: `python_netlist` (`compiled_netlist.json` + firmware)
- HDL source release: `atopile` (`design.ato` + project metadata)
- `reference` is candidate-only; no release path regardless of gate status

See [validation-contract.md](validation-contract.md) for the full gate inventory and
release eligibility rules.
