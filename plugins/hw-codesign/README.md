# hw-codesign plugin

Agentic hardware co-design turns a brief into KiCad, firmware, a 3D review, and
explicit fabrication blockers. The plugin ships one skill
(`design-hardware`) and the `hw-codesign` MCP server, which exposes the `hw_*` tools for PCB
electronics, mechanical parts, firmware interfaces, sourcing, manufacturing, validation, and
release packaging.

One directory serves two hosts. Claude Code reads `.claude-plugin/plugin.json` and `.mcp.json`;
Codex reads `.codex-plugin/plugin.json` and `.mcp.codex.json`. Both share `skills/`.

## Install (Claude Code)

From a clone of this repository:

```bash
python3.11 -m venv .venv
.venv/bin/pip install '.[mcp]'
export PATH="$PWD/.venv/bin:$PATH"
```

Then register the repository marketplace:

```text
/plugin marketplace add /path/to/hw-codesign
/plugin install hw-codesign@hw-codesign
```

`.claude-plugin/marketplace.json` at the repository root registers the plugin, with `source`
pointing at `./plugins/hw-codesign`.

## MCP server

Both hosts copy the plugin out of the repository into their own plugin cache, so the server cannot
be resolved through a path relative to the checkout — a cache-relative `../..` points at the cache,
which has no `pyproject.toml`. Install the source checkout first and expose its `hw-mcp` entry point
on `PATH`; both MCP files invoke that executable directly:

```
hw-mcp
```

The package-index distribution is live. Install the server into an environment
that is on the plugin host's `PATH`:

```bash
python3.11 -m pip install "hw-codesign[mcp]==0.1.4"
hw-mcp --help
```

A copied plugin without an installed `hw-mcp` executable is intentionally
incomplete instead of silently targeting an unavailable command.

`HW_PLATFORM_ROOT` is the workspace the server writes projects, validation reports, review bundles,
and release artifacts into. Neither mcp file sets it: the server falls back to the working
directory the host launched in, and an exported `HW_PLATFORM_ROOT` is inherited and wins. The
workspace must be writable.

Toolchain-dependent gates (`native_erc`, `native_drc`, `autoroute`, `native_zephyr_build`) become
available only when the corresponding native tool is reachable from the server process. Run
`hw_get_capabilities` and `hw_diagnose_environment` to see what is installed.

## Skill

`design-hardware` activates when a task involves turning requirements into hardware artifacts,
diagnosing blocked gates, comparing candidates, or preparing a release. It keeps changes
tool-mediated so requirements, decisions, reports, and iterations stay structured and auditable,
and it holds the evidence line: `blocked` is never `pass`, generated artifacts stay candidates
until the release gate promotes them, and digital checks never imply physical qualification.
