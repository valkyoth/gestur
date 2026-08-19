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
///
/// Version 0.1.0 only preserves this borrowed contract. Callers must not place
/// secrets or personal data in `detail`; the disclosure-safe error mapping is
/// introduced by its dedicated release milestone before any transport exists.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct Problem<'a> {
    /// Stable machine-readable category.
    pub code: ProblemCode,
    /// Caller-supplied human-readable explanation, which must be non-sensitive.
    pub detail: &'a str,
}

#[cfg(test)]
mod tests {
    use gestur_core::{ActorId, RequestId, Revision, SiteId, TenantId};
    use gestur_policy::Capability;

    use super::{CommandContext, Problem, ProblemCode};

    #[test]
    fn command_context_preserves_every_security_dimension() {
        let revision = Revision::new(7);
        let context = revision.map(|expected_revision| CommandContext {
            tenant_id: TenantId::from_u128(1),
            site_id: SiteId::from_u128(2),
            actor_id: ActorId::from_u128(3),
            request_id: RequestId::from_u128(4),
            capability: Capability::GuestWifiRevoke,
            expected_revision: Some(expected_revision),
        });
        assert_eq!(
            context.map(|value| {
                (
                    value.tenant_id.as_u128(),
                    value.site_id.as_u128(),
                    value.actor_id.as_u128(),
                    value.request_id.as_u128(),
                    value.capability,
                    value.expected_revision.map(Revision::get),
                )
            }),
            Ok((1, 2, 3, 4, Capability::GuestWifiRevoke, Some(7)))
        );
    }

    #[test]
    fn problem_preserves_code_and_borrowed_detail() {
        let problem = Problem {
            code: ProblemCode::Forbidden,
            detail: "requested capability is not granted",
        };
        assert_eq!(problem.code, ProblemCode::Forbidden);
        assert_eq!(problem.detail, "requested capability is not granted");
    }
}
