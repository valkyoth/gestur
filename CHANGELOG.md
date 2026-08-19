# Changelog

All notable Gestur changes are documented here.

## Unreleased

## 0.1.0

- Closed the v0.1.0 implementation gaps: request-ID test sequences now fail
  closed on exhaustion, schema keys/purposes reject ambiguous or oversized
  input, and facade tests cover both boundaries.
- Added mutation-tested enforcement for the exact crate dependency graph,
  no_std/unsafe/source-size posture, package publication denial, and registry,
  Git, build, and target-specific dependency escapes.
- Added an owner-driven pentest/retest and CodeQL-remediation record, exact tag
  target validation, and adversarial real-Git release-flow tests.
- Made owner-operated pentest evidence bind the exact tested commit, scope,
  resolved findings, and full-gate result. Later CodeQL changes must record the
  finding, exact paths, and changed regression tests before another CodeQL run.
- Enforced declared annotated predecessor-tag ancestry without adding reviewer
  registries, external trust digests, detached evidence signatures, or a second
  approval ceremony to the owner's release process.
- Locked the EU AI Act base regulation and its 2026 amending regulation as one
  governed source set rather than treating the amendment as the complete act.
- Corrected major-zero release-train chronology, expanded every grouped roadmap
  range into unique ordered versions, split remaining multi-deliverable stops,
  and added tested fail-closed validation for stop ownership, ordering,
  dependencies, proof obligations, and regulatory source locks.
- Strengthened the implementation, crate, and release plans with a
  dependency-correct patch-version register, explicit real-system evidence,
  optional hardware/regulatory gates, and a v1.0 acceptance ledger.
- Made testing mandatory for every change, with explicit unit, integration,
  real-system/acceptance, and adversarial layers and no mock-only support claims.
- Added cross-crate facade integration tests and an executable test-policy gate.
- Initialized the Rust 1.97.1, edition 2024 workspace.
- Added third-party-free no_std domain, policy, workflow, event, API, crypto
  metadata, testkit, and facade crates.
- Added strict unpublished-package, zero-third-party-dependency, 500-line,
  unsafe-code, and no_std gates.
- Added Linux, Windows, macOS, BSD, Android, and iOS CI posture.
- Added security, supply-chain, platform, crate, implementation, release, and
  pentest documentation.
- Moved the complete design discussion into docs/PRODUCT_VISION.md.
