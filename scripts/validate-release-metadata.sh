#!/usr/bin/env sh
set -eu

test ! -f PENTEST.md
test -f LICENSE
test -f SECURITY.md
test -f CHANGELOG.md
test -f release-notes/RELEASE_NOTES_0.1.0.md
test -f docs/IMPLEMENTATION_PLAN.md
test -f docs/RELEASE_PLAN.md
test -f docs/CRATE_PLAN.md
test -f docs/PRODUCT_VISION.md
test -f .github/workflows/release.yml
grep -q '^version = "0.1.0"$' Cargo.toml
grep -q '^channel = "1.97.1"$' rust-toolchain.toml
grep -q '^rust-version = "1.97.1"$' Cargo.toml
grep -q '^  workflow_dispatch:$' .github/workflows/release.yml
! grep -q 'cargo publish' .github/workflows/release.yml
! grep -q 'CARGO_REGISTRY_TOKEN' .github/workflows/release.yml
scripts/validate-workspace-policy.py
