# Security Policy

Gestur coordinates visitor PII, identity, legal evidence, physical sites, and
temporary credentials. Treat every input, kiosk, connector, plugin, network,
administrator, database, edge node, and AI provider as untrusted until a narrow
policy says otherwise.

## Supported Versions

Gestur has not reached a supported production release. Security reports are
still welcome for the current main branch.

## Reporting

Do not publish exploitable details in a public issue. Use GitHub private
vulnerability reporting when enabled, or contact the maintainer privately.
Include affected commit/version, impact, reproduction, and suggested
mitigation where possible. Never send real visitor data or credentials.

## Routine Checks

Run regularly and before release review:

    scripts/checks.sh
    scripts/check_latest_tools.sh
    cargo deny check
    cargo audit
    scripts/generate-sbom.sh --check

GitHub CodeQL default setup must be enabled. Do not add an advanced CodeQL
workflow while default setup is active. See
[GitHub security settings](docs/github-security-settings.md).

## Release Stop

Every version stops after implementation and local verification. A tag is
forbidden until an owner-operated pentest with third-party security tools covers
the exact implementation commit, all findings are fixed and cleanly retested,
the owner confirms PASS, and the permanent record under security/pentest names
the tested commit, tool versions, configuration, scope, and outcome. All local
gates then rerun. Any later CodeQL remediation is separately bound to its
rule/alert, exact diff, regression test, and full-gate result, and must receive
green CI/CodeQL before the maintainer requests the tag. A pushed tag is not a
release until protected CI verifies its authorized signer and exact
evidence-commit target.

Root PENTEST.md is temporary private-to-worktree findings input and must never
be committed.

## Dependency And Publishing Policy

No third-party crates are admitted. Unknown registries and Git sources are
denied. Every package has publish disabled, and CI validates that state.
There is no crates.io credential or publishing workflow. A future SDK exception
requires its own licensing, dependency, compatibility, security, and release
review; it does not authorize publishing internal crates.

## Baseline Trust Rules

- Kiosks, invitation tokens, connector input, and webhook destinations are
  hostile inputs.
- PII, diagnostic logs, audit evidence, and legal evidence are separate data
  classes.
- Connectors receive named capabilities, never generic network, filesystem, or
  router administration.
- AI may propose but cannot admit, deny, identify, issue access, or set a legal
  basis.
- Offline operation must fail closed outside a published site policy.
- Secrets never enter normal logs, event payloads, URLs, or release evidence.

## Verification Rule

Every security-relevant behavior requires unit/invariant, integration/boundary,
negative, and real-system evidence appropriate to its support claim. Mock-only
tests cannot establish that a database, protocol, browser, platform, connector,
plugin, edge path, hardware integration, backup, or failover path works. See
[Testing and verification policy](docs/testing-policy.md).
