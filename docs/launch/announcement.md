# v0.1.4 launch kit

Use these only after the public default branch shows the 3D hero and PyPI
quickstart. Each version points to the same evidence and makes the same
candidate-versus-fabrication boundary explicit.

## Short post

**Give an AI agent a hardware brief. Get KiCad, firmware, an interactive 3D
assembly, and an honest fabrication-blocker report.**

`hw-codesign` v0.1.4 is live for 13 supported board families:

```bash
python3.11 -m pip install "hw-codesign[mcp]==0.1.4"
```

The public RP2040 run records 44/48 gates passing, one sourcing failure, and
three blockers: live supplier evidence, the ARM newlib toolchain, and physical
qualification. Rotate the generated board in the
[interactive 3D review](https://mrcha033.github.io/hw-codesign/#assembly-title),
then inspect every gate and hash.

This is a reviewable hardware candidate, not a fabricated or qualified board:
https://github.com/mrcha033/hw-codesign

## Technical community post

I built `hw-codesign` to test a specific idea: an agentic hardware tool should
produce inspectable artifacts and explicit blockers, not just plausible-looking
CAD.

For supported templates, one brief can generate typed requirements, electronics
source, KiCad artifacts, firmware, BOM data, a self-contained review, an
interactive 3D assembly, and hash-addressed gate reports. The public RP2040 USB
HID/CDC candidate currently has zero raw and post-fill unrouted connections and
zero native ERC/DRC violations. It still stops at candidate status because
sourcing, the native ARM newlib environment, fabrication process disposition,
and nine physical qualification tests remain unresolved.

Try the PyPI quickstart, inspect the
[3D evidence](https://mrcha033.github.io/hw-codesign/#assembly-title), or help
[reproduce the install on a clean platform](https://github.com/mrcha033/hw-codesign/issues/11).

Repository: https://github.com/mrcha033/hw-codesign

## Title options

- Show HN: hw-codesign - prompt to KiCad, firmware, 3D review, and explicit blockers
- Agentic hardware design that refuses to call a CAD candidate fabrication-ready
- From an RP2040 brief to a hash-addressed 3D candidate and blocker report

## Proof links

- [Repository and quickstart](https://github.com/mrcha033/hw-codesign)
- [Interactive 3D review](https://mrcha033.github.io/hw-codesign/#assembly-title)
- [PyPI package](https://pypi.org/project/hw-codesign/)
- [v0.1.4 release assets](https://github.com/mrcha033/hw-codesign/releases/tag/v0.1.4)
- [Validation contract](https://github.com/mrcha033/hw-codesign/blob/master/docs/validation-contract.md)
- [Newcomer install-reproduction issue](https://github.com/mrcha033/hw-codesign/issues/11)

## Distribution rule

Adapt the technical paragraph to each community and follow its posting rules.
Do not cross-post identical hype, buy engagement, imply physical validation, or
treat clone and package counters as proof of adoption. Follow each post with a
new artifact, independently reproduced install, board-family example, external
contribution, or physical test result.
