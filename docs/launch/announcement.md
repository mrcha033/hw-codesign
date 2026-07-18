# v0.1 launch announcement

This is the copy-ready launch post for the first public release. Publish it
only after the release checklist has verified the package, container, GitHub
release, and current physical-evidence boundary.

## Short post

**Prompt to a reviewable hardware candidate in 20 seconds.**

[`hw-codesign`](https://github.com/mrcha033/hw-codesign) turns a brief for a
supported board family into KiCad, firmware, BOM, review artifacts, hashes, and
an explicit fabrication-blocker report. The first RP2040 USB HID/CDC run is
deliberately honest: 44/48 gates pass, one fails on sourcing, and three remain
blocked on live supplier evidence, the ARM newlib toolchain, and physical
qualification.

Watch the [20-second prompt-to-board demo](https://mrcha033.github.io/hw-codesign/)
and open the [self-contained read-only review](https://github.com/mrcha033/hw-codesign/blob/master/docs/demo/index.html).

This release claims reviewable candidate generation and evidence boundaries. It
does not claim that generated CAD is fabrication-qualified, that the golden
board has been ordered, or that software checks replace bring-up measurements.

## Proof links to include

- [Repository](https://github.com/mrcha033/hw-codesign)
- [Release assets](https://github.com/mrcha033/hw-codesign/releases)
- [Hosted review](https://mrcha033.github.io/hw-codesign/)
- [Validation contract](https://github.com/mrcha033/hw-codesign/blob/master/docs/validation-contract.md)
- [Open hardware gaps](https://github.com/mrcha033/hw-codesign/issues)

## Suggested audiences

Share once, with the same proof package, in relevant KiCad, Zephyr, embedded,
open-hardware, and agent-tooling communities. Do not promise a fabricated board
or repeat the announcement without adding a new artifact, independent build,
or measured result.
