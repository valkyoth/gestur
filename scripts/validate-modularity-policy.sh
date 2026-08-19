#!/usr/bin/env sh
set -eu

python3 scripts/validate_modularity_policy.py
test -f docs/modularity-policy.md
