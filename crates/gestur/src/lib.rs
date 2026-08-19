//! Gestur's stable facade over focused internal crates.
//!
//! The current 0.1.0 surface is a repository foundation, not a deployable
//! visitor-management system.

#![no_std]
#![forbid(unsafe_code)]

/// Transport-neutral API types.
pub use gestur_api_types as api_types;
/// Shared domain primitives.
pub use gestur_core as core;
/// Cryptographic metadata without cryptographic implementations.
pub use gestur_crypto_types as crypto_types;
/// Authoritative event-envelope types.
pub use gestur_events as events;
/// Authorization and connector-capability types.
pub use gestur_policy as policy;
/// Privacy-aware field schemas.
pub use gestur_schema as schema;
/// Declarative Guest Journey types.
pub use gestur_workflow as workflow;

#[cfg(test)]
mod tests {
    use gestur_testkit::RequestIdSequence;

    #[test]
    fn facade_and_testkit_compose_without_external_crates() {
        let ids = RequestIdSequence::new(10);
        assert_eq!(ids.next().map(|id| id.as_u128()), Ok(10));
    }
}
