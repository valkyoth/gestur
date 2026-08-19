#!/usr/bin/env sh
set -eu

tag="${1:-}"
case "$tag" in
    v[0-9]*.[0-9]*.[0-9]*) ;;
    *)
        echo "usage: scripts/validate-release-readiness.sh vX.Y.Z" >&2
        exit 2
        ;;
esac

version="${tag#v}"
notes="release-notes/RELEASE_NOTES_${version}.md"
candidate="$(git rev-parse HEAD^)"

test ! -f PENTEST.md
test -f "$notes"
test -s sbom/gestur.spdx.json
scripts/generate-sbom.sh --check
python3 scripts/validate_detailed_version_plan.py \
    --release "$tag" \
    --candidate "$candidate" \
    --repository .

if git rev-parse -q --verify "refs/tags/$tag" >/dev/null; then
    echo "tag already exists locally: $tag" >&2
    exit 1
fi
