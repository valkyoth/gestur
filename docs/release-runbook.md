# Release Runbook

1. Before scheduling the version, reserve the independent pentest provider,
   necessary specialists, approved budget, lead time, clean-retest window, and
   contingency capacity recorded by the `v0.10.4` operating plan. Missing
   capacity blocks scheduling and never waives a pentest.
2. Finish exactly one version's bounded deliverables.
3. Update tests, documentation, threat model, changelog, and release notes.
4. Recheck every source lock against its primary source. Update changed or
   expired revisions, obtain qualified review where needed, and write the
   seven-day release attestation at `evidence/source-freshness/vX.Y.Z.md` using
   the validator's exact source-lock digest.
5. Run scripts/checks.sh, cargo deny check, cargo audit, SBOM verification, and
   the version-specific gate.
6. Run live Rust/tool/action freshness checks and the release-time boundary
   feasibility check. From `v0.10.2`, decisions need reviewed evidence; a
   consuming adapter requires its boundary to be qualified.
7. Stop and report: vX.Y.Z implementation stop reached. Run pentest for this
   exact commit.
8. The maintainer records temporary findings in root PENTEST.md.
9. Fix every finding, add regression tests, update evidence, delete PENTEST.md,
   and repeat all gates.
10. After a clean independent retest, add security/pentest/vX.Y.Z.md with the
   exact reviewed commit, date, tester, scope, and PASS status.
11. Confirm GitHub CI and CodeQL default setup are green.
12. Create and push a signed tag only after explicit maintainer instruction.

No step publishes a Cargo package. A failed check, unresolved finding, missing
evidence, stale source or tool, unavailable pentest capacity, dirty release
metadata, or ambiguous reviewed commit fails closed.
