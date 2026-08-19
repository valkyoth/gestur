#!/usr/bin/env python3
"""Real-Git and mutation tests for Gestur release-evidence validation."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY / "scripts"))

import validate_detailed_version_plan as plan_validator  # noqa: E402
from release_evidence_testkit import (  # noqa: E402
    BOUNDARY_DIGEST,
    SOURCE_DIGEST,
    GitFixture,
    validate,
    write_boundary_evidence,
    write_source_evidence,
)


class ReleaseEvidenceValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.plan = (REPOSITORY / "docs/DETAILED_VERSION_PLAN.md").read_text(
            encoding="utf-8"
        )

    def make_source_release(
        self,
        root: Path,
        release: str = "v0.1.0",
        *,
        predecessors: tuple[str, ...] = (),
        reviewed: str | None = None,
        source_digest: str = SOURCE_DIGEST,
        signature: str = "valid\n",
        extra: str | None = None,
    ) -> tuple[GitFixture, str, set[str]]:
        fixture = GitFixture(root)
        declared = set(predecessors) | {release}
        for predecessor in predecessors:
            fixture.commit(predecessor)
            fixture.tag(predecessor)
        candidate = fixture.commit("candidate")
        write_source_evidence(
            fixture,
            release,
            candidate,
            reviewed=reviewed,
            source_digest=source_digest,
            signature=signature,
        )
        if extra is not None:
            fixture.write(extra, "unauthorized\n")
        fixture.commit("evidence")
        return fixture, candidate, declared

    def assert_error(self, errors: list[str], fragment: str) -> None:
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected {fragment!r} in {errors!r}",
        )

    def test_real_candidate_and_signed_source_evidence_pass(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate, declared = self.make_source_release(Path(directory))
            self.assertEqual(validate(fixture, "v0.1.0", candidate, declared), [])

    def test_undeclared_release_is_rejected_before_evidence(self) -> None:
        errors = plan_validator.validate_release(
            self.plan, "v0.201.1", REPOSITORY
        )
        self.assert_error(errors, "release is not declared by the roadmap")

    def test_nonexistent_candidate_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = GitFixture(Path(directory))
            errors = validate(fixture, "v0.1.0", "a" * 40, {"v0.1.0"})
        self.assert_error(errors, "candidate commit does not exist")

    def test_source_review_must_name_exact_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate, declared = self.make_source_release(
                Path(directory), reviewed="a" * 40
            )
            errors = validate(fixture, "v0.1.0", candidate, declared)
        self.assert_error(errors, "reviewed commit is not the exact candidate")

    def test_source_lock_digest_mutation_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate, declared = self.make_source_release(
                Path(directory), source_digest="0" * 64
            )
            errors = validate(fixture, "v0.1.0", candidate, declared)
        self.assert_error(errors, "source-lock digest does not match")

    def test_wrong_source_signature_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate, declared = self.make_source_release(
                Path(directory), signature="forged\n"
            )
            errors = validate(fixture, "v0.1.0", candidate, declared)
        self.assert_error(errors, "detached signature is invalid")

    def test_unauthorized_evidence_commit_change_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate, declared = self.make_source_release(
                Path(directory), extra="docs/changed.md"
            )
            errors = validate(fixture, "v0.1.0", candidate, declared)
        self.assert_error(errors, "evidence commit changes unauthorized paths")

    def test_dirty_worktree_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate, declared = self.make_source_release(Path(directory))
            fixture.write("untracked.txt", "dirty\n")
            errors = validate(fixture, "v0.1.0", candidate, declared)
        self.assert_error(errors, "worktree is not clean")

    def test_missing_predecessor_tag_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate, _declared = self.make_source_release(
                Path(directory), "v0.2.0", predecessors=("v0.1.0",)
            )
            errors = validate(
                fixture,
                "v0.2.0",
                candidate,
                {"v0.1.0", "v0.1.1", "v0.2.0"},
            )
        self.assert_error(errors, "missing annotated predecessor tag v0.1.1")

    def test_lightweight_predecessor_tag_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = GitFixture(Path(directory))
            fixture.commit("v0.1.0")
            fixture.tag("v0.1.0", annotated=False)
            candidate = fixture.commit("candidate")
            write_source_evidence(fixture, "v0.2.0", candidate)
            fixture.commit("evidence")
            errors = validate(
                fixture, "v0.2.0", candidate, {"v0.1.0", "v0.2.0"}
            )
        self.assert_error(errors, "missing annotated predecessor tag v0.1.0")

    def test_invalid_predecessor_signature_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate, declared = self.make_source_release(
                Path(directory), "v0.2.0", predecessors=("v0.1.0",)
            )
            errors = validate(
                fixture,
                "v0.2.0",
                candidate,
                declared,
                tag_verifier=lambda _root, _tag: False,
            )
        self.assert_error(errors, "predecessor tag v0.1.0 has no valid signature")

    def test_reused_predecessor_commit_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = GitFixture(Path(directory))
            shared = fixture.commit("shared")
            fixture.tag("v0.1.0", shared)
            fixture.tag("v0.1.1", shared)
            candidate = fixture.commit("candidate")
            write_source_evidence(fixture, "v0.2.0", candidate)
            fixture.commit("evidence")
            declared = {"v0.1.0", "v0.1.1", "v0.2.0"}
            errors = validate(fixture, "v0.2.0", candidate, declared)
        self.assert_error(errors, "predecessor tag v0.1.1 reuses a release commit")

    def test_out_of_order_predecessor_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = GitFixture(Path(directory))
            root = fixture.run("rev-parse", "HEAD")
            fixture.commit("later")
            fixture.tag("v0.1.0")
            fixture.tag("v0.1.1", root)
            candidate = fixture.commit("candidate")
            write_source_evidence(fixture, "v0.2.0", candidate)
            fixture.commit("evidence")
            declared = {"v0.1.0", "v0.1.1", "v0.2.0"}
            errors = validate(fixture, "v0.2.0", candidate, declared)
        self.assert_error(errors, "predecessor tag v0.1.1 is out of ancestry order")

    def test_nonancestor_predecessor_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = GitFixture(Path(directory))
            main = fixture.run("branch", "--show-current")
            fixture.run("switch", "-q", "-c", "side")
            fixture.commit("side")
            fixture.tag("v0.1.0")
            fixture.run("switch", "-q", main)
            candidate = fixture.commit("candidate")
            write_source_evidence(fixture, "v0.1.1", candidate)
            fixture.commit("evidence")
            errors = validate(
                fixture, "v0.1.1", candidate, {"v0.1.0", "v0.1.1"}
            )
        self.assert_error(errors, "predecessor tag v0.1.0 is not an ancestor")

    def test_candidate_cannot_reuse_predecessor_commit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = GitFixture(Path(directory))
            candidate = fixture.commit("candidate")
            fixture.tag("v0.1.0", candidate)
            write_source_evidence(fixture, "v0.1.1", candidate)
            fixture.commit("evidence")
            errors = validate(
                fixture, "v0.1.1", candidate, {"v0.1.0", "v0.1.1"}
            )
        self.assert_error(errors, "candidate reuses the last predecessor commit")

    def test_existing_target_tag_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate, declared = self.make_source_release(Path(directory))
            fixture.tag("v0.1.0", candidate)
            errors = validate(fixture, "v0.1.0", candidate, declared)
        self.assert_error(errors, "v0.1.0: tag already exists")

    def make_boundary_release(
        self,
        root: Path,
        *,
        reviewed: str | None = None,
        scope: str = "docs/scope.md",
        plan_digest: str = BOUNDARY_DIGEST,
        support_digest: str | None = None,
        signature: str = "valid\n",
        mutate_scope: bool = False,
    ) -> tuple[GitFixture, str, dict[str, dict[str, str]]]:
        fixture = GitFixture(root)
        review_commit = fixture.run("rev-parse", "HEAD")
        if mutate_scope:
            fixture.write("docs/scope.md", "changed after review\n")
        candidate = fixture.commit("candidate")
        write_source_evidence(fixture, "v0.1.0", candidate)
        entry = write_boundary_evidence(
            fixture,
            candidate,
            reviewed=reviewed or (review_commit if mutate_scope else candidate),
            scope=scope,
            plan_digest=plan_digest,
            support_digest=support_digest,
            signature=signature,
        )
        fixture.commit("evidence")
        return fixture, candidate, {"sqlite": entry}

    def test_real_boundary_review_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate, boundaries = self.make_boundary_release(Path(directory))
            errors = validate(
                fixture,
                "v0.1.0",
                candidate,
                {"v0.1.0"},
                boundaries=boundaries,
            )
        self.assertEqual(errors, [])

    def test_nonexistent_boundary_review_commit_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate, boundaries = self.make_boundary_release(
                Path(directory), reviewed="a" * 40
            )
            errors = validate(
                fixture,
                "v0.1.0",
                candidate,
                {"v0.1.0"},
                boundaries=boundaries,
            )
        self.assert_error(errors, "reviewed commit does not exist")

    def test_later_scoped_change_invalidates_boundary_review(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate, boundaries = self.make_boundary_release(
                Path(directory), mutate_scope=True
            )
            errors = validate(
                fixture,
                "v0.1.0",
                candidate,
                {"v0.1.0"},
                boundaries=boundaries,
            )
        self.assert_error(errors, "reviewed scope changed after review")

    def test_boundary_plan_digest_mutation_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate, boundaries = self.make_boundary_release(
                Path(directory), plan_digest="0" * 64
            )
            errors = validate(
                fixture,
                "v0.1.0",
                candidate,
                {"v0.1.0"},
                boundaries=boundaries,
            )
        self.assert_error(errors, "Boundary-Plan-Digest does not match")

    def test_boundary_support_digest_mutation_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate, boundaries = self.make_boundary_release(
                Path(directory), support_digest="0" * 64
            )
            errors = validate(
                fixture,
                "v0.1.0",
                candidate,
                {"v0.1.0"},
                boundaries=boundaries,
            )
        self.assert_error(errors, "supporting evidence digest does not match")

    def test_wrong_boundary_signature_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate, boundaries = self.make_boundary_release(
                Path(directory), signature="forged\n"
            )
            errors = validate(
                fixture,
                "v0.1.0",
                candidate,
                {"v0.1.0"},
                boundaries=boundaries,
            )
        self.assert_error(errors, "detached signature is invalid")

    def test_consuming_release_requires_implementation_scope(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture, candidate, boundaries = self.make_boundary_release(Path(directory))
            boundaries["sqlite"]["required_by"] = "v0.1.0"
            errors = validate(
                fixture,
                "v0.1.0",
                candidate,
                {"v0.1.0"},
                boundaries=boundaries,
            )
        self.assert_error(errors, "consuming release must cover crates/gestur-db-sqlite")


if __name__ == "__main__":
    unittest.main()
