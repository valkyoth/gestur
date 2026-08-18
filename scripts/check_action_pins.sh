#!/usr/bin/env sh
set -eu

found=0
while IFS= read -r line; do
    found=1
    case "$line" in
        *uses:\ actions/checkout@[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]*'# v'[0-9]*) ;;
        *)
            echo "actions/checkout must use a full SHA and version annotation: $line" >&2
            exit 1
            ;;
    esac
done <<EOF
$(grep -R 'uses: actions/checkout@' .github/workflows)
EOF

test "$found" -eq 1

if grep -R '^[[:space:]]*uses:' .github/workflows |
    grep -vE 'uses: [A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@[0-9a-f]{40}([[:space:]]|$)' >/dev/null; then
    echo "every GitHub Action must be pinned by a full commit SHA" >&2
    exit 1
fi
