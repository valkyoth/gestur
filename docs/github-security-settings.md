# GitHub Security Settings

GitHub CodeQL default setup is required for the public repository.

This project intentionally has no advanced CodeQL workflow. Default and
advanced setups for the same language can produce duplicate analysis and
maintenance ambiguity.

Before a release tag:

1. Confirm CodeQL default setup is active on the default branch.
2. Confirm private vulnerability reporting is enabled.
3. Confirm branch protection requires current CI.
4. Confirm the exact release commit has a successful CodeQL analysis.
5. Record the check in the pentest digest.

## Release Trust Settings

Before any release, configure and retain evidence for all of these external
controls:

1. An active default-branch ruleset requiring pull requests, two distinct
   approvals, code-owner review, dismissed stale approvals, approval of the
   newest push, required CI, signed commits, blocked force-push/deletion, and no
   routine bypass. Protect `security/*reviewers.txt`,
   `security/release-tag-signers.txt`, `security/release-trust-keyring.asc`,
   `.github/workflows/release-tag.yml`, `.github/CODEOWNERS`, and release trust
   policy documentation.
2. A `release-trust` environment with required review, prevent self-review,
   administrator bypass disabled, and deployment limited to protected `v*`
   tags. Store `GESTUR_RELEASE_TRUST_POLICY_SHA256` as an environment variable.
3. An active `v*` tag ruleset restricting creation, update, deletion, and
   bypass. Only designated release actors may create a tag.
4. The `Signed Release Tag Check` workflow enabled for tag pushes. A tag is not
   approved release evidence until this check succeeds.

CODEOWNERS alone does not meet the two-person requirement. If any hosting-plan
feature is unavailable, an equivalently independent protected control is
required; otherwise release remains blocked.
