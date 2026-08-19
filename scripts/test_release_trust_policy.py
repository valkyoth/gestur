#!/usr/bin/env python3
"""Adversarial tests for release trust anchors and pentest evidence."""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

REPOSITORY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY / "scripts"))

from release_evidence_testkit import (  # noqa: E402
    PENTESTER_KEY,
    TAG_SIGNER_KEY,
    GitFixture,
    validate,
    write_pentest_evidence,
    write_source_evidence,
)
from release_trust_policy import validate_trust_policy  # noqa: E402


class ReleaseTrustPolicyTests(unittest.TestCase):
    def assert_error(self, errors: list[str], fragment: str) -> None:
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected {fragment!r} in {errors!r}",
        )

    def make_release(self, root: Path, **pentest: str) -> tuple[GitFixture, str]:
        fixture = GitFixture(root)
        candidate = fixture.commit("candidate")
        write_source_evidence(fixture, "v0.1.0", candidate)
        if pentest:
            write_pentest_evidence(fixture, "v0.1.0", candidate, **pentest)
        fixture.commit("evidence")
        return fixture, candidate

    def test_external_policy_pin_matches_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate = self.make_release(Path(directory))
            errors = validate(fixture, "v0.1.0", candidate, {"v0.1.0"})
        self.assertEqual(errors, [])

    def test_candidate_policy_change_cannot_self_authorize(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate = self.make_release(Path(directory))
            errors = validate(
                fixture,
                "v0.1.0",
                candidate,
                {"v0.1.0"},
                expected_trust_policy_digest="0" * 64,
            )
        self.assert_error(errors, "candidate policy differs from external pin")

    def test_missing_external_policy_pin_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = GitFixture(Path(directory))
            candidate = fixture.commit("candidate")
            with patch.dict(os.environ, {}, clear=True):
                errors = validate_trust_policy(fixture.root, candidate)
        self.assert_error(errors, "missing external")

    def test_malformed_external_policy_pin_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = GitFixture(Path(directory))
            candidate = fixture.commit("candidate")
            errors = validate_trust_policy(fixture.root, candidate, "not-a-digest")
        self.assert_error(errors, "external digest is malformed")

    def test_one_fingerprint_cannot_cross_release_roles(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = GitFixture(Path(directory))
            fixture.write(
                "security/external-pentesters.txt",
                f"{TAG_SIGNER_KEY} | Independent Pentester\n",
            )
            candidate = fixture.commit("candidate")
            write_source_evidence(fixture, "v0.1.0", candidate)
            write_pentest_evidence(
                fixture,
                "v0.1.0",
                candidate,
                tester_key=TAG_SIGNER_KEY,
            )
            fixture.commit("evidence")
            errors = validate(fixture, "v0.1.0", candidate, {"v0.1.0"})
        self.assert_error(errors, "crosses roles")

    def test_duplicate_role_identity_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = GitFixture(Path(directory))
            fixture.write(
                "security/external-pentesters.txt",
                f"{PENTESTER_KEY} | Independent Pentester\n"
                f"{'E' * 40} | Independent Pentester\n",
            )
            candidate = fixture.commit("candidate")
            write_source_evidence(fixture, "v0.1.0", candidate)
            fixture.commit("evidence")
            errors = validate(fixture, "v0.1.0", candidate, {"v0.1.0"})
        self.assert_error(errors, "duplicate identity")

    def test_unsigned_pentest_attestation_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate = self.make_release(
                Path(directory), signature="forged\n"
            )
            errors = validate(fixture, "v0.1.0", candidate, {"v0.1.0"})
        self.assert_error(errors, "detached signature is invalid")

    def test_untrusted_pentester_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate = self.make_release(
                Path(directory), tester_key="E" * 40
            )
            errors = validate(fixture, "v0.1.0", candidate, {"v0.1.0"})
        self.assert_error(errors, "tester key is not externally authorized")

    def test_pentest_must_bind_exact_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate = self.make_release(
                Path(directory), reviewed="a" * 40
            )
            errors = validate(fixture, "v0.1.0", candidate, {"v0.1.0"})
        self.assert_error(errors, "reviewed commit is not the exact candidate")

    def test_non_pass_pentest_result_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate = self.make_release(Path(directory), status="FAIL")
            errors = validate(fixture, "v0.1.0", candidate, {"v0.1.0"})
        self.assert_error(errors, "status is not PASS")

    def test_cross_release_report_path_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate = self.make_release(
                Path(directory),
                report_path="security/pentest/reports/v0.0.1/report.md",
            )
            errors = validate(fixture, "v0.1.0", candidate, {"v0.1.0"})
        self.assert_error(errors, "unsafe evidence path")

    def test_pentest_report_mutation_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate = self.make_release(
                Path(directory), report_digest="0" * 64
            )
            errors = validate(fixture, "v0.1.0", candidate, {"v0.1.0"})
        self.assert_error(errors, "Report-Digest does not match")

    def test_pentest_support_mutation_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate = self.make_release(
                Path(directory), evidence_digest="0" * 64
            )
            errors = validate(fixture, "v0.1.0", candidate, {"v0.1.0"})
        self.assert_error(errors, "Evidence-Digest does not match")

    def test_cryptographically_valid_but_untrusted_predecessor_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = GitFixture(Path(directory))
            fixture.commit("v0.1.0")
            fixture.tag("v0.1.0")
            candidate = fixture.commit("candidate")
            write_source_evidence(fixture, "v0.1.1", candidate)
            fixture.commit("evidence")
            errors = validate(
                fixture,
                "v0.1.1",
                candidate,
                {"v0.1.0", "v0.1.1"},
                tag_verifier=lambda _root, _tag: "E" * 40,
            )
        self.assert_error(errors, "predecessor tag v0.1.0 signer is not authorized")

    def test_current_tag_must_target_approved_evidence_commit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate = self.make_release(Path(directory))
            fixture.tag("v0.1.0", candidate)
            errors = validate(
                fixture,
                "v0.1.0",
                candidate,
                {"v0.1.0"},
                tagged_release=True,
            )
        self.assert_error(errors, "current tag does not target the evidence commit")

    def test_authorized_current_tag_on_evidence_commit_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate = self.make_release(Path(directory))
            fixture.tag("v0.1.0")
            errors = validate(
                fixture,
                "v0.1.0",
                candidate,
                {"v0.1.0"},
                tagged_release=True,
            )
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
