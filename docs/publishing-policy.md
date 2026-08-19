# Publishing Policy

## Current Rule

No package in this repository may be published to crates.io or another Cargo
registry. Every package inherits publish = false, CI validates the resolved
Cargo metadata, and no publishing credential or publishing workflow is allowed.

Tags and GitHub source or binary artifacts do not change this rule.

## Possible Future SDK Exception

Only a deliberately created public SDK or API client may be considered for
dual MIT OR Apache-2.0 licensing and crates.io publication. That decision
requires a separate milestone with:

- a stable public compatibility boundary;
- legal ownership and license review;
- dependency and feature admission;
- API and semver tests;
- security review and owner-operated pentest with third-party security tools;
- package-content and provenance checks;
- an explicit list proving all internal crates remain private;
- maintainer approval of credentials and a least-privilege publish workflow.

The preferred connector compatibility boundary is WIT. Publishing a Rust SDK
must not make internal Rust structs the authoritative cross-language ABI.
