#!/usr/bin/env python3
"""Fail-closed structural and release validation for Gestur's version plans."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from datetime import date
from pathlib import Path

from validate_release_evidence import (
    SignatureVerifier,
    TagVerifier,
    validate_release_evidence,
)

REGISTER_START = "<!-- detailed-stop-register:start -->"
REGISTER_END = "<!-- detailed-stop-register:end -->"
DEPENDENCY_START = "<!-- dependency-locks:start -->"
DEPENDENCY_END = "<!-- dependency-locks:end -->"
TRAIN_START = "<!-- train-stop-declarations:start -->"
TRAIN_END = "<!-- train-stop-declarations:end -->"
BOUNDARY_START = "<!-- boundary-feasibility:start -->"
BOUNDARY_END = "<!-- boundary-feasibility:end -->"
SOURCE_START = "<!-- source-locks:start -->"
SOURCE_END = "<!-- source-locks:end -->"

VERSION_RE = re.compile(r"^v0\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$|^v1\.0\.0$")
BASE_RE = re.compile(r"^## (v0\.([1-9][0-9]*)\.0) — ", re.MULTILINE)
DEPENDENCY_RE = re.compile(r"^- (v(?:0\.[0-9]+\.[0-9]+|1\.0\.0)) <- (.+)$")
TRAIN_RE = re.compile(r"^- (v0\.([1-9][0-9]*)\.0): (none|v0\.[0-9]+\.[0-9]+(?:, v0\.[0-9]+\.[0-9]+)*)$")
BOUNDARY_RE = re.compile(
    r"^- ([a-z0-9-]+) \| decision-by=(v0\.[0-9]+\.[0-9]+) "
    r"\| required-by=(v0\.[0-9]+\.[0-9]+) "
    r"\| status=(pending|qualified|blocked) \| evidence=(\S+)$"
)
SOURCE_RE = re.compile(
    r"^- ([a-z0-9-]+) \| revision=(\S+) \| checked=(\d{4}-\d{2}-\d{2}) "
    r"\| max-age-days=([1-9][0-9]*) \| url=(https://\S+)$"
)

REQUIRED_EDGES = {
    "v0.10.6": {"v0.10.5"},
    "v0.10.7": {"v0.10.5"},
    "v0.12.1": {"v0.10.2", "v0.11.1", "v0.11.3", "v0.11.5"},
    "v0.32.1": {"v0.3.6", "v0.3.7", "v0.11.5", "v0.30.1"},
    "v0.46.1": {"v0.45.6"},
    "v0.48.9": {"v0.46.2", "v0.48.8"},
    "v0.50.1": {"v0.48.9"},
    "v0.71.1": {"v0.10.2", "v0.10.3", "v0.19.1", "v0.29.1"},
    "v0.87.1": {"v0.10.2", "v0.10.3", "v0.19.1"},
    "v0.92.1": {"v0.3.5", "v0.27.1", "v0.91.1", "v0.92.0"},
    "v0.93.1": {"v0.92.4"},
    "v0.99.1": {"v0.98.4"},
    "v0.100.1": {"v0.93.1", "v0.97.1"},
    "v0.101.1": {"v0.92.4"},
    "v0.102.1": {"v0.101.1"},
    "v0.103.1": {"v0.92.4", "v0.101.1", "v0.102.1"},
    "v0.104.1": {"v0.101.1", "v0.102.1"},
    "v0.105.1": {"v0.103.1", "v0.104.1"},
    "v0.107.1": {"v0.106.1"},
    "v0.108.1": {"v0.107.1"},
    "v0.109.5": {"v0.99.1", "v0.105.1", "v0.108.1"},
    "v0.110.2": {"v0.109.5", "v0.110.1"},
    "v0.111.1": {"v0.46.2", "v0.87.1"},
    "v0.112.1": {"v0.10.2", "v0.111.1"},
    "v0.133.1": {"v0.92.4"},
    "v0.141.1": {"v0.46.2"},
    "v0.166.1": {"v0.3.7", "v0.10.2"},
    "v0.168.1": {"v0.58.2", "v0.140.1", "v0.166.1", "v0.167.1", "v0.167.2"},
    "v0.200.1": {"v0.199.1"},
}

REQUIRED_BOUNDARIES = {
    "sqlite": "v0.12.1",
    "postgresql": "v0.13.1",
    "mysql": "v0.14.1",
    "unicode-security": "v0.42.1",
    "tls": "v0.71.1",
    "oidc": "v0.71.1",
    "webauthn": "v0.72.1",
    "wasm": "v0.112.1",
    "pkcs11": "v0.167.1",
}

REQUIRED_SOURCES = {
    "semver": ("https://semver.org/", 365),
    "wcag": ("https://www.w3.org/TR/WCAG22/", 180),
    "nist-800-63": ("https://csrc.nist.gov/pubs/sp/800/63/4/final", 90),
    "nist-800-88": ("https://csrc.nist.gov/pubs/sp/800/88/r2/final", 90),
    "eu-ai-act-base": ("https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng", 30),
    "eu-ai-act-amendment": ("https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng", 30),
    "gdpr": ("https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng", 180),
    "ccpa-cpra": ("https://cppa.ca.gov/regulations/", 30),
    "eidas": ("https://eur-lex.europa.eu/eli/reg/2014/910/2024-10-18/eng", 90),
    "ofac": ("https://ofac.treasury.gov/sanctions-list-service", 30),
    "ear": ("https://www.ecfr.gov/current/title-15/subtitle-B/chapter-VII/subchapter-C", 30),
    "itar": ("https://www.ecfr.gov/current/title-22/chapter-I/subchapter-M", 30),
    "fips-201": ("https://csrc.nist.gov/pubs/fips/201-3/final", 180),
    "oidc-core": ("https://openid.net/specs/openid-connect-core-1_0.html", 180),
    "rfc-5545": ("https://www.rfc-editor.org/rfc/rfc5545", 365),
    "rfc-9421": ("https://www.rfc-editor.org/rfc/rfc9421", 365),
    "rfc-3161": ("https://www.rfc-editor.org/rfc/rfc3161", 365),
    "apple-nearby-interaction": ("https://developer.apple.com/documentation/nearbyinteraction", 90),
    "android-ranging": ("https://developer.android.com/develop/connectivity/ranging", 90),
    "google-smart-tap": ("https://developers.google.com/wallet/smart-tap", 90),
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


def parse_train_declarations(section: str, errors: list[str]) -> dict[str, list[str]]:
    declarations: dict[str, list[str]] = {}
    for line_number, line in enumerate(section.splitlines(), start=1):
        if not line.strip():
            continue
        match = TRAIN_RE.fullmatch(line)
        if not match:
            errors.append(f"train declaration line {line_number}: malformed declaration")
            continue
        base, _minor, raw_stops = match.groups()
        if base in declarations:
            errors.append(f"duplicate train declaration for {base}")
            continue
        declarations[base] = [] if raw_stops == "none" else raw_stops.split(", ")
    return declarations


def parse_boundaries(section: str, errors: list[str]) -> dict[str, dict[str, str]]:
    boundaries: dict[str, dict[str, str]] = {}
    for line_number, line in enumerate(section.splitlines(), start=1):
        if not line.strip():
            continue
        match = BOUNDARY_RE.fullmatch(line)
        if not match:
            errors.append(f"boundary line {line_number}: malformed feasibility entry")
            continue
        boundary, decision_by, required_by, status, evidence = match.groups()
        if boundary in boundaries:
            errors.append(f"duplicate boundary feasibility entry for {boundary}")
            continue
        boundaries[boundary] = {
            "decision_by": decision_by,
            "required_by": required_by,
            "status": status,
            "evidence": evidence,
        }
    return boundaries


def parse_sources(
    section: str, errors: list[str], today: date
) -> dict[str, dict[str, str | int | date]]:
    sources: dict[str, dict[str, str | int | date]] = {}
    for line_number, line in enumerate(section.splitlines(), start=1):
        if not line.strip():
            continue
        match = SOURCE_RE.fullmatch(line)
        if not match:
            errors.append(f"source line {line_number}: malformed source lock")
            continue
        source_id, revision, checked_raw, max_age_raw, url = match.groups()
        if source_id in sources:
            errors.append(f"duplicate source lock for {source_id}")
            continue
        try:
            checked = date.fromisoformat(checked_raw)
        except ValueError:
            errors.append(f"{source_id}: invalid source check date")
            continue
        max_age = int(max_age_raw)
        if checked > today:
            errors.append(f"{source_id}: source check date is in the future")
        elif (today - checked).days > max_age:
            errors.append(
                f"{source_id}: source lock is stale "
                f"({(today - checked).days} days > {max_age})"
            )
        sources[source_id] = {
            "revision": revision,
            "checked": checked,
            "max_age": max_age,
            "url": url,
        }
    return sources


def source_lock_digest(plan_text: str) -> str:
    errors: list[str] = []
    section = marked_section(plan_text, SOURCE_START, SOURCE_END, errors)
    normalized = section.strip() + "\n"
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def validate(
    plan_text: str, release_text: str, *, today: date | None = None
) -> list[str]:
    errors: list[str] = []
    current_date = today or date.today()
    register = marked_section(plan_text, REGISTER_START, REGISTER_END, errors)
    dependency_section = marked_section(
        plan_text, DEPENDENCY_START, DEPENDENCY_END, errors
    )
    train_section = marked_section(plan_text, TRAIN_START, TRAIN_END, errors)
    boundary_section = marked_section(plan_text, BOUNDARY_START, BOUNDARY_END, errors)
    source_section = marked_section(plan_text, SOURCE_START, SOURCE_END, errors)
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

    declarations = parse_train_declarations(train_section, errors)
    if set(declarations) != base_versions:
        missing = sorted(base_versions - set(declarations), key=version_key)
        extra = sorted(set(declarations) - base_versions, key=version_key)
        if missing:
            errors.append(f"missing train declarations: {', '.join(missing)}")
        if extra:
            errors.append(f"unknown train declarations: {', '.join(extra)}")
    for base in sorted(base_versions, key=version_key):
        minor = version_key(base)[1]
        actual = [version for version in versions if version_key(version)[:2] == (0, minor)]
        if declarations.get(base) != actual:
            errors.append(
                f"{base}: declared detailed stops do not match register "
                f"(declared={declarations.get(base, [])}, actual={actual})"
            )

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
            errors.append(
                f"{target}: missing required dependency locks: {', '.join(sorted(missing))}"
            )

    boundaries = parse_boundaries(boundary_section, errors)
    if set(boundaries) != set(REQUIRED_BOUNDARIES):
        missing = sorted(set(REQUIRED_BOUNDARIES) - set(boundaries))
        extra = sorted(set(boundaries) - set(REQUIRED_BOUNDARIES))
        if missing:
            errors.append(f"missing boundary feasibility entries: {', '.join(missing)}")
        if extra:
            errors.append(f"unknown boundary feasibility entries: {', '.join(extra)}")
    for boundary, expected_required_by in REQUIRED_BOUNDARIES.items():
        entry = boundaries.get(boundary)
        if entry is None:
            continue
        if entry["decision_by"] != "v0.10.2":
            errors.append(f"{boundary}: decision-by must be v0.10.2")
        if entry["required_by"] != expected_required_by:
            errors.append(
                f"{boundary}: required-by must be {expected_required_by}"
            )
        status = entry["status"]
        evidence = entry["evidence"]
        if status == "pending" and evidence != "none":
            errors.append(f"{boundary}: pending status must use evidence=none")
        if status in {"qualified", "blocked"}:
            if evidence == "none":
                errors.append(f"{boundary}: {status} status requires evidence")
            elif (
                not evidence.startswith("evidence/feasibility/")
                or Path(evidence).is_absolute()
                or ".." in Path(evidence).parts
            ):
                errors.append(f"{boundary}: feasibility evidence path is not repository-safe")

    sources = parse_sources(source_section, errors, current_date)
    if set(sources) != set(REQUIRED_SOURCES):
        missing = sorted(set(REQUIRED_SOURCES) - set(sources))
        extra = sorted(set(sources) - set(REQUIRED_SOURCES))
        if missing:
            errors.append(f"missing source locks: {', '.join(missing)}")
        if extra:
            errors.append(f"unknown source locks: {', '.join(extra)}")
    for source_id, (expected_url, expected_max_age) in REQUIRED_SOURCES.items():
        source = sources.get(source_id)
        if source is not None and source["url"] != expected_url:
            errors.append(f"{source_id}: source URL does not match the authoritative lock")
        if source is not None and source["max_age"] != expected_max_age:
            errors.append(f"{source_id}: source maximum age does not match policy")

    for required_text in REQUIRED_CONTRACT_TEXT:
        if required_text not in plan_text:
            errors.append(f"missing common stop-contract obligation: {required_text}")
    return errors


def boundary_plan_digest(plan_text: str, boundary: str) -> str:
    errors: list[str] = []
    section = marked_section(plan_text, BOUNDARY_START, BOUNDARY_END, errors)
    line = next(
        (item for item in section.splitlines() if item.startswith(f"- {boundary} |")),
        "",
    )
    return hashlib.sha256(f"{line}\n".encode()).hexdigest()


def validate_release(
    plan_text: str,
    release: str,
    repository: Path,
    *,
    candidate: str | None = None,
    today: date | None = None,
    signature_verifier: SignatureVerifier | None = None,
    tag_verifier: TagVerifier | None = None,
) -> list[str]:
    errors: list[str] = []
    if not VERSION_RE.fullmatch(release):
        return [f"invalid release version: {release}"]

    train_section = marked_section(plan_text, TRAIN_START, TRAIN_END, errors)
    boundary_section = marked_section(
        plan_text, BOUNDARY_START, BOUNDARY_END, errors
    )
    declarations = parse_train_declarations(train_section, errors)
    boundaries = parse_boundaries(boundary_section, errors)
    declared_versions = set(declarations) | {"v1.0.0"}
    for stops in declarations.values():
        declared_versions.update(stops)
    if release not in declared_versions:
        errors.append(f"release is not declared by the roadmap: {release}")

    release_key = version_key(release)
    for boundary, entry in boundaries.items():
        status = entry["status"]
        if release_key >= version_key(str(entry["decision_by"])) and status == "pending":
            errors.append(f"{boundary}: pending feasibility decision blocks {release}")
        if release_key >= version_key(str(entry["required_by"])) and status != "qualified":
            errors.append(
                f"{boundary}: {release} requires qualified feasibility, found {status}"
            )
    if errors:
        return errors

    kwargs = {}
    if signature_verifier is not None:
        kwargs["signature_verifier"] = signature_verifier
    if tag_verifier is not None:
        kwargs["tag_verifier"] = tag_verifier
    boundary_digests = {
        boundary: boundary_plan_digest(plan_text, boundary) for boundary in boundaries
    }
    return validate_release_evidence(
        release,
        repository,
        candidate,
        declared_versions,
        boundaries,
        boundary_digests,
        source_lock_digest(plan_text),
        today=today,
        **kwargs,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, default=Path("docs/DETAILED_VERSION_PLAN.md"))
    parser.add_argument("--release-plan", type=Path, default=Path("docs/RELEASE_PLAN.md"))
    parser.add_argument("--release")
    parser.add_argument("--candidate")
    parser.add_argument("--repository", type=Path, default=Path("."))
    args = parser.parse_args()

    plan_text = args.plan.read_text(encoding="utf-8")
    errors = validate(
        plan_text,
        args.release_plan.read_text(encoding="utf-8"),
    )
    if args.release and not errors:
        errors.extend(
            validate_release(
                plan_text,
                args.release,
                args.repository,
                candidate=args.candidate,
            )
        )
    if errors:
        for error in errors:
            print(f"detailed version plan: {error}", file=sys.stderr)
        return 1
    digest = source_lock_digest(plan_text)
    print(
        "detailed version plan structure, declarations, dependencies, "
        f"feasibility, and source locks are valid; source-lock-digest={digest}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
