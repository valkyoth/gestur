# Release Runbook

1. Finish exactly one version's bounded deliverables.
2. Update tests, documentation, threat model, changelog, and release notes.
3. Run scripts/checks.sh, cargo deny check, cargo audit, SBOM verification, and
   the version-specific gate.
4. Run live Rust/tool/action freshness checks.
5. Stop and report: vX.Y.Z implementation stop reached. Run pentest for this
   exact commit.
6. The maintainer records temporary findings in root PENTEST.md.
7. Fix every finding, add regression tests, update evidence, delete PENTEST.md,
   and repeat all gates.
8. After a clean independent retest, add security/pentest/vX.Y.Z.md with the
   exact reviewed commit, date, tester, scope, and PASS status.
9. Confirm GitHub CI and CodeQL default setup are green.
10. Create and push a signed tag only after explicit maintainer instruction.

No step publishes a Cargo package. A failed check, unresolved finding, missing
evidence, stale tool, dirty release metadata, or ambiguous reviewed commit
fails closed.
