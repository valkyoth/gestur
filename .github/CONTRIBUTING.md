# Contributing To Gestur

Gestur is security-sensitive visitor and physical-site orchestration software.
Contributions must preserve privacy boundaries, least privilege, portability,
testability, and honest capability claims.

## License

Gestur is licensed under the European Union Public Licence 1.2. By
contributing, you agree that your contribution is provided under that license.

## Development Setup

Use the exact toolchain in rust-toolchain.toml:

    cargo check --workspace --all-targets
    cargo test --workspace --all-features
    scripts/checks.sh

## Security-Sensitive Changes

Treat identity, authorization, PII, audit evidence, retention, guest journeys,
offline reconciliation, connectors, credentials, printing, networking, CI, and
release tooling as high risk. Do not put exploitable details in public issues;
follow [SECURITY.md](../SECURITY.md).

## Mandatory Testing

Every change must include repeatable verification. Behavior changes require
unit/invariant tests and integration or boundary tests. A capability that
depends on a database, server, browser, operating system, connector, plugin, or
device also requires testing against the real supported implementation or an
official faithful simulator before support may be claimed.

Mocks and compile checks are useful but cannot be the only evidence for working
behavior. Bug fixes require a regression test. Documentation, CI, build, and
release changes require their corresponding executable policy or smoke checks.

State the test layers, commands, real implementations, and remaining gaps in
every pull request. See [Testing and verification policy](../docs/testing-policy.md).

## Dependency Policy

Third-party crates are not admitted. A proposed exception requires an ADR,
threat and license review, feature/transitive inventory, removal strategy, and
explicit maintainer approval before a manifest changes. Internal path crates
must remain unpublished.
