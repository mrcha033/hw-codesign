# Prompt-to-board demo evidence

This directory is a date-stamped, reproducible product demo for the
`golden_rp2040_usb_hid` candidate. It demonstrates candidate generation and an
explicit blocker report; it does **not** claim that the board has been fabricated
or qualified.

## 20-second flow

The prompt shown in the demo is the prompt supplied to the requirements compiler:

> Design a 2-layer RP2040 USB HID and CDC board powered from USB-C, with 2 MB
> QSPI flash, a 12 MHz crystal, USB ESD protection, SWD debug, 1 ms HID reports,
> and enumeration within 500 ms. Use Zephyr and keep the board within 65 mm by
> 30 mm.

The three frames show:

1. The brief and supported board family.
2. The generated candidate and its persisted CAD/compiler evidence.
3. The unresolved blockers: sourcing, current supplier availability, an ARM
   newlib toolchain gap, the unqualified U2.57 via-in-pad fabrication process,
   and physical qualification.

The animation is available as [GIF](prompt-to-board-20s.gif) and
[MP4](prompt-to-board-20s.mp4). The [read-only review](index.html) is a
self-contained HTML file suitable for static hosting.

## Reproduction

First produce a full-toolchain report snapshot and export the supported
self-contained review. Then let the repository-owned script verify exact
report/bundle agreement and refresh every checked-in demo claim from that one
snapshot:

```bash
hw --root . check golden_rp2040_usb_hid
hw --root . export-standalone-review golden_rp2040_usb_hid
python scripts/refresh_demo.py
python scripts/refresh_demo.py --check
python scripts/refresh_demo.py --verify-release-evidence
```

`refresh_demo.py` never generates or validates the board. It fails before
writing if the 48 gate reports, bundle contents, canonical bundle hash, routed
board hash, native CAD metrics, Zephyr status, or physical-process wording
disagree. The full refresh and byte-for-byte `--check` require `rsvg-convert`,
`ffmpeg` with `libx264`, and `ffprobe`. The cross-platform
`--verify-release-evidence` path needs only Python; it verifies that the
checked-in bundle, standalone review, hash receipt, gate counts, native-tool
claims, and fabrication blockers agree without regenerating evidence.

The demo snapshot was exported on 2026-07-19. It records 48 gates: 44 pass, 1 fail,
and 3 blocked. Freerouting records zero raw unrouted connections and KiCad has
zero post-fill unconnected items. Native ERC and DRC each report zero
violations. The native Zephyr build is blocked because ARM newlib runtime files
are unavailable. The canonical bundle
hash is `7d6731501a24716965593f7fcdc168a3d739d1b0a1b7a57f7a0b29fee51c1b84`.

The failed gate is `sourcing`; the blocked gates are `supplier_availability`,
`native_zephyr_build`, and `physical_qualification`. The board has
not been fabricated. In particular, U2.57 uses via-in-pad, but the required
tented/plugged/filled/capped process and fabricator capability are unqualified.

## Renderer receipt

- `rsvg-convert version 2.61.3`
- `ffmpeg version 8.1.2 Copyright (c) 2000-2026 the FFmpeg developers`

## Artifact hashes

```text
21c863b73e52fe86e9e9d180c082a5b8aa4bc88db0b8519aa72fa70a198953ca  bundle.json
6c2bb23eed798d94cc81169ad03ce89104ba66faa8f695f498d65e5cc51dc29f  index.html
8ff2f75cb0015f9c965dd9d61bc5ad989048a8aaabab8b953fe3d2c374c10c44  prompt-to-board-20s.gif
f749158c4d229d3af3a58bb9bb928ac409bced79236f6617aeadc933aad43ddd  prompt-to-board-20s.mp4
e0e996fbfdd7dad6cf0263587d06f9f2872844174fb84774ec940c43d555bbb7  assets/golden-rp2040-3d.png
a1387f927b1a7e68b0e8b3e9cf842ee8b13e08df8927380204fd86a93f8a5264  assets/golden-rp2040-assembly.svg
6dd05203ac17fb9d22942a2f80b8fe9947c8895efae4468e3e979bb5444842ec  assets/golden-rp2040-assembly.png
93b8ce143706700c29ae4d0aac92a2ffb369e2f85451ef5d784f14cff2b1f8e3  assets/demo-frame-1.svg
abf215afab2cdbc370a293c5bd3bad0fc62dc14d783fad1a158318683b969fbf  assets/demo-frame-1.png
9eea7837984f8da1604800ca6726989e8f5292fb79d2b13cc19cdca5d9b595bb  assets/demo-frame-2.svg
9060df97114ad8ef3d26b325eb65851c69b9fc6f332c59c3b3995c9ecf6da8a1  assets/demo-frame-2.png
68fa2732ba7e4915f0c99975086ac4daa67a8a27617799c689cbc32812e5fe42  assets/demo-frame-3.svg
dadddc0bdb8a206beb1a8709452ff55e03385abfcb779706cb068d1e756ff0f2  assets/demo-frame-3.png
1e0e6b068891733c1b2c50db3317b85cd38793ba0fe363dfa666d7c6eceef2b2  ../../projects/golden_rp2040_usb_hid/electronics/generated/kicad/golden_rp2040_usb_hid.kicad_pcb
```

The assembly render is a CAD preview, not physical evidence. Model declarations,
software gates, and clean native DRC do not establish fit, solderability,
bring-up, thermal, SI/PI, EMI, retention, ESD, or manufacturing-process
qualification.
