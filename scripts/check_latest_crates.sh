#!/usr/bin/env sh
set -eu

scripts/validate-workspace-policy.py
echo "no third-party crates are admitted; direct crate freshness set is empty"
