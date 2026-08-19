# Release Runbook

1. Before scheduling the version, reserve the owner's pentest time, tooling,
   environment, scope, retest availability, and contingency window from `v0.10.4`.
2. Confirm vX.Y.Z is declared; fetch full tag history and validate every lower
   declared version as a distinct authorized signed tag in ancestry order.
3. Finish exactly one version. Update its tests, documentation, threat model,
   changelog, release notes, and evidence index. Run all applicable local gates.
4. Commit the completed implementation and report: vX.Y.Z implementation stop
   reached. Run pentest for this HEAD: COMMIT.
5. The owner runs the pentest against that commit:
   - If it finds anything, fix every finding, add regression tests, run the
     affected and full gates, commit a new HEAD, and request another pentest.
   - Repeat until the owner explicitly reports a direct PASS or clean retest.
6. Write `security/pentest/vX.Y.Z.md` with PASS, date, actual green
   `Pentested-Commit`, current `Release-Candidate`, scope, tester, `Retest` as
   `direct-pass` or `clean-retest`, and `Post-Pentest-Changes: none`.
7. Recheck every source lock and governed source set. Refresh signed source and
   applicable feasibility records against the release-candidate parent.
8. Rerun `scripts/checks.sh`, cargo deny, cargo audit, SBOM verification,
   version-specific real tests, and live Rust/tool/action freshness checks.
9. Create the evidence commit containing the pentest record and authorized
   source/feasibility evidence. Run
   `scripts/validate-release-readiness.sh vX.Y.Z`.
10. Wait for GitHub CI and CodeQL default setup on that commit:
    - If both are green, continue.
    - If CodeQL finds an issue, fix it, add a regression test, and rerun all
      applicable local gates. Update the pentest record so `Pentested-Commit`
      still names the last green pentest and `Post-Pentest-Changes` begins
      `CodeQL: ` with the exact remediation. Refresh candidate-bound review
      evidence, commit it, and wait for CI/CodeQL again. Repeat until green.
11. Only after CI and CodeQL are green, create the authorized signed tag on the
    current commit. Push it only on explicit maintainer instruction, then require
    the `Signed Release Tag Check` to validate its signer, target, evidence, and
    ancestry before treating it as a release.

A CodeQL remediation does not silently become part of the prior pentest claim:
the report preserves the commit actually pentested and records the later delta.
The owner may request another pentest whenever the fix warrants it; if so, the
new green commit becomes `Pentested-Commit` and post-pentest changes reset to
`none`.

No step publishes a Cargo package. An unresolved finding, absent owner PASS,
failed local test, stale source/tool, unavailable pentest, undeclared release,
broken tag history, unrecorded post-pentest code change, non-green CI/CodeQL, or
failed tag check blocks release.
