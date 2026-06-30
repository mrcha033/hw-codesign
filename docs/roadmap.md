# Roadmap: toward a SOTA coding-agent-powered hardware design system

This document supersedes the original 0–6 expansion roadmap (templates → resolver →
backends → mechanical → layout-proposal → GUI/cloud), which is substantially complete.
It defines what "SOTA-class, fully coding-agent-powered" means for this platform and the
ordered horizons to get there.

## What "fully coding-agent-powered" means here

A coding agent (Claude Code, Codex, any MCP client) takes a **one-line natural-language
intent** to a **fab-clean, physics-evidenced board** through structured tool calls, with
**zero human EDA steps** — and the platform, not the agent, decides whether the result is
releasable. "Fully agent-powered" also means the agent can *extend* the platform (new
topologies, new sub-circuits, new checks) without a human rewriting internals.

## H0 win-condition (the thing that makes "SOTA" measurable)

> **An agent, given a one-line spec, produces a board that passes the full native gate
> stack — `validate_spec` → ERC → DRC → autoroute (DRC-clean) → a physics-evidence pass —
> with no human intervention, measured as pass-rate and iteration-count over a held-out
> set of reference designs.**

Everything below is ordered to move this number, not to add capabilities for their own sake.

## The design constraint (read before adding anything)

This platform's entire credibility rests on a discipline the community watches closely:
**evidence-backed gates, blocked-not-silent, no agent-self-reported releases**, and the
documented stance that physical qualification *cannot* be closed by software. The sharpest
skepticism is aimed at exactly the capabilities this roadmap adds (layout, simulation,
sourcing authority).

Therefore every new capability ships **with its release-tier story**, never as a new
unchecked authority:

| Tier | Meaning | Example |
|---|---|---|
| `blocked` | Tool/toolchain absent → say so, never fake | autoroute without Freerouting |
| `candidate_only` | Structural/heuristic, not authoritative | constraint-driven placement proposal |
| `advisory` | Computed, but not release-gating until validated against measurement | SPICE rail-droop estimate |
| `release_authoritative` | Natively verified | KiCad ERC/DRC pass |

**Anti-goal (regressive for *this* platform):** "autoroute everything / full SPICE / EMC /
live sourcing" presented as authority the evidence can't back. For most products that is
merely ambitious; here it attacks the one thing that makes the tool trustworthy. A hardware
reviewer will go straight at any capability claiming authority it can't defend. New physics
and layout capabilities are **evidence that feeds the existing gate machinery**, escalating
tiers only as they earn it against physical measurement.

---

## H0 — Make it measurable and close the current loop

*Prerequisite for everything. Without the benchmark, "SOTA" is unfalsifiable.*

- **Benchmark harness (`hw_run_design_benchmark`).** A held-out set of N reference specs
  (one-line intents) with known-good gate outcomes. Score: full-gate pass-rate, iteration
  count to release, native-ERC/DRC pass-rate, physical-qualification gap categories, and
  regression deltas between commits. Wire into CI as a tracked metric, not a blocking gate
  (toolchain-gated).
- **Expand the grounding benchmark into a verifier/critic loop.** Today
  `run_grounding_benchmark` injects defects and confirms gates catch them. Add an
  independent critic pass over agent-authored candidates (adversarial review of the design,
  not just the gates) so `design_until_release` converges on *defensible* designs, not
  gate-passing ones.
- **Agent-legibility (the `service.py` God-class split).** "The agent extends the platform"
  requires the platform to be agent-readable. Split the 4,500-line `HardwareService` into
  `design_space`, `physical_qualification`, `review_export`, `firmware_service`,
  `candidate_manager` modules with stable seams. This is a SOTA *prerequisite*, not hygiene:
  an agent cannot reliably modify or reason about a 113-method class.
- **Close `design_until_release`.** Make the loop converge on the benchmark: bounded
  iteration with repair-plan application, and a recorded decision/iteration trail that the
  critic loop consumes.

## H1 — Physics-evidence layer (gated evidence, never new authority)

*The biggest real gap. A co-design tool closes the loop with physics, not only rule checks.
Every item below emits `advisory` until validated against bench measurement, then escalates.*

- **Analog/mixed-signal simulation (ngspice bridge).** Power-rail startup, regulator
  stability/transient, divider/bias DC operating points from the extracted graph. Feeds a
  new `power_integrity` gate (advisory → authoritative under measured correlation).
- **Thermal estimation.** Junction-temp / copper-pour heating from BOM dissipation + board
  stackup. Feeds `thermal_integrity` (currently advisory in placement) with real numbers.
- **Signal integrity (SI).** Trace impedance, length-match, and crosstalk checks for flagged
  nets (USB, CAN, QSPI, RF) — gates the layout-autonomy work in H2.
- **EMC pre-compliance heuristics.** Return-path/loop-area and decoupling-coverage scoring;
  strictly advisory, explicitly *not* a compliance claim.
- **Power-integrity / IR-drop** on the routed copper (depends on H2 routing).

## H2 — Layout autonomy (credibility-gated escalation)

*Continues the documented escalation. Each rung is release-authoritative only under native
DRC; nothing here claims authority a clean DRC can't back.*

1. **Constraint-driven placement proposal** — *done* (Phase C).
2. **Autoplacement with DRC-clean proof.** Heuristic/optimizer placement of unconstrained
   refs; only releasable when native DRC passes on the result.
3. **Autoroute as release-authoritative.** Promote Freerouting/native routing from
   candidate to authoritative — *only* under passing native DRC + the H1 SI checks on
   critical nets.
4. **SI/PI-aware routing.** Route respecting H1 impedance/length/return-path constraints.

## H3 — Supply-chain and manufacturing closure

*Replaces static curation with live, evidenced sourcing and real fab-house rules.*

- **Live distributor APIs (Octopart/Nexar, LCSC).** Real-time lifecycle, stock, pricing,
  and EOL into the resolver. Auto-propose qualified alternates on EOL/stockout — as a
  *candidate* substitution requiring re-validation, never silent swap.
- **DFM scoring against real fab capability matrices** (JLCPCB/PCBWay/etc.): min
  trace/space, drill, annular ring, controlled impedance availability — gate the design
  against the *chosen* fab, not a generic rule set.
- **DFA (assembly).** Component-spacing, courtyard, polarity/fiducial checks for the chosen
  assembler.
- **Live fabrication quote integration** as evidence attached to the release bundle.

## H4 — Agent self-improvement

*Turns single-shot design into a system that gets better across designs.*

- **Verified-IP-block reuse.** Promote gate-passing sub-circuits (power trees, USB-C front
  ends, BLE front ends) to a reusable, evidence-carrying block library the agent composes
  from — reuse inherits the prior validation tier.
- **Design memory.** Persist decisions, repair plans, and failure→fix pairs keyed by
  topology; surface them to the agent on similar future intents.
- **Eval-driven iteration.** The H0 benchmark becomes the optimization target: regressions
  block, improvements are tracked per commit.

## Carry-over from the original roadmap

- **#6 GUI / cloud / collaboration** — *partial*. HTML review viewer (`review_viewer.py`),
  `hw_share_review`, and review comments exist; no hosted GUI or multi-user cloud backend.
  This stays the lowest priority frontier and is **not** on the SOTA critical path — it is a
  distribution concern, not a credibility or capability one. Do it after H0–H2 land.

## Sequencing rationale

H0 first because nothing downstream is measurable without it (and the agent can't safely
extend an unsplit `service.py`). H1 before H2 because credible layout autonomy *depends on*
SI/thermal evidence to back a clean-DRC claim. H3 and H4 are parallelizable once H0's
benchmark exists to keep them honest. Throughout: a capability earns its release tier against
physical measurement — it does not assert it.
