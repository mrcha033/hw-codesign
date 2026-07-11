# H1 scoping plan: physics-evidence layer

**Status:** scoping (not yet built). Authored 2026-07-11.
**Prerequisite finding:** the atomic "one grounded-defect check per commit" cadence has
saturated the electrical-*schematic* grounding surface for the real/benchmarked templates
(see `memory/grounding-saturation.md`). The next high-value work is physics evidence and
cross-domain closure — a scoped effort, not more inject-and-catch checks.

## Why this needs a plan (and can't be an atomic check)

Every grounding check landed so far is validated by *inject-and-catch*: mutate a real
generated design, watch a release-gating gate fail. That works because schematic-grounding
truth is discrete and already curated. **Physics evidence is different**: a rail-droop or
junction-temperature *number* has no discrete right/wrong the gate can assert — its
correctness is only knowable against bench measurement. Shipping such a number as
release-authoritative would assert authority the evidence can't back — the roadmap's stated
anti-goal. So H1 is governed by one rule:

> **Every H1 output emits at the `advisory` tier and escalates to `release_authoritative`
> only after its estimate is correlated against physical measurement recorded through the
> existing `physical_qualification` evidence path.** Escalation is data-earned, never asserted.

## What already exists (do not rebuild)

H1 is **not greenfield**. The following gates already run in `run_all_checks` as coarse,
explicitly-advisory heuristics:

| Gate | Location | Current nature |
|---|---|---|
| `power_integrity_estimate` | `validation.py:check_power_integrity_estimate` | Regulator output-current limit vs spec rail peak-current; decoupling/bulk presence. Static, curated-limit-based. |
| `layout_thermal_integrity` | `placement.py:check_layout_thermal_integrity` | Coarse power-component spacing vs a fixed `ADVISORY_THERMAL_SPACING_MM`. No dissipation/stackup. |
| `layout_signal_integrity` | `placement.py:check_layout_signal_integrity` | Placement-proximity heuristics for flagged nets. No impedance/length math. |
| `ir_pcb_sanity` | (run_all_checks) | Coarse IR/stackup sanity. |
| `_candidate_critic_report` | `service.py` | H0 adversarial critic pass already wired. |

The gap is **not** "add thermal/SI/PI gates" — they exist. The gap is **replace the
heuristic core of each with a physics computation, keep the advisory tier, and add the
measurement-correlation escalation path.**

## Ordered increments (each self-contained, each ships advisory)

1. **ngspice bridge + `power_integrity` DC operating point.** Extract a SPICE netlist from
   `electrical_graph.json` (rails, regulators, curated divider/bias resistors, load current
   from spec rail peaks). Solve DC operating point; report rail voltage vs target and divider
   bias points. Feed `power_integrity_estimate` as an *advisory* metric alongside the existing
   static check — do not gate on the number. Verifiable now by: known-good rail solves within
   tolerance on the 4 benchmark designs (regression fixture), not by inject-and-catch.
   Tool-gated like KiCad (`blocked` when ngspice absent — never fake).

2. **Thermal estimate from dissipation + stackup.** Requires a *new curated rating*:
   per-power-component dissipation (or the inputs to compute it). **This is a curation
   sub-project** (datasheet-backed, provenance-carrying, same discipline as the `<N>mhz_xosc`
   tags) — treat it as its own reviewed step, not a code-only change. Junction-temp / copper
   heating replaces the fixed-spacing heuristic in `layout_thermal_integrity`. Advisory.

3. **SI: trace impedance + length-match** for flagged nets (USB/CAN/QSPI/RF) once real routed
   geometry exists (depends on H2 routing for authoritative geometry; advisory on proposal
   geometry meanwhile).

4. **Measurement-correlation escalation.** A recorded bench measurement (via
   `record_physical_evidence`) that matches an advisory estimate within tolerance escalates
   that estimate's tier for that design class. This is the mechanism that lets any H1 number
   *earn* `release_authoritative` — build it once, reuse for all three above.

## Explicit non-goals for H1

- No EMC/EMI compliance *claim* (heuristics only, advisory, never a pass/fail compliance
  verdict).
- No release-authoritative physics number without a correlated measurement.
- No per-component dissipation/height/current data invented to make a check fire — if the
  rating isn't curated with provenance, the check waits on the curation step.

## Sequencing note

Increment 1 (ngspice DC) is the cleanest first move: it needs no new curated ratings (rails,
regulator limits, divider resistors are already in the graph), it is tool-gated cleanly, and
it produces the first genuinely *computed* (not heuristic) evidence. Increments 2–3 are
gated on curation / H2 geometry respectively. Increment 4 is the shared escalation spine.
