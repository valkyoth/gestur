#!/usr/bin/env sh
set -eu

violations="$(
    find crates scripts \
        -type f \
        \( -name '*.rs' -o -name '*.py' -o -name '*.sh' \) \
        -exec wc -l {} \; |
        awk '$1 > 500 { print }'
)"
if [ -n "$violations" ]; then
    echo "code files exceed the 500-line hard limit:" >&2
    echo "$violations" >&2
    exit 1
fi

for source in crates/*/src/lib.rs; do
    grep -q '^#!\[no_std\]$' "$source"
    grep -q '^#!\[forbid(unsafe_code)\]$' "$source"
done

for crate in gestur gestur-core gestur-schema gestur-workflow gestur-policy gestur-events gestur-api-types gestur-crypto-types gestur-testkit; do
    test -f "crates/$crate/Cargo.toml"
done

test -f docs/modularity-policy.md
