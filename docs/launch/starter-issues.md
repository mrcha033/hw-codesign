# v0.1 starter issues

These issue drafts are deliberately tied to visible candidate gaps. Create them
after the v0.1 repository rename and metadata update so links and labels resolve
under the canonical `hw-codesign` name. Follow the public-state verification in
[`repository-settings.md`](repository-settings.md) before posting them.

Do not open the old ground-plane or native-Zephyr drafts: the current persisted
snapshot has zero raw/post-fill unrouted connections and native ERC/DRC at zero
violations. Its 170/170 Zephyr checks are software-level checks; the native
RP2040 Zephyr build remains blocked on the ARM newlib runtime. The issues below
reflect the remaining evidence gaps.

## Qualify the U2.57 via-in-pad fabrication process

**Suggested labels:** `hardware needed`, `electronics`, `manufacturing`

The RP2040 exposed pad U2.57 has one via-in-pad ground escape. Native DRC passes,
but the repository deliberately records the fabrication disposition and
qualification status as unselected/unqualified. Select and document the
tented/plugged/filled/capped or plated-over process, get a compatible fabricator
capability statement, and add released fabrication/assembly notes plus the
first-article inspection and yield evidence required by the physical
qualification plan. A clean DRC result alone cannot close this issue.

## Reproduce the PyPI quickstart on a clean platform

**Suggested labels:** `documentation`, `good first issue`, `help wanted`

Pick a clean Python 3.11 or newer environment on Linux, macOS, or Windows.
Install `hw-codesign[mcp]==0.1.4` from PyPI, create an `rp2040_usb_device`
project, and run `validate-spec`. Record the operating system, architecture,
Python version, exact commands, and pass or failure output. Completion means a
reproducible report or documentation pull request from a clean environment. It
verifies installation and typed-project activation only, not fabrication.

## Add fresh supplier evidence for the golden BOM

**Suggested labels:** `enhancement`, `sourcing`, `help wanted`

The curated BOM resolves identity and datasheet provenance but has unknown live
availability and no accepted resilience plan for several critical roles. Add a
provider adapter or reproducible evidence snapshot with observed timestamps,
stock semantics, and alternate/single-source mitigation tests.

## Fabricate and bring up the first golden board

**Suggested labels:** `hardware needed`, `help wanted`, `validation`

After the U2.57 process and supplier evidence are reviewed, order the exact
hash-addressed RP2040 candidate and execute the nine-test physical qualification
plan. Capture fabrication receipts, assembly photos, current-limited power-up
logs, rail measurements, firmware/interface bring-up, thermal and SI/PI traces,
EMI pre-scan, retention/vibration results, and ESD/ingress evidence or approved
waivers. The board has not yet been fabricated, so no software result or prose
claim can substitute for this evidence.

## Add a second physically brought-up golden board

**Suggested labels:** `hardware needed`, `help wanted`, `validation`

Only after the RP2040 board's fabrication and bring-up evidence is published,
propose one additional deliberately simple supported family. Include
manufacturing hashes, assembly photos, current-limited power-up logs, rail
measurements, firmware revision, interface tests, and explicit remaining
EMI/thermal gaps. Keep this sequencing explicit so a second generated candidate
does not distract from closing the first physical-evidence loop.
