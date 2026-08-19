# Release Runbook

1. Before scheduling the version, reserve the independent pentest provider,
   necessary specialists, approved budget, lead time, clean-retest window, and
   contingency capacity recorded by `v0.10.4`. Missing capacity blocks work.
2. Confirm vX.Y.Z is a declared base, declared stop, or `v1.0.0`; fetch the full
   tag history and verify every lower declared version is a distinct signed
   annotated tag in strict ancestor order.
3. Finish exactly one version's bounded deliverables. Update tests,
   documentation, threat model, changelog, release notes, and evidence index.
4. Run scripts/checks.sh, cargo deny check, cargo audit, SBOM verification,
   version-specific tests, and live Rust/tool/action freshness checks.
5. Freeze this commit as the candidate and report: vX.Y.Z implementation stop
   reached. Run pentest for this exact commit.
6. Record temporary findings only in ignored root PENTEST.md. Fix every finding,
   add regression tests, and repeat steps 3–5 with a new candidate until the
   independent clean retest passes.
7. Recheck every source lock and governed source set against primary sources.
   Record changed-source analysis under `evidence/source-freshness/reviews/`.
8. Write `evidence/source-freshness/vX.Y.Z.md` with PASS status, date, exact
   candidate, source-lock digest, reviewer identity/key fingerprint, support
   path/digest, and detached signature made by that key. The identity/key pair
   must be uniquely authorized in the candidate's reviewer registry.
9. From `v0.10.2`, do the same for each decided feasibility record. Declare the
   complete reviewed scope; a consuming release must include its boundary crate.
   Any scoped change after `Reviewed-Commit` requires a new review and signature.
10. Create exactly one child evidence commit containing only the permanent
    pentest report and the authorized source/feasibility records, support files,
    and detached signatures. Do not change code, plans, or release notes there.
11. Run `scripts/validate-release-readiness.sh vX.Y.Z`. It binds evidence to the
    parent candidate, validates signatures/digests/scopes, and rechecks the
    declared signed predecessor chain.
12. Confirm GitHub CI and CodeQL default setup are green.
13. Create and push a signed tag on the evidence commit only after explicit
    maintainer instruction.

No step publishes a Cargo package. A failed check, unresolved finding, missing
or self-asserted evidence, stale source or tool, unavailable pentest capacity,
undeclared version, broken tag ancestry, unauthorized evidence-commit change,
or ambiguous reviewed commit fails closed.
