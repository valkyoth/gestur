#!/usr/bin/env python3
"""Fail-closed structural validation for Gestur's detailed version plan."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REGISTER_START = "<!-- detailed-stop-register:start -->"
REGISTER_END = "<!-- detailed-stop-register:end -->"
DEPENDENCY_START = "<!-- dependency-locks:start -->"
DEPENDENCY_END = "<!-- dependency-locks:end -->"

VERSION_RE = re.compile(r"^v(0)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$|^v1\.0\.0$")
BASE_RE = re.compile(r"^## (v0\.([1-9][0-9]*)\.0) — ", re.MULTILINE)
DEPENDENCY_RE = re.compile(r"^- (v(?:0\.[0-9]+\.[0-9]+|1\.0\.0)) <- (.+)$")

REQUIRED_EDGES = {
    "v0.12.1": {"v0.10.2", "v0.11.1", "v0.11.3", "v0.11.5"},
    "v0.32.1": {"v0.3.6", "v0.3.7", "v0.11.5", "v0.30.1"},
    "v0.46.1": {"v0.45.6"},
    "v0.48.9": {"v0.46.2", "v0.48.8"},
    "v0.50.1": {"v0.48.9"},
    "v0.71.1": {"v0.10.2", "v0.10.3", "v0.19.1", "v0.29.1"},
    "v0.87.1": {"v0.10.2", "v0.10.3", "v0.19.1"},
    "v0.92.1": {"v0.3.5", "v0.27.1", "v0.91.1", "v0.92.0"},
    "v0.93.1": {"v0.92.4"},
    "v0.111.1": {"v0.46.2", "v0.87.1"},
    "v0.112.1": {"v0.10.2", "v0.111.1"},
    "v0.133.1": {"v0.92.4"},
    "v0.141.1": {"v0.46.2"},
    "v0.166.1": {"v0.3.7", "v0.10.2"},
    "v0.168.1": {"v0.58.2", "v0.140.1", "v0.166.1", "v0.167.1", "v0.167.2"},
    "v0.200.1": {"v0.199.1"},
}

REQUIRED_SOURCES = {
    "Semantic Versioning 2.0.0": "https://semver.org/",
    "WCAG 2.2": "https://www.w3.org/TR/WCAG22/",
    "NIST SP 800-63-4": "https://csrc.nist.gov/pubs/sp/800/63/4/final",
    "NIST SP 800-88 Rev. 2": "https://csrc.nist.gov/pubs/sp/800/88/r2/final",
    "GDPR Regulation (EU) 2016/679": "https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng",
    "California CCPA/CPRA laws and regulations": "https://cppa.ca.gov/regulations/",
    "Consolidated eIDAS Regulation": "https://eur-lex.europa.eu/eli/reg/2014/910/2024-10-18/eng",
    "OFAC Sanctions List Service": "https://ofac.treasury.gov/sanctions-list-service",
    "Export Administration Regulations": "https://www.ecfr.gov/current/title-15/subtitle-B/chapter-VII/subchapter-C",
    "International Traffic in Arms Regulations": "https://www.ecfr.gov/current/title-22/chapter-I/subchapter-M",
    "NIST FIPS 201-3": "https://csrc.nist.gov/pubs/fips/201-3/final",
}

REQUIRED_CONTRACT_TEXT = (
    "**Goal:**",
    "**Deliverables:**",
    "evidence-index entry",
    "**Verification:**",
    "real implementation",
    "**Exit criteria:**",
    "independent pentest",
)


def version_key(version: str) -> tuple[int, int, int]:
    major, minor, patch = version.removeprefix("v").split(".")
    return int(major), int(minor), int(patch)


def marked_section(text: str, start: str, end: str, errors: list[str]) -> str:
    if text.count(start) != 1 or text.count(end) != 1:
        errors.append(f"expected exactly one {start!r} and {end!r} marker")
        return ""
    start_index = text.index(start)
    end_index = text.index(end)
    if start_index >= end_index:
        errors.append(f"invalid marker ordering for {start!r}")
        return ""
    return text[start_index + len(start) : end_index]


def parse_stop_rows(section: str, errors: list[str]) -> list[tuple[str, str, str, int]]:
    rows: list[tuple[str, str, str, int]] = []
    for line_number, line in enumerate(section.splitlines(), start=1):
        if not line.startswith("| v"):
            continue
        cells = [cell.strip() for cell in line.split("|")]
        if len(cells) != 5 or cells[0] or cells[-1]:
            errors.append(f"register line {line_number}: malformed three-column stop row")
            continue
        version, deliverable, proof = cells[1:4]
        if not VERSION_RE.fullmatch(version):
            errors.append(f"register line {line_number}: invalid or unexpanded version {version!r}")
            continue
        if len(deliverable) < 20 or deliverable.casefold() in {"tbd", "todo"}:
            errors.append(f"{version}: missing concrete sole deliverable")
        if "one per stop" in deliverable.casefold():
            errors.append(f"{version}: grouped deliverables are forbidden")
        if len(proof) < 20 or proof.casefold() in {"tbd", "todo"}:
            errors.append(f"{version}: missing mandatory proof")
        rows.append((version, deliverable, proof, line_number))
    if not rows:
        errors.append("detailed stop register contains no stop rows")
    return rows


def parse_dependencies(section: str, errors: list[str]) -> dict[str, set[str]]:
    dependencies: dict[str, set[str]] = {}
    for line_number, line in enumerate(section.splitlines(), start=1):
        if not line.strip():
            continue
        match = DEPENDENCY_RE.fullmatch(line)
        if not match:
            errors.append(f"dependency line {line_number}: malformed dependency lock")
            continue
        target, raw_dependencies = match.groups()
        if target in dependencies:
            errors.append(f"duplicate dependency lock for {target}")
            continue
        dependencies[target] = {item.strip() for item in raw_dependencies.split(",")}
    return dependencies


def validate(plan_text: str, release_text: str) -> list[str]:
    errors: list[str] = []
    register = marked_section(plan_text, REGISTER_START, REGISTER_END, errors)
    dependency_section = marked_section(
        plan_text, DEPENDENCY_START, DEPENDENCY_END, errors
    )
    rows = parse_stop_rows(register, errors)
    versions = [row[0] for row in rows]
    version_set = set(versions)

    if len(versions) != len(version_set):
        duplicates = sorted({version for version in versions if versions.count(version) > 1})
        errors.append(f"duplicate detailed stops: {', '.join(duplicates)}")

    for previous, current in zip(rows, rows[1:]):
        if version_key(previous[0]) >= version_key(current[0]):
            errors.append(
                f"stops are not strictly increasing: {previous[0]} before {current[0]}"
            )

    base_matches = list(BASE_RE.finditer(release_text))
    base_versions = {match.group(1) for match in base_matches}
    base_minors = {int(match.group(2)) for match in base_matches}
    if base_minors != set(range(1, 201)):
        errors.append("release plan must own exactly base trains v0.1.0 through v0.200.0")

    for version in versions:
        major, minor, patch = version_key(version)
        if version == "v1.0.0":
            continue
        if major != 0 or patch == 0 or minor not in base_minors:
            errors.append(f"{version}: detailed stop has no valid v0.N.0 owner")

    dependencies = parse_dependencies(dependency_section, errors)
    known_versions = version_set | base_versions
    for target, prerequisites in dependencies.items():
        if target not in version_set:
            errors.append(f"dependency target is not a detailed stop: {target}")
            continue
        for prerequisite in prerequisites:
            if prerequisite not in known_versions:
                errors.append(f"{target}: unknown prerequisite {prerequisite}")
            elif version_key(prerequisite) >= version_key(target):
                errors.append(f"{target}: prerequisite does not precede it: {prerequisite}")

    for target, required in REQUIRED_EDGES.items():
        missing = required - dependencies.get(target, set())
        if missing:
            errors.append(f"{target}: missing required dependency locks: {', '.join(sorted(missing))}")

    for required_text in REQUIRED_CONTRACT_TEXT:
        if required_text not in plan_text:
            errors.append(f"missing common stop-contract obligation: {required_text}")

    if "## Current Source Locks" not in plan_text or "Checked 2026-08-19" not in plan_text:
        errors.append("missing dated current source-lock section")
    for label, url in REQUIRED_SOURCES.items():
        if label not in plan_text or url not in plan_text:
            errors.append(f"missing required source lock: {label}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, default=Path("docs/DETAILED_VERSION_PLAN.md"))
    parser.add_argument("--release-plan", type=Path, default=Path("docs/RELEASE_PLAN.md"))
    args = parser.parse_args()

    errors = validate(
        args.plan.read_text(encoding="utf-8"),
        args.release_plan.read_text(encoding="utf-8"),
    )
    if errors:
        for error in errors:
            print(f"detailed version plan: {error}", file=sys.stderr)
        return 1
    print("detailed version plan structure and dependency locks are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
