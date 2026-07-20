# Public repository growth control plane

This page separates repository changes from facts that are actually visible to
a first-time visitor. Re-audit every external endpoint before a launch post and
keep candidate-level evidence distinct from fabrication qualification.

## Public state re-audited on 2026-07-21

| Surface | Verified public state |
|---|---|
| Repository | `mrcha033/hw-codesign`, public, default branch `master` |
| Hosted review | `https://mrcha033.github.io/hw-codesign/`, interactive 3D with 31/31 models |
| Python package | `hw-codesign==0.1.4` on PyPI; require a clean Python 3.11 install and typed-project smoke after publication |
| Container | Require an anonymous manifest check for `ghcr.io/mrcha033/hw-codesign:0.1.4` after publication |
| Tagged release | `v0.1.4`, expected to include nine assets and checksums after the release gate passes |
| Community files | GitHub community profile reports 100%; Discussions and issue templates are enabled |
| Social preview | No custom image was configured at audit start; use the current audited 3D render below |
| Traction baseline | 1 star, 0 forks, 0 subscribers; 59 views from 22 unique visitors in GitHub's rolling 14-day window |

The clone counter was 639 from 127 unique cloners in the same window. Treat that
as traffic, not adoption: automation and repeated clean-room checks can clone a
repository without producing a user or a generated board.

## Canonical discovery settings

- Description: `Agentic hardware co-design: brief to KiCad, firmware, 3D review, and explicit fabrication blockers.`
- Homepage: `https://mrcha033.github.io/hw-codesign/`
- Topics: `agentic-ai`, `ai-agents`, `artificial-intelligence`, `cad`,
  `code-generation`, `design-automation`, `developer-tools`, `eda`, `electronics`,
  `embedded`, `hardware-automation`, `hardware-design`, `kicad`, `mcp`,
  `pcb`, `rp2040`, `zephyr`
- Social preview source: `docs/demo/assets/golden-rp2040-3d.png`. It is an
  audited candidate-level CAD render, under 1 MB, and must retain that boundary
  in adjacent launch copy.

## Launch gate

1. Run the demo refresh and byte-for-byte freshness checks.
2. Run the cross-platform release-evidence check and focused test suite.
3. Install the published PyPI package in a clean Python 3.11 environment and
   create and validate an RP2040 project.
4. Open the README, 3D review, PyPI page, tagged release, and anonymous GHCR
   manifest from public endpoints.
5. Push a review branch, require public CI, merge it, and reopen the raw default
   branch README before announcing.
6. Close stale public issues and keep at least one genuine newcomer task open.
7. Publish one proof-led announcement per new artifact. Repeated posts without
   new evidence are not a distribution strategy.

## Funnel interpretation

The repository already has governance, release automation, topics, and a public
proof bundle. The current growth hypothesis is therefore a discovery and
activation problem: low qualified exposure, a stale source-only install warning,
the strongest 3D result absent from the public README, a generic share card, and
no visible external discussion engagement. This is an observational diagnosis,
not a causal result; use the measurement plan in
[`traction-plan.md`](traction-plan.md) to test it.
