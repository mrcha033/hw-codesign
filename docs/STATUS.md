# Status: closed-loop physical correctness — progress and boundary

This is the authoritative status of the platform against its north-star goal —
*an agent designs PCB / mechanical / firmware / sourcing / reviewable release
artifacts with closed-loop physical correctness* — and, just as importantly, an
honest statement of the boundary between what software can close and what it
cannot. Read this before assuming a gap is unaddressed: some named gaps are
**deliberately** open because closing them in software would fabricate authority
the evidence cannot back — the one thing this platform's credibility forbids.

## Capabilities in place

- **Grounding gates (release-authoritative).** Dense, datasheet-tag-grounded checks
  across pinout/footprint parity, power tree, power-integrity (regulator current vs
  rail peaks), interface integrity (I²C/CAN/USB/USB-C), support-circuit completeness,
  crystal load caps, **crystal frequency vs MCU clock requirement** (e.g. RP2040 12 MHz
  USB, ATmega32U4 16 MHz USB), status-LED path, mechanical fit/cutouts/mounting, and
  hardware↔firmware parity. Each is verified by inject-and-catch against real designs.
- **Design benchmark (`_BENCHMARK_SPECS`): all 12 buildable templates.** Expanding it
  from 4→12 also repaired 5 templates that were listed as supported but crashed
  `generate_all` (schema-nonconformant firmware module; missing hard-required mechanical
  keys). Session-cached in tests to stay practical.
- **Simulation oracle — DC operating point (ngspice), built and wired.** The first
  *computed* (not heuristic) physics evidence: a conservative DC netlist (rails as ideal
  sources at grounded nominal voltage, resistors as R, caps open) solved by ngspice,
  verified against a hand-computed divider (2.5 V / 1.25 V). Wired into `run_all_checks`
  as an **advisory, always-PASS** gate that attaches rail and computed-node voltages to
  every design record. Tool-gated: absent ngspice is reported, never faked, and never
  blocks release. See `docs/h1-physics-evidence-plan.md`.

## The boundary — why the core condition is not "closed" in software

"Closed-loop physical correctness" as stated requires validation against **thermal
behaviour, signal integrity, and bring-up risk on real hardware**. That is not an
incomplete feature; it is outside what software can produce, and the platform documents
this deliberately: **physical qualification cannot be closed by software.** Advisory
physics evidence escalates to release-authoritative only when correlated against bench
measurement recorded through `record_physical_evidence` — i.e. real hardware in the loop.

Three independently-probed candidate increments all hit the **same** wall and were
**correctly not built** (building them would fabricate data or authority):

| Candidate | Wall |
|---|---|
| Component-height vs enclosure clearance | per-component heights not curated (inventing = the pitfall) |
| Per-component current vs supply budget | already covered *and* per-component current draw not curated |
| Firmware pinmap vs pin alt-function | alt-function/pinmux tables not curated |
| **DC intermediate-node / IR-drop defect detection** | the DC model has no active-load currents; a 100 Ω series resistor on a supply pin produces **0 V drop** (verified empirically). Meaningful IR-drop needs curated per-IC load currents. |

When independent probes converge on one wall, the wall is the finding: the remaining
work is not code an agent can write this session — it is **datasheet-sourced curation**
and **physical measurement**.

## Logged next efforts (not started; each carries a stated risk)

- **H1 increment 2 — load-current curation.** Model ICs as DC current sinks so IR-drop /
  supply-integrity becomes computable. This is the genuine unlock for the DC oracle, but
  it is **the highest fabrication-risk work in the plan**: per-pin current distribution
  and whether real copper drops meaningfully are open modelling questions. Must be
  datasheet-sourced with provenance and validated against measurement — never defaulted.
- **H1 thermal / SI.** Depend on curated dissipation and on routed geometry (H2)
  respectively; advisory until measurement-correlated.
- **Advisory → release-authoritative escalation.** Requires bench measurement via
  `record_physical_evidence`. Hardware-in-the-loop; uncloseable by software alone.
- **Natural-language intent → topology** (designs are template-driven today). A real
  research effort, not an atomic increment; a shallow keyword→template mapper would be
  plausible-but-wrong template selection — the pitfall in a new place.

## The discipline that governs all of the above

Every capability ships at a release tier it can defend
(`blocked` → `candidate_only` → `advisory` → `release_authoritative`) and earns escalation
against physical measurement — it never asserts it. The correct response to an
unsatisfiable ask is to state the boundary precisely, not to fabricate evidence across it.
