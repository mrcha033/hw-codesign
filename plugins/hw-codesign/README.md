# hw-codesign plugin

Agentic hardware design with evidence-backed release gates. The plugin ships one skill
(`design-hardware`) and the `hw-codesign` MCP server, which exposes the `hw_*` tools for PCB
electronics, mechanical parts, firmware interfaces, sourcing, manufacturing, validation, and
release packaging.

One directory serves two hosts. Claude Code reads `.claude-plugin/plugin.json` and `.mcp.json`;
Codex reads `.codex-plugin/plugin.json` and `.mcp.codex.json`. Both share `skills/`.

## Install (Claude Code)

From a clone of this repository:

```
/plugin marketplace add /path/to/hw-cli
/plugin install hw-codesign@hw-cli
```

`.claude-plugin/marketplace.json` at the repository root registers the plugin, with `source`
pointing at `./plugins/hw-codesign`.

## MCP server

Both hosts copy the plugin out of the repository into their own plugin cache, so the server cannot
be resolved through a path relative to the checkout — a cache-relative `../..` points at the cache,
which has no `pyproject.toml`. Both mcp files therefore install the platform from git:

```
uvx --from 'hw-codesign-platform[mcp] @ git+https://github.com/mrcha033/hw-cli' hw-mcp
```

The package is not published to PyPI, so a bare `--from hw-codesign-platform[mcp]` does not
resolve; the git source above is the working form.

`HW_PLATFORM_ROOT` is the workspace the server writes projects, validation reports, review bundles,
and release artifacts into. Neither mcp file sets it: the server falls back to the working
directory the host launched in, and an exported `HW_PLATFORM_ROOT` is inherited and wins. The
workspace must be writable.

### Host difference: variable expansion

Claude Code expands `${VAR:-default}` inside `.mcp.json`; Codex passes the string through
verbatim. So `.mcp.json` (Claude) uses an overridable source and `.mcp.codex.json` (Codex) hardcodes
the git URL.

Under Claude Code, point the server at a local checkout to run code you are editing:

```
export HW_CODESIGN_FROM='/path/to/hw-cli[mcp]'
```

Codex has no such override — edit `.mcp.codex.json` directly, or install the plugin from a local
marketplace, to develop against a checkout.

Toolchain-dependent gates (`native_erc`, `native_drc`, `autoroute`, `native_zephyr_build`) become
available only when the corresponding native tool is reachable from the server process. Run
`hw_get_capabilities` and `hw_diagnose_environment` to see what is installed. For the full
toolchain (KiCad, OpenCASCADE, Freerouting, Zephyr), use the container documented in the
repository README.

## Skill

`design-hardware` activates when a task involves turning requirements into hardware artifacts,
diagnosing blocked gates, comparing candidates, or preparing a release. It keeps changes
tool-mediated so requirements, decisions, reports, and iterations stay structured and auditable,
and it holds the evidence line: `blocked` is never `pass`, generated artifacts stay candidates
until the release gate promotes them, and digital checks never imply physical qualification.
