//! Portable, privacy-aware field schemas.

#![no_std]
#![forbid(unsafe_code)]

use gestur_core::TenantId;

/// Security and privacy classification applied to a value.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum DataClassification {
    /// Safe for intentional public display.
    Public,
    /// Internal operational data without visitor PII.
    Internal,
    /// Personal data requiring purpose and access controls.
    Personal,
    /// Highly sensitive data requiring additional safeguards.
    Restricted,
}

/// Supported dependency-free field shapes.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum FieldKind {
    /// A bounded single-line text value.
    Text,
    /// An email address validated at an infrastructure boundary.
    Email,
    /// A telephone number validated at an infrastructure boundary.
    Phone,
    /// A true-or-false value.
    Boolean,
}

/// A version-independent field definition.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FieldDefinition<'a> {
    tenant_id: TenantId,
    key: &'a str,
    purpose: &'a str,
    kind: FieldKind,
    classification: DataClassification,
}

impl<'a> FieldDefinition<'a> {
    /// Creates a field after validating its stable key and declared purpose.
    pub fn new(
        tenant_id: TenantId,
        key: &'a str,
        purpose: &'a str,
        kind: FieldKind,
        classification: DataClassification,
    ) -> Result<Self, SchemaError> {
        validate_text(key, SchemaError::InvalidKey)?;
        validate_text(purpose, SchemaError::InvalidPurpose)?;
        Ok(Self {
            tenant_id,
            key,
            purpose,
            kind,
            classification,
        })
    }

    /// Returns the owning tenant.
    #[must_use]
    pub const fn tenant_id(&self) -> TenantId {
        self.tenant_id
    }

    /// Returns the stable field key.
    #[must_use]
    pub const fn key(&self) -> &'a str {
        self.key
    }

    /// Returns the declared collection purpose.
    #[must_use]
    pub const fn purpose(&self) -> &'a str {
        self.purpose
    }

    /// Returns the field shape.
    #[must_use]
    pub const fn kind(&self) -> FieldKind {
        self.kind
    }

    /// Returns the data classification.
    #[must_use]
    pub const fn classification(&self) -> DataClassification {
        self.classification
    }
}

fn validate_text(value: &str, error: SchemaError) -> Result<(), SchemaError> {
    if value.is_empty() || value.len() > 128 {
        Err(error)
    } else {
        Ok(())
    }
}

/// Schema validation failures.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum SchemaError {
    /// The field key is empty or exceeds its bound.
    InvalidKey,
    /// The purpose is empty or exceeds its bound.
    InvalidPurpose,
}

#[cfg(test)]
mod tests {
    use gestur_core::TenantId;

    use super::{DataClassification, FieldDefinition, FieldKind, SchemaError};

    #[test]
    fn field_requires_key_and_purpose() {
        let tenant = TenantId::from_u128(1);
        assert_eq!(
            FieldDefinition::new(
                tenant,
                "",
                "host notification",
                FieldKind::Email,
                DataClassification::Personal,
            ),
            Err(SchemaError::InvalidKey)
        );
        assert_eq!(
            FieldDefinition::new(
                tenant,
                "visitor.email",
                "",
                FieldKind::Email,
                DataClassification::Personal,
            ),
            Err(SchemaError::InvalidPurpose)
        );
    }

    #[test]
    fn field_preserves_privacy_metadata() {
        let field = FieldDefinition::new(
            TenantId::from_u128(7),
            "visitor.phone",
            "emergency contact",
            FieldKind::Phone,
            DataClassification::Restricted,
        );
        assert_eq!(
            field.map(|value| (value.key(), value.classification())),
            Ok(("visitor.phone", DataClassification::Restricted))
        );
    }
}
