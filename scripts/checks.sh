#!/usr/bin/env sh
set -eu

cargo fmt --all --check
scripts/check_shell_syntax.sh
scripts/check_doc_links.sh
scripts/check_release_plan.sh
python3 scripts/test_validate_detailed_version_plan.py
python3 scripts/test_validate_release_evidence.py
python3 scripts/test_release_trust_policy.py
python3 scripts/test_release_signature_integration.py
scripts/check_action_pins.sh
scripts/validate-workspace-policy.py
scripts/validate-modularity-policy.sh
scripts/validate-security-policy.sh
scripts/validate-test-policy.sh
scripts/validate-release-metadata.sh
cargo check --workspace --all-targets --all-features --locked
cargo clippy --workspace --all-targets --all-features --locked -- -D warnings
cargo test --workspace --all-features --locked
