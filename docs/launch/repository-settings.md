# Public repository launch checklist

This checklist separates changes prepared in a working tree from facts that are
actually visible to a first-time visitor. Do not mark an item complete until its
public URL has been opened in a clean browser session.

## Public state re-audited on 2026-07-19

The repository is now `mrcha033/hw-codesign`. GitHub reports the canonical
description, Apache-2.0 metadata, homepage, topics, and Discussions enabled;
the latest authoritative CI run is green and Pages serves the read-only review.
There is still no public PyPI package, GHCR image, or GitHub release until the
OIDC publisher and first-package visibility bootstrap are completed.

## Canonical settings

- Repository name: `hw-codesign`; the old `hw-cli` URL should remain only as a
  redirect and historical compatibility reference.
- Description: `Agent-ready hardware co-design for supported board families:
  brief to KiCad, firmware, and explicit fabrication blockers.`
- Topics: `hardware-design`, `pcb`, `kicad`, `eda`, `embedded`, `zephyr`,
  `rp2040`, `mcp`, `ai-agents`, `code-generation`.
- Homepage: `https://mrcha033.github.io/hw-codesign/` after the post-rename Pages
  deployment is verified anonymously.
- Discussions: enabled; seed welcome, show-and-tell, and support posts before
  announcing the release.
- License: confirm that GitHub detects Apache-2.0 while the vendored KiCad
  footprint attribution remains visible in `NOTICE`.

## External control-plane preflight

These settings are not created by files in this repository and must be applied
by an account with repository or registry administration access:

- Keep the authenticated `gh` session available for repository settings, tags,
  releases, package visibility, issues, and Discussions.
- In PyPI, register a pending Trusted Publisher for project `hw-codesign`,
  owner `mrcha033`, the repository slug that will emit the release OIDC token,
  workflow `release.yml`, and environment `pypi`. Under the launch sequence
  below that repository slug is `hw-codesign`, because the rename happens
  before the release tag. A pending publisher does not reserve the name, and a
  later repository rename requires the publisher identity to be updated. See the
  [PyPI pending-publisher instructions](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/).
- In repository Settings -> Pages, select **GitHub Actions** as the publishing
  source before expecting `pages.yml` to deploy. See the
  [GitHub Pages publishing-source instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).
- Treat the first GHCR publication as a fail-closed bootstrap. GitHub creates a
  new container package as private. The release workflow will push the image,
  log out, and then intentionally fail its anonymous pull. After that package
  exists, open its package settings, change visibility to **Public**, and rerun
  the failed workflow jobs. Making a package public is irreversible; confirm
  the package name and repository link before doing so. A private image or an
  authenticated pull is not a successful public-channel check. See GitHub's
  [package visibility](https://docs.github.com/en/packages/learn-github-packages/configuring-a-packages-access-control-and-visibility)
  and [anonymous GHCR access](https://docs.github.com/en/packages/learn-github-packages/about-permissions-for-github-packages)
  documentation.

## Release preflight

1. Review the complete diff and preserve unrelated user artifacts.
2. From a clean clone, install with Python 3.11 and run `hw --help` and
   `hw-mcp --help` from the built wheel.
3. Require green public CI on every declared operating system. A locally green
   suite does not replace the hosted result.
4. Open the README's demo, documentation, issue-template, license, and security
   links from the public default branch.
5. Open the self-contained golden-board review and verify that its counts,
   blocker details, and artifact hashes match the checked-in evidence.
6. Confirm the pending PyPI publisher, Pages source, and GHCR bootstrap owner
   before creating the tag; repository files cannot satisfy those prerequisites.
7. Create a signed or annotated `v0.1.0` tag only after the default branch is
   green. Let the tag workflow create the GitHub release after its uploaded
   wheel, container, and review artifacts pass their smoke tests.
8. Publish to an external package or container registry only when that endpoint
   exists, its exact public install command succeeds in a clean environment,
   and rollback ownership is clear. Otherwise keep the source-install wording.

## Launch sequence

1. Confirm the old `hw-cli` clone URL redirects to `hw-codesign`.
2. Push the canonical URL cleanup and require CI to pass again.
3. Apply or recheck the canonical description, topics, Discussions, and license.
4. Deploy Pages from the renamed repository, open the public URL anonymously,
   then set it as the homepage.
5. Register the pending PyPI publisher against the renamed repository,
   push the signed or annotated release
   tag, and follow the fail-closed GHCR bootstrap above if this is the first
   container publication.
6. Require the rerun to pass its anonymous GHCR pull, public PyPI install, and
   GitHub release-asset checks; then verify every attached artifact and hash.
7. Publish one focused RP2040 prompt-to-candidate demonstration, explicitly
   labeling routing, sourcing, firmware-toolchain, and physical blockers.
8. Seed the starter issues in `docs/launch/starter-issues.md` and seed
   Discussions.
9. Share the same proof package with hardware, KiCad, Zephyr, and agent-tooling
   communities; do not substitute repeated announcement posts for new evidence.

## Funnel metrics

Track impressions or unique repository visitors, README-to-install clicks,
successful clean installs, first generated candidates, repeat projects, issues
from outside contributors, and release downloads. Stars are a useful public
signal, but without exposure and successful activation they cannot distinguish
weak demand from a repository that was never operationally launched.
