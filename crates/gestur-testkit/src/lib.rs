//! Deterministic helpers for unit and conformance tests.

#![no_std]
#![forbid(unsafe_code)]

use core::cell::Cell;

use gestur_core::RequestId;

/// A deterministic request-identifier source for tests.
#[derive(Debug)]
pub struct RequestIdSequence {
    next: Cell<Option<u128>>,
}

impl RequestIdSequence {
    /// Creates a sequence whose first result is start.
    #[must_use]
    pub const fn new(start: u128) -> Self {
        Self {
            next: Cell::new(Some(start)),
        }
    }

    /// Returns the next deterministic identifier or fails after exhaustion.
    ///
    /// The maximum identifier is returned exactly once. Refusing every later
    /// request prevents test scenarios from silently reusing an idempotency
    /// identity.
    pub fn next(&self) -> Result<RequestId, RequestIdSequenceError> {
        let current = self.next.get().ok_or(RequestIdSequenceError::Exhausted)?;
        self.next.set(current.checked_add(1));
        Ok(RequestId::from_u128(current))
    }
}

/// Failures produced by deterministic request-identifier sequences.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum RequestIdSequenceError {
    /// Every representable identifier has already been returned.
    Exhausted,
}

#[cfg(test)]
mod tests {
    use super::{RequestId, RequestIdSequence, RequestIdSequenceError};

    #[test]
    fn sequence_is_deterministic() {
        let sequence = RequestIdSequence::new(4);
        assert_eq!(sequence.next().map(RequestId::as_u128), Ok(4));
        assert_eq!(sequence.next().map(RequestId::as_u128), Ok(5));
    }

    #[test]
    fn sequence_fails_closed_after_maximum() {
        let saturated = RequestIdSequence::new(u128::MAX);
        assert_eq!(saturated.next().map(RequestId::as_u128), Ok(u128::MAX));
        assert_eq!(saturated.next(), Err(RequestIdSequenceError::Exhausted));
        assert_eq!(saturated.next(), Err(RequestIdSequenceError::Exhausted));
    }
}
