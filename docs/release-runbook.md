# Release Runbook

1. Before scheduling the version, reserve the independent pentest provider,
   necessary specialists, approved budget, lead time, clean-retest window, and
   contingency capacity recorded by `v0.10.4`. Missing capacity blocks work.
2. Confirm vX.Y.Z is a declared base, declared stop, or `v1.0.0`; fetch the full
   tag history and verify every lower declared version is a distinct signed
   annotated tag in strict ancestor order from an authorized tag-role key.
3. Confirm reviewer, external-pentester, and tag-signer identities are distinct,
   valid, and present in exactly one candidate registry. Calculate the candidate
   digest with `python3 scripts/release_trust_policy.py CANDIDATE` and match it
   to the protected `GESTUR_RELEASE_TRUST_POLICY_SHA256` value. Follow
   [release trust governance](release-trust-governance.md) for every change.
4. Finish exactly one version's bounded deliverables. Update tests,
   documentation, threat model, changelog, release notes, and evidence index.
5. Run scripts/checks.sh, cargo deny check, cargo audit, SBOM verification,
   version-specific tests, and live Rust/tool/action freshness checks.
6. Freeze this commit as the candidate and report: vX.Y.Z implementation stop
   reached. Run pentest for this exact commit.
7. Record temporary findings only in ignored root PENTEST.md. Fix every finding,
   add regression tests, and repeat steps 4–6 with a new candidate until the
   independent clean retest passes.
8. Recheck every source lock and governed source set against primary sources.
   Record changed-source analysis under `evidence/source-freshness/reviews/`.
9. Write `evidence/source-freshness/vX.Y.Z.md` with PASS status, date, exact
   candidate, source-lock digest, reviewer identity/key fingerprint, support
   path/digest, and detached signature made by that key. The identity/key pair
   must be uniquely authorized by the externally pinned reviewer registry.
10. From `v0.10.2`, do the same for each decided feasibility record. Declare the
   complete reviewed scope; a consuming release must include its boundary crate.
   Any scoped change after `Reviewed-Commit` requires a new review and signature.
11. Have the independent provider create `security/pentest/vX.Y.Z.md` as a
    signed attestation naming PASS status, exact candidate, date, scope, tester
    identity/key, provider report path/digest, support path/digest, and detached
    signature. The key must exist only in the external-pentester registry.
12. Create exactly one child evidence commit containing only the signed pentest
    attestation/report/support set and the authorized source/feasibility records,
    support files, and signatures. Do not change code, plans, or release notes.
13. Run `scripts/validate-release-readiness.sh vX.Y.Z`. It binds evidence to the
    parent candidate, validates signatures/digests/scopes, and rechecks the
    declared signed predecessor chain.
14. Confirm GitHub CI and CodeQL default setup are green.
15. Create and push a signed tag on the evidence commit only after explicit
    maintainer instruction. Do not announce or use it until the protected
    `Signed Release Tag Check` verifies its authorized fingerprint, exact target,
    evidence, and ancestry. A failed check is a security incident, not a release.

No step publishes a Cargo package. A failed check, unresolved finding, missing
or self-asserted evidence, stale source or tool, unavailable pentest capacity,
undeclared version, broken tag ancestry, unauthorized evidence-commit change,
ambiguous reviewed commit, missing external policy pin, role reuse, unsigned
pentest evidence, unauthorized tag signer, or failed post-tag check fails closed.
