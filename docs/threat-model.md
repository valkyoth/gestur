# Gestur Threat Model

Status: v0.1.0 foundation; update whenever assets, trust boundaries, or
deployment behavior change.

## Security Objectives

Gestur must preserve tenant isolation, visitor privacy, authorized physical
presence, correct credential lifecycles, availability of safe reception and
emergency functions, attributable actions, verifiable evidence, and integrity
of software and configuration releases.

Safety takes precedence over convenience. A degraded service may refuse a new
credential while still preserving emergency occupancy and controlled checkout.

## Protected Assets

- Visitor and host identities, identifiers, contact data, photos, documents,
  accessibility data, and custom form values.
- Visit state, current occupancy, escort state, approvals, and emergency muster.
- Badge, Wi-Fi, parking, locker, and physical-access credentials.
- Authentication factors, sessions, workload identities, connector secrets,
  encryption keys, signing keys, and invitation capabilities.
- Published journeys, policies, forms, notices, agreements, retention rules,
  compliance packs, and site configuration.
- Append-only audit events, legal evidence, deletion receipts, signed roots,
  backups, and release evidence.
- Availability of reception, checkout, revocation, and emergency operations.
- Repository, CI, toolchain, dependencies, artifacts, and update channels.

## Adversaries

- A malicious or curious visitor with physical kiosk access.
- A leaked, replayed, altered, or enumerated invitation token.
- A hostile browser input, document, webhook, calendar item, directory record,
  connector response, printer response, or AI prompt.
- A compromised kiosk, printer, access controller, Wi-Fi controller, edge node,
  connector, plugin, administrator, receptionist, host account, or CI account.
- An insider abusing search, export, break-glass, retention, or configuration.
- A database or backup operator altering or exfiltrating records.
- A tenant attempting to cross tenant/site boundaries.
- A network attacker controlling DNS, routes, proxies, TLS termination, or WAN
  availability.
- A dependency, toolchain, action, build environment, or release-channel
  supply-chain attacker.
- A repository committer fabricating review/pentest fields, self-authorizing a
  signer, or pushing a validly signed tag from an unapproved key or wrong commit.
- Resource-exhaustion attempts through forms, workflows, files, searches,
  notifications, retries, plugin execution, or offline replay.

## Trust Boundaries

- Public guest browser to guest API.
- Reception/admin browser to authenticated API.
- Identity provider to principal/session establishment.
- Tenant/site scope to every query, command, cache key, event, and job.
- Domain commands to authoritative storage transactions.
- Database, cache, blob store, and backup media to application-held integrity
  and confidentiality controls.
- Central control plane to edge through outbound mutually authenticated sync.
- Edge to printers, Wi-Fi controllers, and physical-access systems.
- Application to connector/plugin capability broker.
- Outbound webhook/HTTP request to DNS and remote networks.
- AI gateway to model provider and untrusted prompt content.
- Build source to CI, artifact, tag, update, and deployment.
- Candidate-controlled release registries to the protected external policy pin,
  independent evidence signers, tag ruleset, and post-tag verification job.

## Baseline Mitigations

- Typed tenant/site/actor/request context for security-sensitive commands.
- Fail-closed named capabilities instead of generic plugin/network power.
- no_std domain logic, forbidden unsafe code, bounded inputs, and strict lints.
- Opaque expiring invitation capabilities with audience and replay protection
  when invitation work lands.
- Privacy-preserving host discovery and enumeration resistance.
- Separation of PII, visit history, diagnostic logs, legal evidence, and audit.
- Application-generated identifiers and explicit event sequences.
- Transactional outbox/inbox and idempotency for external effects.
- Automatic credential expiry/revocation and reconciliation.
- Webhook destination validation against SSRF and replay.
- Plugin denial of network/filesystem/environment access by default.
- AI has no direct high-impact authority and receives typed tools only.
- Tamper-evident audit roots replicated outside the mutable database.
- Encrypted, bounded offline journals and explicit degraded-mode policy.
- Exact tool/action pins, locked builds, source denial, SBOM, CI, CodeQL,
  independent pentest, and signed release evidence.
- Role-separated externally pinned release identities, digest-bound provider
  evidence, authorized tag fingerprints, and current-tag target validation.

## Foundation Residual Risk

Version 0.1.0 contains types and policy gates only. It does not implement
authentication, cryptography, storage, networking, retention, audit integrity,
connectors, offline operation, user interfaces, or production hardening.
no_std, zero dependencies, tests, and file-size limits reduce some risks but do
not prove correctness or security.

## Required Future Abuse Tests

- Cross-tenant and cross-site object substitution.
- Host-directory enumeration and timing.
- Token replay, fixation, race, expiry, and audience mismatch.
- Duplicate check-in, badge, Wi-Fi, access, webhook, and offline events.
- Denied-to-onsite and checked-out-with-live-credential invariants.
- Legal-hold versus erasure races.
- Audit gap, reorder, truncation, and independent-root mismatch.
- SSRF through redirects, DNS rebinding, alternate IP encodings, and proxies.
- Plugin escape, excessive fuel/memory/time, and capability confusion.
- Prompt injection, data exfiltration, tool confusion, and AI-disabled parity.
- Database/Valkey/object-store/WAN/printer/controller partial failures.
- Upgrade, migration, backup, restore, and rollback under fault injection.
- Registry self-authorization, role/key reuse, forged or mutated pentest
  evidence, unauthorized valid tag keys, and tags targeting non-evidence commits.
