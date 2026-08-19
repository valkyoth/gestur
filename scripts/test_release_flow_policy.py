#!/usr/bin/env python3
"""Adversarial tests for pentest/retest and post-pentest CodeQL handling."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY / "scripts"))

from release_evidence_testkit import (  # noqa: E402
    GitFixture,
    make_release,
    validate,
    write_pentest_record,
)


class ReleaseFlowPolicyTests(unittest.TestCase):
    def assert_error(self, errors: list[str], fragment: str) -> None:
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected {fragment!r} in {errors!r}",
        )

    def errors_for_record(self, **record: str) -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            fixture, _pentested, candidate, declared = make_release(
                Path(directory), **record
            )
            return validate(fixture, "v0.1.0", candidate, declared)

    def test_non_pass_status_is_rejected(self) -> None:
        self.assert_error(self.errors_for_record(status="FAIL"), "status is not PASS")

    def test_future_date_is_rejected(self) -> None:
        self.assert_error(
            self.errors_for_record(checked="2026-08-20"), "date is in the future"
        )

    def test_clean_retest_requires_resolved_findings(self) -> None:
        self.assert_error(
            self.errors_for_record(findings="none"),
            "clean retest must identify resolved findings",
        )

    def test_direct_pass_cannot_claim_resolved_findings(self) -> None:
        self.assert_error(
            self.errors_for_record(retest="direct-pass", findings="something"),
            "direct pass must record Findings-Resolved as none",
        )

    def test_unknown_pentested_commit_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = GitFixture(Path(directory))
            fixture.commit("implementation")
            write_pentest_record(fixture, "v0.1.0", "a" * 40)
            candidate = fixture.commit("release finalization")
            errors = validate(fixture, "v0.1.0", candidate, {"v0.1.0"})
        self.assert_error(errors, "pentested commit does not exist")

    def test_pass_placeholder_in_pentested_commit_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = GitFixture(Path(directory))
            before = fixture.run("rev-parse", "HEAD")
            write_pentest_record(fixture, "v0.1.0", before)
            pentested = fixture.commit("implementation with PASS placeholder")
            write_pentest_record(fixture, "v0.1.0", pentested)
            candidate = fixture.commit("release finalization")
            errors = validate(fixture, "v0.1.0", candidate, {"v0.1.0"})
        self.assert_error(errors, "PASS record existed before the pentest result")

    def test_unrecorded_post_pentest_code_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = GitFixture(Path(directory))
            pentested = fixture.commit("implementation")
            fixture.write("crates/core.rs", "changed after pentest\n")
            write_pentest_record(fixture, "v0.1.0", pentested)
            candidate = fixture.commit("undocumented code change")
            errors = validate(fixture, "v0.1.0", candidate, {"v0.1.0"})
        self.assert_error(errors, "post-pentest code changes require CodeQL details")

    def make_codeql_release(
        self, root: Path, **record: str
    ) -> tuple[GitFixture, str, set[str]]:
        fixture = GitFixture(root)
        fixture.write("crates/core.rs", "before\n")
        pentested = fixture.commit("implementation")
        fixture.write("crates/core.rs", "after CodeQL fix\n")
        fixture.write("tests/codeql_regression.rs", "regression\n")
        defaults = {
            "codeql_finding": "rust/example-rule alert 123",
            "codeql_changed_paths": "crates/core.rs,tests/codeql_regression.rs",
            "regression_tests": "tests/codeql_regression.rs",
        }
        defaults.update(record)
        write_pentest_record(fixture, "v0.1.0", pentested, **defaults)
        candidate = fixture.commit("CodeQL remediation")
        return fixture, candidate, {"v0.1.0"}

    def test_documented_codeql_remediation_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate, declared = self.make_codeql_release(Path(directory))
            self.assertEqual(validate(fixture, "v0.1.0", candidate, declared), [])

    def test_codeql_changed_path_mismatch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate, declared = self.make_codeql_release(
                Path(directory), codeql_changed_paths="tests/codeql_regression.rs"
            )
            errors = validate(fixture, "v0.1.0", candidate, declared)
        self.assert_error(errors, "does not match Git history")

    def test_codeql_remediation_requires_regression_test(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate, declared = self.make_codeql_release(
                Path(directory), regression_tests="none"
            )
            errors = validate(fixture, "v0.1.0", candidate, declared)
        self.assert_error(errors, "requires regression tests")

    def test_codeql_regression_path_must_be_executable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = GitFixture(Path(directory))
            fixture.write("crates/core.rs", "before\n")
            pentested = fixture.commit("implementation")
            fixture.write("crates/core.rs", "fixed\n")
            fixture.write("docs/regression.md", "not executable\n")
            write_pentest_record(
                fixture,
                "v0.1.0",
                pentested,
                codeql_finding="rust/example-rule",
                codeql_changed_paths="crates/core.rs,docs/regression.md",
                regression_tests="docs/regression.md",
            )
            candidate = fixture.commit("CodeQL remediation")
            errors = validate(fixture, "v0.1.0", candidate, {"v0.1.0"})
        self.assert_error(errors, "regression test path is not executable")

    def test_failed_full_gate_is_rejected(self) -> None:
        self.assert_error(
            self.errors_for_record(full_gate="FAIL"), "Full-Gate is not PASS"
        )


if __name__ == "__main__":
    unittest.main()
