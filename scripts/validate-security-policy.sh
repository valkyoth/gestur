#!/usr/bin/env sh
set -eu

grep -q 'unknown-git = "deny"' deny.toml
grep -q 'unknown-registry = "deny"' deny.toml
grep -q 'allow-registry = \[\]' deny.toml
grep -q 'allow-git = \[\]' deny.toml
grep -q 'panic = "abort"' Cargo.toml
grep -q 'unsafe_code = "forbid"' Cargo.toml
grep -q 'CodeQL default setup' SECURITY.md
grep -q 'AI may propose but cannot' SECURITY.md
test -f docs/threat-model.md
test -f docs/security-controls.md
test -f docs/supply-chain-security.md
test -f docs/unsafe-policy.md
test -f docs/github-security-settings.md
test ! -f PENTEST.md
