# Platform Support

## Day-One Posture

| Platform | Gate | Current claim |
| --- | --- | --- |
| Linux | Host build, lint, and tests | Development supported |
| Windows | Host workspace tests in CI | Development supported |
| macOS | Host workspace tests in CI | Development supported |
| BSD | x86_64 FreeBSD cross-check | Portable core compile target |
| Android | AArch64 Android cross-check | Portable core compile target |
| iOS | AArch64 iOS cross-check on macOS | Portable core compile target |
| Aesynx | Architecture review only | Prepared, not supported yet |

Cross-compilation proves source portability, not runtime integration. A
production platform claim additionally requires platform-native tests,
packaging, upgrade/rollback, filesystem, clock, entropy, certificate-store,
network, accessibility, and operational evidence.

Aesynx support must not require weakening the no_std core or embedding
Unix/Windows assumptions into domain crates. When Aesynx publishes a stable
target and runtime contract, add a dedicated host adapter and conformance gate.
