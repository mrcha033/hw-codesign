---
name: design-hardware
description: Design, inspect, iterate, validate, and package cross-domain hardware projects through the hw-codesign MCP server. Use when turning requirements into PCB electronics, placement, mechanical, firmware, sourcing, manufacturing, candidate-review, or release artifacts; diagnosing blocked or failed hardware gates; comparing candidates; or preparing an evidence-backed release.
---

# Design Hardware

Use the `hw_*` MCP tools as the primary interface. Keep project changes tool-mediated so requirements, decisions, reports, and iterations remain structured and auditable.

## Core workflow

1. Call `hw_get_capabilities` and `hw_diagnose_environment` before promising a backend or release tier. Treat unavailable native tools as explicit blockers.
2. Use `hw_open_project` for an existing project or `hw_create_project` for a new one. Discover current templates through capabilities instead of assuming a fixed list.
3. Lower natural-language intent with `hw_update_requirements`. Inspect `hw_list_assumptions` and resolve only decisions the user has actually authorized with `hw_resolve_assumption`.
4. Author design intent through semantic tools:
   - Search with `hw_propose_circuit_block`, then commit with `hw_add_circuit_block`.
   - Express relative placement using `hw_set_placement_constraint`.
   - Add behaviors with `hw_design_firmware_module`.
   - Run `hw_check_cross_domain_consistency` after cross-domain edits.
5. Call `hw_design_candidate` to generate electronics, mechanical, firmware, sourcing, validation, and review artifacts. For deliberate alternatives, use design-space exploration, candidate listing/review tools, and comparison tools.
6. Inspect failures with `hw_get_failure_report` and `hw_generate_repair_plan`. Apply repairs only when their required approval is present. Snapshot meaningful iterations and record design decisions.
7. Run `hw_run_all_checks` at the requested evidence level. Use `hw_prepare_fabrication_review` before a fabrication handoff.
8. Promote only through `hw_check_release_gate`, then package with `hw_export_release_bundle`. Verify the result with `hw_verify_release`.

## Evidence rules

- Treat `blocked` as unresolved, never as `pass`.
- Treat generated artifacts as candidates until the release gate promotes them.
- Never manually claim `release_eligible=true`. Only `hw_check_release_gate` and a successful `hw_export_release_bundle` may report release eligibility.
- Keep the `reference` backend candidate-only. Use a release-capable backend and satisfy its tier-specific gates for netlist, HDL-source, or fabrication release.
- Do not infer physical qualification from digital checks. Thermal behavior, EMI/EMC, vibration, ingress, connector life, assembly quality, and board bring-up require approved physical evidence.
- Use `hw_generate_physical_qualification_plan` and `hw_record_physical_evidence` for real bench evidence. Do not invent measurements or provenance.
- Preserve structured failure and provenance data. Do not bypass failed gates by editing generated reports or release manifests directly.

## Scope control

Lead with agent-driven hardware candidate generation across PCB, CAD, firmware, sourcing, and manufacturing. Explain evidence-backed promotion boundaries after the design capability; do not reduce the system to a release wrapper, and do not overclaim autonomous physical correctness.

If a requested topology is materially different from available templates or curated components, report the unsupported roles and extend the source catalogs/templates only when the user has asked for repository development. Do not disguise a renamed template as a new board family.
