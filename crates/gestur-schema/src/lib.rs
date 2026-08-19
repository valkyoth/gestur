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
        validate_key(key)?;
        validate_purpose(purpose)?;
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

fn validate_key(value: &str) -> Result<(), SchemaError> {
    let mut bytes = value.bytes();
    let valid_first = bytes.next().is_some_and(|byte| byte.is_ascii_lowercase());
    let valid_rest = bytes.all(|byte| {
        byte.is_ascii_lowercase() || byte.is_ascii_digit() || matches!(byte, b'.' | b'_' | b'-')
    });
    if value.len() <= 128 && valid_first && valid_rest {
        Ok(())
    } else {
        Err(SchemaError::InvalidKey)
    }
}

fn validate_purpose(value: &str) -> Result<(), SchemaError> {
    if value.is_empty()
        || value.len() > 128
        || value.trim() != value
        || value.chars().any(char::is_control)
    {
        Err(SchemaError::InvalidPurpose)
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
    fn field_key_is_canonical_and_bounded() {
        let tenant = TenantId::from_u128(1);
        let create = |key| {
            FieldDefinition::new(
                tenant,
                key,
                "host notification",
                FieldKind::Text,
                DataClassification::Personal,
            )
        };
        assert!(create("visitor.email_2-primary").is_ok());
        assert_eq!(create("Visitor.Email"), Err(SchemaError::InvalidKey));
        assert_eq!(create(".visitor"), Err(SchemaError::InvalidKey));
        assert_eq!(create("visitor email"), Err(SchemaError::InvalidKey));
        let maximum = "a".repeat(128);
        let oversized = "a".repeat(129);
        assert!(create(&maximum).is_ok());
        assert_eq!(create(&oversized), Err(SchemaError::InvalidKey));
    }

    #[test]
    fn purpose_rejects_ambiguous_or_control_text() {
        let tenant = TenantId::from_u128(1);
        let create = |purpose| {
            FieldDefinition::new(
                tenant,
                "visitor.email",
                purpose,
                FieldKind::Text,
                DataClassification::Personal,
            )
        };
        assert_eq!(
            create(" host notification"),
            Err(SchemaError::InvalidPurpose)
        );
        assert_eq!(
            create("host\nnotification"),
            Err(SchemaError::InvalidPurpose)
        );
        let maximum = "a".repeat(128);
        let oversized = "a".repeat(129);
        assert!(create(&maximum).is_ok());
        assert_eq!(create(&oversized), Err(SchemaError::InvalidPurpose));
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
