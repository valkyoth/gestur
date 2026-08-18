//! Declarative Guest Journey primitives.

#![no_std]
#![forbid(unsafe_code)]

use gestur_core::Revision;

/// Stable identifier for a node within one journey revision.
#[derive(Clone, Copy, Debug, Eq, Ord, PartialEq, PartialOrd)]
pub struct NodeId(u32);

impl NodeId {
    /// Creates a node identifier.
    #[must_use]
    pub const fn new(value: u32) -> Self {
        Self(value)
    }

    /// Returns the numeric identifier.
    #[must_use]
    pub const fn get(self) -> u32 {
        self.0
    }
}

/// A deliberately bounded primitive in a Guest Journey.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum NodeKind {
    /// Entry point for a journey.
    Start,
    /// Collect configured schema fields.
    CollectFields,
    /// Display a versioned privacy notice.
    PresentPrivacyNotice,
    /// Request an authorized approval.
    RequireApproval,
    /// Issue only policy-authorized credentials.
    IssueCredentials,
    /// Successful terminal node.
    Complete,
    /// Denied terminal node.
    Reject,
}

/// One immutable journey node.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct JourneyNode {
    /// Identifier unique inside the journey revision.
    pub id: NodeId,
    /// Typed operation performed by the node.
    pub kind: NodeKind,
}

/// A directed transition between distinct nodes.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct Transition {
    /// Origin node.
    pub from: NodeId,
    /// Destination node.
    pub to: NodeId,
}

impl Transition {
    /// Creates a transition and rejects a direct self-loop.
    pub const fn new(from: NodeId, to: NodeId) -> Result<Self, WorkflowError> {
        if from.0 == to.0 {
            Err(WorkflowError::DirectSelfLoop)
        } else {
            Ok(Self { from, to })
        }
    }
}

/// Identity of an immutable published journey revision.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct JourneyRevision {
    /// Application-assigned journey identifier.
    pub journey_id: u128,
    /// Strictly positive revision.
    pub revision: Revision,
}

/// Workflow validation failures.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum WorkflowError {
    /// A node cannot directly transition to itself.
    DirectSelfLoop,
}

#[cfg(test)]
mod tests {
    use super::{NodeId, Transition, WorkflowError};

    #[test]
    fn transitions_reject_direct_self_loops() {
        let node = NodeId::new(9);
        assert_eq!(
            Transition::new(node, node),
            Err(WorkflowError::DirectSelfLoop)
        );
    }

    #[test]
    fn transitions_preserve_direction() {
        let from = NodeId::new(1);
        let to = NodeId::new(2);
        assert_eq!(Transition::new(from, to).map(|edge| edge.to), Ok(to));
    }
}
