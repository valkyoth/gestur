# Gestur Implementation Plan

Status: planning document

Production target: v1.0.0

Gestur will be a security-first, API-first, self-hostable visitor and guest
orchestration platform. The complete source discussion is retained in
[Product vision](PRODUCT_VISION.md); its final architecture and v1.0 scenario
are the controlling direction.

## Product Boundary

Gestur is not a CRUD visitor log. It coordinates versioned Guest Journeys
across identity, host discovery, privacy/legal notices, approvals, safety,
badges, temporary network/physical credentials, notifications, occupancy,
emergency response, retention, evidence, and site-local hardware.

The architecture is a modular monolith first. Separate binaries exist only
where a trust or locality boundary requires one, especially the outbound-only
site edge and isolated native vendor agent.

## Non-Negotiable Engineering Baseline

- Exact latest stable Rust, currently 1.97.1; edition 2024; resolver 3.
- Latest tools rechecked weekly and at every release.
- No third-party crates under the current policy.
- Never reimplement cryptography, TLS, OIDC, SQL engines, Unicode security, or
  a Wasm runtime merely to preserve that policy. If a safe capability cannot be
  delivered with the standard library, platform facilities, or Gestur-owned
  code suitable for independent review, it remains blocked until an explicit
  dependency-policy decision is approved.
- no_std domain crates where possible; std only at explicit host boundaries.
- No unsafe code in the current workspace.
- No normal Rust source file over 500 lines.
- No Cargo package publication and no registry credentials.
- Linux, Windows, BSD, macOS, Android, and iOS portability from the beginning;
  Aesynx readiness without a current support claim.
- Every behavior receives deterministic, negative, boundary, and failure tests.
- Unit tests never stand alone as capability evidence: integration boundaries
  and actual supported implementations must also be exercised.
- Documentation, release notes, threat changes, and pentest evidence are part
  of the implementation.
- No release tag before an independent exact-commit pentest and clean retest.
- Release reviewer and tag-signer keys are separate roles; candidate registry
  changes cannot take effect without an externally protected digest update and
  two-person governance.
- Pentest results follow the owner-confirmed finding/retest loop. Later CodeQL
  fixes are documented, fully retested, and rechecked by CodeQL before tagging.

## Architectural Decisions To Freeze

1. Crates are boundaries, not automatic microservices.
2. PostgreSQL is the reference enterprise database, while PostgreSQL, MySQL,
   and SQLite implement the same Gestur-owned storage contracts.
3. Valkey is disposable acceleration and never authoritative.
4. Site hardware is reached through an outbound-authenticated gestur-edge cell.
5. PII, visit state, audit, diagnostics, and legal evidence are separate.
6. Guest Journeys are typed, declarative, versioned, and immutable once
   published; arbitrary workflow JavaScript is forbidden.
7. Connectors and plugins receive named capabilities, never generic system
   access.
8. AI is optional and advisory only.
9. Every mutation binds tenant, site, actor, request, idempotency, and expected
   revision where relevant.
10. Every package remains private until a future SDK exception is independently
    approved.
11. Canonical identifiers, bounded values, command/event envelopes,
    idempotency, and inbox/outbox semantics exist before any persistent or
    external effect can depend on them.
12. A Guest Journey has four separate concepts: editable definition, immutable
    published bundle, deterministic execution, and outbox-driven effects saga.
13. Edge nodes, adapters, plugins, connectors, kiosks, devices, and AI report
    observations or request effects; none can mint authorization facts or
    authoritative domain events.
14. AI remains a dependency leaf. Authoritative crates and flows cannot depend
    on AI crates, types, providers, or availability.

## Dependency-Correct Build Order

The phase numbers remain the release envelopes, while the
[detailed version plan](DETAILED_VERSION_PLAN.md) defines mandatory patch-sized
stops inside them. The following ordering is architectural, not optional:

1. Canonical IDs, time, encoding, bounds, command/event envelopes, algorithm
   profiles, and key-provider contracts.
2. Transaction, revision, idempotency, inbox/outbox, migration, deletion-ledger,
   pagination, and blob semantics.
3. Tenant/site/workload authority and adversarial isolation proof.
4. Visit facts, privacy-vault references, and credential-lifecycle invariants.
5. Typed journey graphs, whole-graph validation, privacy/capability data-flow
   analysis, signed publication, deterministic reducers, and effect intents.
6. Privacy, evidence, audit, identity, connector, edge, plugin, and UI adapters
   that consume those contracts without bypassing them.

This corrects three hazards in the original ordering: PII envelopes no longer
precede key-provider contracts; device adapters no longer precede signed edge
authority; and connectors no longer precede the shared capability/data-flow
rules later reused by the Wasm host.

## Phase 1 — Foundation (v0.1.0–v0.10.0)

Establish reproducible CI, canonical nonzero identifiers and time, stable error
codes, deterministic encoding, bounded values, command/event envelopes,
algorithm-agile key-provider contracts, no_std gates, validated configuration,
redaction-aware observability contracts, zero-dependency enforcement,
deterministic test support, threat model v1, and a production-boundary
feasibility/blocker ledger. Before Phase 2 adapters, SQLite, PostgreSQL, MySQL,
TLS, OIDC, WebAuthn, Unicode security, PKCS#11, and Wasm must each have a safe
reviewable path under current policy plus a real test environment, or their
implementation milestones remain blocked and unreachable.

Verification emphasizes workspace metadata, all-target builds, strict Clippy,
unit tests, doc links, source-size limits, publish prohibition, action pins,
SBOM, audit tooling, and cross-platform compilation.

## Phase 2 — Storage (v0.11.0–v0.20.0)

Define storage semantics before adapters: transactions, isolation expectations,
idempotency, optimistic concurrency, ordering, pagination, outbox/inbox,
migrations, anti-resurrection deletion ledger, and BlobStore. Implement SQLite,
PostgreSQL, and MySQL independently and require the same conformance and
fault-injection suite.

Do not leak database types into domain or application crates. Backend-specific
indexes may improve performance but cannot alter authorization or results.

## Phase 3 — Organisation And Authority (v0.21.0–v0.30.0)

Model tenants, legal entities, sites, buildings, entrances, zones, reception
desks, kiosk workload identities, principals, and initial RBAC. Prove
tenant/site isolation through adversarial conformance tests before PII lands.

## Phase 4 — Visitors And Visits (v0.31.0–v0.40.0)

Separate VisitorSubject from optional PII envelopes and make the privacy vault
a storage and key boundary rather than a table convention. Implement visit
aggregates, explicit transitions, multiple hosts, parties, invitations, arrival,
check-in, checkout, expiry, and authoritative occupancy. Contractors and
deliveries use distinct lifecycle aggregates instead of long or special visits.

The early PII-envelope abstraction is test-only and non-production until a real,
independently reviewed key provider, plaintext-lifetime controls, blind-index
policy, restore-safe deletion ledger, and real-system tests exist.

Core invariants include denial cannot jump to onsite, retries cannot duplicate
a visit, and checkout cannot leave a Gestur-owned credential live.

## Phase 5 — Forms And Guest Journeys (v0.41.0–v0.50.0)

Create typed, purpose-bound, classified fields; immutable form revisions;
bounded submissions; Guest Journey graphs; compilation; conditions; immutable
publication; site/visitor-type assignment; and deterministic simulation. Static
analysis rejects undeclared field, purpose, capability, connector, evidence, and
AI flows. Adapters can return observations and effect results but cannot directly
transition a journey.

Published revisions remain replayable so historical evidence always names the
exact notice, agreement, form, and decision graph used.

## Phase 6 — Privacy, Legal, Evidence, And Audit (v0.51.0–v0.70.0)

Keep privacy-notice delivery, optional consent, agreement acceptance, and
signature evidence distinct. Add purpose-scoped privacy-vault envelopes,
policy-driven retention, restriction of processing, scoped legal holds,
idempotent deny-read-first erasure, processor deletion obligations,
anti-resurrection restore, subject export, evidence bundles, security audit
events, append-only segments, signed roots, external anchoring, sensitive-read
audit, delegation, break-glass, dual control, and offline verification.

Gestur offers technical controls and evidence; it never claims a deployment is
automatically GDPR or ISO certified.

## Phase 7 — Identity, Directory, And Communications (v0.71.0–v0.90.0)

Add OIDC administration, passkeys, a tightly controlled break-glass account,
directory contracts, Entra delta sync, LDAP/AD profiles, enumeration-resistant
host search, notification models/templates, SMTP, Teams, Slack, SMS contracts,
signed webhooks, preferences, escalation, and delivery visibility.

External delivery is always outbox-driven so an outage cannot roll back an
authoritative check-in. Every inbound provider path authenticates and bounds raw
bytes before parsing, records a durable inbox identity plus digest, and treats a
reused delivery identity with different bytes as a security event. Outbound HTTP
uses one SSRF-safe destination-profile broker shared with plugins.

## Phase 8 — Site Hardware And Credentials (v0.91.0–v0.110.0)

Build gestur-edge enrollment, per-node workload identity, signed authority
epochs, signed commands, bounded inbox/outbox, signed site packages, and OS
hardening before device adapters. Then add bounded/idempotent printer
capabilities, IPP, typed ZPL, badge templates, print spooling, opaque QR and
optional Wallet credentials, Wi-Fi capability and lifecycle, UniFi reference
integration, physical access, scoped zone/time grants, revocation, expiry, and
reconciliation.

UWB and LPR are optional observations only and always retain a manual,
accessible fallback. Elevator integrations may request a destination but never
receive a generic movement API. Wallet NFC support is not claimed without the
required vendor entitlement/certification and compatible terminal evidence.

Central Gestur never receives generic SSH/router administration. Native vendor
SDKs remain out of process.

## Phase 9 — Sandboxed Plugins (v0.111.0–v0.120.0)

Freeze a WIT capability ABI; implement the Component Model host, broker,
deny-by-default sandbox, scoped outbound HTTP, opaque secret handles, resource
limits, signed packages, declarative configuration, and conformance suite.

A plugin without a capability must be structurally unable to exercise it.
Invocation context is host-minted and unforgeable; plugins receive minimized
opaque handles, propose effects only through the normal command/outbox path, and
run behind both a capability boundary and a process/OS boundary.

## Phase 10 — User Interfaces (v0.121.0–v0.130.0)

Add guest SSR, kiosk lifecycle, invitation/QR, schema-driven forms, legal
rendering, reception console, administration application, visual journey
editor, branding, accessibility, and localization. Treat the kiosk as an
untrusted public terminal: no durable browser PII, no ambient authority, short
sessions, accessible timeout recovery, privacy shielding, and non-touch/manual
alternatives. WCAG 2.2 AA is a web-content baseline, not the whole physical
kiosk acceptance claim.

Reception permissions are purpose-specific and never imply platform
administration or bulk export.

## Phase 11 — Emergency, Offline, And HA (v0.131.0–v0.140.0)

Implement emergency incidents and deterministic muster snapshots/deltas,
ordered epoch/sequence edge journals with signed segment roots, bounded offline
projections, policy-controlled offline check-in and effects, gap-detecting
signed reconciliation with durable acknowledgement watermarks, optional Valkey
acceleration, multi-node operation, database failover, and backup/PITR/restore.

Offline mode exposes degraded state, preserves one site authority, and uses
idempotent ordered reconciliation rather than generic multi-master CRUD.

## Phase 12 — Advisory AI (v0.141.0–v0.150.0)

Build a provider-neutral gateway, classification/DLP boundary, disclosure,
multilingual assistance, human-reviewed translation and extraction, constrained
query/configuration proposals, evidence summaries, and injection evaluation.

With AI disabled, every authoritative visit, credential, privacy, emergency,
audit, and administration path continues to work. AI output is untrusted text or
a typed proposal requiring deterministic validation and human authority; it
cannot construct commands, events, policy facts, screening dispositions, access
grants, or effects.

## Phase 13 — Preregistration And Enterprise Policy (v0.151.0–v0.170.0)

Add calendar capability, Microsoft and hostile-input iCalendar adapters, meeting
mapping, host preregistration, groups, recurrence, plus-ones, invitation
templates, pre-arrival documents, versioned jurisdictional technical baselines,
residency, real KMS/HSM/edge secure-storage adapters, per-tenant and per-purpose
keys, online rotation, and SIEM export. Optional contractor, export-control,
sanctions, UWB, Wallet, LPR, and identity-verification packs remain disabled
until their exact legal, vendor, hardware, privacy, and real-test profiles close.

Legal and standards inputs require source/date/version evidence and explicit
non-claims before implementation.

## Phase 14 — Advanced Security And Operations (v0.171.0–v0.190.0)

Add fine-grained ABAC with typed assertions and obligations, approved exports,
connector egress policy, plugin trust stores, security notifications, governed
screening/watchlists with human disposition, optional identity verification,
incident preservation, remote audit copies, revised threat model, OpenTelemetry,
SLOs, connector health, signed edge fleet updates, A/B rollback, rolling
compatibility, zero-downtime migrations, regional topology, replicated object
recovery, disaster runbooks, and automated restore proof.

## Phase 15 — Release Qualification (v0.191.0–v0.200.0)

Stop feature work. Run complete database conformance, migration-from-every-
supported-version, disaster restoration, chaos, load/soak, manual
accessibility, privacy/compliance review, owner-operated pentest with third-party
security tools, compatibility freeze, and an exact v1.0 release candidate.

v1.0.0 adds no surprise functionality. It promotes only the qualified candidate
after evidence, artifacts, checksums, provenance, documentation, CI, CodeQL,
and independent security results are complete.

## Testing Pyramid

- Unit tests for every value, parser, state transition, and policy decision.
- Cross-crate and assembled-boundary integration tests for every behavior.
- Real supported databases, servers, browsers, operating systems, connectors,
  devices, or official faithful simulators for every support claim; mocks alone
  cannot close a milestone.
- Compile-time no_std, unsafe, dependency-direction, file-size, and publish
  gates.
- Property/model tests for state machines, idempotency, ordering, retention,
  authorization, reconciliation, and credential lifecycle.
- Storage conformance against all authoritative backends.
- Connector/plugin/API contract tests and malicious-provider doubles.
- Browser E2E and accessibility tests.
- Fuzzing for every untrusted byte/text/protocol boundary.
- Concurrency tests, deterministic fault injection, chaos, load, and soak.
- Backup, PITR, restore, migration, upgrade, downgrade/rollback, and disaster
  rehearsals.
- Owner-operated pentest with third-party security tools at every base or patch
  milestone stop, recording exact tool versions, configuration, commit, scope,
  date, result, and retest outcome. Specialist cumulative campaigns remain at
  storage/privacy, edge/offline, plugin/egress, cryptography/evidence, and
  release qualification boundaries.
- Any later CodeQL fix is restricted to a structured, digest-bound delta with
  changed regression tests and a full-gate PASS before CI/CodeQL reruns.

## v1.0 Acceptance Scenario

A fresh organization can configure a branded site, fields, notices, agreements,
safety, directory, notifications, edge, printer, guest Wi-Fi, and optional
physical access; preregister a visitor; complete a QR-driven journey; notify and
obtain approval; issue each credential exactly once; preserve occupancy through
WAN loss; checkout and revoke; verify audit/evidence; apply retention and
privacy rights; restore a clean backup; pass all three database profiles; resist
plugin escape; and complete the flow with AI disabled.

The detailed, evidence-addressable acceptance ledger is maintained in the
[detailed version plan](DETAILED_VERSION_PLAN.md). The release must survive
owner-operated pentesting with third-party security tools. Anything less
remains pre-1.0.
