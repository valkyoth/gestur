# Release Trust Governance

Status: fail-closed bootstrap policy; no release identity is authorized yet.

## Trust Boundary

Git content can describe release identities but cannot authorize itself. Gestur
separates three OpenPGP roles:

- `security/release-reviewers.txt` signs source and feasibility review records;
- `security/external-pentesters.txt` signs independent pentest attestations;
- `security/release-tag-signers.txt` signs annotated release tags.

One fingerprint or identity must not cross roles. The validator hashes the exact
candidate versions of all three registries with domain and length separation.
Every release compares that digest with the externally stored
`GESTUR_RELEASE_TRUST_POLICY_SHA256`. Missing, malformed, stale, or mismatched
external state blocks release.

`security/release-trust-keyring.asc` contains public verification keys only.
Adding an unlisted key grants no authority because verification also requires an
exact role-registry match. Secret keys and passphrases never enter the repository
or GitHub Actions.

## Bootstrap And Change Procedure

1. Nominate distinct real people for the needed roles and verify their key
   fingerprints through an independent channel.
2. Add public keys and exact identity/fingerprint registry entries in one pull
   request. Record the reason, effective releases, expiry/rotation plan, and
   independent fingerprint-verification evidence.
3. Require two distinct approving reviewers for registry, keyring, workflow,
   CODEOWNERS, and this policy. The author cannot approve. Dismiss stale reviews
   and require approval of the most recent reviewable push.
4. After merge, a different security administrator calculates the merged
   candidate digest with `python3 scripts/release_trust_policy.py REVISION` and
   updates the `release-trust` environment variable. Retain the audit record.
5. Configure that environment with a required reviewer, prevent self-review,
   and disallow administrator bypass. Restrict it to protected release tags.
6. Configure an active tag ruleset for `v*`: restrict creation to designated
   release actors, block update/deletion/force-push, and require the repository's
   normal protected checks where GitHub permits them. No bypass actor is routine.
7. Treat the tag-triggered `Signed Release Tag Check` as mandatory release
   evidence. A pushed tag is not a release until this check succeeds.

GitHub CODEOWNERS requests the right review but cannot provide two-person
authorization on its own. The repository ruleset, protected environment, and
external digest are mandatory controls. If the hosting plan cannot enforce
them, use an equivalently protected external policy/check service or keep
releases blocked.

## Rotation And Incident Handling

- Add a replacement key and update the external digest before first use.
- Retain historical authorized tag fingerprints while supported predecessor
  tags depend on them; removal requires an explicit history-verification design.
- Remove compromised reviewer or pentester authority immediately, rotate the
  external pin, and invalidate affected unsigned/untrusted evidence.
- A compromised tag key triggers the security incident process. Freeze release
  activity, preserve refs and logs, assess every affected tag, and publish a
  signed incident decision before resuming. Never silently retarget a tag.

The relevant platform controls are documented by GitHub under
[rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets),
[available rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets),
and [deployment environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments).
