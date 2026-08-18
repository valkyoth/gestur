//! Versioned, transport-neutral domain events.

#![no_std]
#![forbid(unsafe_code)]

use gestur_core::{ActorId, EventId, Revision, TenantId, UnixMillis, VisitId};

/// Stable event categories used by projections and integrations.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum EventKind {
    /// A visitor arrived at a site boundary.
    VisitorArrived,
    /// A privacy notice revision was presented.
    PrivacyNoticePresented,
    /// An authorized party approved the visit.
    VisitApproved,
    /// A visit entered checked-in state.
    VisitCheckedIn,
    /// A visit completed checkout.
    VisitCheckedOut,
    /// A temporary credential was revoked.
    CredentialRevoked,
}

/// Metadata common to every authoritative visit event.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct VisitEvent {
    /// Globally unique event identifier.
    pub event_id: EventId,
    /// Tenant boundary.
    pub tenant_id: TenantId,
    /// Aggregate identity.
    pub visit_id: VisitId,
    /// Aggregate sequence.
    pub sequence: Revision,
    /// Responsible actor.
    pub actor_id: ActorId,
    /// Event occurrence time.
    pub occurred_at: UnixMillis,
    /// Stable event category.
    pub kind: EventKind,
}

#[cfg(test)]
mod tests {
    use gestur_core::{ActorId, EventId, Revision, TenantId, UnixMillis, VisitId};

    use super::{EventKind, VisitEvent};

    #[test]
    fn event_carries_required_attribution() {
        let sequence = Revision::new(1);
        let time = UnixMillis::new(10);
        let event = sequence.and_then(|sequence| {
            time.map(|occurred_at| VisitEvent {
                event_id: EventId::from_u128(1),
                tenant_id: TenantId::from_u128(2),
                visit_id: VisitId::from_u128(3),
                sequence,
                actor_id: ActorId::from_u128(4),
                occurred_at,
                kind: EventKind::VisitorArrived,
            })
        });
        assert_eq!(event.map(|value| value.actor_id.as_u128()), Ok(4));
    }
}
