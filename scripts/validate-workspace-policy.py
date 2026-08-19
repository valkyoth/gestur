#!/usr/bin/env python3
"""Enforce Gestur's private, first-party-only Cargo workspace policy."""

from __future__ import annotations

import json
import subprocess
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def manifests(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("Cargo.toml")
        if not any(part in {".git", "target"} for part in path.parts)
    )


def dependency_tables(document: dict[str, object]):
    for name in ("dependencies", "dev-dependencies", "build-dependencies"):
        table = document.get(name, {})
        if isinstance(table, dict):
            yield name, table
    target = document.get("target", {})
    if isinstance(target, dict):
        for target_table in target.values():
            if isinstance(target_table, dict):
                for name in ("dependencies", "dev-dependencies", "build-dependencies"):
                    table = target_table.get(name, {})
                    if isinstance(table, dict):
                        yield name, table


def path_is_inside(root: Path, manifest: Path, relative: str) -> bool:
    try:
        dependency = (manifest.parent / relative).resolve()
        dependency.relative_to(root.resolve())
    except ValueError:
        return False
    return (dependency / "Cargo.toml").is_file()


def validate_static(root: Path) -> list[str]:
    errors: list[str] = []
    root_manifest = root / "Cargo.toml"
    if not root_manifest.is_file():
        return ["workspace Cargo.toml is missing"]
    document = tomllib.loads(root_manifest.read_text(encoding="utf-8"))
    workspace = document.get("workspace", {})
    package_defaults = workspace.get("package", {}) if isinstance(workspace, dict) else {}
    if not isinstance(package_defaults, dict) or package_defaults.get("publish") is not False:
        errors.append("workspace.package.publish must be false")
    if not isinstance(package_defaults, dict) or package_defaults.get("license") != "EUPL-1.2":
        errors.append("workspace license must be EUPL-1.2")
    workspace_dependencies = (
        workspace.get("dependencies", {}) if isinstance(workspace, dict) else {}
    )
    if isinstance(workspace_dependencies, dict):
        for name, specification in workspace_dependencies.items():
            path = specification.get("path") if isinstance(specification, dict) else None
            if not isinstance(path, str) or not path_is_inside(root, root_manifest, path):
                errors.append(f"workspace dependency is not an in-tree path: {name}")

    for manifest in manifests(root):
        manifest_document = tomllib.loads(manifest.read_text(encoding="utf-8"))
        package = manifest_document.get("package")
        if isinstance(package, dict) and package.get("publish") != {"workspace": True}:
            errors.append(f"{manifest.relative_to(root)}: package must inherit publish = false")
        for table_name, table in dependency_tables(manifest_document):
            for name, specification in table.items():
                workspace_reference = (
                    isinstance(specification, dict)
                    and specification.get("workspace") is True
                    and name in workspace_dependencies
                )
                path = specification.get("path") if isinstance(specification, dict) else None
                local_path = isinstance(path, str) and path_is_inside(
                    root, manifest, path
                )
                if not (workspace_reference or local_path):
                    errors.append(
                        f"{manifest.relative_to(root)}: external dependency forbidden "
                        f"in {table_name}: {name}"
                    )
    return errors


def validate_resolved(root: Path) -> list[str]:
    result = subprocess.run(
        ["cargo", "metadata", "--format-version", "1", "--locked", "--offline"],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        return ["cargo metadata failed under locked offline policy"]
    metadata = json.loads(result.stdout)
    errors: list[str] = []
    for package in metadata["packages"]:
        manifest = Path(package["manifest_path"]).resolve()
        try:
            manifest.relative_to(root.resolve())
        except ValueError:
            errors.append(f"{package['name']}: resolved package is outside the workspace")
        if package.get("publish") != []:
            errors.append(f"{package['name']}: resolved package is publishable")
        for dependency in package["dependencies"]:
            if dependency.get("source") is not None:
                errors.append(
                    f"{package['name']}: resolved external dependency "
                    f"{dependency['name']} is forbidden"
                )
    return errors


def main() -> int:
    errors = validate_static(ROOT)
    if not errors:
        errors.extend(validate_resolved(ROOT))
    if errors:
        for error in errors:
            print(error)
        return 1
    print("all Cargo packages are private and first-party-only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
