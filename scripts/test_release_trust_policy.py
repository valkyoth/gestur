#!/usr/bin/env python3
"""Adversarial tests for release trust and the owner-driven pentest loop."""

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
    REVIEWER_KEY,
    TAG_SIGNER_KEY,
    GitFixture,
    codeql_delta_fields,
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

    def make_release(
        self, root: Path, **pentest: str
    ) -> tuple[GitFixture, str]:
        fixture = GitFixture(root)
        candidate = fixture.commit("candidate")
        write_source_evidence(fixture, "v0.1.0", candidate)
        if pentest:
            write_pentest_evidence(fixture, "v0.1.0", candidate, **pentest)
        fixture.commit("evidence")
        return fixture, candidate

    def make_codeql_release(
        self, root: Path, **overrides: str
    ) -> tuple[GitFixture, str]:
        fixture = GitFixture(root)
        pentested = fixture.commit("pentested implementation")
        write_source_evidence(fixture, "v0.1.0", pentested)
        base = fixture.commit("initial green pentest evidence")
        fixture.write("docs/scope.md", "CodeQL remediation\n")
        fixture.write("tests/codeql_regression.txt", "regression coverage\n")
        candidate = fixture.commit("CodeQL remediation")
        write_source_evidence(
            fixture,
            "v0.1.0",
            candidate,
            signature="valid-codeql\n",
            support="Primary-source review after CodeQL remediation\n",
        )
        fields = codeql_delta_fields(
            fixture, base, candidate, "tests/codeql_regression.txt"
        )
        if overrides.get("codeql_delta_base") == "pentested":
            overrides["codeql_delta_base"] = pentested
        fields.update(overrides)
        write_pentest_evidence(
            fixture,
            "v0.1.0",
            candidate,
            pentested=pentested,
            **fields,
        )
        fixture.commit("updated release evidence")
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
                "security/release-tag-signers.txt",
                f"{REVIEWER_KEY} | Release Tag Signer\n",
            )
            candidate = fixture.commit("candidate")
            write_source_evidence(fixture, "v0.1.0", candidate)
            fixture.commit("evidence")
            errors = validate(fixture, "v0.1.0", candidate, {"v0.1.0"})
        self.assert_error(errors, "crosses roles")

    def test_duplicate_role_identity_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = GitFixture(Path(directory))
            fixture.write(
                "security/release-tag-signers.txt",
                f"{TAG_SIGNER_KEY} | Release Tag Signer\n"
                f"{'E' * 40} | Release Tag Signer\n",
            )
            candidate = fixture.commit("candidate")
            write_source_evidence(fixture, "v0.1.0", candidate)
            fixture.commit("evidence")
            errors = validate(fixture, "v0.1.0", candidate, {"v0.1.0"})
        self.assert_error(errors, "duplicate identity")

    def test_direct_green_pentest_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate = self.make_release(Path(directory))
            errors = validate(fixture, "v0.1.0", candidate, {"v0.1.0"})
        self.assertEqual(errors, [])

    def test_clean_retest_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate = self.make_release(
                Path(directory), retest="clean-retest"
            )
            errors = validate(fixture, "v0.1.0", candidate, {"v0.1.0"})
        self.assertEqual(errors, [])

    def test_pentest_tool_without_version_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate = self.make_release(
                Path(directory), tools="unversioned-scanner"
            )
            errors = validate(fixture, "v0.1.0", candidate, {"v0.1.0"})
        self.assert_error(errors, "Tools must name each third-party tool and version")

    def test_duplicate_pentest_tool_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate = self.make_release(
                Path(directory), tools="scanner@1.0,scanner@1.0"
            )
            errors = validate(fixture, "v0.1.0", candidate, {"v0.1.0"})
        self.assert_error(errors, "duplicate pentest tool")

    def test_missing_pentest_configuration_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate = self.make_release(Path(directory), configuration="")
            errors = validate(fixture, "v0.1.0", candidate, {"v0.1.0"})
        self.assert_error(errors, "expected exactly one Configuration field")

    def test_future_pentest_date_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate = self.make_release(
                Path(directory), checked="2026-08-20"
            )
            errors = validate(fixture, "v0.1.0", candidate, {"v0.1.0"})
        self.assert_error(errors, "date is in the future")

    def test_non_pass_pentest_result_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate = self.make_release(Path(directory), status="FAIL")
            errors = validate(fixture, "v0.1.0", candidate, {"v0.1.0"})
        self.assert_error(errors, "status is not PASS")

    def test_unknown_pentested_commit_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate = self.make_release(
                Path(directory), pentested="a" * 40
            )
            errors = validate(fixture, "v0.1.0", candidate, {"v0.1.0"})
        self.assert_error(errors, "pentested commit does not exist")

    def test_nonancestor_pentested_commit_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = GitFixture(Path(directory))
            main = fixture.run("branch", "--show-current")
            fixture.run("switch", "-q", "-c", "pentest-side")
            pentested = fixture.commit("unrelated pentest target")
            fixture.run("switch", "-q", main)
            candidate = fixture.commit("candidate")
            write_source_evidence(fixture, "v0.1.0", candidate)
            write_pentest_evidence(
                fixture,
                "v0.1.0",
                candidate,
                pentested=pentested,
                post_changes="CodeQL: unrelated branch must not pass",
            )
            fixture.commit("evidence")
            errors = validate(fixture, "v0.1.0", candidate, {"v0.1.0"})
        self.assert_error(errors, "pentested commit is not a candidate ancestor")

    def test_report_must_name_evidence_parent_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate = self.make_release(
                Path(directory), release_candidate="a" * 40
            )
            errors = validate(fixture, "v0.1.0", candidate, {"v0.1.0"})
        self.assert_error(errors, "release candidate is not the evidence parent")

    def test_retest_outcome_is_bounded(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate = self.make_release(Path(directory), retest="maybe")
            errors = validate(fixture, "v0.1.0", candidate, {"v0.1.0"})
        self.assert_error(errors, "Retest must be direct-pass or clean-retest")

    def test_codeql_fix_after_green_pentest_is_recorded(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate = self.make_codeql_release(Path(directory))
            errors = validate(fixture, "v0.1.0", candidate, {"v0.1.0"})
        self.assertEqual(errors, [])

    def test_free_text_codeql_delta_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate = self.make_codeql_release(
                Path(directory),
                post_changes="CodeQL: free text is not structured evidence",
            )
            errors = validate(fixture, "v0.1.0", candidate, {"v0.1.0"})
        self.assert_error(errors, "later candidate changes must be a CodeQL delta")

    def test_codeql_changed_paths_are_exact(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate = self.make_codeql_release(
                Path(directory), changed_paths="tests/codeql_regression.txt"
            )
            errors = validate(fixture, "v0.1.0", candidate, {"v0.1.0"})
        self.assert_error(errors, "Changed-Paths does not match")

    def test_codeql_delta_base_must_be_candidate_parent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate = self.make_codeql_release(
                Path(directory), codeql_delta_base="pentested"
            )
            errors = validate(fixture, "v0.1.0", candidate, {"v0.1.0"})
        self.assert_error(errors, "CodeQL delta base is not the candidate parent")

    def test_codeql_diff_digest_mutation_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate = self.make_codeql_release(
                Path(directory), diff_digest="0" * 64
            )
            errors = validate(fixture, "v0.1.0", candidate, {"v0.1.0"})
        self.assert_error(errors, "Diff-Digest does not match")

    def test_codeql_remediation_requires_regression_test(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate = self.make_codeql_release(
                Path(directory), regression_test="none"
            )
            errors = validate(fixture, "v0.1.0", candidate, {"v0.1.0"})
        self.assert_error(errors, "requires a regression test")

    def test_codeql_full_gate_must_pass(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate = self.make_codeql_release(
                Path(directory), full_gate="FAIL"
            )
            errors = validate(fixture, "v0.1.0", candidate, {"v0.1.0"})
        self.assert_error(errors, "Full-Gate is not PASS")

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
