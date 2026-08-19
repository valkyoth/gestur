#!/usr/bin/env python3
"""Validate Gestur's owner-driven release state and exact tag target."""

from __future__ import annotations

import re
import subprocess
from datetime import date
from pathlib import Path

from validate_pentest_evidence import validate_pentest_evidence

HEX_40_RE = re.compile(r"^[0-9a-f]{40}$")


def version_key(version: str) -> tuple[int, int, int]:
    return tuple(int(part) for part in version.removeprefix("v").split("."))  # type: ignore[return-value]


def git(repository: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repository), *arguments],
        check=False,
        capture_output=True,
        text=True,
    )


def git_output(repository: Path, *arguments: str) -> str | None:
    result = git(repository, *arguments)
    return result.stdout.strip() if result.returncode == 0 else None


def commit_exists(repository: Path, commit: str) -> bool:
    return git(repository, "cat-file", "-e", f"{commit}^{{commit}}").returncode == 0


def is_ancestor(repository: Path, ancestor: str, descendant: str) -> bool:
    return (
        git(repository, "merge-base", "--is-ancestor", ancestor, descendant).returncode
        == 0
    )


def finalization_paths(release: str) -> set[str]:
    version = release.removeprefix("v")
    return {
        "CHANGELOG.md",
        "README.md",
        "docs/DETAILED_VERSION_PLAN.md",
        "docs/RELEASE_PLAN.md",
        f"release-notes/RELEASE_NOTES_{version}.md",
        f"security/pentest/{release}.md",
    }


def validate_predecessors(
    release: str,
    repository: Path,
    candidate: str,
    declared_versions: set[str],
    errors: list[str],
) -> None:
    predecessors = sorted(
        (item for item in declared_versions if version_key(item) < version_key(release)),
        key=version_key,
    )
    prior_commit: str | None = None
    for tag in predecessors:
        if git_output(repository, "cat-file", "-t", f"refs/tags/{tag}") != "tag":
            errors.append(f"{release}: missing annotated predecessor tag {tag}")
            continue
        tagged = git_output(repository, "rev-parse", f"refs/tags/{tag}^{{commit}}")
        if tagged is None:
            errors.append(f"{release}: predecessor tag {tag} has no commit")
            continue
        if prior_commit is not None:
            if tagged == prior_commit:
                errors.append(f"{release}: predecessor tag {tag} reuses a release commit")
            elif not is_ancestor(repository, prior_commit, tagged):
                errors.append(f"{release}: predecessor tag {tag} is out of ancestry order")
        if not is_ancestor(repository, tagged, candidate):
            errors.append(f"{release}: predecessor tag {tag} is not an ancestor")
        prior_commit = tagged
    if prior_commit == candidate:
        errors.append(f"{release}: candidate reuses the last predecessor commit")


def validate_release_evidence(
    release: str,
    repository: Path,
    candidate: str | None,
    declared_versions: set[str],
    _boundaries: dict[str, dict[str, str]],
    _boundary_digests: dict[str, str],
    _source_digest: str,
    *,
    today: date | None = None,
    tagged_release: bool = False,
) -> list[str]:
    errors: list[str] = []
    root = repository.resolve()
    selected = candidate or git_output(root, "rev-parse", "HEAD")
    if selected is None or not HEX_40_RE.fullmatch(selected):
        return ["release evidence: candidate commit is missing or invalid"]
    if not commit_exists(root, selected):
        return ["release evidence: candidate commit does not exist"]
    if git_output(root, "rev-parse", "HEAD") != selected:
        errors.append("release evidence: candidate is not the checked-out HEAD")
    if git_output(root, "status", "--porcelain", "--untracked-files=all"):
        errors.append("release evidence: worktree is not clean")

    tagged = git_output(root, "rev-parse", f"refs/tags/{release}^{{commit}}")
    if tagged_release:
        if git_output(root, "cat-file", "-t", f"refs/tags/{release}") != "tag":
            errors.append(f"{release}: current release tag is missing or lightweight")
        if tagged != selected:
            errors.append(f"{release}: current tag does not target the release commit")
    elif tagged is not None:
        errors.append(f"{release}: tag already exists")

    validate_predecessors(release, root, selected, declared_versions, errors)
    validate_pentest_evidence(
        release,
        root,
        selected,
        today or date.today(),
        errors,
        finalization_paths(release),
    )
    return errors
