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
- Create annotated release tags and publish checksums/provenance only after the
  pentest, full local gate, and green GitHub CI/CodeQL stops.
- Accept only roadmap-declared releases. Verify every predecessor as a distinct
  annotated tag in strict Git ancestry order.
- After the owner confirms the exact implementation commit green, permit only
  the pentest record and release-status documentation before the first
  GitHub/CodeQL run.
- Record later CodeQL remediation without rewriting which commit received the
  green pentest; rerun all local gates and CodeQL before tagging.
- Validate the newly pushed tag's exact release target and ancestry in
  tag-triggered CI before treating it as a release.

## Dependency Admission

The zero-dependency rule may only change through an ADR that records the need,
alternatives, current version, upstream source, maintenance, licenses, enabled
features, full transitive graph, unsafe/native/build-script use, no_std impact,
platform impact, security history, removal strategy, tests, and reviewer
approval. Security-critical standards must not be reimplemented merely to
avoid a dependency, but admitting an implementation still requires this review.
