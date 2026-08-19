//! Cross-crate tests for Gestur's assembled foundation contracts.

use gestur::api_types::CommandContext;
use gestur::core::{ActorId, EventId, RequestId, Revision, SiteId, TenantId, UnixMillis, VisitId};
use gestur::crypto_types::{AlgorithmProfile, CryptoTypeError, DigestReference};
use gestur::events::{EventKind, VisitEvent};
use gestur::policy::Capability;
use gestur::schema::{DataClassification, FieldDefinition, FieldKind};
use gestur::workflow::{NodeId, Transition};
use gestur_testkit::{RequestIdSequence, RequestIdSequenceError};

#[test]
fn guest_journey_input_keeps_security_and_privacy_context() {
    let tenant_id = TenantId::from_u128(11);
    let site_id = SiteId::from_u128(12);
    let actor_id = ActorId::from_u128(13);
    let revision = Revision::new(2);

    let context = revision.map(|expected_revision| CommandContext {
        tenant_id,
        site_id,
        actor_id,
        request_id: RequestId::from_u128(14),
        capability: Capability::HostProjectionRead,
        expected_revision: Some(expected_revision),
    });
    let field = FieldDefinition::new(
        tenant_id,
        "visitor.email",
        "invitation delivery",
        FieldKind::Email,
        DataClassification::Personal,
    );
    let transition = Transition::new(NodeId::new(1), NodeId::new(2));

    assert_eq!(context.map(|value| value.tenant_id), Ok(tenant_id));
    assert_eq!(
        field.map(|value| (value.tenant_id(), value.classification())),
        Ok((tenant_id, DataClassification::Personal))
    );
    assert_eq!(transition.map(|value| value.to.get()), Ok(2));
}

#[test]
fn visit_event_preserves_attribution_and_ordering_across_facade_crates() {
    let event = Revision::new(1).and_then(|sequence| {
        UnixMillis::new(1_000).map(|occurred_at| VisitEvent {
            event_id: EventId::from_u128(21),
            tenant_id: TenantId::from_u128(22),
            visit_id: VisitId::from_u128(23),
            sequence,
            actor_id: ActorId::from_u128(24),
            occurred_at,
            kind: EventKind::VisitorArrived,
        })
    });

    assert_eq!(
        event.map(|value| {
            (
                value.sequence.get(),
                value.actor_id.as_u128(),
                value.occurred_at.get(),
            )
        }),
        Ok((1, 24, 1_000))
    );
}

#[test]
fn invalid_crypto_metadata_is_rejected_at_the_facade_boundary() {
    assert_eq!(
        DigestReference::new(AlgorithmProfile::Sha3_512, &[0_u8; 32]),
        Err(CryptoTypeError::InvalidDigestLength)
    );
}

#[test]
fn foundation_boundaries_fail_closed_on_ambiguous_input_and_id_exhaustion() {
    let tenant_id = TenantId::from_u128(31);
    assert!(matches!(
        FieldDefinition::new(
            tenant_id,
            "Visitor Email",
            "invitation delivery",
            FieldKind::Email,
            DataClassification::Personal,
        ),
        Err(gestur::schema::SchemaError::InvalidKey)
    ));
    assert!(matches!(
        FieldDefinition::new(
            tenant_id,
            "visitor.email",
            "invitation\ndelivery",
            FieldKind::Email,
            DataClassification::Personal,
        ),
        Err(gestur::schema::SchemaError::InvalidPurpose)
    ));

    let ids = RequestIdSequence::new(u128::MAX);
    assert_eq!(ids.next().map(RequestId::as_u128), Ok(u128::MAX));
    assert_eq!(ids.next(), Err(RequestIdSequenceError::Exhausted));
}
