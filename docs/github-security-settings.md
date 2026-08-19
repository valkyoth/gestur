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
5. Tag only the exact commit whose CI and CodeQL run is green.

## Release Tag Settings

Before any release:

1. Require current repository CI on the default branch and block force-pushes.
2. Keep CodeQL default setup enabled and confirm it is green on the exact commit
   to be tagged.
3. Protect `v*` tags from update and deletion where the hosting plan supports
   it; do not use a routine bypass.
4. Keep the `Release Tag Check` workflow enabled for tag pushes. A tag is not a
   release until its record, exact target, and ancestry check succeeds.
