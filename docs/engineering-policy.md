# Engineering Policy

## Mandatory Rules

- Use the latest stable Rust; the current exact pin is 1.97.1.
- Use edition 2024 and workspace resolver 3.
- Keep normal Rust files at or below 500 lines.
- Keep pure domain crates no_std, adding alloc only when a bounded owned model
  requires it.
- Forbid unsafe code unless a future dedicated boundary crate is approved by an
  ADR, audit plan, and platform-specific tests.
- Add no third-party crate without an explicit policy change and dependency
  admission review.
- Keep every Cargo package publish-disabled.
- Put infrastructure behind Gestur-owned semantic contracts.
- Treat documentation, release notes, threat-model updates, and tests as part
  of the feature.
- Require unit/invariant and integration/boundary tests for every behavior.
  External implementation and platform claims additionally require real-system
  or acceptance evidence; mocks alone cannot close a milestone.
- Stop every release for owner-operated pentesting with third-party security
  tools before tags.

## Testability

Every behavior must have a deterministic test seam and assembled-boundary
coverage. Time, identifiers, connectors, storage, notifications, secrets,
network calls, and hardware must be abstractable without a production service.
Add negative, boundary,
cross-tenant, replay, retry, concurrency, fault, and resource-limit tests as
their corresponding features arrive.

See [Testing and verification policy](testing-policy.md) for mandatory layers
and the no-waiver rule for claimed behavior.

## Module Shape

A crate represents a stable responsibility and dependency boundary. A module
represents a cohesive implementation area. Split before a file reaches the hard
limit. Generated code must live in a clearly named generated directory and
receive a separate size and provenance policy.
