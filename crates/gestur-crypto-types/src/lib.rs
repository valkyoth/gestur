//! Algorithm-agile cryptographic metadata.
//!
//! This crate defines metadata only. It does not implement cryptography.

#![no_std]
#![forbid(unsafe_code)]

/// Reviewed algorithm profiles that durable records may identify.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
#[non_exhaustive]
pub enum AlgorithmProfile {
    /// SHA3-256 digest profile.
    Sha3_256,
    /// SHA3-512 digest profile.
    Sha3_512,
}

/// A borrowed digest bound to its declared algorithm profile.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct DigestReference<'a> {
    profile: AlgorithmProfile,
    bytes: &'a [u8],
}

impl<'a> DigestReference<'a> {
    /// Creates a digest reference only when its width matches the profile.
    pub fn new(profile: AlgorithmProfile, bytes: &'a [u8]) -> Result<Self, CryptoTypeError> {
        let expected = match profile {
            AlgorithmProfile::Sha3_256 => 32,
            AlgorithmProfile::Sha3_512 => 64,
        };
        if bytes.len() == expected {
            Ok(Self { profile, bytes })
        } else {
            Err(CryptoTypeError::InvalidDigestLength)
        }
    }

    /// Returns the declared profile.
    #[must_use]
    pub const fn profile(self) -> AlgorithmProfile {
        self.profile
    }

    /// Returns the validated digest bytes.
    #[must_use]
    pub const fn bytes(self) -> &'a [u8] {
        self.bytes
    }
}

/// Cryptographic metadata validation failures.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum CryptoTypeError {
    /// Digest width does not match the declared profile.
    InvalidDigestLength,
}

#[cfg(test)]
mod tests {
    use super::{AlgorithmProfile, CryptoTypeError, DigestReference};

    #[test]
    fn digest_width_must_match_profile() {
        assert_eq!(
            DigestReference::new(AlgorithmProfile::Sha3_256, &[0_u8; 31]),
            Err(CryptoTypeError::InvalidDigestLength)
        );
        assert_eq!(
            DigestReference::new(AlgorithmProfile::Sha3_256, &[0_u8; 32])
                .map(|digest| (digest.profile(), digest.bytes().len())),
            Ok((AlgorithmProfile::Sha3_256, 32))
        );
        assert_eq!(
            DigestReference::new(AlgorithmProfile::Sha3_512, &[0_u8; 64])
                .map(|digest| (digest.profile(), digest.bytes().len())),
            Ok((AlgorithmProfile::Sha3_512, 64))
        );
        assert_eq!(
            DigestReference::new(AlgorithmProfile::Sha3_512, &[0_u8; 65]),
            Err(CryptoTypeError::InvalidDigestLength)
        );
    }
}
