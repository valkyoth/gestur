//! Dependency-free domain primitives shared across Gestur.
//!
//! These types carry identity and time without depending on operating-system,
//! network, database, or serialization facilities.

#![no_std]
#![forbid(unsafe_code)]

#[cfg(test)]
extern crate std;

use core::fmt;
use core::num::NonZeroU64;

macro_rules! identifier {
    ($name:ident, $doc:literal) => {
        #[doc = $doc]
        #[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
        pub struct $name(u128);

        impl $name {
            #[doc = "Creates an identifier from its canonical integer value."]
            #[must_use]
            pub const fn from_u128(value: u128) -> Self {
                Self(value)
            }

            #[doc = "Returns the canonical integer value."]
            #[must_use]
            pub const fn as_u128(self) -> u128 {
                self.0
            }
        }

        impl fmt::Display for $name {
            fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
                write!(formatter, "{}", self.0)
            }
        }
    };
}

identifier!(TenantId, "Identifies one isolated Gestur tenant.");
identifier!(SiteId, "Identifies one physical or logical site.");
identifier!(VisitId, "Identifies one visit aggregate.");
identifier!(
    ActorId,
    "Identifies the principal responsible for an action."
);
identifier!(RequestId, "Identifies one end-to-end request.");
identifier!(EventId, "Identifies one immutable domain event.");

/// A non-negative Unix timestamp represented as milliseconds.
#[derive(Clone, Copy, Debug, Eq, Ord, PartialEq, PartialOrd)]
pub struct UnixMillis(i64);

impl UnixMillis {
    /// Creates a timestamp, rejecting values before the Unix epoch.
    pub const fn new(value: i64) -> Result<Self, CoreError> {
        if value < 0 {
            Err(CoreError::BeforeUnixEpoch)
        } else {
            Ok(Self(value))
        }
    }

    /// Returns milliseconds since the Unix epoch.
    #[must_use]
    pub const fn get(self) -> i64 {
        self.0
    }
}

/// A strictly positive aggregate or event revision.
#[derive(Clone, Copy, Debug, Eq, Ord, PartialEq, PartialOrd)]
pub struct Revision(NonZeroU64);

impl Revision {
    /// Creates a revision, rejecting zero.
    pub const fn new(value: u64) -> Result<Self, CoreError> {
        match NonZeroU64::new(value) {
            Some(value) => Ok(Self(value)),
            None => Err(CoreError::ZeroRevision),
        }
    }

    /// Returns the numeric revision.
    #[must_use]
    pub const fn get(self) -> u64 {
        self.0.get()
    }
}

/// Errors raised by foundational value validation.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum CoreError {
    /// A timestamp predates the supported Unix epoch.
    BeforeUnixEpoch,
    /// Revisions begin at one.
    ZeroRevision,
}

#[cfg(test)]
mod tests {
    use super::{CoreError, Revision, TenantId, UnixMillis};

    #[test]
    fn identifiers_round_trip() {
        let id = TenantId::from_u128(42);
        assert_eq!(id.as_u128(), 42);
        assert_eq!(std::format!("{id}"), "42");
    }

    #[test]
    fn timestamps_reject_pre_epoch_values() {
        assert_eq!(UnixMillis::new(-1), Err(CoreError::BeforeUnixEpoch));
        assert_eq!(UnixMillis::new(0).map(UnixMillis::get), Ok(0));
    }

    #[test]
    fn revisions_are_strictly_positive() {
        assert_eq!(Revision::new(0), Err(CoreError::ZeroRevision));
        assert_eq!(Revision::new(1).map(Revision::get), Ok(1));
    }
}
