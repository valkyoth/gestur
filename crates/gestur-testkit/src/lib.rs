//! Deterministic helpers for unit and conformance tests.

#![no_std]
#![forbid(unsafe_code)]

use core::cell::Cell;

use gestur_core::RequestId;

/// A deterministic request-identifier source for tests.
#[derive(Debug)]
pub struct RequestIdSequence {
    next: Cell<u128>,
}

impl RequestIdSequence {
    /// Creates a sequence whose first result is start.
    #[must_use]
    pub const fn new(start: u128) -> Self {
        Self {
            next: Cell::new(start),
        }
    }

    /// Returns the next deterministic identifier.
    #[must_use]
    pub fn next(&self) -> RequestId {
        let current = self.next.get();
        self.next.set(current.saturating_add(1));
        RequestId::from_u128(current)
    }
}

#[cfg(test)]
mod tests {
    use super::RequestIdSequence;

    #[test]
    fn sequence_is_deterministic_and_saturating() {
        let sequence = RequestIdSequence::new(4);
        assert_eq!(sequence.next().as_u128(), 4);
        assert_eq!(sequence.next().as_u128(), 5);

        let saturated = RequestIdSequence::new(u128::MAX);
        assert_eq!(saturated.next().as_u128(), u128::MAX);
        assert_eq!(saturated.next().as_u128(), u128::MAX);
    }
}
