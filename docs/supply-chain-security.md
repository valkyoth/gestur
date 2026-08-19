# Supply-Chain Security

Gestur currently has no third-party crate dependencies. The Cargo lockfile,
source policy, tool pins, action SHA pins, and SBOM still form release evidence.

## Required Controls

- Commit Cargo.lock.
- Deny unknown registries, Git sources, wildcard versions, yanked crates, and
  multiple versions.
- Pin GitHub Actions by full commit SHA with a human-readable release tag.
- Run cargo audit and cargo deny for every release candidate.
- Generate and compare an SPDX SBOM.
- Use GitHub CodeQL default setup.
- Keep CI permissions read-only unless a reviewed job needs more.
- Never store a crates.io credential while all packages are private.
- Sign release tags and publish checksums/provenance only after the pentest stop.
- Accept only roadmap-declared releases. Verify every predecessor as a distinct
  signed annotated tag from an externally pinned authorized fingerprint in
  strict Git ancestry order.
- Freeze the candidate, then permit one evidence-only child commit whose signed
  source/feasibility reviews and owner-confirmed pentest record bind that
  candidate and identify the commit actually pentested.
- Keep reviewer and tag-signer roles separate; bind their candidate registries
  to a protected digest outside Git.
- Record later CodeQL remediation without rewriting which commit received the
  green pentest; rerun all local gates and CodeQL before tagging.
- Validate the newly pushed tag's signer and exact evidence target in protected
  tag-triggered CI before treating it as a release.

## Dependency Admission

The zero-dependency rule may only change through an ADR that records the need,
alternatives, current version, upstream source, maintenance, licenses, enabled
features, full transitive graph, unsafe/native/build-script use, no_std impact,
platform impact, security history, removal strategy, tests, and reviewer
approval. Security-critical standards must not be reimplemented merely to
avoid a dependency, but admitting an implementation still requires this review.
