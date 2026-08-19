# Testing And Verification Policy

Status: mandatory for every change and every release.

## Absolute Rule

Everything added to Gestur must be tested. A change is incomplete when its
behavior, configuration, documentation, migration, build path, failure mode, or
security boundary has no repeatable verification.

Unit tests are necessary, but unit tests alone are not sufficient evidence for
a behavior or support claim. Every implemented capability must also be tested
through the real boundary at which users, services, platforms, storage engines,
browsers, networks, plugins, or hardware interact with it.

Mocks, fakes, and compile checks help isolate failures. They never substitute
for real integration, conformance, system, or operational evidence when Gestur
claims that an implementation works.

## Required Test Layers

### Layer 0 — Repository And Static Policy

Every change is covered by applicable formatting, lint, documentation-link,
metadata, dependency, publishing, source-size, no_std, unsafe, action-pin,
release-plan, SBOM, and workflow checks.

Documentation-only and policy-only changes still require these executable
checks. They are not exempt because they do not change Rust behavior.

### Layer 1 — Unit And Invariant Tests

Every value type, parser, state transition, policy decision, error path, and
resource bound receives focused positive, negative, boundary, and invariant
tests in its owning crate.

A defect fix must add a regression test that fails without the fix.

### Layer 2 — Integration And Boundary Tests

Every behavior change must have at least one test outside its implementation
unit that exercises the assembled public or internal contract. Cross-crate
types, command flow, serialization, storage transactions, process IPC, API
routes, plugin capabilities, and edge reconciliation are tested at their real
boundary.

An implementation is not complete if only its private functions were tested.

### Layer 3 — Real Implementation And Acceptance Tests

When a capability depends on an external system or platform, test it against a
real supported implementation in an isolated test environment:

- database adapters use actual supported PostgreSQL, MySQL, and SQLite engines;
- cache and object adapters use actual supported servers and storage behavior;
- HTTP, TLS, OIDC, LDAP, SMTP, webhook, and vendor protocols use real servers,
  official conformance suites, or faithful vendor-supported simulators;
- browser interfaces run end-to-end in real supported browser engines and
  receive automated plus manual accessibility testing;
- Linux, Windows, macOS, BSD, Android, and iOS claims receive native or
  cross-target evidence appropriate to the claim;
- edge, offline, upgrade, backup, restore, and failover behavior runs as
  assembled processes with actual network/process/storage faults;
- printer, Wi-Fi, access-control, and proprietary connector claims require a
  physical reference device, vendor test environment, or documented official
  simulator before production support is claimed.

A mock-only adapter remains experimental and must be labeled as such.

Tests never use production credentials or real visitor PII.

### Layer 4 — Adversarial And Operational Evidence

Security-sensitive and production-facing milestones add fuzzing, property or
model testing, concurrency testing, deterministic fault injection, chaos,
load/soak, migration, backup/restore, upgrade/rollback, and owner-operated
pentesting with third-party security tools as applicable.

Pentesting complements these layers and does not replace them.

## Change-Type Minimums

| Change | Minimum verification |
| --- | --- |
| Domain behavior | Unit/invariant, cross-crate integration, negative/security |
| Parser or untrusted input | Unit/boundary, fuzz/property, assembled consumer |
| Storage or migration | Unit, shared conformance, actual engine, fault/recovery |
| Connector or plugin | Contract, denial tests, actual provider/simulator |
| API | Handler/service integration, real transport, authz and malformed input |
| UI | Component, real-browser E2E, accessibility, failure/degraded state |
| Platform/runtime | Build plus native/system smoke on every claimed platform |
| CI/build/release script | Positive and fail-closed fixture or smoke test |
| Documentation/policy | Link, structure, metadata, and policy gate |
| Security fix | Reproducer, regression, adversarial variants, affected boundary |
| Release | Complete repository gate, real acceptance scenario, pentest/retest |

These are minimums. Add more tests whenever failure could affect privacy,
physical security, legal evidence, tenant isolation, credentials, emergency
operation, availability, or release integrity.

## Evidence And Traceability

Each pull request and release note must state:

- what was tested;
- which layers ran;
- which real implementations/platforms were exercised;
- commands and evidence locations;
- what was not tested and why;
- whether any support claim remains experimental or blocked.

Test fixtures contain synthetic data and stable provenance. External
conformance inputs are pinned by revision and hash.

## No Waiver For Claimed Behavior

There is no test waiver for behavior Gestur claims to support. If a real
implementation, device, platform, browser, security review, or operational
environment is unavailable, the capability stays planned or experimental and
cannot satisfy release exit criteria.

A temporary test deferral must name a future milestone, document the limitation
in release notes, and keep the capability unreachable or clearly unsupported.
