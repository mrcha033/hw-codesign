# Adapting the specification

The included template is a robotics controller, not a generic board generator.
There are two different levels of adaptation.

## Parameter adaptation

Use this path when the board remains within the included role set and topology.
After `create-project`, edit the YAML files under `projects/<name>/spec/`:

- `system.yaml`: supply rails, MCU family, channel count, sensing, assumptions,
  and electronics backend.
- `electrical.yaml`: electrical constraints and interface requirements.
- `mechanical.yaml`: board envelope, enclosure dimensions, clearances, connector
  placement, and mechanical variants.
- `firmware.yaml`: Zephyr target and firmware constraints.
- `sourcing.yaml`: supplier snapshot provider.
- `manufacturing.yaml`, `safety.yaml`, and `test_plan.yaml`: release requirements.

For example, changing the supported motor-channel count and peak-current budget
is a spec edit, followed by regeneration and inspection:

```yaml
# projects/my_controller/spec/system.yaml
actuation:
  motor_channels: 8
  motor_channel_peak_current_a: 6.0
  max_simultaneous_peak_channels: 8
```

```bash
uvx --from hw-codesign-platform hw --root . validate-spec my_controller
uvx --from hw-codesign-platform hw --root . iterate my_controller --no-external
```

Do not treat a schema-valid edit as an engineering approval. Semantic, sourcing,
layout, mechanical, firmware, and release gates still decide whether the change
is acceptable.

## Adding a new board family

A board with materially different topology is extension work. At minimum:

1. Add component definitions under `parts/components/` with pin, footprint,
   supplier, and datasheet evidence.
2. Add a role set under `parts/role_sets/` describing the required functional
   roles and allowed component choices.
3. Add or extend a project template under `src/hw_codesign/templates/`.
4. Update generators where the new topology cannot be expressed by the existing
   robotics-controller assumptions.
5. Add tests proving graph resolution, pin/footprint parity, backend compilation,
   manufacturing export, mechanical fit, and firmware parity for the new family.

The project does not currently offer a plugin API that makes all five steps
configuration-only. A second maintained template is the clearest milestone for
demonstrating that the architecture generalizes beyond the current reference.

## Choosing a backend

- Choose `reference` to inspect generation and gating without claiming release.
- Choose `tscircuit` when the topology is supported by the pinned compiler and
  footprint mappings; native KiCad export is still required for manufacturing.
- Choose `kicad` for the strongest current native release path.
- Use `python_netlist` only for deterministic netlist/parity experiments.
- Do not select `atopile` expecting release output. It emits `.ato` source and
  runs `ato build`, but post-compile netlist, parity, layout, and manufacturing
  gates are still blocked with `gate_not_implemented`: Atopile 0.15.7 produces
  no parseable netlist or PCB output without a configured KiCad plugin path.

Every backend reports missing support as `blocked` or `fail`. Do not replace those
statuses with manual green checks unless the missing evidence is represented by a
new explicit gate and auditable artifact.
