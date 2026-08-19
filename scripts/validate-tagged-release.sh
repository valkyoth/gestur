#!/usr/bin/env sh
set -eu

tag="${1:-}"
case "$tag" in
    v[0-9]*.[0-9]*.[0-9]*) ;;
    *)
        echo "usage: scripts/validate-tagged-release.sh vX.Y.Z" >&2
        exit 2
        ;;
esac

target="$(git rev-parse "refs/tags/${tag}^{commit}")"
candidate="$(git rev-parse "${target}^")"
test "$(git rev-parse HEAD)" = "$target"

python3 scripts/validate_detailed_version_plan.py \
    --release "$tag" \
    --candidate "$candidate" \
    --repository . \
    --tagged-release
