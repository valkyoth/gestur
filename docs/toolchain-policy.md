# Toolchain Policy

The repository pins Rust 1.97.1 exactly in rust-toolchain.toml. The pin follows
the latest stable release rather than serving as a long-lived MSRV.

## Update Process

At least weekly and before every release:

1. Run scripts/check_latest_tools.sh.
2. Verify the latest stable Rust from the official stable-channel manifest and
   Rust release announcement.
3. Update the exact Rust pin, workspace rust-version, CI tools, and action SHA
   annotations together.
4. Read release notes for language, compiler, Cargo, rustfmt, Clippy, and tool
   behavior changes.
5. Run the complete workspace gate and all available platform checks.
6. Record fixes and changed behavior in CHANGELOG.md and release notes.
7. Re-run the pentest scope if toolchain behavior affects generated code,
   linking, parsers, unsafe boundaries, dependencies, or release artifacts.

The current pinned support tools are cargo-deny 0.20.2, cargo-audit 0.22.2,
cargo-sbom 0.10.0, and actions/checkout v7.0.1 at its reviewed full commit SHA.
The scheduled Monday CI freshness job detects drift. The live freshness script
is authoritative at release time.
