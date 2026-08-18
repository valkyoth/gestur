//! Policy and least-privilege capability primitives.

#![no_std]
#![forbid(unsafe_code)]

use gestur_core::{ActorId, SiteId, TenantId};

/// Privacy choices for discovering a host.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum HostDiscoveryPolicy {
    /// Hosts are available only through an invitation.
    InvitationOnly,
    /// A visitor must provide a host-issued code.
    HostCode,
    /// Reception performs the search.
    ReceptionMediated,
    /// Exact names may be queried without broad enumeration.
    ExactNameOnly,
}

/// Narrow powers that may be granted to a service or connector.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum Capability {
    /// Issue a temporary guest Wi-Fi credential.
    GuestWifiIssue,
    /// Revoke a temporary guest Wi-Fi credential.
    GuestWifiRevoke,
    /// Submit a bounded badge print job.
    BadgePrint,
    /// Notify a configured recipient.
    NotificationSend,
    /// Read the minimum host projection allowed by policy.
    HostProjectionRead,
}

/// Context required for a deterministic authorization decision.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct AuthorizationContext {
    /// Tenant boundary.
    pub tenant_id: TenantId,
    /// Site boundary.
    pub site_id: SiteId,
    /// Effective actor.
    pub actor_id: ActorId,
    /// Capability being requested.
    pub capability: Capability,
}

/// A fail-closed policy result.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum Decision {
    /// The exact requested action is permitted.
    Allow,
    /// The action is denied.
    Deny,
}

#[cfg(test)]
mod tests {
    use gestur_core::{ActorId, SiteId, TenantId};

    use super::{AuthorizationContext, Capability};

    #[test]
    fn context_binds_capability_to_tenant_site_and_actor() {
        let context = AuthorizationContext {
            tenant_id: TenantId::from_u128(1),
            site_id: SiteId::from_u128(2),
            actor_id: ActorId::from_u128(3),
            capability: Capability::BadgePrint,
        };
        assert_eq!(context.site_id.as_u128(), 2);
        assert_eq!(context.capability, Capability::BadgePrint);
    }
}
