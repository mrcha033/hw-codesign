# Reference designs

The repository currently maintains one runnable design family:

- [Robotics motor controller](robotics-motor-controller/README.md): STM32H7,
  12 motor channels, CAN, 24 V VBAT, four-layer PCB, enclosure, firmware, and
  manufacturing outputs.

## Generality milestone

A second reference design is intentionally not represented by a reduced copy of
the robotics controller. A credible secondary design must have a materially
different topology, its own role set and component evidence, native backend
outputs, tests, and a reviewable artifact bundle.

Until that design exists, public claims should describe hw-codesign as strongest
for the included robotics-controller family and present the pipeline and refusal
semantics as the reusable system.
