#!/usr/bin/env python3
"""Adversarial tests for the active-crate modularity policy."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY / "scripts"))

from validate_modularity_policy import (  # noqa: E402
    EXPECTED_DEPENDENCIES,
    EXPECTED_DEV_DEPENDENCIES,
    validate,
)


class ModularityPolicyTests(unittest.TestCase):
    def fixture(self, root: Path) -> None:
        members = ", ".join(
            f'"crates/{crate}"' for crate in sorted(EXPECTED_DEPENDENCIES)
        )
        workspace_dependencies = "".join(
            f'{crate} = {{ path = "crates/{crate}" }}\n'
            for crate in sorted(set(EXPECTED_DEPENDENCIES) - {"gestur"})
        )
        (root / "Cargo.toml").write_text(
            f"[workspace]\nmembers = [{members}]\n"
            'default-members = ["crates/gestur"]\n'
            f"[workspace.dependencies]\n{workspace_dependencies}",
            encoding="utf-8",
        )
        for crate, dependencies in EXPECTED_DEPENDENCIES.items():
            crate_root = root / "crates" / crate
            (crate_root / "src").mkdir(parents=True)
            dependency_text = "".join(
                f'{dependency} = {{ path = "../{dependency}" }}\n'
                for dependency in sorted(dependencies)
            )
            dev_dependency_text = "".join(
                f'{dependency} = {{ path = "../{dependency}" }}\n'
                for dependency in sorted(EXPECTED_DEV_DEPENDENCIES.get(crate, set()))
            )
            (crate_root / "Cargo.toml").write_text(
                f'[package]\nname = "{crate}"\nversion = "0.1.0"\n'
                f"[dependencies]\n{dependency_text}"
                f"[dev-dependencies]\n{dev_dependency_text}",
                encoding="utf-8",
            )
            (crate_root / "src/lib.rs").write_text(
                "#![no_std]\n#![forbid(unsafe_code)]\n",
                encoding="utf-8",
            )

    def assert_error(self, errors: list[str], fragment: str) -> None:
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected {fragment!r} in {errors!r}",
        )

    def test_declared_foundation_graph_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            self.assertEqual(validate(root), [])

    def test_reverse_dependency_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            manifest = root / "crates/gestur-core/Cargo.toml"
            manifest.write_text(
                manifest.read_text(encoding="utf-8").replace(
                    "[dependencies]\n",
                    '[dependencies]\ngestur = { path = "../gestur" }\n',
                    1,
                ),
                encoding="utf-8",
            )
            self.assert_error(validate(root), "gestur-core: dependencies boundary")

    def test_hidden_workspace_dependency_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            manifest = root / "Cargo.toml"
            manifest.write_text(
                manifest.read_text(encoding="utf-8")
                + 'unused = { path = "crates/gestur" }\n',
                encoding="utf-8",
            )
            self.assert_error(validate(root), "workspace dependency declarations differ")

    def test_testkit_cannot_enter_facade_runtime(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            manifest = root / "crates/gestur/Cargo.toml"
            content = manifest.read_text(encoding="utf-8")
            manifest.write_text(
                content.replace(
                    "[dependencies]\n",
                    '[dependencies]\ngestur-testkit = { path = "../gestur-testkit" }\n',
                    1,
                ).replace(
                    '[dev-dependencies]\ngestur-testkit = { path = "../gestur-testkit" }\n',
                    "[dev-dependencies]\n",
                ),
                encoding="utf-8",
            )
            self.assert_error(validate(root), "gestur: dependencies boundary")

    def test_missing_no_std_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            (root / "crates/gestur-core/src/lib.rs").write_text(
                "#![forbid(unsafe_code)]\n", encoding="utf-8"
            )
            self.assert_error(validate(root), "gestur-core: no_std is missing")

    def test_missing_unsafe_prohibition_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            (root / "crates/gestur-core/src/lib.rs").write_text(
                "#![no_std]\n", encoding="utf-8"
            )
            self.assert_error(
                validate(root), "gestur-core: unsafe-code prohibition is missing"
            )

    def test_missing_crate_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            manifest = root / "crates/gestur-core/Cargo.toml"
            manifest.unlink()
            self.assert_error(validate(root), "active crate set differs")

    def test_oversized_source_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            (root / "crates/gestur-core/src/oversized.rs").write_text(
                "line\n" * 501, encoding="utf-8"
            )
            self.assert_error(validate(root), "501 lines exceeds 500")


if __name__ == "__main__":
    unittest.main()
