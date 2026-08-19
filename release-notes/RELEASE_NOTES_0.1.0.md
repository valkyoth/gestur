# Gestur 0.1.0 Release Notes

Status: release candidate; implementation and owner pentest/retest complete;
tagging requires green GitHub CI and CodeQL on the exact final commit

## Summary

Version 0.1.0 establishes Gestur's security-first repository and third-party-free
no_std workspace foundation. It is not a usable visitor management release.

## Added

- Rust 1.97.1, edition 2024, resolver 3 workspace.
- Nine unpublished first-party crates with explicit dependency direction.
- Domain primitives for identity, time, schema classification, Guest Journey
  nodes, connector capabilities, event attribution, API contexts, and
  cryptographic metadata.
- Unit tests for validation and invariants in every crate with behavior.
- Cross-crate integration tests exercising the assembled facade contracts.
- Canonical bounded schema keys and bounded purposes that reject control text
  and ambiguous surrounding whitespace.
- Deterministic request-ID fixtures that return the maximum value once and then
  fail closed instead of silently reusing an idempotency identity.
- A mandatory testing policy requiring real-system/acceptance evidence, not
  only unit or mock tests, before capabilities can be claimed as supported.
- CI, security reporting, dependency policy, SBOM support, and CodeQL default
  setup documentation.
- Granular implementation and release plans through v0.200.0 and v1.0.0,
  including dependency-correct patch stops and an evidence-addressable v1.0
  acceptance ledger.
- Machine-enforced detailed stop ordering, ownership, dependency prerequisites,
  mandatory proof, source locks, and correct `v0.N.0` then `v0.N.P` chronology.
- A fail-closed release gate that rejects undeclared versions, broken annotated
  predecessor-tag ancestry, invalid pentest records, unrecorded post-pentest
  code, and tags targeting the wrong commit.
- An owner-driven pentest/retest record that preserves the green pentested
  commit and machine-verifies the exact changed paths and regression tests for
  any later CodeQL remediation.
- Release-evidence validation that treats renames as deletion/addition pairs,
  preventing implementation removal from being disguised as an allowed
  release-finalization change.
- Linux, Windows, macOS, BSD, Android, and iOS verification posture.
- A 500-line Rust source limit and no_std/unsafe/publishing/dependency gates.
- Mutation tests proving crate-graph reversal, lost no_std posture, oversized
  source, publication escape, and registry/Git/build/target dependency escapes
  are rejected.

## Security Notes

- There are no third-party crate dependencies.
- No cryptographic operation, authentication, database, network, UI, hardware,
  connector, or deployment functionality exists yet.
- Algorithm types are metadata only and must not be read as a cryptographic
  implementation claim.
- The schema and workflow types are early portable contracts, not proof of
  tenant isolation, authorization, persistence, or a usable Guest Journey.
- A tag remains blocked until owner-operated pentest findings are resolved and
  the owner confirms a direct PASS or clean retest, all local gates and CodeQL
  are green on the final documented commit, and the tag targets that exact
  commit and passes its tag-triggered check.

## Verification

    scripts/checks.sh
    cargo deny check
    cargo audit
    scripts/generate-sbom.sh --check
    scripts/release_0_1_gate.sh

The local foundation suite exercises repository/static policy, unit/invariant,
and assembled facade boundaries. No external runtime is implemented in v0.1.0,
so there is no database, server, browser, device, or network support claim to
qualify with a real-system test. Platform CI establishes development and
portable-compilation posture only, as documented in `docs/platform-support.md`.
