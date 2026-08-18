# Unsafe Rust Policy

Unsafe Rust is forbidden throughout the current workspace.

If a future operating-system, cryptographic, FFI, or performance boundary
cannot be implemented safely, it requires a dedicated boundary crate and a
separate release milestone. Admission must document the exact invariant,
minimal unsafe block, safe public wrapper, platform assumptions, provenance,
Miri/sanitizer or equivalent evidence, fuzzing, code review, independent audit,
and removal alternative.

Unsafe code may never be introduced into a portable domain crate, hidden in
generated code, or admitted solely to improve benchmark results.
