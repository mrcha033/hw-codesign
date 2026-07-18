# Contributing to hw-codesign

Thanks for helping make agent-authored hardware easier to inspect and harder to
overclaim.

## Good first contributions

- Reproduce a failing or blocked gate and improve its diagnostic output.
- Add a manufacturer-grounded component or alternate with explicit provenance.
- Improve a supported template while preserving its schema and evidence boundary.
- Add a regression test for a generated schematic, board, firmware, or review artifact.
- Improve documentation for one concrete prompt-to-candidate workflow.

The planned starter work is listed in
[`docs/launch/starter-issues.md`](docs/launch/starter-issues.md).

## Claim boundary

Please use these terms precisely:

- **generated**: source or output files were emitted;
- **candidate**: the artifacts are reviewable but not release-approved;
- **released**: the configured software/native gates authorized an export;
- **physically qualified**: required bench or lab evidence was recorded and approved.

Never convert `blocked` to `pass`, infer hardware validation from a Python test,
or describe generated fabrication files as proof of a working board.

## Development setup

```bash
python3.11 -m venv .venv
.venv/bin/pip install '.[dev,mcp]'
npm ci --ignore-scripts
pytest -q
ruff check .
```

Before changing a native-tool path, inspect the environment:

```bash
PYTHONPATH=src .venv/bin/python -m hw_codesign.cli \
  diagnose-environment --target fabrication_release --backend kicad
```

Missing KiCad, Freerouting, OpenCASCADE, or Zephyr dependencies should produce a
structured `blocked` result. Do not weaken a gate to make a local machine green.

## Pull requests

1. Keep one problem and one evidence story per pull request.
2. Add or update focused tests.
3. Run the focused tests, `ruff check .`, and `git diff --check`.
4. Describe generated files separately from hand-authored files.
5. State which native tools and physical checks were not run.
6. Do not commit credentials, local paths, caches, duplicate KiCad files, or
   unreviewed generated project history.

For a new board family, include:

- the manufacturer MPNs and datasheet evidence used for critical parts;
- a current-schema template and role set;
- source generation plus semantic gate tests;
- an explicit physical-qualification plan;
- a README example that calls the result a candidate until evidence proves more.

Contributions are accepted under the repository's Apache-2.0 license. Third-party
assets must retain compatible license and attribution files.
