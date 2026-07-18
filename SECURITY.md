# Security policy

## Supported versions

Until the first tagged release exists, security fixes are applied to the default
branch. After releases begin, fixes will target the latest supported release and
the default branch; pre-release artifacts and older snapshots are not maintained
independently.

## Reporting a vulnerability

Please use GitHub's private vulnerability reporting for this repository rather
than opening a public issue. Include:

- the affected command, MCP tool, or receiver endpoint;
- a minimal reproduction that does not contain secrets or third-party data;
- the expected and observed security boundary;
- the operating system and `hw-codesign` version;
- whether the issue requires untrusted project files or a forwarded loopback port.

Do not test against systems, networks, hardware, or accounts you do not own or
have permission to assess. We will acknowledge a complete report, reproduce it,
and coordinate disclosure after a fix is available.

## Receiver boundary

The review receiver is a local collaboration utility. It binds only to
`127.0.0.1`, accepts hash-addressed JSON bundles, enforces size and read-time
limits, and does not provide production authentication or multi-tenant
isolation. For remote collaboration, keep the receiver on loopback and use an
authenticated SSH tunnel or reverse proxy with an explicit storage quota.
