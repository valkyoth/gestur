# Gestur 0.1.0 Release Notes

Status: implementation complete; owner-operated pentest with third-party
security tools required before tagging

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
- Machine-enforced detailed stop ordering, ownership, dependency prerequisites,
  mandatory proof, source locks, and correct `v0.N.0` then `v0.N.P` chronology.
- A fail-closed release-evidence gate that rejects undeclared versions, broken
  signed predecessor-tag ancestry, self-asserted reviews, stale reviewed scopes,
  invalid support digests/signatures, and non-evidence changes after candidate
  freeze.
- Role-separated reviewer and tag-signer registries bound to a protected digest
  outside Git, with candidate-only self-authorization and cross-role reuse
  rejected.
- An owner-driven pentest/retest record that preserves the green pentested
  commit and its tool versions/configuration, and machine-verifies any later
  CodeQL remediation before protected tag checks.
- Linux, Windows, macOS, BSD, Android, and iOS verification posture.
- A 500-line Rust source limit and no_std/unsafe/publishing/dependency gates.

## Security Notes

- There are no third-party crate dependencies.
- No cryptographic operation, authentication, database, network, UI, hardware,
  connector, or deployment functionality exists yet.
- Algorithm types are metadata only and must not be read as a cryptographic
  implementation claim.
- A tag remains blocked until owner-operated pentest findings are resolved and
  the owner confirms a direct PASS or clean retest, all local gates and CodeQL
  are green on the final documented commit, and the tag itself uses an
  authorized fingerprint and passes its tag-triggered check.

## Verification

    scripts/checks.sh
    cargo deny check
    cargo audit
    scripts/generate-sbom.sh --check
    scripts/release_0_1_gate.sh
