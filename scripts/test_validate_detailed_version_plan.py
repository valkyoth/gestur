#!/usr/bin/env python3
"""Positive and fail-closed tests for the detailed version-plan validator."""

from __future__ import annotations

import sys
import unittest
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

    def assert_rejected(self, plan: str, fragment: str) -> None:
        errors = self.errors_for(plan)
        self.assertTrue(errors, "mutated plan unexpectedly passed")
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected {fragment!r} in {errors!r}",
        )

    def test_repository_plan_is_valid(self) -> None:
        self.assertEqual(self.errors_for(self.plan), [])

    def test_duplicate_stop_fails_closed(self) -> None:
        row = next(line for line in self.plan.splitlines() if line.startswith("| v0.1.1 |"))
        self.assert_rejected(self.plan.replace(row, f"{row}\n{row}"), "duplicate detailed stops")

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
        mutated = self.plan.replace(row, "|".join(cells))
        self.assert_rejected(mutated, "missing mandatory proof")

    def test_invalid_base_owner_fails_closed(self) -> None:
        mutated = self.plan.replace("| v0.1.1 |", "| v0.201.1 |", 1)
        self.assert_rejected(mutated, "no valid v0.N.0 owner")

    def test_missing_required_dependency_fails_closed(self) -> None:
        lock = "- v0.12.1 <- v0.10.2, v0.11.1, v0.11.3, v0.11.5\n"
        self.assert_rejected(self.plan.replace(lock, ""), "missing required dependency locks")

    def test_future_dependency_fails_closed(self) -> None:
        old = "- v0.12.1 <- v0.10.2, v0.11.1, v0.11.3, v0.11.5"
        new = f"{old}, v0.200.1"
        self.assert_rejected(self.plan.replace(old, new), "prerequisite does not precede")

    def test_missing_source_lock_fails_closed(self) -> None:
        mutated = self.plan.replace("https://ofac.treasury.gov/sanctions-list-service", "")
        self.assert_rejected(mutated, "missing required source lock: OFAC")

    def test_missing_register_marker_fails_closed(self) -> None:
        mutated = self.plan.replace(validator.REGISTER_END, "", 1)
        self.assert_rejected(mutated, "expected exactly one")


if __name__ == "__main__":
    unittest.main()
