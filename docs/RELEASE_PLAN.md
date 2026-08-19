# Gestur Release Plan To 1.0

Status: planning document; v0.1.0 implementation complete and awaiting an
owner-operated pentest with third-party security tools

This plan is intentionally granular. Every milestone must remain small enough to
implement, review, test, document, pentest, and stop cleanly. Split a milestone
or add patch versions whenever its risk or scope no longer fits one review pass.

The 200 capability milestones below are release envelopes. The
[Detailed version plan](DETAILED_VERSION_PLAN.md) is the authoritative register
of mandatory patch-sized stops, dependency corrections, proof obligations, and
the v1.0 acceptance ledger. A patch stop is a real release stop—not an informal
task—and inherits every verification, pentest, documentation, and tag rule in
this document.

Tags use:

    v0.N.0      release-train opening contract
    v0.N.P      next bounded train increment during major-zero development
    v0.200.P    release-candidate fixes only
    v1.0.0      first serious production release

No tag or workflow publishes a Cargo package.

## Roadmap Authority And Change Control

- A base `v0.N.0` closes only its train-opening contract and, if tagged, must
  precede `v0.N.1`. The train's complete capability claim cannot close until
  every required patch stop has closed in numeric order.
- Each stop has one outcome, context explaining why it exists, mandatory proof,
  an evidence index entry, and the exact-commit pentest/retest stop below.
- New work is inserted as the next free patch version under the owning base
  milestone. Published version numbers are never reused or silently redefined.
- Every base train has a machine-enforced detailed-stop declaration, including
  an explicit `none`. The declaration and detailed register must match exactly,
  so accidental row deletion, addition, or reassignment fails closed.
- A requested release must be one declared base, one stop in that base's exact
  declaration, or `v1.0.0`. Every lower declared release must have a distinct,
  cryptographically valid annotated tag from an authorized release-tag signer
  in ancestor order before the candidate.
- Candidate-controlled registry text is never a complete trust anchor. The
  exact role-separated reviewer and tag-signer registry digest must match a
  protected value outside Git; key reuse across roles fails.
- Every v0 patch release states its compatibility impact explicitly. Gestur is
  in Semantic Versioning major-zero development; from v1.0.0 onward, fixes,
  compatible features, and breaking changes use patch, minor, and major
  increments respectively.
- A changed trust boundary reruns all affected cumulative campaigns even when
  its local tests pass.
- The implementation plan controls architectural dependency direction; the
  detailed plan controls sequencing; this plan controls release governance.
- Roadmap text is not implementation evidence. Release notes and the status
  inventory must state only behavior present in the exact commit.

## Corrected Dependency Invariants

The detailed stops enforce these prerequisite chains:

1. canonical IDs/time/encoding/bounds → command and event envelopes → storage;
2. algorithm and key-provider contracts → PII envelope types → real key
   providers → production PII enablement;
3. transaction/idempotency/inbox/outbox contracts → adapters and effects;
4. journey graph typing → privacy/capability flow analysis → publication →
   deterministic execution → effect sagas;
5. edge enrollment/identity/authority/signing → device adapters → offline
   journal/reconciliation;
6. shared capability/data-flow and SSRF rules → first-party connectors → Wasm
   host reuse;
7. AI leaf dependency and disclosure/DLP → advisory features → disabled-AI
   parity qualification.

No third-party crate is authorized by this roadmap. A capability that would
otherwise require hand-written cryptography, TLS, OIDC, SQL, Unicode security,
or a Wasm runtime remains blocked until maintainers explicitly change the
dependency policy. “Planned” never means permission to implement an unsafe
substitute.

Before the first production adapter, `v0.10.2` must record a safe,
independently reviewable first-party/platform/process path and real test
environment for every mature protocol/runtime boundary, or mark its later stops
blocked and unreachable. This feasibility gate does not itself authorize a
dependency or weaken the zero-third-party rule. Its machine-readable ledger is
checked again at release time: pending decisions block `v0.10.2`, and a later
consumer cannot release unless its exact boundary is qualified with evidence.
The evidence names an existing ancestor commit and complete reviewed scope,
binds the exact boundary-plan and supporting-evidence digests, and carries an
attributable detached signature from an externally pinned reviewer-role key. A
later scoped change invalidates it; the consuming release must cover the planned
boundary implementation crate.

## Release Principles

Every release has one outcome, bounded deliverables, release-specific tests,
updated security/privacy documentation, release notes, exact tool/dependency
evidence, a clean implementation stop, an owner-operated pentest with
third-party security tools against that HEAD,
remediation and clean retest until the owner confirms green, a complete local
rerun, green GitHub CI and CodeQL default setup, and an explicitly authorized
signed tag on the final commit. The PASS record identifies each security tool
and version, the applied configuration, tested commit, scope, date, result, and
retest disposition. A CodeQL fix after the pentest is bounded by structured
delta evidence and receives the full local and CodeQL gates again.

The pentest obligation is also a capacity gate. Before scheduling a train,
maintainers reserve the owner's pentest/retest time, tooling, environment, scope,
and contingency window. Missing capacity blocks the release; it never reduces
pentest scope, frequency, or exact-commit binding. `v0.10.4` establishes and
tests this operating plan before later trains expand the attack surface.

A milestone is deployable or exercisable at its declared maturity. Early
versions may expose only libraries, test harnesses, or a non-production binary;
release notes must state those limitations plainly.

## Mandatory Verification In Every Version

- Run scripts/checks.sh, cargo test --workspace --all-features, cargo deny
  check, cargo audit, and committed SBOM comparison.
- Run the live stable-Rust, cargo-tool, and GitHub Action freshness check.
- Run release-specific unit, negative, boundary, invariant, integration,
  conformance, fault-injection, or operational tests named by the deliverables.
- Do not accept unit-only or mock-only evidence for a behavior claim. Exercise
  assembled boundaries and every actual supported implementation applicable to
  the milestone.
- Recheck Linux, Windows, macOS, BSD, Android, and iOS impact; run affected host
  or cross-target gates.
- Update the threat model, security controls, documentation, changelog, and
  release notes when behavior or trust changes.
- Confirm Cargo metadata has no publishable package and no third-party crate.
- Confirm no normal Rust source file exceeds 500 lines.
- Validate the detailed stop's evidence index, source locks, support/non-claims,
  and real-system proof. Never use a hard-coded repository test count as a
  release claim.
- Fail when a source lock exceeds its per-source maximum age. Add a release-time
  freshness attestation that binds the current source-lock digest, and obtain
  qualified review when a legal/regulatory revision affects scope or claims.
- Run the boundary-feasibility release check. From `v0.10.2`, every decision
  must carry reviewed evidence; a consuming adapter requires `qualified`, not
  merely a dependency edge to the feasibility milestone.
- Validate the exact candidate and evidence-only child commit. Source and
  feasibility records require real Git ancestry, scope invalidation checks,
  support digests, reviewer identity/key, and a valid detached signature.
- Reject undeclared releases and require every lower declared version's signed
  annotated tag to be a distinct ancestor in numeric order and signed by an
  externally pinned authorized tag-role fingerprint.
- Verify the owner-confirmed pentest record names a real ancestor commit, PASS,
  direct-pass or clean-retest outcome, every security tool and version, applied
  configuration, scope, and any later CodeQL remediation included in the
  release candidate.
- For a later CodeQL remediation, recompute the recorded rule/alert-bound delta
  direct-parent base, exact changed paths, canonical binary-diff SHA-256,
  changed regression tests, and full-gate PASS; reject free-text or unrecorded
  later code.
- After tag creation, require protected tag-triggered CI to revalidate its
  signer, target evidence commit, full evidence set, and predecessor ancestry.

## Pentest And Tag Stop

For every version:

1. Complete deliverables and local verification.
2. Confirm the owner's third-party pentest tools and exact versions,
   configuration, scope, environment, and clean-retest window are available.
3. Freeze the implementation candidate and stop with: vX.Y.Z implementation
   stop reached. Run pentest for this exact commit.
4. The owner runs the pentest; record temporary findings only in ignored root
   PENTEST.md.
5. If it reports a finding, fix it, add regression tests, commit the new
   HEAD, and request another pentest. Repeat until the owner reports green.
6. Record PASS, date, direct-pass or clean-retest, tester, scope, every tool and
   version, applied configuration, and the actual green `Pentested-Commit`;
   then rerun every applicable local repository gate.
7. Confirm the candidate's reviewer/tag-signer registries match the protected
   external trust-policy digest, and refresh signed source/feasibility evidence.
8. Commit the pentest and review evidence, then wait for GitHub CI and CodeQL.
9. If CodeQL reports an issue, fix it, add regression tests, and rerun all local
   gates. Record `Post-Pentest-Changes: CodeQL`, rule and alert IDs, the delta
   base, exact changed paths, canonical diff digest, changed regression-test
   paths, and full-gate PASS. Commit refreshed evidence and wait for CI/CodeQL
   again; repeat until green.
10. Create and push a signed tag on that final green commit only on explicit
    maintainer instruction; protected tag-triggered CI then validates the tag.

The Exit criteria in every section below and every detailed patch stop include
this complete rule. A pentest is not replaced by automated testing, fuzzing,
formal methods, CodeQL, or audit. Specialist cumulative reviews supplement the
per-version pentest; they never reduce it.

## Phase Map

| Versions | Phase |
| --- | --- |
| v0.1.0–v0.10.0 | Foundation |
| v0.11.0–v0.20.0 | Storage |
| v0.21.0–v0.30.0 | Organisations and sites |
| v0.31.0–v0.40.0 | Visitors and visits |
| v0.41.0–v0.50.0 | Forms and journeys |
| v0.51.0–v0.60.0 | Privacy, legal, and evidence |
| v0.61.0–v0.70.0 | Audit and assurance |
| v0.71.0–v0.80.0 | Identity and directory |
| v0.81.0–v0.90.0 | Communications |
| v0.91.0–v0.100.0 | Site hardware |
| v0.101.0–v0.110.0 | Wi-Fi and access |
| v0.111.0–v0.120.0 | WebAssembly plugins |
| v0.121.0–v0.130.0 | User interfaces |
| v0.131.0–v0.140.0 | Emergency, offline, and HA |
| v0.141.0–v0.150.0 | Advisory AI |
| v0.151.0–v0.160.0 | Calendar and preregistration |
| v0.161.0–v0.170.0 | Enterprise policy |
| v0.171.0–v0.180.0 | Advanced security |
| v0.181.0–v0.190.0 | Operational maturity |
| v0.191.0–v0.200.0 | Release qualification |

## Gap-Closure Version Index

These are bounded additions to the existing trains, not replacement milestones.
Their full deliverables and mandatory proof live in the detailed register.

| Version | Added context |
| --- | --- |
| v0.10.2 | Record reviewed qualified/blocked feasibility outcomes for each production boundary. |
| v0.10.4 | Reserve owner pentest/retest time, tooling, environment, scope, and contingency capacity without waivers. |
| v0.10.5 | Bind feasibility and source evidence to real commits, scope, digests, reviewer keys, and verified detached signatures. |
| v0.10.6 | Reject undeclared releases and enforce distinct signed predecessor tags in strict ancestry order. |
| v0.10.7 | Keep legal base instruments, applicable amendments, and consolidation state as one governed source set. |
| v0.10.8 | Anchor reviewer and tag-signer identities to a protected digest outside candidate-controlled Git. |
| v0.10.9 | Enforce the owner-driven pentest/retest, full-test, CodeQL-fix, final-green loop. |
| v0.10.10 | Authorize tag signer fingerprints and validate each newly created tag in protected CI. |
| v0.10.11 | Bind owner-operated pentest PASS to tool versions, configuration, exact commit, scope, date, and retest outcome. |
| v0.10.12 | Machine-verify the direct-parent CodeQL-only delta, regression test, and full-gate evidence after pentest. |
| v0.99.1 | Establish one authoritative lifecycle for badge, Wallet, network, access, and parking projections. |
| v0.100.1 | Qualify multi-printer routing and failover on two real supported devices. |
| v0.101.1 | Bound guest Wi-Fi credentials and exclude router-administration authority. |
| v0.103.1 | Qualify the UniFi reference connector against a real isolated controller and access point. |
| v0.104.1 | Qualify Wi-Fi QR presentation on real supported Android and iOS devices. |
| v0.105.1 | Prove automatic Wi-Fi expiry/revocation and reconciliation on a real controller. |
| v0.107.1 | Define vendor-independent zone, direction, and time-bounded access entitlements. |
| v0.108.1 | Prove physical-access revoke/expiry convergence in a controller or contracted vendor lab. |
| v0.109.5 | Reconcile provider projections without guessing ambiguous device state. |
| v0.110.2 | Prove checkout/expiry revocation across every issued credential as an assembled invariant. |

# Foundation

## v0.1.0 — Workspace genesis

Status: Implemented; owner-operated pentest with third-party security tools
pending.

Goal:

Deliver workspace genesis as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Pin Rust 1.97.1 with edition 2024 and resolver 3 in one locked EUPL-1.2
  workspace whose packages are unpublishable.
- Establish the `gestur` facade plus eight focused, third-party-free no_std
  domain/support crates without a deployable service or infrastructure claim.
- Enforce the exact allowed crate graph, no_std and unsafe-code posture,
  500-line source ceiling, first-party-only dependencies, and publish denial.
- Make the existing bounded schema seam reject noncanonical keys, surrounding
  whitespace, control text, and oversize input; make deterministic request IDs
  fail closed instead of repeating after exhaustion.
- Add unit, cross-crate boundary, policy-mutation, metadata, documentation,
  security, SBOM, and host/portable CI checks for the implemented foundation.
- Document architecture, testing, security, privacy, platform, dependency,
  release, pentest, and explicit non-production boundaries.

Verification:

- Run `scripts/checks.sh`, `scripts/check_latest_tools.sh`, `cargo deny check`,
  `cargo audit`, and committed SBOM comparison.
- Exercise every active crate through unit tests and the external facade
  integration suite, including schema-boundary rejection and request-ID
  exhaustion without reuse.
- Mutation-test crate dependency reversal, missing no_std posture, oversized
  source, publish escape, and registry/Git/target-specific dependency escape.
- Run host tests on Linux, Windows, and macOS plus no_std compile checks for
  FreeBSD, Android, and iOS in CI; retain those as portability, not runtime
  support, claims.

Exit criteria:

- The workspace graph and all package metadata match the documented foundation;
  every current behavior has unit and assembled-boundary evidence, policy
  escapes fail closed, and unsupported product behavior remains unreachable.
- Owner-operated pentesting with third-party security tools covers the exact
  implementation commit; every finding is fixed and cleanly retested before
  permanent PASS evidence or a tag.
- v0.1.0 implementation stop reached. Run pentest for this exact commit.

## v0.2.0 — Reproducible CI

Status: Planned.

Goal:

Deliver reproducible ci as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for reproducible ci.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate reproducible ci through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.2.0 implementation stop reached. Run pentest for this exact commit.

## v0.3.0 — gestur-core

Status: Planned.

Goal:

Deliver gestur-core as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for gestur-core.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate gestur-core through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.3.0 implementation stop reached. Run pentest for this exact commit.

## v0.4.0 — Error taxonomy

Status: Planned.

Goal:

Deliver error taxonomy as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for error taxonomy.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate error taxonomy through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.4.0 implementation stop reached. Run pentest for this exact commit.

## v0.5.0 — no_std gate

Status: Planned.

Goal:

Deliver no_std gate as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for no_std gate.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate no_std gate through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.5.0 implementation stop reached. Run pentest for this exact commit.

## v0.6.0 — Configuration model

Status: Planned.

Goal:

Deliver configuration model as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for configuration model.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate configuration model through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.6.0 implementation stop reached. Run pentest for this exact commit.

## v0.7.0 — Observability foundation

Status: Planned.

Goal:

Deliver observability foundation as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for observability foundation.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate observability foundation through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.7.0 implementation stop reached. Run pentest for this exact commit.

## v0.8.0 — Dependency policy

Status: Planned.

Goal:

Deliver dependency policy as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for dependency policy.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate dependency policy through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.8.0 implementation stop reached. Run pentest for this exact commit.

## v0.9.0 — gestur-testkit

Status: Planned.

Goal:

Deliver gestur-testkit as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for gestur-testkit.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate gestur-testkit through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.9.0 implementation stop reached. Run pentest for this exact commit.

## v0.10.0 — Threat model v1

Status: Planned.

Goal:

Deliver threat model v1 as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for threat model v1.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate threat model v1 through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.10.0 implementation stop reached. Run pentest for this exact commit.

# Storage

## v0.11.0 — GesturStore semantic contracts

Status: Planned.

Goal:

Deliver gesturstore semantic contracts as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for gesturstore semantic contracts.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate gesturstore semantic contracts through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.11.0 implementation stop reached. Run pentest for this exact commit.

## v0.12.0 — SQLite reference adapter

Status: Planned.

Goal:

Deliver sqlite reference adapter as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for sqlite reference adapter.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate sqlite reference adapter through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.12.0 implementation stop reached. Run pentest for this exact commit.

## v0.13.0 — PostgreSQL adapter

Status: Planned.

Goal:

Deliver postgresql adapter as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for postgresql adapter.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate postgresql adapter through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.13.0 implementation stop reached. Run pentest for this exact commit.

## v0.14.0 — MySQL adapter

Status: Planned.

Goal:

Deliver mysql adapter as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for mysql adapter.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate mysql adapter through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.14.0 implementation stop reached. Run pentest for this exact commit.

## v0.15.0 — Cross-database conformance suite

Status: Planned.

Goal:

Deliver cross-database conformance suite as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for cross-database conformance suite.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate cross-database conformance suite through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.15.0 implementation stop reached. Run pentest for this exact commit.

## v0.16.0 — Versioned migration framework

Status: Planned.

Goal:

Deliver versioned migration framework as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for versioned migration framework.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate versioned migration framework through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.16.0 implementation stop reached. Run pentest for this exact commit.

## v0.17.0 — Optimistic concurrency and row revisions

Status: Planned.

Goal:

Deliver optimistic concurrency and row revisions as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for optimistic concurrency and row revisions.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate optimistic concurrency and row revisions through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.17.0 implementation stop reached. Run pentest for this exact commit.

## v0.18.0 — Idempotency storage

Status: Planned.

Goal:

Deliver idempotency storage as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for idempotency storage.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate idempotency storage through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.18.0 implementation stop reached. Run pentest for this exact commit.

## v0.19.0 — Transactional outbox/inbox

Status: Planned.

Goal:

Deliver transactional outbox/inbox as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for transactional outbox/inbox.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate transactional outbox/inbox through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.19.0 implementation stop reached. Run pentest for this exact commit.

## v0.20.0 — BlobStore with filesystem reference backend

Status: Planned.

Goal:

Deliver blobstore with filesystem reference backend as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for blobstore with filesystem reference backend.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate blobstore with filesystem reference backend through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.20.0 implementation stop reached. Run pentest for this exact commit.

# Organisations and sites

## v0.21.0 — Tenant model

Status: Planned.

Goal:

Deliver tenant model as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for tenant model.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate tenant model through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.21.0 implementation stop reached. Run pentest for this exact commit.

## v0.22.0 — Legal entities

Status: Planned.

Goal:

Deliver legal entities as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for legal entities.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate legal entities through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.22.0 implementation stop reached. Run pentest for this exact commit.

## v0.23.0 — Sites

Status: Planned.

Goal:

Deliver sites as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for sites.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate sites through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.23.0 implementation stop reached. Run pentest for this exact commit.

## v0.24.0 — Buildings and entrances

Status: Planned.

Goal:

Deliver buildings and entrances as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for buildings and entrances.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate buildings and entrances through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.24.0 implementation stop reached. Run pentest for this exact commit.

## v0.25.0 — Zones

Status: Planned.

Goal:

Deliver zones as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for zones.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate zones through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.25.0 implementation stop reached. Run pentest for this exact commit.

## v0.26.0 — Reception desks

Status: Planned.

Goal:

Deliver reception desks as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for reception desks.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate reception desks through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.26.0 implementation stop reached. Run pentest for this exact commit.

## v0.27.0 — Kiosk identities

Status: Planned.

Goal:

Deliver kiosk identities as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for kiosk identities.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate kiosk identities through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.27.0 implementation stop reached. Run pentest for this exact commit.

## v0.28.0 — Principal model

Status: Planned.

Goal:

Deliver principal model as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for principal model.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate principal model through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.28.0 implementation stop reached. Run pentest for this exact commit.

## v0.29.0 — Initial RBAC

Status: Planned.

Goal:

Deliver initial rbac as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for initial rbac.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate initial rbac through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.29.0 implementation stop reached. Run pentest for this exact commit.

## v0.30.0 — Tenant/site isolation conformance tests

Status: Planned.

Goal:

Deliver tenant/site isolation conformance tests as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for tenant/site isolation conformance tests.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate tenant/site isolation conformance tests through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.30.0 implementation stop reached. Run pentest for this exact commit.

# Visitors and visits

## v0.31.0 — Privacy-separated VisitorSubject

Status: Planned.

Goal:

Deliver privacy-separated visitorsubject as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for privacy-separated visitorsubject.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate privacy-separated visitorsubject through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.31.0 implementation stop reached. Run pentest for this exact commit.

## v0.32.0 — Encrypted PII envelope abstraction

Status: Planned.

Goal:

Deliver encrypted pii envelope abstraction as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for encrypted pii envelope abstraction.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate encrypted pii envelope abstraction through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.32.0 implementation stop reached. Run pentest for this exact commit.

## v0.33.0 — Visit aggregate

Status: Planned.

Goal:

Deliver visit aggregate as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for visit aggregate.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate visit aggregate through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.33.0 implementation stop reached. Run pentest for this exact commit.

## v0.34.0 — Visit state machine

Status: Planned.

Goal:

Deliver visit state machine as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for visit state machine.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate visit state machine through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.34.0 implementation stop reached. Run pentest for this exact commit.

## v0.35.0 — Host association supporting multiple hosts

Status: Planned.

Goal:

Deliver host association supporting multiple hosts as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for host association supporting multiple hosts.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate host association supporting multiple hosts through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.35.0 implementation stop reached. Run pentest for this exact commit.

## v0.36.0 — Visitor parties/groups

Status: Planned.

Goal:

Deliver visitor parties/groups as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for visitor parties/groups.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate visitor parties/groups through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.36.0 implementation stop reached. Run pentest for this exact commit.

## v0.37.0 — Preregistration/invitations

Status: Planned.

Goal:

Deliver preregistration/invitations as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for preregistration/invitations.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate preregistration/invitations through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.37.0 implementation stop reached. Run pentest for this exact commit.

## v0.38.0 — Arrival and check-in commands

Status: Planned.

Goal:

Deliver arrival and check-in commands as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for arrival and check-in commands.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate arrival and check-in commands through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.38.0 implementation stop reached. Run pentest for this exact commit.

## v0.39.0 — Checkout and expiry

Status: Planned.

Goal:

Deliver checkout and expiry as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for checkout and expiry.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate checkout and expiry through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.39.0 implementation stop reached. Run pentest for this exact commit.

## v0.40.0 — Authoritative current-occupancy projection

Status: Planned.

Goal:

Deliver authoritative current-occupancy projection as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for authoritative current-occupancy projection.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate authoritative current-occupancy projection through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.40.0 implementation stop reached. Run pentest for this exact commit.

# Forms and journeys

## v0.41.0 — Typed field schema

Status: Planned.

Goal:

Deliver typed field schema as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for typed field schema.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate typed field schema through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.41.0 implementation stop reached. Run pentest for this exact commit.

## v0.42.0 — Form definition/revisions

Status: Planned.

Goal:

Deliver form definition/revisions as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for form definition/revisions.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate form definition/revisions through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.42.0 implementation stop reached. Run pentest for this exact commit.

## v0.43.0 — Typed submission validation

Status: Planned.

Goal:

Deliver typed submission validation as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for typed submission validation.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate typed submission validation through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.43.0 implementation stop reached. Run pentest for this exact commit.

## v0.44.0 — Data classification attached to fields

Status: Planned.

Goal:

Deliver data classification attached to fields as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for data classification attached to fields.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate data classification attached to fields through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.44.0 implementation stop reached. Run pentest for this exact commit.

## v0.45.0 — Guest Journey graph model

Status: Planned.

Goal:

Deliver guest journey graph model as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for guest journey graph model.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate guest journey graph model through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.45.0 implementation stop reached. Run pentest for this exact commit.

## v0.46.0 — Journey compiler/validator

Status: Planned.

Goal:

Deliver journey compiler/validator as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for journey compiler/validator.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate journey compiler/validator through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.46.0 implementation stop reached. Run pentest for this exact commit.

## v0.47.0 — Conditional branching

Status: Planned.

Goal:

Deliver conditional branching as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for conditional branching.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate conditional branching through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.47.0 implementation stop reached. Run pentest for this exact commit.

## v0.48.0 — Journey revisions and publication

Status: Planned.

Goal:

Deliver journey revisions and publication as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for journey revisions and publication.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate journey revisions and publication through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.48.0 implementation stop reached. Run pentest for this exact commit.

## v0.49.0 — Per-site and visitor-type journey assignment

Status: Planned.

Goal:

Deliver per-site and visitor-type journey assignment as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for per-site and visitor-type journey assignment.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate per-site and visitor-type journey assignment through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.49.0 implementation stop reached. Run pentest for this exact commit.

## v0.50.0 — Journey simulation/test engine

Status: Planned.

Goal:

Deliver journey simulation/test engine as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for journey simulation/test engine.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate journey simulation/test engine through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.50.0 implementation stop reached. Run pentest for this exact commit.

# Privacy, legal, and evidence

## v0.51.0 — Document and immutable document revisions

Status: Planned.

Goal:

Deliver document and immutable document revisions as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for document and immutable document revisions.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate document and immutable document revisions through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.51.0 implementation stop reached. Run pentest for this exact commit.

## v0.52.0 — Privacy-notice delivery evidence

Status: Planned.

Goal:

Deliver privacy-notice delivery evidence as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for privacy-notice delivery evidence.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate privacy-notice delivery evidence through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.52.0 implementation stop reached. Run pentest for this exact commit.

## v0.53.0 — Consent records separated from notices

Status: Planned.

Goal:

Deliver consent records separated from notices as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for consent records separated from notices.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate consent records separated from notices through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.53.0 implementation stop reached. Run pentest for this exact commit.

## v0.54.0 — NDA/agreement acceptance

Status: Planned.

Goal:

Deliver nda/agreement acceptance as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for nda/agreement acceptance.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate nda/agreement acceptance through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.54.0 implementation stop reached. Run pentest for this exact commit.

## v0.55.0 — Signature evidence abstraction

Status: Planned.

Goal:

Deliver signature evidence abstraction as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for signature evidence abstraction.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate signature evidence abstraction through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.55.0 implementation stop reached. Run pentest for this exact commit.

## v0.56.0 — Retention policy engine

Status: Planned.

Goal:

Deliver retention policy engine as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for retention policy engine.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate retention policy engine through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.56.0 implementation stop reached. Run pentest for this exact commit.

## v0.57.0 — Legal holds

Status: Planned.

Goal:

Deliver legal holds as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for legal holds.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate legal holds through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.57.0 implementation stop reached. Run pentest for this exact commit.

## v0.58.0 — Erasure/anonymization jobs

Status: Planned.

Goal:

Deliver erasure/anonymization jobs as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for erasure/anonymization jobs.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate erasure/anonymization jobs through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.58.0 implementation stop reached. Run pentest for this exact commit.

## v0.59.0 — Privacy-request export

Status: Planned.

Goal:

Deliver privacy-request export as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for privacy-request export.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate privacy-request export through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.59.0 implementation stop reached. Run pentest for this exact commit.

## v0.60.0 — Evidence bundle v1

Status: Planned.

Goal:

Deliver evidence bundle v1 as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for evidence bundle v1.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate evidence bundle v1 through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.60.0 implementation stop reached. Run pentest for this exact commit.

# Audit and assurance

## v0.61.0 — Security audit event schema

Status: Planned.

Goal:

Deliver security audit event schema as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for security audit event schema.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate security audit event schema through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.61.0 implementation stop reached. Run pentest for this exact commit.

## v0.62.0 — Append-only audit writer

Status: Planned.

Goal:

Deliver append-only audit writer as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for append-only audit writer.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate append-only audit writer through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.62.0 implementation stop reached. Run pentest for this exact commit.

## v0.63.0 — Hash-linked audit segments

Status: Planned.

Goal:

Deliver hash-linked audit segments as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for hash-linked audit segments.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate hash-linked audit segments through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.63.0 implementation stop reached. Run pentest for this exact commit.

## v0.64.0 — Signed audit roots

Status: Planned.

Goal:

Deliver signed audit roots as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for signed audit roots.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate signed audit roots through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.64.0 implementation stop reached. Run pentest for this exact commit.

## v0.65.0 — External audit-root export

Status: Planned.

Goal:

Deliver external audit-root export as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for external audit-root export.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate external audit-root export through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.65.0 implementation stop reached. Run pentest for this exact commit.

## v0.66.0 — Sensitive-read audit

Status: Planned.

Goal:

Deliver sensitive-read audit as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for sensitive-read audit.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate sensitive-read audit through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.66.0 implementation stop reached. Run pentest for this exact commit.

## v0.67.0 — Administrative delegation

Status: Planned.

Goal:

Deliver administrative delegation as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for administrative delegation.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate administrative delegation through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.67.0 implementation stop reached. Run pentest for this exact commit.

## v0.68.0 — Break-glass operation

Status: Planned.

Goal:

Deliver break-glass operation as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for break-glass operation.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate break-glass operation through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.68.0 implementation stop reached. Run pentest for this exact commit.

## v0.69.0 — Dual-control framework

Status: Planned.

Goal:

Deliver dual-control framework as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for dual-control framework.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate dual-control framework through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.69.0 implementation stop reached. Run pentest for this exact commit.

## v0.70.0 — Audit verification CLI

Status: Planned.

Goal:

Deliver audit verification cli as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for audit verification cli.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate audit verification cli through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.70.0 implementation stop reached. Run pentest for this exact commit.

# Identity and directory

## v0.71.0 — OIDC admin authentication

Status: Planned.

Goal:

Deliver oidc admin authentication as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for oidc admin authentication.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate oidc admin authentication through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.71.0 implementation stop reached. Run pentest for this exact commit.

## v0.72.0 — WebAuthn/passkey support

Status: Planned.

Goal:

Deliver webauthn/passkey support as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for webauthn/passkey support.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate webauthn/passkey support through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.72.0 implementation stop reached. Run pentest for this exact commit.

## v0.73.0 — Local break-glass account

Status: Planned.

Goal:

Deliver local break-glass account as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for local break-glass account.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate local break-glass account through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.73.0 implementation stop reached. Run pentest for this exact commit.

## v0.74.0 — Directory connector contract

Status: Planned.

Goal:

Deliver directory connector contract as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for directory connector contract.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate directory connector contract through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.74.0 implementation stop reached. Run pentest for this exact commit.

## v0.75.0 — Entra initial synchronization

Status: Planned.

Goal:

Deliver entra initial synchronization as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for entra initial synchronization.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate entra initial synchronization through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.75.0 implementation stop reached. Run pentest for this exact commit.

## v0.76.0 — Entra delta synchronization

Status: Planned.

Goal:

Deliver entra delta synchronization as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for entra delta synchronization.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate entra delta synchronization through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.76.0 implementation stop reached. Run pentest for this exact commit.

## v0.77.0 — LDAP connector

Status: Planned.

Goal:

Deliver ldap connector as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for ldap connector.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate ldap connector through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.77.0 implementation stop reached. Run pentest for this exact commit.

## v0.78.0 — AD-oriented LDAP profile

Status: Planned.

Goal:

Deliver ad-oriented ldap profile as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for ad-oriented ldap profile.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate ad-oriented ldap profile through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.78.0 implementation stop reached. Run pentest for this exact commit.

## v0.79.0 — Privacy-preserving host search

Status: Planned.

Goal:

Deliver privacy-preserving host search as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for privacy-preserving host search.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate privacy-preserving host search through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.79.0 implementation stop reached. Run pentest for this exact commit.

## v0.80.0 — Directory health/staleness controls

Status: Planned.

Goal:

Deliver directory health/staleness controls as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for directory health/staleness controls.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate directory health/staleness controls through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.80.0 implementation stop reached. Run pentest for this exact commit.

# Communications

## v0.81.0 — Notification domain model

Status: Planned.

Goal:

Deliver notification domain model as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for notification domain model.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate notification domain model through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.81.0 implementation stop reached. Run pentest for this exact commit.

## v0.82.0 — Template system

Status: Planned.

Goal:

Deliver template system as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for template system.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate template system through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.82.0 implementation stop reached. Run pentest for this exact commit.

## v0.83.0 — SMTP/email

Status: Planned.

Goal:

Deliver smtp/email as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for smtp/email.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate smtp/email through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.83.0 implementation stop reached. Run pentest for this exact commit.

## v0.84.0 — Microsoft Teams

Status: Planned.

Goal:

Deliver microsoft teams as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for microsoft teams.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate microsoft teams through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.84.0 implementation stop reached. Run pentest for this exact commit.

## v0.85.0 — Slack

Status: Planned.

Goal:

Deliver slack as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for slack.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate slack through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.85.0 implementation stop reached. Run pentest for this exact commit.

## v0.86.0 — SMS provider contract

Status: Planned.

Goal:

Deliver sms provider contract as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for sms provider contract.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate sms provider contract through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.86.0 implementation stop reached. Run pentest for this exact commit.

## v0.87.0 — Generic signed webhook

Status: Planned.

Goal:

Deliver generic signed webhook as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for generic signed webhook.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate generic signed webhook through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.87.0 implementation stop reached. Run pentest for this exact commit.

## v0.88.0 — Recipient preferences

Status: Planned.

Goal:

Deliver recipient preferences as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for recipient preferences.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate recipient preferences through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.88.0 implementation stop reached. Run pentest for this exact commit.

## v0.89.0 — Fallback/escalation routing

Status: Planned.

Goal:

Deliver fallback/escalation routing as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for fallback/escalation routing.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate fallback/escalation routing through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.89.0 implementation stop reached. Run pentest for this exact commit.

## v0.90.0 — Delivery/retry dashboard

Status: Planned.

Goal:

Deliver delivery/retry dashboard as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for delivery/retry dashboard.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate delivery/retry dashboard through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.90.0 implementation stop reached. Run pentest for this exact commit.

# Site hardware

## v0.91.0 — Initial gestur-edge

Status: Planned.

Goal:

Deliver initial gestur-edge as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for initial gestur-edge.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate initial gestur-edge through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.91.0 implementation stop reached. Run pentest for this exact commit.

## v0.92.0 — Edge workload identity/mTLS

Status: Planned.

Goal:

Deliver edge workload identity/mtls as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for edge workload identity/mtls.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate edge workload identity/mtls through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.92.0 implementation stop reached. Run pentest for this exact commit.

## v0.93.0 — Printer capability API

Status: Planned.

Goal:

Deliver printer capability api as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for printer capability api.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate printer capability api through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.93.0 implementation stop reached. Run pentest for this exact commit.

## v0.94.0 — IPP connector

Status: Planned.

Goal:

Deliver ipp connector as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for ipp connector.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate ipp connector through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.94.0 implementation stop reached. Run pentest for this exact commit.

## v0.95.0 — ZPL connector

Status: Planned.

Goal:

Deliver zpl connector as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for zpl connector.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate zpl connector through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.95.0 implementation stop reached. Run pentest for this exact commit.

## v0.96.0 — Badge template engine

Status: Planned.

Goal:

Deliver badge template engine as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for badge template engine.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate badge template engine through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.96.0 implementation stop reached. Run pentest for this exact commit.

## v0.97.0 — Print spool/idempotency

Status: Planned.

Goal:

Deliver print spool/idempotency as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for print spool/idempotency.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate print spool/idempotency through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.97.0 implementation stop reached. Run pentest for this exact commit.

## v0.98.0 — Visitor QR credential

Status: Planned.

Goal:

Deliver visitor qr credential as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for visitor qr credential.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate visitor qr credential through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.98.0 implementation stop reached. Run pentest for this exact commit.

## v0.99.0 — Badge expiry/revocation

Status: Planned.

Goal:

Deliver badge expiry/revocation as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for badge expiry/revocation.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate badge expiry/revocation through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.99.0 implementation stop reached. Run pentest for this exact commit.

## v0.100.0 — Multi-printer routing/failover

Status: Planned.

Goal:

Deliver multi-printer routing/failover as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for multi-printer routing/failover.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate multi-printer routing/failover through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.100.0 implementation stop reached. Run pentest for this exact commit.

# Wi-Fi and access

## v0.101.0 — Guest Wi-Fi capability model

Status: Planned.

Goal:

Deliver guest wi-fi capability model as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for guest wi-fi capability model.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate guest wi-fi capability model through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.101.0 implementation stop reached. Run pentest for this exact commit.

## v0.102.0 — Secure credential lifecycle

Status: Planned.

Goal:

Deliver secure credential lifecycle as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for secure credential lifecycle.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate secure credential lifecycle through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.102.0 implementation stop reached. Run pentest for this exact commit.

## v0.103.0 — UniFi reference connector

Status: Planned.

Goal:

Deliver unifi reference connector as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for unifi reference connector.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate unifi reference connector through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.103.0 implementation stop reached. Run pentest for this exact commit.

## v0.104.0 — Wi-Fi QR provisioning

Status: Planned.

Goal:

Deliver wi-fi qr provisioning as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for wi-fi qr provisioning.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate wi-fi qr provisioning through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.104.0 implementation stop reached. Run pentest for this exact commit.

## v0.105.0 — Automatic Wi-Fi revocation

Status: Planned.

Goal:

Deliver automatic wi-fi revocation as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for automatic wi-fi revocation.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate automatic wi-fi revocation through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.105.0 implementation stop reached. Run pentest for this exact commit.

## v0.106.0 — Physical-access capability API

Status: Planned.

Goal:

Deliver physical-access capability api as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for physical-access capability api.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate physical-access capability api through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.106.0 implementation stop reached. Run pentest for this exact commit.

## v0.107.0 — Zone/time-scoped credentials

Status: Planned.

Goal:

Deliver zone/time-scoped credentials as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for zone/time-scoped credentials.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate zone/time-scoped credentials through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.107.0 implementation stop reached. Run pentest for this exact commit.

## v0.108.0 — Access revoke/expiry

Status: Planned.

Goal:

Deliver access revoke/expiry as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for access revoke/expiry.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate access revoke/expiry through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.108.0 implementation stop reached. Run pentest for this exact commit.

## v0.109.0 — Credential reconciliation

Status: Planned.

Goal:

Deliver credential reconciliation as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for credential reconciliation.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate credential reconciliation through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.109.0 implementation stop reached. Run pentest for this exact commit.

## v0.110.0 — Checkout revokes all visit credentials invariant

Status: Planned.

Goal:

Deliver checkout revokes all visit credentials invariant as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for checkout revokes all visit credentials invariant.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate checkout revokes all visit credentials invariant through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.110.0 implementation stop reached. Run pentest for this exact commit.

# WebAssembly plugins

## v0.111.0 — WIT ABI v0

Status: Planned.

Goal:

Deliver wit abi v0 as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for wit abi v0.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate wit abi v0 through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.111.0 implementation stop reached. Run pentest for this exact commit.

## v0.112.0 — Wasmtime Component Model host

Status: Planned.

Goal:

Deliver wasmtime component model host as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for wasmtime component model host.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate wasmtime component model host through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.112.0 implementation stop reached. Run pentest for this exact commit.

## v0.113.0 — Capability broker

Status: Planned.

Goal:

Deliver capability broker as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for capability broker.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate capability broker through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.113.0 implementation stop reached. Run pentest for this exact commit.

## v0.114.0 — No-network/no-filesystem default sandbox

Status: Planned.

Goal:

Deliver no-network/no-filesystem default sandbox as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for no-network/no-filesystem default sandbox.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate no-network/no-filesystem default sandbox through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.114.0 implementation stop reached. Run pentest for this exact commit.

## v0.115.0 — Scoped HTTP broker

Status: Planned.

Goal:

Deliver scoped http broker as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for scoped http broker.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate scoped http broker through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.115.0 implementation stop reached. Run pentest for this exact commit.

## v0.116.0 — Secret handles

Status: Planned.

Goal:

Deliver secret handles as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for secret handles.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate secret handles through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.116.0 implementation stop reached. Run pentest for this exact commit.

## v0.117.0 — Fuel/time/memory limits

Status: Planned.

Goal:

Deliver fuel/time/memory limits as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for fuel/time/memory limits.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate fuel/time/memory limits through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.117.0 implementation stop reached. Run pentest for this exact commit.

## v0.118.0 — Signed plugin package format

Status: Planned.

Goal:

Deliver signed plugin package format as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for signed plugin package format.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate signed plugin package format through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.118.0 implementation stop reached. Run pentest for this exact commit.

## v0.119.0 — Declarative connector configuration schemas

Status: Planned.

Goal:

Deliver declarative connector configuration schemas as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for declarative connector configuration schemas.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate declarative connector configuration schemas through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.119.0 implementation stop reached. Run pentest for this exact commit.

## v0.120.0 — Plugin compatibility/conformance suite

Status: Planned.

Goal:

Deliver plugin compatibility/conformance suite as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for plugin compatibility/conformance suite.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate plugin compatibility/conformance suite through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.120.0 implementation stop reached. Run pentest for this exact commit.

# User interfaces

## v0.121.0 — Leptos guest SSR shell

Status: Planned.

Goal:

Deliver leptos guest ssr shell as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for leptos guest ssr shell.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate leptos guest ssr shell through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.121.0 implementation stop reached. Run pentest for this exact commit.

## v0.122.0 — Kiosk session lifecycle

Status: Planned.

Goal:

Deliver kiosk session lifecycle as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for kiosk session lifecycle.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate kiosk session lifecycle through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.122.0 implementation stop reached. Run pentest for this exact commit.

## v0.123.0 — Invitation/QR flow

Status: Planned.

Goal:

Deliver invitation/qr flow as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for invitation/qr flow.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate invitation/qr flow through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.123.0 implementation stop reached. Run pentest for this exact commit.

## v0.124.0 — Dynamic form renderer

Status: Planned.

Goal:

Deliver dynamic form renderer as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for dynamic form renderer.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate dynamic form renderer through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.124.0 implementation stop reached. Run pentest for this exact commit.

## v0.125.0 — Document/legal renderer

Status: Planned.

Goal:

Deliver document/legal renderer as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for document/legal renderer.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate document/legal renderer through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.125.0 implementation stop reached. Run pentest for this exact commit.

## v0.126.0 — Reception console

Status: Planned.

Goal:

Deliver reception console as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for reception console.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate reception console through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.126.0 implementation stop reached. Run pentest for this exact commit.

## v0.127.0 — Admin application

Status: Planned.

Goal:

Deliver admin application as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for admin application.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate admin application through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.127.0 implementation stop reached. Run pentest for this exact commit.

## v0.128.0 — Visual Guest Journey editor

Status: Planned.

Goal:

Deliver visual guest journey editor as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for visual guest journey editor.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate visual guest journey editor through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.128.0 implementation stop reached. Run pentest for this exact commit.

## v0.129.0 — Brand/theme editor

Status: Planned.

Goal:

Deliver brand/theme editor as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for brand/theme editor.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate brand/theme editor through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.129.0 implementation stop reached. Run pentest for this exact commit.

## v0.130.0 — Accessibility and localization baseline

Status: Planned.

Goal:

Deliver accessibility and localization baseline as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for accessibility and localization baseline.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate accessibility and localization baseline through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.130.0 implementation stop reached. Run pentest for this exact commit.

# Emergency, offline, and HA

## v0.131.0 — Emergency incident/muster model

Status: Planned.

Goal:

Deliver emergency incident/muster model as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for emergency incident/muster model.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate emergency incident/muster model through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.131.0 implementation stop reached. Run pentest for this exact commit.

## v0.132.0 — Emergency dashboard

Status: Planned.

Goal:

Deliver emergency dashboard as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for emergency dashboard.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate emergency dashboard through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.132.0 implementation stop reached. Run pentest for this exact commit.

## v0.133.0 — Edge local encrypted journal

Status: Planned.

Goal:

Deliver edge local encrypted journal as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for edge local encrypted journal.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate edge local encrypted journal through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.133.0 implementation stop reached. Run pentest for this exact commit.

## v0.134.0 — Offline host/config projection

Status: Planned.

Goal:

Deliver offline host/config projection as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for offline host/config projection.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate offline host/config projection through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.134.0 implementation stop reached. Run pentest for this exact commit.

## v0.135.0 — Offline check-in

Status: Planned.

Goal:

Deliver offline check-in as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for offline check-in.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate offline check-in through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.135.0 implementation stop reached. Run pentest for this exact commit.

## v0.136.0 — Edge-central reconciliation

Status: Planned.

Goal:

Deliver edge-central reconciliation as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for edge-central reconciliation.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate edge-central reconciliation through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.136.0 implementation stop reached. Run pentest for this exact commit.

## v0.137.0 — Valkey cache adapter

Status: Planned.

Goal:

Deliver valkey cache adapter as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for valkey cache adapter.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate valkey cache adapter through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.137.0 implementation stop reached. Run pentest for this exact commit.

## v0.138.0 — Multi-node API/session operation

Status: Planned.

Goal:

Deliver multi-node api/session operation as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for multi-node api/session operation.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate multi-node api/session operation through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.138.0 implementation stop reached. Run pentest for this exact commit.

## v0.139.0 — Database HA/failover procedures

Status: Planned.

Goal:

Deliver database ha/failover procedures as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for database ha/failover procedures.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate database ha/failover procedures through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.139.0 implementation stop reached. Run pentest for this exact commit.

## v0.140.0 — Backup/PITR/restore framework

Status: Planned.

Goal:

Deliver backup/pitr/restore framework as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for backup/pitr/restore framework.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate backup/pitr/restore framework through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.140.0 implementation stop reached. Run pentest for this exact commit.

# Advisory AI

## v0.141.0 — Provider-neutral AI gateway

Status: Planned.

Goal:

Deliver provider-neutral ai gateway as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for provider-neutral ai gateway.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate provider-neutral ai gateway through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.141.0 implementation stop reached. Run pentest for this exact commit.

## v0.142.0 — AI data-classification and DLP boundary

Status: Planned.

Goal:

Deliver ai data-classification and dlp boundary as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for ai data-classification and dlp boundary.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate ai data-classification and dlp boundary through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.142.0 implementation stop reached. Run pentest for this exact commit.

## v0.143.0 — AI disclosure/transparency framework

Status: Planned.

Goal:

Deliver ai disclosure/transparency framework as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for ai disclosure/transparency framework.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate ai disclosure/transparency framework through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.143.0 implementation stop reached. Run pentest for this exact commit.

## v0.144.0 — Multilingual reception assistant

Status: Planned.

Goal:

Deliver multilingual reception assistant as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for multilingual reception assistant.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate multilingual reception assistant through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.144.0 implementation stop reached. Run pentest for this exact commit.

## v0.145.0 — Translation-draft assistant

Status: Planned.

Goal:

Deliver translation-draft assistant as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for translation-draft assistant.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate translation-draft assistant through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.145.0 implementation stop reached. Run pentest for this exact commit.

## v0.146.0 — Invitation extraction

Status: Planned.

Goal:

Deliver invitation extraction as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for invitation extraction.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate invitation extraction through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.146.0 implementation stop reached. Run pentest for this exact commit.

## v0.147.0 — Constrained admin query assistant

Status: Planned.

Goal:

Deliver constrained admin query assistant as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for constrained admin query assistant.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate constrained admin query assistant through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.147.0 implementation stop reached. Run pentest for this exact commit.

## v0.148.0 — Journey/configuration assistant

Status: Planned.

Goal:

Deliver journey/configuration assistant as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for journey/configuration assistant.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate journey/configuration assistant through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.148.0 implementation stop reached. Run pentest for this exact commit.

## v0.149.0 — Incident/evidence summarization

Status: Planned.

Goal:

Deliver incident/evidence summarization as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for incident/evidence summarization.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate incident/evidence summarization through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.149.0 implementation stop reached. Run pentest for this exact commit.

## v0.150.0 — AI evaluation, prompt-injection and human-authority gates

Status: Planned.

Goal:

Deliver ai evaluation, prompt-injection and human-authority gates as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for ai evaluation, prompt-injection and human-authority gates.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate ai evaluation, prompt-injection and human-authority gates through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.150.0 implementation stop reached. Run pentest for this exact commit.

# Calendar and preregistration

## v0.151.0 — Calendar connector capability

Status: Planned.

Goal:

Deliver calendar connector capability as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for calendar connector capability.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate calendar connector capability through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.151.0 implementation stop reached. Run pentest for this exact commit.

## v0.152.0 — Microsoft calendar integration

Status: Planned.

Goal:

Deliver microsoft calendar integration as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for microsoft calendar integration.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate microsoft calendar integration through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.152.0 implementation stop reached. Run pentest for this exact commit.

## v0.153.0 — Generic iCalendar import

Status: Planned.

Goal:

Deliver generic icalendar import as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for generic icalendar import.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate generic icalendar import through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.153.0 implementation stop reached. Run pentest for this exact commit.

## v0.154.0 — Meeting-to-visit mapping

Status: Planned.

Goal:

Deliver meeting-to-visit mapping as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for meeting-to-visit mapping.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate meeting-to-visit mapping through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.154.0 implementation stop reached. Run pentest for this exact commit.

## v0.155.0 — Host-controlled pre-registration

Status: Planned.

Goal:

Deliver host-controlled pre-registration as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for host-controlled pre-registration.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate host-controlled pre-registration through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.155.0 implementation stop reached. Run pentest for this exact commit.

## v0.156.0 — Bulk/group invitations

Status: Planned.

Goal:

Deliver bulk/group invitations as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for bulk/group invitations.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate bulk/group invitations through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.156.0 implementation stop reached. Run pentest for this exact commit.

## v0.157.0 — Recurring visitors

Status: Planned.

Goal:

Deliver recurring visitors as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for recurring visitors.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate recurring visitors through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.157.0 implementation stop reached. Run pentest for this exact commit.

## v0.158.0 — Plus-one guests

Status: Planned.

Goal:

Deliver plus-one guests as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for plus-one guests.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate plus-one guests through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.158.0 implementation stop reached. Run pentest for this exact commit.

## v0.159.0 — Invitation email templates

Status: Planned.

Goal:

Deliver invitation email templates as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for invitation email templates.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate invitation email templates through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.159.0 implementation stop reached. Run pentest for this exact commit.

## v0.160.0 — Pre-arrival document completion

Status: Planned.

Goal:

Deliver pre-arrival document completion as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for pre-arrival document completion.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate pre-arrival document completion through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.160.0 implementation stop reached. Run pentest for this exact commit.

# Enterprise policy

## v0.161.0 — EU/EEA technical compliance baseline

Status: Planned.

Goal:

Deliver eu/eea technical compliance baseline as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for eu/eea technical compliance baseline.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate eu/eea technical compliance baseline through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.161.0 implementation stop reached. Run pentest for this exact commit.

## v0.162.0 — Swedish deployment profile

Status: Planned.

Goal:

Deliver swedish deployment profile as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for swedish deployment profile.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate swedish deployment profile through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.162.0 implementation stop reached. Run pentest for this exact commit.

## v0.163.0 — UK/Swiss profiles

Status: Planned.

Goal:

Deliver uk/swiss profiles as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for uk/swiss profiles.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate uk/swiss profiles through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.163.0 implementation stop reached. Run pentest for this exact commit.

## v0.164.0 — North-American policy-pack framework

Status: Planned.

Goal:

Deliver north-american policy-pack framework as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for north-american policy-pack framework.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate north-american policy-pack framework through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.164.0 implementation stop reached. Run pentest for this exact commit.

## v0.165.0 — Data residency controls

Status: Planned.

Goal:

Deliver data residency controls as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for data residency controls.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate data residency controls through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.165.0 implementation stop reached. Run pentest for this exact commit.

## v0.166.0 — KMS integration

Status: Planned.

Goal:

Deliver kms integration as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for kms integration.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate kms integration through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.166.0 implementation stop reached. Run pentest for this exact commit.

## v0.167.0 — HSM/PKCS#11 capability

Status: Planned.

Goal:

Deliver hsm/pkcs#11 capability as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for hsm/pkcs#11 capability.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate hsm/pkcs#11 capability through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.167.0 implementation stop reached. Run pentest for this exact commit.

## v0.168.0 — Per-tenant encryption keys

Status: Planned.

Goal:

Deliver per-tenant encryption keys as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for per-tenant encryption keys.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate per-tenant encryption keys through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.168.0 implementation stop reached. Run pentest for this exact commit.

## v0.169.0 — Online key rotation

Status: Planned.

Goal:

Deliver online key rotation as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for online key rotation.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate online key rotation through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.169.0 implementation stop reached. Run pentest for this exact commit.

## v0.170.0 — SIEM/security-event export

Status: Planned.

Goal:

Deliver siem/security-event export as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for siem/security-event export.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate siem/security-event export through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.170.0 implementation stop reached. Run pentest for this exact commit.

# Advanced security

## v0.171.0 — Fine-grained ABAC

Status: Planned.

Goal:

Deliver fine-grained abac as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for fine-grained abac.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate fine-grained abac through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.171.0 implementation stop reached. Run pentest for this exact commit.

## v0.172.0 — Sensitive-export approvals

Status: Planned.

Goal:

Deliver sensitive-export approvals as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for sensitive-export approvals.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate sensitive-export approvals through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.172.0 implementation stop reached. Run pentest for this exact commit.

## v0.173.0 — Connector egress policy editor

Status: Planned.

Goal:

Deliver connector egress policy editor as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for connector egress policy editor.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate connector egress policy editor through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.173.0 implementation stop reached. Run pentest for this exact commit.

## v0.174.0 — Plugin signing/trust stores

Status: Planned.

Goal:

Deliver plugin signing/trust stores as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for plugin signing/trust stores.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate plugin signing/trust stores through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.174.0 implementation stop reached. Run pentest for this exact commit.

## v0.175.0 — Security notification center

Status: Planned.

Goal:

Deliver security notification center as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for security notification center.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate security notification center through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.175.0 implementation stop reached. Run pentest for this exact commit.

## v0.176.0 — Controlled watchlist framework

Status: Planned.

Goal:

Deliver controlled watchlist framework as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for controlled watchlist framework.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate controlled watchlist framework through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.176.0 implementation stop reached. Run pentest for this exact commit.

## v0.177.0 — Optional identity-verification connectors

Status: Planned.

Goal:

Deliver optional identity-verification connectors as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for optional identity-verification connectors.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate optional identity-verification connectors through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.177.0 implementation stop reached. Run pentest for this exact commit.

## v0.178.0 — Security incident preservation mode

Status: Planned.

Goal:

Deliver security incident preservation mode as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for security incident preservation mode.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate security incident preservation mode through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.178.0 implementation stop reached. Run pentest for this exact commit.

## v0.179.0 — Tamper-evident remote audit copy

Status: Planned.

Goal:

Deliver tamper-evident remote audit copy as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for tamper-evident remote audit copy.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate tamper-evident remote audit copy through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.179.0 implementation stop reached. Run pentest for this exact commit.

## v0.180.0 — Full enterprise threat-model revision

Status: Planned.

Goal:

Deliver full enterprise threat-model revision as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for full enterprise threat-model revision.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate full enterprise threat-model revision through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.180.0 implementation stop reached. Run pentest for this exact commit.

# Operational maturity

## v0.181.0 — OpenTelemetry export

Status: Planned.

Goal:

Deliver opentelemetry export as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for opentelemetry export.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate opentelemetry export through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.181.0 implementation stop reached. Run pentest for this exact commit.

## v0.182.0 — SLO dashboards

Status: Planned.

Goal:

Deliver slo dashboards as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for slo dashboards.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate slo dashboards through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.182.0 implementation stop reached. Run pentest for this exact commit.

## v0.183.0 — Connector health scoring

Status: Planned.

Goal:

Deliver connector health scoring as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for connector health scoring.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate connector health scoring through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.183.0 implementation stop reached. Run pentest for this exact commit.

## v0.184.0 — Edge fleet administration

Status: Planned.

Goal:

Deliver edge fleet administration as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for edge fleet administration.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate edge fleet administration through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.184.0 implementation stop reached. Run pentest for this exact commit.

## v0.185.0 — Rolling upgrade compatibility

Status: Planned.

Goal:

Deliver rolling upgrade compatibility as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for rolling upgrade compatibility.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate rolling upgrade compatibility through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.185.0 implementation stop reached. Run pentest for this exact commit.

## v0.186.0 — Zero-downtime migration framework

Status: Planned.

Goal:

Deliver zero-downtime migration framework as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for zero-downtime migration framework.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate zero-downtime migration framework through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.186.0 implementation stop reached. Run pentest for this exact commit.

## v0.187.0 — Multi-region residency topology

Status: Planned.

Goal:

Deliver multi-region residency topology as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for multi-region residency topology.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate multi-region residency topology through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.187.0 implementation stop reached. Run pentest for this exact commit.

## v0.188.0 — Object-storage replication/recovery

Status: Planned.

Goal:

Deliver object-storage replication/recovery as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for object-storage replication/recovery.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate object-storage replication/recovery through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.188.0 implementation stop reached. Run pentest for this exact commit.

## v0.189.0 — Disaster runbooks

Status: Planned.

Goal:

Deliver disaster runbooks as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for disaster runbooks.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate disaster runbooks through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.189.0 implementation stop reached. Run pentest for this exact commit.

## v0.190.0 — Automated restore verification

Status: Planned.

Goal:

Deliver automated restore verification as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for automated restore verification.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate automated restore verification through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.190.0 implementation stop reached. Run pentest for this exact commit.

# Release qualification

## v0.191.0 — Complete PostgreSQL/MySQL/SQLite conformance run

Status: Planned.

Goal:

Deliver complete postgresql/mysql/sqlite conformance run as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for complete postgresql/mysql/sqlite conformance run.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate complete postgresql/mysql/sqlite conformance run through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.191.0 implementation stop reached. Run pentest for this exact commit.

## v0.192.0 — Migration testing from every supported pre-1.0 schema

Status: Planned.

Goal:

Deliver migration testing from every supported pre-1.0 schema as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for migration testing from every supported pre-1.0 schema.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate migration testing from every supported pre-1.0 schema through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.192.0 implementation stop reached. Run pentest for this exact commit.

## v0.193.0 — Backup/restore disaster rehearsal

Status: Planned.

Goal:

Deliver backup/restore disaster rehearsal as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for backup/restore disaster rehearsal.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate backup/restore disaster rehearsal through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.193.0 implementation stop reached. Run pentest for this exact commit.

## v0.194.0 — WAN/Valkey/DB/connector chaos campaign

Status: Planned.

Goal:

Deliver wan/valkey/db/connector chaos campaign as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for wan/valkey/db/connector chaos campaign.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate wan/valkey/db/connector chaos campaign through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.194.0 implementation stop reached. Run pentest for this exact commit.

## v0.195.0 — Large-site load/soak tests

Status: Planned.

Goal:

Deliver large-site load/soak tests as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for large-site load/soak tests.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate large-site load/soak tests through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.195.0 implementation stop reached. Run pentest for this exact commit.

## v0.196.0 — Manual accessibility review

Status: Planned.

Goal:

Deliver manual accessibility review as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for manual accessibility review.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate manual accessibility review through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.196.0 implementation stop reached. Run pentest for this exact commit.

## v0.197.0 — Privacy/compliance review

Status: Planned.

Goal:

Deliver privacy/compliance review as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for privacy/compliance review.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate privacy/compliance review through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.197.0 implementation stop reached. Run pentest for this exact commit.

## v0.198.0 — Independent security/pentest release

Status: Planned.

Goal:

Deliver independent security/pentest release as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for independent security/pentest release.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate independent security/pentest release through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.198.0 implementation stop reached. Run pentest for this exact commit.

## v0.199.0 — API/WIT/config compatibility freeze

Status: Planned.

Goal:

Deliver api/wit/config compatibility freeze as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for api/wit/config compatibility freeze.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate api/wit/config compatibility freeze through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.199.0 implementation stop reached. Run pentest for this exact commit.

## v0.200.0 — 1.0 release candidate

Status: Planned.

Goal:

Deliver 1.0 release candidate as one bounded, security-reviewed capability
without widening unrelated authority or coupling portable domain logic to an
infrastructure implementation.

Deliverables:

- Define and implement the smallest stable domain, contract, adapter, UI, or
  operational surface needed for 1.0 release candidate.
- Keep tenant, site, actor, purpose, classification, revision, idempotency,
  resource bounds, and failure behavior explicit wherever they apply.
- Add focused positive, negative, boundary, replay/retry, cross-tenant,
  degraded-mode, and misuse tests appropriate to this capability.
- Update architecture/security/privacy documentation, the threat model,
  changelog, and release notes; state unsupported behavior and non-claims.
- Add or tighten a dedicated crate/module boundary and test seam when the
  capability would otherwise enlarge an existing responsibility.

Verification:

- Run the complete mandatory repository and release verification defined above.
- Demonstrate 1.0 release candidate through deterministic tests or recorded
  operational/conformance evidence; no production service may be the only test
  oracle.
- Prove failure is closed, attributable, bounded, and free of duplicate
  authoritative side effects for the release-specific trust boundaries.
- Review every affected platform and no_std boundary and record any deliberate
  limitation in the release notes.

Exit criteria:

- The stated capability and adversarial tests pass, documentation matches
  behavior, no unresolved high-impact finding or hidden dependency remains,
  and the release can stop without unfinished migration or compatibility work.
- Owner-operated pentesting with third-party security tools covers the exact implementation commit; every finding
  is fixed and cleanly retested before permanent PASS evidence or a tag.
- v0.200.0 implementation stop reached. Run pentest for this exact commit.

# Production Promotion

## v1.0.0 — Serious production release

Status: Planned; no new feature scope after v0.200.0.

Goal:

Promote the exact qualified release candidate into the first serious production
Gestur release without introducing surprise code, configuration, schema, API,
WIT, dependency, toolchain, or artifact changes.

Deliverables:

- Complete the 37-step acceptance scenario in the implementation plan with AI
  disabled and with each declared database/deployment profile.
- Freeze supported APIs, WIT, configuration, storage/migration compatibility,
  platform matrix, operations, security non-claims, and support policy.
- Produce signed source/binary artifacts as applicable, checksums, SBOM,
  provenance, restore evidence, complete documentation, and final release notes.
- Keep every internal Cargo package publish-disabled; no crates.io action is
  part of v1.0.0.

Verification:

- Repeat the full qualification, compatibility, restore, chaos, load,
  accessibility, privacy, audit, and security gates on the exact candidate.
- Require an independent cumulative pentest and clean retest, green GitHub CI,
  green CodeQL default setup, and artifact reproducibility evidence.
- Prove the v1.0.0 artifacts are bit/content equivalent to the approved release
  candidate except for reviewed release metadata.

Exit criteria:

- All v1.0 claims have direct evidence, no release blocker or unresolved
  security finding remains, and the maintainer explicitly approves promotion.
- Owner-operated pentesting with third-party security tools covers the exact production candidate.
- v1.0.0 implementation stop reached. Run pentest for this exact commit.
