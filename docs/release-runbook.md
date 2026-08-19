# Release Runbook

1. Confirm `vX.Y.Z` is declared, every lower declared version has a distinct
   annotated ancestor tag, and no target tag already exists.
2. Finish exactly one version. Update its implementation, tests, documentation,
   threat model, changelog, and release notes. Run all applicable local gates.
3. Commit the completed implementation and report: `vX.Y.Z implementation stop
   reached. Run pentest for this exact commit: COMMIT`.
4. The owner runs the pentest against that commit:
   - If it finds anything, fix every finding, add regression tests, run affected
     and full gates, commit a new HEAD, and request another pentest.
   - Repeat until the owner explicitly reports a direct PASS or clean retest.
5. Write `security/pentest/vX.Y.Z.md` with `Status: PASS`, ISO `Date`, the actual
   green `Pentested-Commit`, `Scope`, `Retest` as `direct-pass` or
   `clean-retest`, and `Findings-Resolved`. A direct pass uses `none`; a clean
   retest names the fixed findings.
6. Set `CodeQL-Finding`, `CodeQL-Changed-Paths`, and `Regression-Tests` to
   `none`, run `scripts/release_X_Y_gate.sh`, and record `Full-Gate: PASS`.
7. Update only release-status documentation, commit the permanent pentest
   record and status changes, and wait for GitHub CI and CodeQL default setup.
8. If CI and CodeQL are green, the exact commit is tag-ready.
9. If CodeQL finds an issue, fix it and add a regression test. Update the
   pentest record with the CodeQL finding, exact sorted changed paths since the
   green pentested commit, and changed regression-test paths. Rerun all local
   gates, retain `Full-Gate: PASS`, commit, and wait for CI/CodeQL again.
10. Repeat step 9 until CI and CodeQL are green. Do not require a new pentest
    solely because CodeQL produced the documented fix; the owner may still
    request one when the change warrants it.
11. Create an annotated `vX.Y.Z` tag on that exact green commit. Do not change
    code, evidence, or documentation between the green run and the tag. The
    owner pushes; tag-triggered CI validates the record, target, and ancestry.

No step publishes a Cargo package. An unresolved finding, absent owner PASS,
failed local test, stale source/tool, unavailable pentest, undeclared release,
broken tag history, unrecorded post-pentest code, non-green CI/CodeQL, or failed
tag check blocks release.
