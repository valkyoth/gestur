#!/usr/bin/env sh
set -eu

test -f docs/testing-policy.md
test -f crates/gestur/tests/foundation_integration.rs

for source in crates/*/src/lib.rs; do
    if ! grep -q '^#\[cfg(test)\]$' "$source"; then
        echo "crate source has no colocated unit-test module: $source" >&2
        exit 1
    fi
done

grep -q '^## Absolute Rule$' docs/testing-policy.md
grep -q '^### Layer 2 — Integration And Boundary Tests$' docs/testing-policy.md
grep -q '^### Layer 3 — Real Implementation And Acceptance Tests$' docs/testing-policy.md
grep -q '^## No Waiver For Claimed Behavior$' docs/testing-policy.md
grep -q 'scripts/validate-test-policy.sh' scripts/checks.sh
grep -q 'scripts/test_validate_detailed_version_plan.py' scripts/checks.sh
grep -q 'scripts/test_validate_release_evidence.py' scripts/checks.sh
grep -q 'scripts/test_release_trust_policy.py' scripts/checks.sh
grep -q 'scripts/test_release_signature_integration.py' scripts/checks.sh
grep -q 'scripts/validate-tagged-release.sh' .github/workflows/release-tag.yml
grep -q 'Testing policy' README.md
grep -q 'Real-system / acceptance tests' .github/PULL_REQUEST_TEMPLATE.md
