## Outcome

What narrow behavior or evidence boundary does this change improve?

## Verification

- Focused tests:
- Full tests or reason not run:
- Native tools run:
- Physical evidence run:

## Generated artifacts

List generated files separately from hand-authored changes. State whether each
artifact is candidate-only, release-eligible, or physically qualified.

## Checklist

- [ ] I preserved `blocked != pass` and did not upgrade software evidence into a hardware claim.
- [ ] I added or updated focused tests.
- [ ] I ran `ruff check src tests` and `git diff --check`.
- [ ] I added manufacturer/source attribution for new third-party parts or assets.
- [ ] I did not include secrets, local machine paths, caches, or duplicate KiCad files.
