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

The demo snapshot was exported on 2026-07-18. It records 48 gates: 44 pass, 1 fail,
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
18d93e1faaec112fd96d12af8ba1a98ccfc5d2e5c7754f14594a0b778b6aae7e  bundle.json
4f7bb07316a89d962b89d6582c7500788afe680bc542e2a4ab4d4c15bc802b05  index.html
f83362a16af519cf7ea397cc14c9f84a4aa58db382342bd1a8242181b7620c4f  prompt-to-board-20s.gif
d6577d9976007b648544e358c8e18b8c2412db8ab591031cac3192aa87bd2ac6  prompt-to-board-20s.mp4
a1387f927b1a7e68b0e8b3e9cf842ee8b13e08df8927380204fd86a93f8a5264  assets/golden-rp2040-assembly.svg
6dd05203ac17fb9d22942a2f80b8fe9947c8895efae4468e3e979bb5444842ec  assets/golden-rp2040-assembly.png
93b8ce143706700c29ae4d0aac92a2ffb369e2f85451ef5d784f14cff2b1f8e3  assets/demo-frame-1.svg
abf215afab2cdbc370a293c5bd3bad0fc62dc14d783fad1a158318683b969fbf  assets/demo-frame-1.png
2ae8f429328c3026562d99fe15ed4241cb9781a171ebd34cda63b35fd2caf218  assets/demo-frame-2.svg
055ed304d0bd3a072f4cffb96325b34f40c0973b61bb722c7f2fb5dfeccb56e8  assets/demo-frame-2.png
68fa2732ba7e4915f0c99975086ac4daa67a8a27617799c689cbc32812e5fe42  assets/demo-frame-3.svg
dadddc0bdb8a206beb1a8709452ff55e03385abfcb779706cb068d1e756ff0f2  assets/demo-frame-3.png
1e0e6b068891733c1b2c50db3317b85cd38793ba0fe363dfa666d7c6eceef2b2  ../../projects/golden_rp2040_usb_hid/electronics/generated/kicad/golden_rp2040_usb_hid.kicad_pcb
```

The assembly render is a CAD preview, not physical evidence. Model declarations,
software gates, and clean native DRC do not establish fit, solderability,
bring-up, thermal, SI/PI, EMI, retention, ESD, or manufacturing-process
qualification.
