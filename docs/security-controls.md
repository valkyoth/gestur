# Security Controls

Status: v0.1.0 foundation controls.

## Enforced Now

- Exact Rust 1.97.1 and current reviewed CI tool pins.
- Edition 2024, resolver 3, locked dependency graph.
- No third-party crates, Git sources, or registries.
- publish = false resolved for every Cargo package.
- no_std and forbid(unsafe_code) in every active crate.
- Strict compiler/Clippy lints and a 500-line code-file gate.
- Unit, doc, policy, release-plan, metadata, and cross-target checks.
- Mandatory unit, assembled-boundary, real-system/acceptance, and adversarial
  evidence appropriate to every capability claim.
- Read-only CI permissions and full-SHA GitHub Action pins.
- cargo-deny, cargo-audit, SPDX SBOM, and CodeQL default setup policy.
- Exact-commit independent pentest stop before every tag.
- Closed declared-release set; distinct signed predecessor tags must form a
  strict ancestor chain, and only an evidence child commit may follow candidate
  freeze.
- Source and feasibility reviews bind real commits, scoped-change invalidation,
  support digests, externally pinned reviewer key fingerprints, and verified
  detached signatures.
- Role-separated reviewer/tag-signer registries are bound to an external digest;
  missing pins, ambiguous entries, and cross-role fingerprint reuse fail closed.
- Independent pentest approval follows an owner-confirmed finding/retest loop;
  the record preserves the green pentested commit and any later CodeQL delta.
- Tag fingerprints require explicit authorization, and every newly pushed tag
  receives a protected signer/target/evidence validation workflow.
- EUPL-1.2 internal workspace with no registry publishing path.

## Designed Now, Implemented Later

- Tenant/site isolation and capability-based authorization.
- Privacy-separated PII and purpose-bound fields.
- Opaque invitation tokens, replay protection, and idempotent mutations.
- Application-layer PII encryption through reviewed key-provider boundaries.
- Append-only tamper-evident audit with independent roots.
- Automatic credential expiry, revocation, and reconciliation.
- Outbound-authenticated site cells and encrypted offline journals.
- Deny-by-default Wasm plugins with bounded resources.
- SSRF-resistant outbound HTTP and signed webhook replay defense.
- AI classification, disclosure, typed tools, and no authoritative decisions.

Planned controls are not current product claims. Each becomes active only when
its release deliverables, tests, documentation, and pentest evidence exist.
No signing role is currently populated, so release gates intentionally remain
blocked until the external two-person bootstrap is completed.
