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
