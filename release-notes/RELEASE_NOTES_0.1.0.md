# Gestur 0.1.0 Release Notes

Status: implementation complete; independent pentest required before tagging

## Summary

Version 0.1.0 establishes Gestur's security-first repository and dependency-free
no_std workspace foundation. It is not a usable visitor management release.

## Added

- Rust 1.97.1, edition 2024, resolver 3 workspace.
- Nine unpublished first-party crates with explicit dependency direction.
- Domain primitives for identity, time, schema classification, Guest Journey
  nodes, connector capabilities, event attribution, API contexts, and
  cryptographic metadata.
- Unit tests for validation and invariants in every crate with behavior.
- Cross-crate integration tests exercising the assembled facade contracts.
- A mandatory testing policy requiring real-system/acceptance evidence, not
  only unit or mock tests, before capabilities can be claimed as supported.
- CI, security reporting, dependency policy, SBOM support, and CodeQL default
  setup documentation.
- Granular implementation and release plans through v0.200.0 and v1.0.0,
  including dependency-correct patch stops and an evidence-addressable v1.0
  acceptance ledger.
- Linux, Windows, macOS, BSD, Android, and iOS verification posture.
- A 500-line Rust source limit and no_std/unsafe/publishing/dependency gates.

## Security Notes

- There are no third-party crate dependencies.
- No cryptographic operation, authentication, database, network, UI, hardware,
  connector, or deployment functionality exists yet.
- Algorithm types are metadata only and must not be read as a cryptographic
  implementation claim.
- A tag remains blocked until independent pentest findings are resolved and the
  exact reviewed commit has permanent PASS evidence.

## Verification

    scripts/checks.sh
    cargo deny check
    cargo audit
    scripts/generate-sbom.sh --check
    scripts/release_0_1_gate.sh
