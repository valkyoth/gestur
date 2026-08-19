#!/usr/bin/env python3
"""Validate Gestur's active crate boundaries and source-shape policy."""

from __future__ import annotations

import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_DEPENDENCIES = {
    "gestur": {
        "gestur-api-types",
        "gestur-core",
        "gestur-crypto-types",
        "gestur-events",
        "gestur-policy",
        "gestur-schema",
        "gestur-workflow",
    },
    "gestur-api-types": {"gestur-core", "gestur-policy"},
    "gestur-core": set(),
    "gestur-crypto-types": set(),
    "gestur-events": {"gestur-core"},
    "gestur-policy": {"gestur-core"},
    "gestur-schema": {"gestur-core"},
    "gestur-testkit": {"gestur-core"},
    "gestur-workflow": {"gestur-core", "gestur-schema"},
}
EXPECTED_DEV_DEPENDENCIES = {"gestur": {"gestur-testkit"}}


def table_dependencies(document: dict[str, object], name: str) -> set[str]:
    table = document.get(name, {})
    return set(table) if isinstance(table, dict) else set()


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    workspace_manifest = root / "Cargo.toml"
    if workspace_manifest.is_file():
        document = tomllib.loads(workspace_manifest.read_text(encoding="utf-8"))
        workspace = document.get("workspace", {})
        if not isinstance(workspace, dict):
            errors.append("root manifest has no workspace table")
        else:
            expected_members = {f"crates/{crate}" for crate in EXPECTED_DEPENDENCIES}
            members = set(workspace.get("members", ()))
            if members != expected_members:
                errors.append("workspace members differ from the active crate set")
            if workspace.get("default-members") != ["crates/gestur"]:
                errors.append("gestur must be the sole default workspace member")
            dependencies = workspace.get("dependencies", {})
            dependency_names = set(dependencies) if isinstance(dependencies, dict) else set()
            if dependency_names != set(EXPECTED_DEPENDENCIES) - {"gestur"}:
                errors.append("workspace dependency declarations differ")
    else:
        errors.append("root workspace manifest is missing")

    crates = root / "crates"
    actual = {
        path.name
        for path in crates.iterdir()
        if path.is_dir() and (path / "Cargo.toml").is_file()
    } if crates.is_dir() else set()
    expected = set(EXPECTED_DEPENDENCIES)
    if actual != expected:
        errors.append(
            "active crate set differs: "
            f"missing={sorted(expected - actual)}, unexpected={sorted(actual - expected)}"
        )

    for crate in sorted(expected & actual):
        crate_root = crates / crate
        manifest = tomllib.loads(
            (crate_root / "Cargo.toml").read_text(encoding="utf-8")
        )
        package = manifest.get("package", {})
        if not isinstance(package, dict) or package.get("name") != crate:
            errors.append(f"{crate}: manifest package name does not match directory")
        for table_name, required in (
            ("dependencies", EXPECTED_DEPENDENCIES[crate]),
            ("dev-dependencies", EXPECTED_DEV_DEPENDENCIES.get(crate, set())),
            ("build-dependencies", set()),
        ):
            dependencies = table_dependencies(manifest, table_name)
            if dependencies != required:
                errors.append(
                    f"{crate}: {table_name} boundary differs: "
                    f"missing={sorted(required - dependencies)}, "
                    f"unexpected={sorted(dependencies - required)}"
                )

        library = crate_root / "src/lib.rs"
        if not library.is_file():
            errors.append(f"{crate}: src/lib.rs is missing")
            continue
        lines = library.read_text(encoding="utf-8").splitlines()
        if "#![no_std]" not in lines:
            errors.append(f"{crate}: no_std is missing")
        if "#![forbid(unsafe_code)]" not in lines:
            errors.append(f"{crate}: unsafe-code prohibition is missing")

    for directory in (root / "crates", root / "scripts"):
        if not directory.is_dir():
            continue
        for source in directory.rglob("*"):
            if source.is_file() and source.suffix in {".rs", ".py", ".sh"}:
                line_count = len(source.read_text(encoding="utf-8").splitlines())
                if line_count > 500:
                    errors.append(
                        f"{source.relative_to(root)}: {line_count} lines exceeds 500"
                    )
    return errors


def main() -> int:
    errors = validate(ROOT)
    if errors:
        for error in errors:
            print(error)
        return 1
    print("active crate boundaries, no_std posture, and source limits are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
