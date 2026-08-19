#!/usr/bin/env python3
"""Real-Git tests for declared versions, ancestry, and exact tag targets."""

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


class ReleaseEvidenceTests(unittest.TestCase):
    def assert_error(self, errors: list[str], fragment: str) -> None:
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected {fragment!r} in {errors!r}",
        )

    def test_green_retest_finalization_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, _pentested, candidate, declared = make_release(Path(directory))
            self.assertEqual(validate(fixture, "v0.1.0", candidate, declared), [])

    def test_direct_pass_finalization_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, _pentested, candidate, declared = make_release(
                Path(directory), retest="direct-pass", findings="none"
            )
            self.assertEqual(validate(fixture, "v0.1.0", candidate, declared), [])

    def test_missing_record_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = GitFixture(Path(directory))
            candidate = fixture.commit("implementation")
            errors = validate(fixture, "v0.1.0", candidate, {"v0.1.0"})
        self.assert_error(errors, "pentest record: record is missing")

    def test_dirty_worktree_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, _pentested, candidate, declared = make_release(Path(directory))
            fixture.write("untracked.txt", "dirty\n")
            errors = validate(fixture, "v0.1.0", candidate, declared)
        self.assert_error(errors, "worktree is not clean")

    def test_candidate_must_be_checked_out_head(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, pentested, _candidate, declared = make_release(Path(directory))
            errors = validate(fixture, "v0.1.0", pentested, declared)
        self.assert_error(errors, "candidate is not the checked-out HEAD")

    def test_missing_predecessor_tag_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, _pentested, candidate, _declared = make_release(Path(directory))
            errors = validate(
                fixture,
                "v0.2.0",
                candidate,
                {"v0.1.0", "v0.2.0"},
            )
        self.assert_error(errors, "missing annotated predecessor tag v0.1.0")

    def test_lightweight_predecessor_tag_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = GitFixture(Path(directory))
            fixture.commit("v0.1.0")
            fixture.tag("v0.1.0", annotated=False)
            pentested = fixture.commit("implementation")
            write_pentest_record(fixture, "v0.2.0", pentested)
            candidate = fixture.commit("release finalization")
            errors = validate(
                fixture,
                "v0.2.0",
                candidate,
                {"v0.1.0", "v0.2.0"},
            )
        self.assert_error(errors, "missing annotated predecessor tag v0.1.0")

    def test_existing_target_tag_blocks_readiness(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, _pentested, candidate, declared = make_release(Path(directory))
            fixture.tag("v0.1.0", candidate)
            errors = validate(fixture, "v0.1.0", candidate, declared)
        self.assert_error(errors, "tag already exists")

    def test_annotated_tag_on_exact_candidate_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, _pentested, candidate, declared = make_release(Path(directory))
            fixture.tag("v0.1.0", candidate)
            errors = validate(
                fixture,
                "v0.1.0",
                candidate,
                declared,
                tagged_release=True,
            )
        self.assertEqual(errors, [])

    def test_lightweight_current_tag_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, _pentested, candidate, declared = make_release(Path(directory))
            fixture.tag("v0.1.0", candidate, annotated=False)
            errors = validate(
                fixture,
                "v0.1.0",
                candidate,
                declared,
                tagged_release=True,
            )
        self.assert_error(errors, "missing or lightweight")

    def test_tag_on_wrong_commit_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, pentested, candidate, declared = make_release(Path(directory))
            fixture.tag("v0.1.0", pentested)
            errors = validate(
                fixture,
                "v0.1.0",
                candidate,
                declared,
                tagged_release=True,
            )
        self.assert_error(errors, "does not target the release commit")


if __name__ == "__main__":
    unittest.main()
