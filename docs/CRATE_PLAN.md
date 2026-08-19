# Gestur Crate Setup Plan

Status: approved repository architecture; crates are added only at the milestone
that gives them tested behavior.

## Dependency Direction

    binaries and frontends
             |
             v
      application services
             |
             v
       domain contracts
             |
             v
    no_std domain primitives

Infrastructure adapters implement contracts and are injected upward. Domain
crates never depend on HTTP, asynchronous runtimes, databases, operating-system
APIs, UI frameworks, plugin runtimes, or vendor SDKs. The main gestur crate is
a small facade over stable portable crates; deployment binaries compose
application and infrastructure crates without turning the facade into a large
implementation file.

Crates are architectural boundaries, not automatic network services. Gestur
starts as a modular monolith and splits processes only for a demonstrated
security, failure-isolation, scaling, or site-locality reason.

## Active Foundation Crates

| Crate | Responsibility | Allowed dependencies |
| --- | --- | --- |
| gestur-core | IDs, revisions, time, shared errors | core only |
| gestur-schema | Typed fields, purposes, classification | gestur-core |
| gestur-workflow | Guest Journey graph primitives | gestur-core, gestur-schema |
| gestur-policy | Authorization and named capabilities | gestur-core |
| gestur-events | Versioned event envelopes | gestur-core |
| gestur-api-types | Transport-neutral commands/problems | gestur-core, gestur-policy |
| gestur-crypto-types | Algorithm and evidence metadata | core only |
| gestur-testkit | Deterministic reusable test support | gestur-core |
| gestur | Portable public facade | all stable domain crates |

Every active crate is no_std, forbids unsafe code, inherits EUPL-1.2, and has
publishing disabled.

The active type crates are contracts, not security implementations.
`gestur-crypto-types` may describe algorithm profiles, key references, envelope
metadata, and provider operations, but cannot contain home-grown cryptographic
primitives or imply that production encryption exists. `gestur-api-types` and
`gestur-events` converge on the canonical command/event envelopes before any
storage, connector, edge, plugin, or AI effect path is admitted.

## Planned Portable Domain Crates

Create these only with their matching milestone:

- gestur-config: validated configuration values and version identities.
- gestur-store: storage traits and semantic conformance contracts.
- gestur-visits: visitor/visit aggregates and state transitions.
- gestur-forms: versioned forms and bounded submissions.
- gestur-documents: document revisions and acceptance evidence.
- gestur-retention: purpose-bound retention, holds, and erasure decisions.
- gestur-privacy-vault: purpose-scoped PII envelopes, deny-read tombstones,
  blind-index policy, and key-provider-independent erasure contracts.
- gestur-evidence: evidence manifests and verification inputs.
- gestur-audit: security/audit events and tamper-evident segment metadata.
- gestur-directory: privacy-preserving host projection contracts.
- gestur-notifications: routing, retry, and minimal-data message models.
- gestur-credentials: badge, Wi-Fi, and physical-access lifecycle.
- gestur-edge-protocol: signed authority epochs, commands, site packages,
  ordered journals, acknowledgements, and reconciliation values.
- gestur-emergency: occupancy snapshots and muster state.
- gestur-connectors: capability names, request/response contracts, and health.
- gestur-plugin-abi: WIT-facing stable value contracts.
- gestur-ai-policy: advisory-only AI requests, classifications, and approvals.
- gestur-compliance: versioned technical baseline inputs and non-claims.

Use no_std plus alloc where owned bounded collections become necessary. Keep
pure validation and state machines independent of std even if their caller is a
server.

## Planned Application Crates

These may use std but remain infrastructure-independent:

- gestur-application: command/query orchestration and transaction boundaries.
- gestur-authn: authentication evidence and principal binding.
- gestur-authz: RBAC/ABAC evaluation over gestur-policy.
- gestur-occupancy: authoritative occupancy projection.
- gestur-journey-engine: compilation, simulation, and execution.
- gestur-privacy: privacy request orchestration.
- gestur-reconciliation: edge/central idempotency and conflict rules.
- gestur-notification-worker: outbox-driven delivery orchestration.

Application crates depend on portable contracts, never concrete database,
network, hardware, cloud, or vendor crates.

The application dependency graph is checked so authoritative application and
domain crates cannot depend on `gestur-ai-policy`. AI is always a leaf reached
through an advisory boundary.

## Planned Infrastructure Boundary Crates

A third-party crate remains prohibited. If a future dependency is admitted, it
must be contained in the narrowest boundary crate, modeled after the adapter
splits in the eth workspace. The feature does not leak third-party types into
portable APIs.

Potential boundaries:

- gestur-db-sqlite, gestur-db-postgres, gestur-db-mysql
- gestur-http-host and gestur-tls-host
- gestur-cache-valkey
- gestur-blob-filesystem and gestur-blob-s3
- gestur-plugin-host
- gestur-egress-broker
- gestur-connector-entra, gestur-connector-ldap
- gestur-connector-smtp, gestur-connector-teams, gestur-connector-slack
- gestur-connector-unifi, gestur-connector-ipp, gestur-connector-zpl
- gestur-observability-host
- gestur-key-provider-* adapters

The zero-third-party rule remains in force for every boundary above. If a safe
implementation is unavailable under that rule, the crate may contain contracts,
fixtures, and disabled experimental seams only; it cannot claim support or grow
a hand-written substitute for a mature security protocol. Admitting any future
dependency requires an explicit policy change, threat/dependency review, source
and license evidence, containment here, and maintainer approval.

The `v0.10.2` feasibility ledger must resolve each planned boundary before its
adapter crate is created. Resolution means either a safe first-party, platform,
or isolated-process mechanism with an owned test environment, or an explicit
blocked state. The ledger is not a dependency-admission shortcut.

Vendor libraries that require a DLL, JVM, privileged daemon, or proprietary
runtime run out of process in a gestur-vendor-agent. They never link into the
central API process.

## Planned Deployable Crates

- gestur-server: modular-monolith API and worker host.
- gestur-edge: outbound-authenticated, offline-capable site cell.
- gestur-admin: administration application.
- gestur-reception: purpose-built reception application.
- gestur-front: kiosk, mobile check-in, invitation, and checkout application.
- gestur-audit-cli: offline evidence verification.
- gestur-vendor-agent: narrow IPC bridge for unavoidable native SDKs.

## Crate Admission Checklist

Before adding a crate:

1. State its single responsibility and why a module is insufficient.
2. Define allowed incoming and outgoing dependency edges.
3. Select no_std, no_std plus alloc, or std and justify the choice.
4. Define its test seam and adversarial cases.
5. Confirm all package metadata inherits publish = false.
6. Document any security boundary or new trusted input.
7. Keep every normal Rust source file at or below 500 lines.
8. Update this plan, Cargo metadata checks, README, and release notes.
