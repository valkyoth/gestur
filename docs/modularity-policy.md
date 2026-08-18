# Modularity Policy

Gestur uses crates to enforce responsibility and dependency direction, and
modules to keep each implementation cohesive. Crate count is not a goal by
itself.

## Hard Rules

- No normal Rust, Python, or shell source file may exceed 500 lines.
- Split a file before it reaches the hard limit; do not compress readability
  to satisfy the counter.
- Portable domain crates cannot import infrastructure crates.
- Infrastructure adapters implement Gestur-owned contracts and cannot expose
  third-party types across the boundary.
- The gestur facade composes stable domain crates and does not absorb their
  implementations.
- A generated file needs identified input, generator version, reproducibility
  checks, and an explicit exception from the normal source-size policy.

scripts/validate-modularity-policy.sh enforces the current crate set, no_std
attributes, unsafe prohibition, and code-file size limit.
