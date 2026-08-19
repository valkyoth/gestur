#!/usr/bin/env python3
"""Positive and fail-closed tests for the detailed version-plan validator."""

from __future__ import annotations

import re
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY / "scripts"))

import validate_detailed_version_plan as validator  # noqa: E402


class DetailedVersionPlanValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.plan = (REPOSITORY / "docs/DETAILED_VERSION_PLAN.md").read_text(
            encoding="utf-8"
        )
        cls.release = (REPOSITORY / "docs/RELEASE_PLAN.md").read_text(
            encoding="utf-8"
        )

    def errors_for(self, plan: str) -> list[str]:
        return validator.validate(plan, self.release)

    def errors_for_on(self, plan: str, today: date) -> list[str]:
        return validator.validate(plan, self.release, today=today)

    def assert_rejected(self, plan: str, fragment: str) -> None:
        errors = self.errors_for(plan)
        self.assertTrue(errors, "mutated plan unexpectedly passed")
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected {fragment!r} in {errors!r}",
        )

    def qualify_boundaries(self, plan: str) -> str:
        def replacement(match: re.Match[str]) -> str:
            boundary = match.group(1)
            return (
                f"- {boundary} | decision-by={match.group(2)} "
                f"| required-by={match.group(3)} | status=qualified "
                f"| evidence=evidence/feasibility/{boundary}.md"
            )

        section_errors: list[str] = []
        section = validator.marked_section(
            plan,
            validator.BOUNDARY_START,
            validator.BOUNDARY_END,
            section_errors,
        )
        self.assertEqual(section_errors, [])
        updated = "\n".join(
            replacement(match) if (match := validator.BOUNDARY_RE.fullmatch(line)) else line
            for line in section.split("\n")
        )
        return plan.replace(section, updated)

    def write_release_evidence(
        self, root: Path, plan: str, release: str, *, blocked: set[str] | None = None
    ) -> None:
        blocked = blocked or set()
        for boundary in validator.REQUIRED_BOUNDARIES:
            path = root / "evidence" / "feasibility" / f"{boundary}.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            status = "BLOCKED" if boundary in blocked else "QUALIFIED"
            path.write_text(
                f"Boundary: {boundary}\n"
                f"Status: {status}\n"
                f"Reviewed-Commit: {'a' * 40}\n",
                encoding="utf-8",
            )
        attestation = root / "evidence" / "source-freshness" / f"{release}.md"
        attestation.parent.mkdir(parents=True, exist_ok=True)
        attestation.write_text(
            "Status: PASS\n"
            f"Date: {date.today().isoformat()}\n"
            f"Source-Lock-Digest: {validator.source_lock_digest(plan)}\n",
            encoding="utf-8",
        )

    def test_repository_plan_is_valid(self) -> None:
        self.assertEqual(self.errors_for(self.plan), [])

    def test_duplicate_stop_fails_closed(self) -> None:
        row = next(line for line in self.plan.splitlines() if line.startswith("| v0.1.1 |"))
        self.assert_rejected(
            self.plan.replace(row, f"{row}\n{row}"), "duplicate detailed stops"
        )

    def test_deleted_stop_fails_train_declaration(self) -> None:
        row = next(
            line for line in self.plan.splitlines() if line.startswith("| v0.45.2 |")
        )
        self.assert_rejected(
            self.plan.replace(f"{row}\n", ""),
            "declared detailed stops do not match register",
        )

    def test_out_of_order_stop_fails_closed(self) -> None:
        first = next(line for line in self.plan.splitlines() if line.startswith("| v0.1.1 |"))
        second = next(line for line in self.plan.splitlines() if line.startswith("| v0.2.1 |"))
        mutated = self.plan.replace(first, "ORDER_PLACEHOLDER").replace(second, first)
        mutated = mutated.replace("ORDER_PLACEHOLDER", second)
        self.assert_rejected(mutated, "not strictly increasing")

    def test_unexpanded_range_fails_closed(self) -> None:
        mutated = self.plan.replace("| v0.1.1 |", "| v0.1.1–v0.1.2 |", 1)
        self.assert_rejected(mutated, "invalid or unexpanded version")

    def test_missing_proof_fails_closed(self) -> None:
        row = next(line for line in self.plan.splitlines() if line.startswith("| v0.1.1 |"))
        cells = row.split("|")
        cells[3] = " "
        self.assert_rejected(self.plan.replace(row, "|".join(cells)), "missing mandatory proof")

    def test_invalid_base_owner_fails_closed(self) -> None:
        mutated = self.plan.replace("| v0.1.1 |", "| v0.201.1 |", 1)
        self.assert_rejected(mutated, "no valid v0.N.0 owner")

    def test_missing_train_declaration_fails_closed(self) -> None:
        declaration = "- v0.50.0: v0.50.1, v0.50.2, v0.50.3\n"
        self.assert_rejected(
            self.plan.replace(declaration, ""), "missing train declarations"
        )

    def test_missing_required_dependency_fails_closed(self) -> None:
        lock = "- v0.12.1 <- v0.10.2, v0.11.1, v0.11.3, v0.11.5\n"
        self.assert_rejected(
            self.plan.replace(lock, ""), "missing required dependency locks"
        )

    def test_future_dependency_fails_closed(self) -> None:
        old = "- v0.12.1 <- v0.10.2, v0.11.1, v0.11.3, v0.11.5"
        self.assert_rejected(
            self.plan.replace(old, f"{old}, v0.200.1"),
            "prerequisite does not precede",
        )

    def test_missing_boundary_fails_closed(self) -> None:
        entry = (
            "- sqlite | decision-by=v0.10.2 | required-by=v0.12.1 "
            "| status=pending | evidence=none\n"
        )
        self.assert_rejected(
            self.plan.replace(entry, ""), "missing boundary feasibility entries"
        )

    def test_decided_boundary_requires_evidence(self) -> None:
        old = (
            "- sqlite | decision-by=v0.10.2 | required-by=v0.12.1 "
            "| status=pending | evidence=none"
        )
        new = old.replace("status=pending", "status=qualified")
        self.assert_rejected(
            self.plan.replace(old, new), "qualified status requires evidence"
        )

    def test_missing_source_lock_fails_closed(self) -> None:
        line = next(
            line for line in self.plan.splitlines() if line.startswith("- ofac |")
        )
        self.assert_rejected(
            self.plan.replace(f"{line}\n", ""), "missing source locks: ofac"
        )

    def test_stale_source_lock_fails_closed(self) -> None:
        mutated = self.plan.replace(
            "- semver | revision=2.0.0 | checked=2026-08-19 | max-age-days=365",
            "- semver | revision=2.0.0 | checked=2025-01-01 | max-age-days=365",
        )
        errors = self.errors_for_on(mutated, date(2026, 8, 19))
        self.assertTrue(any("semver: source lock is stale" in error for error in errors))

    def test_source_maximum_age_cannot_be_silently_widened(self) -> None:
        mutated = self.plan.replace("max-age-days=30", "max-age-days=30000", 1)
        self.assert_rejected(mutated, "source maximum age does not match policy")

    def test_missing_register_marker_fails_closed(self) -> None:
        mutated = self.plan.replace(validator.REGISTER_END, "", 1)
        self.assert_rejected(mutated, "expected exactly one")

    def test_release_feasibility_passes_with_qualified_evidence(self) -> None:
        plan = self.qualify_boundaries(self.plan)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_release_evidence(root, plan, "v0.10.2")
            self.assertEqual(
                validator.validate_release(plan, "v0.10.2", root),
                [],
            )

    def test_pending_boundary_blocks_decision_release(self) -> None:
        plan = self.qualify_boundaries(self.plan)
        qualified = (
            "- sqlite | decision-by=v0.10.2 | required-by=v0.12.1 "
            "| status=qualified | evidence=evidence/feasibility/sqlite.md"
        )
        pending = (
            "- sqlite | decision-by=v0.10.2 | required-by=v0.12.1 "
            "| status=pending | evidence=none"
        )
        plan = plan.replace(qualified, pending)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_release_evidence(root, plan, "v0.10.2")
            errors = validator.validate_release(plan, "v0.10.2", root)
        self.assertTrue(
            any("sqlite: pending feasibility decision blocks" in error for error in errors)
        )

    def test_blocked_boundary_blocks_consuming_release(self) -> None:
        plan = self.qualify_boundaries(self.plan)
        qualified = (
            "- sqlite | decision-by=v0.10.2 | required-by=v0.12.1 "
            "| status=qualified | evidence=evidence/feasibility/sqlite.md"
        )
        blocked = qualified.replace("status=qualified", "status=blocked")
        plan = plan.replace(qualified, blocked)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_release_evidence(root, plan, "v0.12.1", blocked={"sqlite"})
            errors = validator.validate_release(plan, "v0.12.1", root)
        self.assertTrue(
            any("sqlite: v0.12.1 requires qualified feasibility" in error for error in errors)
        )

    def test_source_attestation_digest_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "evidence" / "source-freshness" / "v0.1.0.md"
            path.parent.mkdir(parents=True)
            path.write_text(
                "Status: PASS\n"
                f"Date: {date.today().isoformat()}\n"
                f"Source-Lock-Digest: {'0' * 64}\n",
                encoding="utf-8",
            )
            errors = validator.validate_release(self.plan, "v0.1.0", root)
        self.assertTrue(any("source-lock digest does not match" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
