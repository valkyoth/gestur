//! Transport-neutral API command and error types.

#![no_std]
#![forbid(unsafe_code)]

use gestur_core::{ActorId, RequestId, Revision, SiteId, TenantId};
use gestur_policy::Capability;

/// Metadata required by security-sensitive mutations.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct CommandContext {
    /// Tenant boundary.
    pub tenant_id: TenantId,
    /// Site boundary.
    pub site_id: SiteId,
    /// Effective actor.
    pub actor_id: ActorId,
    /// End-to-end request identifier.
    pub request_id: RequestId,
    /// Capability presented for the command.
    pub capability: Capability,
    /// Optional optimistic-concurrency precondition.
    pub expected_revision: Option<Revision>,
}

/// Stable machine-readable problem categories.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum ProblemCode {
    /// Authentication evidence is missing or invalid.
    Unauthenticated,
    /// The principal lacks the exact requested capability.
    Forbidden,
    /// Input failed bounded validation.
    InvalidInput,
    /// An optimistic-concurrency precondition failed.
    RevisionConflict,
    /// A requested object does not exist or is intentionally concealed.
    NotFound,
}

/// A dependency-free problem description for later RFC 9457 adapters.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct Problem<'a> {
    /// Stable machine-readable category.
    pub code: ProblemCode,
    /// Safe human-readable explanation without secrets.
    pub detail: &'a str,
}

#[cfg(test)]
mod tests {
    use super::{Problem, ProblemCode};

    #[test]
    fn problem_has_stable_code_and_safe_detail() {
        let problem = Problem {
            code: ProblemCode::Forbidden,
            detail: "requested capability is not granted",
        };
        assert_eq!(problem.code, ProblemCode::Forbidden);
    }
}
