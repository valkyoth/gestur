#!/usr/bin/env sh
set -eu

rust_manifest="${RUST_STABLE_MANIFEST_URL:-https://static.rust-lang.org/dist/channel-rust-stable.toml}"
pinned_rust="$(sed -n 's/^channel = "\([0-9][0-9.]*\)"$/\1/p' rust-toolchain.toml)"
latest_rust="$(curl -fsSL "$rust_manifest" | sed -n '/^\[pkg\.rust\]$/,/^\[/ { s/^version = "\([0-9][0-9.]*\) .*/\1/p; }' | head -n 1)"
test -n "$pinned_rust"
test -n "$latest_rust"
if [ "$pinned_rust" != "$latest_rust" ]; then
    echo "Rust pin is stale: pinned $pinned_rust, latest $latest_rust" >&2
    exit 1
fi

check_tool() {
    name="$1"
    pinned="$2"
    latest="$(CARGO_TERM_COLOR=never cargo info "$name" | sed -n 's/^version: //p' | head -n 1)"
    test -n "$latest"
    if [ "$pinned" != "$latest" ]; then
        echo "$name pin is stale: pinned $pinned, latest $latest" >&2
        exit 1
    fi
}

check_tool cargo-deny 0.20.2
check_tool cargo-audit 0.22.2
check_tool cargo-sbom 0.10.0

latest_checkout_tag="$(git ls-remote --tags --refs https://github.com/actions/checkout.git 'refs/tags/v*' | sed 's#.*refs/tags/##' | grep -E '^v[0-9]+(\.[0-9]+)*$' | sort -V | tail -n 1)"
latest_checkout_sha="$(git ls-remote --tags --refs https://github.com/actions/checkout.git "refs/tags/$latest_checkout_tag" | awk '{ print $1 }')"
test -n "$latest_checkout_tag"
test -n "$latest_checkout_sha"
if ! grep -Rq "actions/checkout@$latest_checkout_sha # $latest_checkout_tag" .github/workflows; then
    echo "actions/checkout pin is not latest $latest_checkout_tag ($latest_checkout_sha)" >&2
    exit 1
fi

scripts/check_action_pins.sh
scripts/check_latest_crates.sh
echo "Rust and repository tooling pins are current"
