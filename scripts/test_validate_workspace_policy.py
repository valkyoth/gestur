#!/usr/bin/env python3
"""Mutation tests for private, first-party-only Cargo workspace policy."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
VALIDATOR = REPOSITORY / "scripts/validate-workspace-policy.py"
SPEC = importlib.util.spec_from_file_location("workspace_policy", VALIDATOR)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load workspace policy validator")
WORKSPACE_POLICY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(WORKSPACE_POLICY)


class WorkspacePolicyTests(unittest.TestCase):
    def fixture(self, root: Path, dependency: str = "") -> Path:
        crate = root / "crates/example"
        crate.mkdir(parents=True)
        (root / "Cargo.toml").write_text(
            "[workspace]\n"
            'members = ["crates/example"]\n'
            "[workspace.package]\n"
            'license = "EUPL-1.2"\n'
            "publish = false\n",
            encoding="utf-8",
        )
        manifest = crate / "Cargo.toml"
        manifest.write_text(
            "[package]\n"
            'name = "example"\n'
            'version = "0.1.0"\n'
            "license.workspace = true\n"
            "publish.workspace = true\n"
            f"{dependency}",
            encoding="utf-8",
        )
        return manifest

    def assert_error(self, errors: list[str], fragment: str) -> None:
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected {fragment!r} in {errors!r}",
        )

    def test_private_first_party_fixture_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            self.assertEqual(WORKSPACE_POLICY.validate_static(root), [])

    def test_publishable_workspace_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            workspace = root / "Cargo.toml"
            workspace.write_text(
                workspace.read_text(encoding="utf-8").replace(
                    "publish = false", "publish = true"
                ),
                encoding="utf-8",
            )
            self.assert_error(
                WORKSPACE_POLICY.validate_static(root),
                "workspace.package.publish must be false",
            )

    def test_workspace_license_cannot_change_silently(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            workspace = root / "Cargo.toml"
            workspace.write_text(
                workspace.read_text(encoding="utf-8").replace(
                    'license = "EUPL-1.2"', 'license = "MIT"'
                ),
                encoding="utf-8",
            )
            self.assert_error(
                WORKSPACE_POLICY.validate_static(root),
                "workspace license must be EUPL-1.2",
            )

    def test_package_must_inherit_publish_false(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = self.fixture(root)
            manifest.write_text(
                manifest.read_text(encoding="utf-8").replace(
                    "publish.workspace = true", "publish = false"
                ),
                encoding="utf-8",
            )
            self.assert_error(
                WORKSPACE_POLICY.validate_static(root), "must inherit publish = false"
            )

    def test_registry_dependency_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root, '\n[dependencies]\nserde = "1"\n')
            self.assert_error(
                WORKSPACE_POLICY.validate_static(root), "external dependency forbidden"
            )

    def test_workspace_registry_dependency_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            workspace = root / "Cargo.toml"
            workspace.write_text(
                workspace.read_text(encoding="utf-8")
                + '\n[workspace.dependencies]\nforeign = "1"\n',
                encoding="utf-8",
            )
            self.assert_error(
                WORKSPACE_POLICY.validate_static(root),
                "workspace dependency is not an in-tree path",
            )

    def test_git_dependency_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(
                root,
                '\n[build-dependencies]\nforeign = { git = "https://example.invalid" }\n',
            )
            self.assert_error(
                WORKSPACE_POLICY.validate_static(root), "external dependency forbidden"
            )

    def test_out_of_tree_path_dependency_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "workspace"
            root.mkdir()
            self.fixture(
                root,
                '\n[dependencies]\nforeign = { path = "../../foreign" }\n',
            )
            self.assert_error(
                WORKSPACE_POLICY.validate_static(root), "external dependency forbidden"
            )

    def test_target_dependency_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(
                root,
                "\n[target.'cfg(unix)'.dependencies]\nforeign = { version = \"1\" }\n",
            )
            self.assert_error(
                WORKSPACE_POLICY.validate_static(root), "external dependency forbidden"
            )


if __name__ == "__main__":
    unittest.main()
