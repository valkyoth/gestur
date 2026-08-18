#!/usr/bin/env python3
"""Enforce Gestur's private, first-party-only Cargo workspace policy."""

from __future__ import annotations

import json
import subprocess
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def manifests() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("Cargo.toml")
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


def main() -> int:
    root = tomllib.loads((ROOT / "Cargo.toml").read_text(encoding="utf-8"))
    package_defaults = root["workspace"]["package"]
    if package_defaults.get("publish") is not False:
        raise SystemExit("workspace.package.publish must be false")
    if package_defaults.get("license") != "EUPL-1.2":
        raise SystemExit("workspace license must be EUPL-1.2")

    for manifest in manifests():
        document = tomllib.loads(manifest.read_text(encoding="utf-8"))
        package = document.get("package")
        if isinstance(package, dict):
            if package.get("publish") != {"workspace": True}:
                raise SystemExit(f"{manifest}: package must inherit publish = false")
        for table_name, table in dependency_tables(document):
            for name, specification in table.items():
                if not (
                    isinstance(specification, dict)
                    and (
                        specification.get("workspace") is True
                        or isinstance(specification.get("path"), str)
                    )
                ):
                    raise SystemExit(
                        f"{manifest}: external dependency forbidden in "
                        f"{table_name}: {name}"
                    )

    output = subprocess.check_output(
        ["cargo", "metadata", "--format-version", "1", "--locked", "--offline"],
        cwd=ROOT,
        text=True,
    )
    metadata = json.loads(output)
    for package in metadata["packages"]:
        if package.get("publish") != []:
            raise SystemExit(f"{package['name']}: resolved package is publishable")
        for dependency in package["dependencies"]:
            if dependency.get("source") is not None:
                raise SystemExit(
                    f"{package['name']}: resolved external dependency "
                    f"{dependency['name']} is forbidden"
                )
    print("all Cargo packages are private and first-party-only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
