# Gestur Detailed Version Plan

Status: planning document; v0.1.0 foundation implemented, independent pentest
pending

Production target: v1.0.0

This register strengthens the 200 capability envelopes in the
[release plan](RELEASE_PLAN.md). It records the mandatory patch-sized stops
needed to make their dependency order, security context, and proof concrete.
It does not claim that a planned capability exists.

## Authority And Stop Contract

For every row below:

- **Goal:** deliver only the named outcome without widening authority.
- **Deliverables:** the named contract or behavior, its tests, threat/privacy
  delta, documentation, release notes, and evidence-index entry.
- **Verification:** all repository gates plus the row's mandatory proof. A
  support claim additionally requires its real implementation, device,
  platform, browser, service, or an official faithful simulator. Unit-only and
  mock-only evidence cannot close a stop.
- **Exit criteria:** behavior and documentation agree; failures are bounded,
  attributable, fail closed, and do not duplicate authoritative effects; no
  hidden migration or compatibility work remains; the exact commit passes an
  independent pentest, findings receive regression tests and a clean retest,
  and only then may maintainers explicitly authorize a signed tag.

A base `v0.N.0` release cannot close until its listed `v0.N.P` stops close in
order. A stop that becomes too large is split at the next unused patch number.
In a grouped range, deliverables listed left-to-right map to versions in
ascending order; rows spell out any non-one-to-one grouping. No stop publishes
a Cargo package or authorizes a third-party crate.

## Review Disposition

The architecture gap review was treated as review input and checked against the
repository rather than copied over the existing plans.

Accepted corrections:

- canonical values/envelopes and key-provider contracts move before storage and
  PII abstractions;
- idempotency, inbox/outbox, deletion-ledger, and fault semantics precede
  production adapters/effects;
- journeys separate definition, published bundle, deterministic execution, and
  effect saga, with whole-graph privacy/capability analysis;
- signed edge authority precedes hardware adapters and later offline sync;
- privacy-vault, erasure, evidence, legal-hold, plugin, connector, kiosk, and AI
  boundaries receive explicit adversarial and real-system proof;
- Wallet, UWB, LPR, elevator, delivery, contractor, export-control, sanctions,
  restore, update, and release-candidate gaps receive named stops.

Accepted with qualification:

- UWB is a proximity/ranging observation, never identity or authorization;
- LPR is optional personal-data observation with strict retention and a manual
  fallback;
- Wallet NFC support is conditional on vendor approval/certification and
  compatible terminals; QR/manual remains available;
- WCAG 2.2 AA is a web-content baseline, while physical kiosk accessibility,
  reach, privacy, timeouts, and alternatives require additional testing;
- compliance packs are versioned technical controls and evidence, never legal
  advice, automatic compliance, or automatic denial authority.

Rejected or corrected:

- The review's fixed test-count snapshot is stale by design; gates discover and
  run the current suite instead of documenting a count.
- Third-party boundary libraries are not admitted. Where the current rule makes
  safe TLS, cryptography, OIDC, SQL, Unicode security, or Wasm execution
  impossible, the capability remains blocked rather than being hand-written or
  silently exempted.
- Specialist cumulative reviews do not replace Gestur's independent
  exact-commit pentest and clean-retest requirement at every version.

## Dependency Invariants

1. `v0.3.1–v0.3.4` precede every durable or external envelope.
2. `v0.11.1–v0.11.5` precede database adapters and effect workers.
3. `v0.29.0` and `v0.30.0` authority/isolation proof precede PII.
4. `v0.3.4` permits PII metadata at `v0.32.x`; production PII stays disabled
   until `v0.166.0–v0.169.0` and the privacy/restore gates close.
5. `v0.46.1–v0.50.3` precede journeys that can request external effects.
6. `v0.92.0–v0.92.4` precede printer, network, access, UWB, and LPR adapters.
7. `v0.87.1` egress rules are reused by first-party connectors and the later
   Wasm broker; Wasm never becomes the source of those rules.
8. AI remains a leaf from `v0.141.0`; `v0.150.1` proves disabled-AI parity.

## Phase 1 — Foundation Detail (v0.1.x–v0.10.x)

| Stop | Context and sole deliverable | Mandatory proof |
| --- | --- | --- |
| v0.1.1 | Reconcile foundation status and generated inventory; state only implemented controls. | Inventory matches Cargo metadata; documentation structure/link/policy gates pass. |
| v0.2.1 | Add signed provenance and reproducible artifact-attestation contract. | Tampered source, toolchain, SBOM, and artifact attestations are rejected. |
| v0.3.1 | Add canonical nonzero 128-bit ID parsing and a collision-safe generator contract. | Golden byte/text vectors; zero, overflow, malformed, and type-confusion rejection; generator model tests. |
| v0.3.2 | Add explicit instant, civil-time, timezone, duration, deadline, and uncertainty vocabulary. | DST, leap-boundary, skew, overflow, ordering, and serialization vectors. |
| v0.3.3 | Freeze canonical encoding, bounded strings/bytes/collections, and schema-version rules. | Cross-platform golden vectors; noncanonical, oversized, ambiguous, and unknown-version rejection. |
| v0.3.4 | Define command/event envelopes plus algorithm, key-reference, and key-provider contracts. | Attribution, tenant/site, purpose, revision, idempotency, causation/correlation, sequence, unknown algorithm, downgrade, and key-state tests. |
| v0.4.1 | Freeze stable public/internal error mapping and disclosure budget. | Every failure maps deterministically; secrets and PII cannot enter messages or debug output. |
| v0.5.1 | Prove no_std/core/alloc/std feature and dependency tiers. | Target matrix and dependency-direction fixtures fail when a forbidden edge or std use is introduced. |
| v0.6.1 | Add layered configuration provenance, bounds, secret references, and fail-closed reload. | Unknown/duplicate keys, precedence, rollback, redaction, hostile sizes, and partial-reload tests. |
| v0.7.1 | Add telemetry classification, cardinality budgets, and canary redaction. | PII/secret canaries and hostile labels never cross the telemetry contract. |
| v0.8.1 | Make zero-third-party admission and unsafe-substitution blocking executable. | Registry, git, transitive, build/dev dependency, patch, target, vendoring, and publication escape fixtures fail. |
| v0.9.1 | Extend deterministic testkit with clock, entropy, scheduler, fault, and trace controls. | Repeatability across platforms; injected failures cannot be skipped silently. |
| v0.10.1 | Validate threat model v1 against abuse cases and control-to-test traceability. | Independent review maps each trust boundary and control to current or explicitly future evidence. |

Phase exit: canonical envelopes and crypto-provider contracts are independently
reviewed before storage/PII implementation; the foundation remains
non-deployable until later phases close.

## Phase 2 — Storage Detail (v0.11.x–v0.20.x)

| Stop | Context and sole deliverable | Mandatory proof |
| --- | --- | --- |
| v0.11.1 | Define `UnitOfWork`, isolation, durability, retry, commit, and rollback semantics. | Model histories cover crash at every boundary and ambiguous commit. |
| v0.11.2 | Define revision, deterministic ordering, cursor, limit, and snapshot pagination semantics. | Lost-update, stale-write, duplicate/skip, malformed cursor, and hostile-limit tests. |
| v0.11.3 | Define idempotency, inbox identity+digest, outbox effect, lease, attempt, and acknowledgement semantics. | Same-key/same-body replay is stable; same-key/different-body alarms; crash/retry creates no duplicate effect. |
| v0.11.4 | Define migration, schema compatibility, and mixed-version behavior. | Expand/migrate/contract, interruption, rollback, and N/N-1 fixtures. |
| v0.11.5 | Define independently durable anti-resurrection deletion ledger and restore ordering. | Restored old data is denied before reads; ledger loss/corruption fails closed. |
| v0.12.1 | Complete SQLite contract, including concurrency, WAL, backup, and corruption behavior. | Actual supported SQLite engine under lock, disk-full, kill, restore, and corruption faults. |
| v0.13.1 | Complete PostgreSQL contract, including transaction, pool, failover, and timeout behavior. | Actual supported PostgreSQL versions and configurations pass identical histories. |
| v0.14.1 | Complete MySQL contract, including collation, isolation, failover, and timeout behavior. | Actual supported MySQL versions and configurations pass identical histories. |
| v0.15.1 | Add semantic differential and deterministic storage fault suite. | Same black-box histories/results on all engines; injected commit/IO/network failures are attributable. |
| v0.16.1 | Add signed migration manifest and deletion-ledger migrations. | Tamper, reorder, partial apply, restore, downgrade, and mixed-schema tests. |
| v0.17.1 | Close optimistic-revision and stable-pagination implementation gaps. | Real-engine concurrency and pagination soak; no backend-specific authorization/result differences. |
| v0.18.1 | Implement idempotency records with request digests and bounded retention. | Real-engine concurrent replay and key-reuse attack tests. |
| v0.19.1 | Implement transactional outbox and inbox with lease recovery and ambiguity state. | Kill at every write/send/ack point; exactly one semantic effect despite at-least-once delivery. |
| v0.20.1 | Complete filesystem BlobStore with integrity, atomicity, path, quota, and durability rules. | Real filesystem crash, traversal, symlink, short-write, disk-full, corruption, and restore tests on claimed OSes. |

Phase exit: the same conformance corpus passes all three real databases; storage
and privacy reviewers close findings before tenant or PII persistence expands.

## Phases 3–4 — Authority, Visitors, And Visits (v0.21.x–v0.40.x)

| Stop | Context and sole deliverable | Mandatory proof |
| --- | --- | --- |
| v0.21.1 | Bind tenants to legal entities, residency profile, status, and immutable identity. | Cross-tenant object/reference/cache/job tests and tenant lifecycle model. |
| v0.23.1 | Model site jurisdiction, timezone, emergency authority, and edge ownership. | Cross-site authority, timezone, transfer, and incident-boundary tests. |
| v0.27.1 | Give every kiosk/desk/edge workload a distinct, revocable identity. | Cloned, stale, reassigned, lost, and wrong-site workload denial. |
| v0.29.1 | Add typed obligations and delegated authority with scope and expiry. | Unknown facts fail closed; delegation cannot widen grant, site, purpose, or time. |
| v0.30.1 | Run adversarial tenant/site isolation campaign across storage, cache, jobs, blobs, logs, and exports. | Negative matrix on every real backend plus concurrency and identifier-confusion cases. |
| v0.31.1 | Separate visit facts, random subject reference, PII vault, evidence, audit, diagnostics, and deletion ledger. | Dependency/schema/access review proves no broad ORM or credential crosses the boundaries. |
| v0.32.1 | Define purpose-scoped PII envelopes, AAD profile, plaintext lifetime, and blind-index policy. | Wrong tenant/purpose/schema/key/version fails; low-entropy unkeyed indexes prohibited; no production-support claim. |
| v0.34.1 | Make arrival/check-in prerequisites explicit obligations. | Denied, expired, missing-host, missing-document, stale-policy, and concurrent transition model. |
| v0.34.2 | Make checkout/expiry enqueue revocation effects atomically. | Crash/retry/race tests cannot leave an untracked Gestur credential. |
| v0.40.1 | Add bounded arrival/approval queue as a projection, never authority. | Rebuild/replay/staleness tests and no projection-to-state shortcut. |
| v0.40.2 | Add contractor credential lifecycle distinct from a visit. | Employer/work order/training/sponsor/zones/suspension/expiry and revocation tests. |
| v0.40.3 | Add courier/delivery lifecycle distinct from visitor identity. | Package/courier/recipient/chain-of-custody/retention and minimal-data tests. |

Phase exit: tenant isolation is demonstrated before real PII; production PII
remains disabled pending the privacy, key-provider, deletion, and restore gates.

## Phase 5 — Typed Guest Journeys (v0.41.x–v0.50.x)

| Stop | Context and sole deliverable | Mandatory proof |
| --- | --- | --- |
| v0.41.1 | Attach stable purpose, legal-basis input, source, classification, recipients, visibility, retention, residency, connector, AI, and erasure metadata to fields. | Missing or contradictory metadata prevents publication. |
| v0.42.1 | Make form and validation revisions immutable, bounded, localized, and reconstructable. | Old revisions render/validate identically; hostile regex/size/locale inputs are bounded. |
| v0.43.1 | Add typed routing and disclosure checks to submission validation. | Fields cannot reach undeclared nodes, evidence, connectors, exports, or AI. |
| v0.45.1–v0.45.6 | Add one pure input node per stop: `Start`, `IdentifySubject`, `FindHost`, `SelectEntrance`, `CollectFields`, `PresentPrivacyNotice`. | Per-node positive/negative/boundary/property tests and typed-port golden vectors. |
| v0.47.1–v0.47.7 | Add one legal node per stop: `RecordAcknowledgement`, `RequestConsent`, `AcceptAgreement`, `SignDocument`, `RequireDocumentRevision`, `WithdrawConsent`, `ApplyRestriction`. | Notice/consent/agreement/signature semantics remain distinct; withdrawal and accessibility paths close. |
| v0.48.1–v0.48.8 | Add one policy node per stop: `SafetyBriefing`, `SafetyQuiz`, `HostApproval`, `ReceptionApproval`, `SecurityApproval`, `ScreeningCheck`, `EscortRequirement`, `ManualComplianceReview`. | Deterministic obligations; potential screening match never auto-denies or grants. |
| v0.49.1–v0.49.13 | Add one effect-intent node per stop: badge, Wi-Fi, access, locker, parking, digital pass, proximity, plate observation, three notifications, visitor instructions, escalation. | Nodes create bounded effect intents only; retries and adapter ambiguity never transition directly. |
| v0.49.14–v0.49.20 | Add one control node per stop: `Branch`, `Condition`, `Wait`, `Expire`, `Reject`, `ManualReview`, `Complete`. | Exhaustive outputs, durable timers, bounded cycles, terminal invariants, no secret-bearing reasons. |
| v0.46.1 | Implement whole-graph validation: one start, reachability, terminals, typed ports, bounded cycles/waits/retries. | Mutation/property corpus proves every invalid graph class is rejected deterministically. |
| v0.46.2 | Implement whole-graph privacy, purpose, capability, connector, evidence, and AI data-flow analysis. | Prohibited paths fail compilation even when hidden behind branches or reusable subgraphs. |
| v0.48.9 | Publish an immutable signed bundle pinning graph, policy, fields, forms, documents, renderer, localization, and dependency digests. | Canonicalization, substitution, rollback, signature, and offline verification vectors. |
| v0.50.1 | Implement execution pinned to one published bundle and one exact policy revision. | Replay produces byte-identical state and effect intents. |
| v0.50.2 | Separate effect saga state from journey state. | Adapter response, duplicate callback, timeout, and compensation cannot bypass command/policy/outbox. |
| v0.50.3 | Complete deterministic simulator, scenario DSL, and visual trace. | Golden success, denial, timeout, retry, offline, and every-node scenarios. |

Phase exit: a journey cannot publish unless graph, privacy, purpose, authority,
resource, and effect-flow analysis pass; every node is independently testable.

## Phase 6 — Privacy, Evidence, And Audit (v0.51.x–v0.70.x)

| Stop | Context and sole deliverable | Mandatory proof |
| --- | --- | --- |
| v0.51.1 | Pin immutable source bytes, canonical text, rendered artifact, locale, assets, renderer, and digests. | Historical reconstruction on clean tooling with substitution detection. |
| v0.52.1 | Record privacy-notice presentation separately from consent. | Exact revision/locale/time/render/session evidence; replay and wrong-notice rejection. |
| v0.53.1 | Implement purpose-specific consent grant/withdrawal ledger. | Optional path, coercion, withdrawal race, and retained-other-legal-basis tests. |
| v0.54.1 | Implement agreement evidence manifest and atomic acceptance. | Challenge replay, wrong document/journey, partial commit, and identity-binding tests. |
| v0.55.1 | Add typed acknowledgement, click, drawn-mark, authenticated, and external e-signature assurance profiles. | Profile downgrade fails; claims never overstate legal/technical assurance; accessible alternative works. |
| v0.56.1–v0.56.5 | Add collection, read, export/DSAR, connector-disclosure, and AI-disclosure gates one per stop. | Exact policy revision controls each field; cache/export/provider paths cannot bypass. |
| v0.57.1 | Add restriction-of-processing and scoped append-only legal-hold lifecycle. | Hold/retention/erasure race model; dual control; hold preserves but never broadens use. |
| v0.58.1 | Implement deny-read-first idempotent erasure and scoped key/index/cache/session removal. | Concurrent read/hold/retry/restore; no partial-success or instant-erasure overclaim. |
| v0.58.2 | Implement processor, connector, blob, replica, export, and backup deletion obligations. | Timeout/retry/exception/escalation receipts and recurring suppression tests. |
| v0.58.3 | Implement unlinking and anonymous-analytics threshold policy. | Re-identification attacks over IDs, hashes, dates, plates, and small cells. |
| v0.59.1 | Complete verified access, correction, portability, objection, restriction, and erasure request state machines. | Impostor, third-party rights, overcollection, deadline, and appeal tests. |
| v0.60.1 | Add full, minimized, and redacted evidence bundle manifests plus offline inputs. | Missing, reordered, substituted, revoked, and erased-content verification. |
| v0.61.1 | Enforce minimized security/privacy/audit schemas. | Schemas cannot carry secrets, full payloads, raw tokens, or unnecessary stable subject IDs. |
| v0.62.1–v0.65.1 | Close gap-free audit sequencing, hash/Merkle segments, root signing/key lifecycle, and independent WORM/RFC 3161 anchoring one per stop. | Insert/delete/reorder/truncate/fork/rollback/key-compromise/anchor-outage detection. |
| v0.66.1 | Separate audit integrity from PII-bearing evidence confidentiality. | Lawful content-key destruction does not invalidate non-identifying integrity roots. |
| v0.67.1–v0.69.1 | Close delegated actor chain, alarmed expiring break-glass, and dual-control semantics one per stop. | Effective actor is reconstructable; no standing vendor privilege or self-approval. |
| v0.70.1 | Complete dependency-free offline verifier package and hostile-evidence corpus. | Clean machine verifies valid evidence and diagnoses every tamper class without production credentials. |

Phase exit: privacy-vault and cryptographic-evidence designs receive specialist
review. No real visitor PII trial starts before required key, erasure, and
restore assumptions are demonstrated.

## Phases 7–8 — Identity, Communications, Edge, And Credentials

| Stop | Context and sole deliverable | Mandatory proof |
| --- | --- | --- |
| v0.71.1 | Add strict OIDC code+PKCE, issuer/subject tenant binding, nonce/state, token/JWKS, session, and step-up policy. | Real provider/conformance evidence plus mix-up, fixation, rotation, outage, and email-linking attacks. |
| v0.72.1 | Add passkey assurance, backup state, recovery, revocation, and sensitive-operation step-up. | Real authenticators/browsers; recovery cannot downgrade or bypass tenant binding. |
| v0.74.1 | Define bounded raw-ingestion envelope shared by directories, calendars, callbacks, and webhooks. | Authenticate/MAC before parse; delivery-ID digest mismatch alarms; replay is stable. |
| v0.75.1–v0.76.1 | Complete Entra staged full and delta generations with atomic watermark publication. | Real tenant/test service; repeated entities, removals, partial pages, expired token, and rollback. |
| v0.77.1–v0.80.1 | Close LDAP TLS/escaping/stable IDs/paged generation sync at `v0.77.1`; AD rename/delete/referral/cycle profile at `v0.78.1`; privacy host search at `v0.79.1`; stale/unknown health at `v0.80.1`. | Real supported directory; hostile attributes/referrals/cycles and partial failure. |
| v0.81.1 | Bind every notification to an immutable effect ID and minimal disclosure budget. | Retry/provider ambiguity cannot duplicate semantics or expand PII. |
| v0.83.1–v0.86.1 | Qualify SMTP, Teams, Slack, and SMS independently. | Real service/vendor environment, secret rotation, outage, replay, rate, and redaction evidence per adapter. |
| v0.87.1 | Implement destination-profile HTTP broker with DNS/redirect revalidation and private/control-plane denial. | SSRF corpus: rebinding, CNAME, dual-stack, metadata, loopback, ambiguous IP, proxy, redirect, body/timeout limits. |
| v0.87.2 | Implement signed raw-body webhook profiles and durable replay cache. | RFC 9421 profile vectors, content digest, covered target, nonce, expiry, rotation, replay, and body mutation. |
| v0.91.1 | Add edge enrollment, ownership transfer, inventory identity, revoke, and quarantine. | Wrong tenant/site, stolen/cloned node, stale enrollment, mass revoke, and recovery tests. |
| v0.92.1 | Add signed command envelope with authority epoch, route, expiry, nonce, effect ID, and policy/bundle revision. | Wrong/revoked node, route, epoch, time, signature, replay, and rollback denial. |
| v0.92.2 | Add bounded edge inbox/outbox and effect-result ambiguity model. | Crash at receive/apply/send/ack; replay never duplicates device effect. |
| v0.92.3 | Add signed minimized site package with explicit offline authority and expiry. | Substitution, rollback, stale policy, excessive data, cross-site, and expired-package denial. |
| v0.92.4 | Publish and test edge OS/process hardening, least privilege, firewall, secret, and update baseline. | Assembled supported OS image; service compromise cannot reach unrelated devices/control plane. |
| v0.93.1–v0.97.1 | Close typed printer requests at `v0.93.1`, IPP semantics at `v0.94.1`, ZPL AST/renderer at `v0.95.1`, template bounds at `v0.96.1`, and idempotent spool at `v0.97.1`. | Real claimed printers or official simulators; ambiguous status, duplicate, parser, injection, jam, restart, and reroute tests. |
| v0.98.1 | Add opaque revocable Apple Wallet pass profile with QR fallback. | Real supported Apple devices; expiry/revocation/update/privacy and no-NFC non-claim. |
| v0.98.2 | Add Apple Wallet NFC profile only behind entitlement/certificate/terminal qualification. | Vendor approval plus real compatible terminal/device; cloned/replayed/stale pass tests. |
| v0.98.3 | Add opaque revocable Google Wallet pass profile with QR fallback. | Real supported Android devices; expiry/revocation/update/privacy. |
| v0.98.4 | Add Google Smart Tap only behind certification and compatible terminal qualification. | Certified test path plus real compatible terminal/device and replay/revoke tests. |
| v0.102.1 | Make every issued secret non-exportable where possible and short-lived by policy. | Rotation, revoke, log/crash-dump/cache redaction, and provider ambiguity tests. |
| v0.106.1 | Isolate native/vendor access adapters in a narrow authenticated agent. | Compromised adapter cannot mint grants, widen site/zone/time, or reach control-plane credentials. |
| v0.106.2 | Add turnstile observation/effect contract and destination-only elevator request contract. | Physical/vendor lab; no generic movement API; emergency/manual/failure fallbacks. |
| v0.109.1–v0.109.2 | Add Apple and Android UWB observation profiles separately. | Real supported phones/accessories; consent, capability, ranging error, relay/replay, stale observation, and manual fallback. |
| v0.109.3 | Add privacy-gated LPR observation profile. | Real approved camera/vendor environment; plate minimization, confidence, correction, retention, spoof, and manual fallback. |
| v0.109.4 | Add parking entitlement lifecycle independent of raw plate observation. | Grant/revoke/expiry/reconcile and plate-change tests. |
| v0.110.1 | Add edge/device compromise and checkout-revocation cumulative campaign. | Lost node, cloned key, controller outage, stale grant, ambiguous device state, and eventual reconciled revoke. |

Phase exit: edge authority and checkout revocation survive assembled hardware and
fault campaigns. Optional modalities remain disabled outside their qualified
hardware, privacy, jurisdiction, and accessibility profiles.

## Phases 9–10 — Wasm And User Interfaces (v0.111.x–v0.130.x)

| Stop | Context and sole deliverable | Mandatory proof |
| --- | --- | --- |
| v0.111.1 | Define minimal WIT worlds per plugin class and host-minted unforgeable invocation context. | ABI golden vectors; tenant/capability/purpose/resource claims cannot be forged by a component. |
| v0.112.1 | Isolate the runtime in a dedicated least-privilege process with no control-plane credentials. | Malicious/trapping component and runtime-process compromise encounter an OS boundary. |
| v0.113.1 | Issue invocation-bound opaque handles and minimized typed projections only. | Cross-tenant, enumeration, serialization, expiry, reuse, and upgrade denial. |
| v0.114.1–v0.114.16 | Admit one deny-by-default capability per stop: clock, random, KV, secret use, HTTP profile, directory read, visit projection, notification proposal, print proposal, Wi-Fi proposal, access proposal, blob read, blob write, audit proposal, config read, health report. | For each stop, missing capability is structurally unavailable; scope, purpose, class, quota, and revocation tests pass. |
| v0.115.1 | Reuse the `v0.87.1` egress broker; plugins never receive raw sockets or arbitrary URLs. | Same SSRF corpus plus plugin-specific quota, credential-injection, and response-minimization tests. |
| v0.116.1–v0.117.1 | Close non-exportable secret handles at `v0.116.1`; close memory/table/stack/fuel/deadline/host-call/body/concurrency/log quotas at `v0.117.1`. | Exhaustion, trap cleanup, decompression/parser bomb, cancellation, and noisy-neighbor tests. |
| v0.118.1 | Add signed package manifest, ABI range, SBOM/provenance, signer rotation/revocation, and emergency disable. | Tamper, rollback, stale signer, mixed package, migration, and fleet-revocation tests. |
| v0.120.1 | Run malicious-component and compatibility corpus against every admitted runtime/profile. | Escape, ambient import, forged handle, resource abuse, and N/N-1 ABI cases. |
| v0.122.1 | Harden kiosk sessions: no durable PII, ambient authority, cache/history residue, or cross-user continuation. | Real browsers/kiosk OS; crash/restart/back/timeout/network-loss/shoulder-surfing tests. |
| v0.124.1–v0.125.1 | Make form rendering schema-driven and bounded at `v0.124.1`; make legal rendering revision-pinned, reconstructable, localized, and accessible at `v0.125.1`. | Real-browser E2E, historical artifact reconstruction, hostile content, screen reader, keyboard/switch tests. |
| v0.130.1 | Qualify web surfaces against WCAG 2.2 AA on supported browsers/assistive technology. | Automated and manual report; every failure remediated and retested. |
| v0.130.2 | Qualify physical kiosk reach, privacy, timeouts, audio/visual prompts, QR/manual/touchless alternatives, and staff fallback. | Representative supported hardware and disabled-user review; WCAG report alone cannot close. |

Phase exit: a malicious plugin cannot acquire ambient authority and a public
kiosk cannot retain the previous visitor's data or strand a user without an
accessible/manual path.

## Phases 11–12 — Offline, Emergency, HA, And Advisory AI

| Stop | Context and sole deliverable | Mandatory proof |
| --- | --- | --- |
| v0.131.1 | Define deterministic incident snapshot/delta reducer pinned to authority and policy revisions. | Replay, concurrent check-in/out, stale source, transfer, and headcount model. |
| v0.131.2 | Define isolated muster-station identity and bounded local authority. | Wrong incident/site/station, cloned station, and expired authority denial. |
| v0.133.1 | Add append-only edge journal ordered by authority epoch and sequence with signed segment roots. | Power loss at every write, disk-full reserve, corruption, fork, clone, rotation, and rollback detection. |
| v0.134.1 | Build minimized expiring offline projection from signed site package. | No excess PII, stale/expired denial, bounded cache, key loss, and policy-change behavior. |
| v0.135.1 | Add policy-bounded offline effect intents; no generic offline authorization. | Printer/access/network outages and ambiguous results remain explicit and replay-safe. |
| v0.135.2 | Add offline checkout and emergency revoke queue. | Concurrent central/edge transitions and eventual complete revocation. |
| v0.136.1 | Implement signed, at-least-once, gap-detecting reconciliation and quarantine. | Missing/reordered/duplicated batches, two-edge partition, schema/policy mismatch, and replay. |
| v0.136.2 | Add signed durable acknowledgement watermark; prune only authenticated acknowledged data. | Ack loss/forgery/rollback and crash before/after prune cannot lose unacknowledged facts. |
| v0.136.3 | Run offline model/red-team campaign. | Total WAN loss, clock drift, stale package, cloned key, disk pressure, KMS/TPM loss, corrupted segment, and final muster proof. |
| v0.140.1 | Restore control plane, privacy vault, deletion ledger, edge state, and audit anchors in correct order. | Clean-room restore meets RPO/RTO without resurrecting erased data or accepting rolled-back authority. |
| v0.141.1 | Enforce compile-time dependency rule that authoritative crates cannot depend on AI. | Dependency-graph negative fixture and AI-feature-disabled builds. |
| v0.142.1 | Add classification/DLP/egress budget before any provider call. | Canary PII/secrets, indirect prompt injection, encoded exfiltration, and wrong-region provider denial. |
| v0.143.1 | Add AI interaction disclosure and source/revision evidence. | UI/E2E verifies disclosure before interaction and records provider/model/policy without secret prompts. |
| v0.144.1–v0.149.1 | Qualify each assistant as untrusted draft/proposal only: reception, translation, extraction/OCR, constrained query, configuration, summary. | Malicious output cannot create fact, command, event, policy decision, screening disposition, credential, or effect; human review is attributable. |
| v0.150.1 | Prove disabled-AI parity and run injection/evasion evaluation. | Every authoritative acceptance flow is identical with AI compiled out; red-team corpus closes. |

Phase exit: offline authority is deterministic and cryptographically attributable;
AI is technically unable—not merely instructed—to govern access or evidence.

## Phases 13–14 — Enterprise Policy, Security, And Operations

| Stop | Context and sole deliverable | Mandatory proof |
| --- | --- | --- |
| v0.151.1–v0.153.1 | Close calendar contract, Microsoft Graph staged sync, and hostile iCalendar parsing separately. | Real provider/feed; UID/recurrence/sequence/timezone/cancel/partial-page/replay/size tests. |
| v0.154.1–v0.160.1 | Close deterministic meeting mapping, host approval, groups, recurrence, plus-one, templates, and pre-arrival evidence one per stop. | Calendar input creates proposals only; no visit/credential without policy and host authority. |
| v0.161.1–v0.164.1 | Version EU/EEA at `v0.161.1`, Sweden at `v0.162.1`, UK/Swiss at `v0.163.1`, and North America plus a distinct contractor deployment profile at `v0.164.1`, all with source locks and non-claims. | Qualified review, jurisdiction fixtures, conflict tests, dated sources, and customer-responsibility docs. |
| v0.164.2 | Add typed Controlled Program/Technology Control Plan facts and obligations. | Missing provenance/authorization fails closed; counsel-owned classifications remain external. |
| v0.164.3–v0.164.4 | Add separately reviewed ITAR and EAR technical deployment packs. | Counsel-reviewed source/version, end-use/end-user/destination/license, escort, zone, evidence, and anti-discrimination tests. |
| v0.165.1 | Enforce tenant/site/data-class residency over DB, blob, job, log, connector, AI, backup, and failover paths. | Wrong-region denial and controlled disaster exception evidence. |
| v0.166.1 | Qualify the first real KMS adapter against the early provider contract. | Real service: wrap/unwrap/sign/status/rotation/throttle/outage/permission/cross-tenant tests. |
| v0.167.1 | Qualify HSM/PKCS#11 and TPM/secure edge storage as separate profiles. | Real supported hardware: session/object/HA/PIN/seal/PCR/clone/loss/recovery/no-export tests. |
| v0.168.1 | Enable production PII only with per-tenant/purpose KEKs and per-envelope DEKs. | Cross-tenant blast radius, plaintext-copy inventory, key-use audit, erasure, backup, and migration proof. |
| v0.169.1 | Add online rotation/re-encryption and compromised-key quarantine. | Mixed versions, crash/restart, rollback, old evidence verification, and no silent data loss. |
| v0.171.1 | Add typed `AttributeAssertion`, policy conflicts, `Allow`/`Deny`/`Require`, obligations, and reason codes. | Model/property tests; unknown/missing assertions cannot silently allow. |
| v0.172.1–v0.175.1 | Close dual-controlled export, constrained egress editor, plugin signer revocation, and incident actions one per stop. | Exfiltration, stale signer/node, emergency disable, alert replay, and no alert-to-authority shortcut. |
| v0.176.1 | Ingest immutable authenticated OFAC/BIS/CSL source snapshots with freshness. | Authenticity/digest/delta/rollback/outage; stale snapshot is visible and cannot self-update a local watchlist. |
| v0.176.2 | Add deterministic normalization/candidate matching and benchmark. | Multilingual aliases/dates/IDs plus measured false-positive/negative corpus; no AI authority. |
| v0.176.3 | Add attributable human screening disposition, rescreen, expiry, appeal, and correction. | Potential hit never auto-denies; list change and concurrent review tests. |
| v0.176.4 | Add governed local watchlist lifecycle. | Lawful purpose, source authority, site scope, two-person change, expiry, read audit, and prohibited-attribute tests. |
| v0.177.1 | Add optional identity-verification assertion contract with raw-document/biometric minimization. | Provider can return bounded evidence only; it cannot grant access or become a durable raw-ID store. |
| v0.179.1 | Add independently verifiable remote audit/evidence copy. | Database/site compromise, fork, delayed anchor, rollback, and regional-loss detection. |
| v0.180.1 | Revise threat model and DPIAs for assembled production architecture. | External review covers modern modalities, regulated packs, edge, plugins, AI, abuse, and residual risks. |
| v0.184.1 | Add signed TUF-like fleet metadata, SBOM/provenance, staged channels, and emergency revoke. | Freeze, rollback, mix-and-match, mirror, signer compromise, and stale-edge tests. |
| v0.184.2 | Add A/B atomic edge update and health rollback. | Power loss, disk full, bad binary/config, protocol mismatch; journal and authority survive. |
| v0.185.1–v0.190.1 | Close N/N-1 fleet compatibility, zero-downtime schemas, regional failover, encrypted object/WORM recovery, hands-on disaster runbooks, and scheduled clean-room restore separately. | Mixed fleet, split brain, region/key/object loss, timed operator exercise, RPO/RTO, deletion and audit continuity. |

Phase exit: every optional regulated or hardware pack is disabled outside its
reviewed profile; fleet update and restore are demonstrated, not document-only.

## Phase 15 — Production Qualification (v0.191.x–v1.0.0)

No new feature enters this phase. A feature change returns to its owning phase,
uses the next patch stop, and reruns affected cumulative campaigns.

| Stop | Context and sole deliverable | Mandatory proof |
| --- | --- | --- |
| v0.191.1 | Pin and publish the complete three-database semantic matrix. | Identical black-box histories/results on every supported engine/version/configuration. |
| v0.192.1 | Upgrade from every supported pre-1.0 schema and N/N-1 service/edge version. | Checksummed fixture catalog, interruption, rollback, deletion-ledger preservation. |
| v0.193.1 | Rehearse DB/blob/KMS/audit-anchor disaster and clean-room restore. | Measured RPO/RTO, no PII resurrection, exact evidence continuity. |
| v0.194.1 | Run full boundary chaos plus offline muster red-team. | WAN/DNS/clock/DB/cache/blob/KMS/IdP/connector/device/power faults; no duplicate effects or lost headcount. |
| v0.195.1 | Qualify agreed small/standard/large capacity profiles and 72h+ soak. | Check-in/revoke/muster latency, queue recovery, growth, fairness, and exhaustion evidence. |
| v0.196.1 | Complete manual accessibility/usability review on supported browsers, assistive technology, and kiosk hardware. | WCAG 2.2 AA plus physical reach/privacy/timeout/alternative remediation and retest. |
| v0.197.1 | Complete independent privacy/regulatory review. | Retention/hold/restriction/erasure/restore/processor evidence; LPR/AI/ID DPIAs where applicable. |
| v0.197.2 | Complete export-control/sanctions counsel review of optional packs. | Exact sources/versions, authority boundaries, anti-discrimination, non-claims, and customer responsibility. |
| v0.198.1 | External exact-commit application/API/authn/storage/privacy/plugin pentest and clean retest. | All findings triaged; blockers fixed with regression tests; final report digest recorded. |
| v0.198.2 | External edge/kiosk/hardware/Wasm/offline red-team and clean retest. | Physical kiosk, stolen edge, lateral movement, malicious component/device/protocol/update-chain scope. |
| v0.198.3 | Independent cryptography/key/evidence design and implementation review. | Profiles, canonicalization, key lifecycle, erasure assumptions, signing/timestamp/verifier findings closed. |
| v0.199.1 | Freeze API/event/WIT/config/bundle/storage compatibility and claims. | Golden compatibility suite, support/deprecation policy, every documentation claim linked to proof. |
| v0.200.1+ | Release-blocker fixes only; every fix produces a new exact candidate. | Reproducer/regression, affected campaign rerun, pentest revalidation, reproducible artifacts. |
| v1.0.0 | Promote the unchanged qualified candidate. | Explicit approval; green CI/CodeQL; clean reviews; signed tag/artifacts; rollback, incident, and on-call readiness. |

## v1.0 Acceptance Ledger

GA is blocked until the evidence index identifies exact commands, environments,
artifacts, dates, revisions, and reviewers for every statement:

- A fresh tenant configures site/topology, desk/kiosk identities, purposes,
  fields, documents, a published journey, directory, notifications, edge,
  printer, Wi-Fi, and optional access without direct database edits.
- QR/manual and at least one Wallet path complete on qualified devices. UWB,
  Wallet NFC, and LPR activate only in separately qualified profiles and retain
  accessible/manual alternatives.
- Visitor, contractor, party, and courier/delivery aggregates remain distinct;
  denial cannot become onsite; checkout/expiry reconciles every Gestur-issued
  credential to revoked.
- All external effects are outbox-driven and idempotent; provider or device
  ambiguity is explicit and never guessed successful.
- Total WAN loss preserves bounded check-in, checkout, incident snapshot, and
  muster; signed gap-detecting replay is idempotent and conflict-visible.
- Privacy-vault compromise does not yield keys from visit storage; deny-read,
  scoped key destruction, processor obligations, unlinking, and backup restore
  preserve lawful erasure without overstating cryptographic erase.
- Historical notice, agreement, safety, and signature evidence pins exact
  source/render/journey/policy revisions and verifies after database tampering.
- Legal hold preserves only its approved scope, blocks ordinary use, conflicts
  safely with erasure, and requires attributable dual control to release.
- Directory/calendar/webhook/message replay, partial pages, SSRF, signature
  mutation, outage, and secret rotation cannot duplicate or widen authority.
- A malicious Wasm component cannot obtain an undeclared import, tenant handle,
  raw socket, filesystem, environment, secret, command/event authority, or
  unbounded resource; runtime escape encounters a process/OS boundary.
- AI-disabled parity covers every authoritative journey, credential, privacy,
  emergency, evidence, audit, and administration flow; malicious AI output
  cannot construct or trigger authority.
- All claimed databases, browsers, OSes, devices/vendor simulators, HA,
  migrations, backup/restore, fleet update/rollback, regional failure,
  accessibility, load/soak, chaos, and exact-commit reviews have current proof.

## Current Source Locks

Checked 2026-08-19. These sources justify roadmap inputs, not compliance claims.
Recheck the latest stable revision and errata when the owning stop begins and at
release qualification.

- [WCAG 2.2](https://www.w3.org/TR/WCAG22/) is the current W3C accessibility
  baseline used here and explicitly covers web content on kiosks.
- [NIST SP 800-63-4](https://csrc.nist.gov/pubs/sp/800/63/4/final) is the current
  digital-identity guideline input; Gestur does not claim NIST certification.
- [NIST SP 800-88 Rev. 2](https://csrc.nist.gov/pubs/sp/800/88/r2/final) is the
  current media-sanitization input and does not make cryptographic erasure
  automatic or complete when plaintext/key copies survive.
- [EU AI Act enforcement update](https://digital-strategy.ec.europa.eu/en/news/commission-starts-enforcing-ai-act-rules-and-new-transparency-requirements-2-august)
  confirms the relevant 2 August 2026 enforcement/transparency date; exact
  applicability still requires qualified review.
- [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html),
  [RFC 5545](https://www.rfc-editor.org/rfc/rfc5545),
  [RFC 9421](https://www.rfc-editor.org/rfc/rfc9421), and
  [RFC 3161](https://www.rfc-editor.org/rfc/rfc3161) anchor identity, calendar,
  HTTP-message-signature, and timestamp profiles.
- [Apple Nearby Interaction](https://developer.apple.com/documentation/nearbyinteraction)
  and [Android ranging](https://developer.android.com/develop/connectivity/ranging)
  describe ranging observations and platform/device constraints; neither turns
  proximity into identity or authorization.
- [Google Smart Tap](https://developers.google.com/wallet/smart-tap) documents
  its proprietary NFC protocol and certification/terminal constraints.

The architectural rule is: deterministic versioned facts and policy decide;
immutable journeys declare; transactionally recorded effect intents request;
untrusted edges, plugins, connectors, devices, kiosks, and AI report; and
independently anchored evidence makes tampering detectable under documented
key/anchor assumptions.
