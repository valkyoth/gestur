# Changelog

All notable Gestur changes are documented here.

## Unreleased

- Made testing mandatory for every change, with explicit unit, integration,
  real-system/acceptance, and adversarial layers and no mock-only support claims.
- Added cross-crate facade integration tests and an executable test-policy gate.
- Initialized the Rust 1.97.1, edition 2024 workspace.
- Added dependency-free no_std domain, policy, workflow, event, API, crypto
  metadata, testkit, and facade crates.
- Added strict unpublished-package, zero-third-party-dependency, 500-line,
  unsafe-code, and no_std gates.
- Added Linux, Windows, macOS, BSD, Android, and iOS CI posture.
- Added security, supply-chain, platform, crate, implementation, release, and
  pentest documentation.
- Moved the complete design discussion into docs/PRODUCT_VISION.md.
