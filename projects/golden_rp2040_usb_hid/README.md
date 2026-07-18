# RP2040 USB HID golden candidate

This is the first deliberately simple `hw-codesign` golden-board candidate. It
is intended to become a physically brought-up reference board, but the current
snapshot is **not fabrication-qualified and has not been ordered**.

## Brief

> Design a 2-layer RP2040 USB HID and CDC board powered from USB-C, with 2 MB
> QSPI flash, a 12 MHz crystal, USB ESD protection, SWD debug, 1 ms HID reports,
> and enumeration within 500 ms. Use Zephyr and keep the board within 65 mm by
> 30 mm.

## Current evidence

- The current spec schema passes with zero errors.
- The resolved graph contains 31 manufacturer-identified components and 24
  named nets.
- A real KiCad schematic is generated with 36 intentional no-connect markers;
  native KiCad ERC passes with zero violations.
- The tscircuit layout places all 31 components with parity, emits 91 traces,
  and reports zero PCB validation errors.
- Freerouting records zero raw unrouted connections; the persisted zone fill has
  zero post-import unconnected items, and native KiCad DRC has zero violations.
- The native RP2040 Zephyr build is blocked because ARM newlib runtime files
  (`nosys.specs`, `libc.a`, `libnosys.a`) are unavailable; no firmware build
  completion is claimed.
- Electronics, mechanical, firmware, BOM, candidate fabrication, and review
  artifacts were generated.
- The dated full-toolchain review records 48 gates: 44 pass, 1 fail, 3 blocked.
- Review bundle hash:
  `7d6731501a24716965593f7fcdc168a3d739d1b0a1b7a57f7a0b29fee51c1b84`.

Open the repository demo and review in [`docs/demo`](../../docs/demo/README.md).

## Release blockers

- Current supplier availability and critical-role resilience need fresh,
  timestamped evidence; `sourcing` fails, while `sourcing_resilience` passes and
  `supplier_availability` remains blocked. The native Zephyr build is also
  blocked because ARM newlib runtime files are unavailable.
- U2 exposed pad U2.57 uses a via-in-pad connection. Native DRC acceptance does
  not qualify its tented, plugged, filled, or capped fabrication process; the
  required stack-up/fabricator capability and acceptance evidence are open.
- The candidate has not been fabricated or ordered. Assembly inspection,
  current-limited power-up, rail measurements, firmware interface bring-up,
  thermal, SI/PI, EMI, vibration/retention, and ESD/ingress evidence are absent.

The qualification checklist is in
[`validation/physical/qualification_plan.md`](validation/physical/qualification_plan.md).
Physical evidence must be captured with artifact hashes and approval status via
`hw record-physical-evidence`; prose in this README cannot close a gate.
