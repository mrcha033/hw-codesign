# MCP tool reference

## Setup

```bash
HW_PLATFORM_ROOT="$PWD" uvx --from 'hw-codesign-platform[mcp]' hw-mcp
```

Claude Desktop configuration:

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

The workspace must be writable; projects, validation reports, review bundles, and release
artifacts are created beneath it.

## Canonical agent workflow

```
hw_get_capabilities          ← which backends and external tools are installed
hw_create_project / hw_open_project
hw_update_requirements       ← lowers natural-language requirements; returns release_blocking_failures

# Author topology, parts, placement, and firmware
hw_get_part_types            ← available parametric part types and their intent schemas
hw_design_part               ← design a 3D-printable part; returns STEP/STL + printability report
hw_propose_circuit_block     ← find catalog candidates for a given category before committing
hw_add_circuit_block         ← author a circuit block into the topology; ERC runs immediately
hw_set_placement_constraint  ← express adjacent_to / near_connector / thermal_separation relationships; gate runs on write
hw_design_firmware_module    ← author a firmware behavior (timeout_shutdown, periodic_transmit, …)
hw_record_design_decision    ← log a decision + rationale to history/decisions.jsonl
hw_check_cross_domain_consistency ← validate placement refs against BOM, firmware signals against pinmap

hw_design_candidate          ← primary design workflow: generate + gates + review bundle
hw_explore_design_space      ← rank backend, component, mechanical, and supplier alternatives
hw_run_grounding_benchmark   ← adversarial check: injected defects must be caught by gates
hw_run_design_benchmark      ← held-out suite: one-line intent → design_until_release, tracks gate pass-rate plus physical evidence gaps
hw_generate_physical_qualification_plan ← define the external evidence contract
hw_record_physical_evidence  ← attach approved bench measurements to the qualification gate
hw_generate_all              ← always candidate_only=true, release_eligible=false
hw_run_all_checks            ← include_external=true for the full gate matrix; includes candidate_critic
hw_review_release_readiness  ← non-authoritative summary: blocking gates, requirements, assumptions
hw_generate_repair_plan / hw_apply_repair_plan / hw_resolve_assumption
hw_design_until_release      ← autonomous loop: returns 'released', 'software_gates_ready' (all SW gates pass; run with include_external=True for native gates), 'blocked', or 'fail'
hw_check_release_gate        ← release_eligible=true when status==pass
hw_export_candidate_bundle   ← archive checkpoint (candidate_only=true, release_eligible=false)
hw_export_release_bundle     ← release_eligible=true when status==released
```

## Response envelope

Every tool response carries a consistent envelope that enforces the core invariant:
**candidate generated ≠ release passed ≠ fabrication qualified.**
The public tool registry exposes this as the shared top-level
`mcp_response_envelope` output schema; tool-specific fields compose underneath it.

| Field | Meaning |
|---|---|
| `release_eligible` | `false` on every tool; `true` only from `hw_check_release_gate` (status `pass`) and `hw_export_release_bundle` (status `released`) |
| `candidate_only` | `true` when the backend or gate state precludes release |
| `release_blocking_failures` | always-present list; empty only when no blockers are known |

`hw_review_release_readiness` additionally carries:

| Field | Meaning |
|---|---|
| `release_gate_authoritative` | always `false`; only `hw_check_release_gate` is authoritative |
| `readiness_estimate` | `pass` / `fail` / `blocked` from persisted reports; not a gate outcome |
| `data_freshness` | `current` / `possibly_stale` / `unknown` based on spec-vs-report file timestamps |

## Tools

### Platform introspection
- `hw_get_capabilities` — available backends, explicit release tiers,
  fabrication/netlist/source backend partitions, external tools, and which gates each enables
- `hw_diagnose_environment` — Python version, toolchain paths, installed packages

### Project and spec
- `hw_create_project` — create a new project from a template
- `hw_open_project` — open an existing project and return its spec
- `hw_snapshot_project` — snapshot the current project state as a named iteration
- `hw_compare_iterations` — diff two iteration snapshots
- `hw_read_spec` — read the merged project spec
- `hw_validate_spec` — validate the spec against its JSON Schema; returns failures with field paths
- `hw_update_spec` — write a spec section; requires `user_approved=true` for safety-critical sections
- `hw_update_requirements` — lower natural-language requirements into typed spec fields;
  also returns and persists `requirements_ir_v1` with lowered fields, explicitly
  resolved assumptions, unresolved assumptions, unsupported constraints, conflicting
  typed fields, required approvals, and affected gates.
  Retained critical assumptions such as motor-driver topology or cooling are
  release-blocking until explicitly resolved or waived.
  Explicit low/moderate/high vibration environment text is lowered into
  `mechanical.vibration_environment` for connector-retention and mounting gates.
  Explicit CAN/UART/I2C periodic telemetry text is lowered into
  `firmware.modules.<id>` `periodic_transmit` contracts for firmware-interface gates.
  Physical qualification and protocol claims such as EMI/EMC, vibration/shock
  standards, CAN-FD, USB-C PD, and numeric thermal limits are preserved as unresolved
  release blockers unless they are backed by explicit modeled fields or evidence.
  Its public output schema is `requirements_update_result`, not an opaque blob.
- `hw_list_assumptions` — list all declared design assumptions and their resolution state
- `hw_resolve_assumption` — resolve a named assumption; requires `approved=true`

### Mechanical part design
- `hw_get_part_types` — available parametric part types with their intent schemas
- `hw_design_part` — design a 3D-printable part from typed intent; returns STEP/STL + FDM report
- `hw_list_parts` — list all agent-designed parts for a project

### Electronics topology authoring
- `hw_propose_circuit_block` — search component catalog by category; returns candidates before commit
- `hw_add_circuit_block` — add or replace a circuit block; ERC gate result returned inline
- `hw_list_circuit_blocks` — list all agent-authored circuit blocks for a project

### Placement constraint authoring
- `hw_set_placement_constraint` — author an adjacent, connector-near, or minimum thermal-separation relationship; placement gate runs on write and generated coordinates and selected tscircuit source are refreshed for downstream candidate fabrication
- `hw_list_placement_constraints` — list all placement constraints for a project

### Firmware module authoring
- `hw_design_firmware_module` — author a firmware behavior module; emits `.c` + config
- `hw_list_firmware_modules` — list all agent-designed firmware modules for a project

### Design traceability
- `hw_record_design_decision` — log a decision + rationale to `history/decisions.jsonl`
- `hw_check_cross_domain_consistency` — validate placement refs against BOM and firmware signals against pinmap

### Primary design workflow
- `hw_design_candidate` — optionally lower a brief into the spec, generate all domains, run gates, return semantic-first representation and review bundle; always `release_eligible=false` until promotion gates pass
- `hw_explore_design_space` — score alternatives across backend, component, mechanical, and supplier axes; writes `history/design_space/exploration.json`
- `hw_run_grounding_benchmark` — adversarial check over pinout, footprint, support circuits including USB-C CC Rd, USB ESD pair mapping, I2C pull-up rail/value, crystal load-cap presence/grounding/pF-range value, boot strap bias, and status-LED device/polarity/current limiting, power tree including regulator VIN, dropout/headroom, enable bias, and powered-load supply ranges, rail decoupling, layout, oscillator placement, decoupling placement, RF, high-current loop area, connector retention, connector cutout alignment, mounting keepout intrusion, sourcing, critical-role alternate integrity, firmware pin assignment, motor PWM channel coverage, firmware modules, and dependency order
- `hw_generate_physical_qualification_plan` — write the external evidence contract (thermal, EMI/EMC, SI/PI, vibration, ingress, connector, assembly, bring-up)
- `hw_record_physical_evidence` — record approved external qualification evidence; `physical_qualification` remains `blocked` until every test has an approved passing record

### Generation
- `hw_generate_all` — generate electronics, mechanical, and firmware in one step
- `hw_generate_reference_intent` — reference-backend intent artifacts only
- `hw_generate_electronics_source` — electronics source for the configured backend
- `hw_generate_mechanical` — mechanical source (enclosure, mounting, fixtures)
- `hw_generate_firmware` — Zephyr pinmap, devicetree, app scaffold, and authored modules
- `hw_generate_bringup_tests` — bring-up test scripts from the firmware source

### Validation
- `hw_run_all_checks` — run all configured gates; `include_external=false` skips native toolchain gates plus tscircuit/KiCad backend compilers, returning blocked contract reports instead.
  The `candidate_critic` report performs a second-pass review over the whole candidate:
  false release-eligibility claims fail, while open physical/native evidence gaps are recorded as warnings.
- `hw_check_release_gate` — authoritative gate; the only tool that sets `release_eligible=true`
- `hw_get_failure_report` — read persisted gate reports; optionally filter by gate name
- `hw_run_erc` — KiCad-native ERC; returns structured failures
- `hw_run_drc` — KiCad-native DRC against a named fab profile
- `hw_check_electrical_semantics` — validate electrical graph semantics against spec constraints
- `hw_extract_electrical_graph` — return the resolved electrical graph JSON
- `hw_check_pinmap` — validate firmware pin assignments against the electrical graph
- `hw_check_mechanical_fit` — mechanical clearance, interference, and alignment checks
- `hw_build_firmware` — invoke `west build`; returns structured build result

### Iteration and repair
- `hw_run_design_iteration` — single supervised generate→check→repair cycle
- `hw_generate_repair_plan` — propose spec patches for current gate failures; includes `agent_actions`
- `hw_apply_repair_plan` — apply safe patches automatically; proposals requiring approval are returned
- `hw_design_until_release` — autonomous loop; requires `user_approved_autonomous_iteration=true`

### Candidate management
- `hw_export_candidate_bundle` — snapshot and ZIP the current state
- `hw_list_candidates` — list all candidate bundles for a project
- `hw_get_candidate` — retrieve metadata for a specific candidate bundle
- `hw_review_candidate` — structured review: gate summary, blocking failures, provenance
- `hw_compare_candidates` — diff two candidate bundles by gate status and artifact hashes

### Release readiness and export
- `hw_review_release_readiness` — non-authoritative summary from persisted reports
- `hw_check_release_gate` — authoritative gate; sets `release_eligible=true` on `pass`
- `hw_prepare_fabrication_review` — assemble a fabrication review package for external DFM
- `hw_export_pcb_fabrication` — Gerber, drill, BOM, pick-and-place; requires KiCad native
- `hw_export_mechanical` — STEP/STL files; requires OpenCASCADE
- `hw_import_board_step` — import an externally sourced board STEP into the assembly
- `hw_export_release_bundle` — ZIP the release directory; sets `release_eligible=true`
- `hw_generate_design_report` — human-readable design report markdown
- `hw_verify_release` — verify artifact integrity against the release manifest

## Resources

URI-template resources for structured reads without tool calls:

| Resource | Contents |
|---|---|
| `hw://project/{project}/release-gate` | Non-authoritative release readiness summary (`release_gate_authoritative: false`) |
| `hw://project/{project}/spec` | Full merged project spec |
| `hw://project/{project}/requirements` | Active requirements: lowered and unresolved constraints |

## Distribution

- PyPI publishes `hw-codesign-platform` from semantic-version tags using Trusted Publishing.
- GHCR publishes `ghcr.io/mrcha033/hw-cli` with the full native toolchain for `linux/amd64`.
- Each GitHub release attaches a canonical `bundle.json` and its `review_bundle.schema.json` contract.
- Homebrew is deferred; the container is the more reliable path for mixed Python/system dependencies.
- MCP registry publication is deferred until the public tool interface and versioning policy are stable.
