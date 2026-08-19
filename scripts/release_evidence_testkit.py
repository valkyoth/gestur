"""Shared real-Git fixtures for Gestur release-flow tests."""

from __future__ import annotations

import subprocess
from datetime import date
from pathlib import Path

import validate_release_evidence as release_validator


class GitFixture:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.run("init", "-q")
        self.run("config", "user.name", "Gestur Test")
        self.run("config", "user.email", "gestur-test@example.invalid")
        self.write("README.md", "# fixture\n")
        self.commit("root")

    def run(self, *arguments: str) -> str:
        result = subprocess.run(
            ["git", "-C", str(self.root), *arguments],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    def write(self, relative: str, content: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def commit(self, message: str) -> str:
        self.run("add", "--all")
        self.run("commit", "-q", "--allow-empty", "-m", message)
        return self.run("rev-parse", "HEAD")

    def tag(self, tag: str, target: str = "HEAD", *, annotated: bool = True) -> None:
        if annotated:
            self.run("tag", "-a", tag, target, "-m", tag)
        else:
            self.run("tag", tag, target)


def write_pentest_record(
    fixture: GitFixture,
    release: str,
    pentested: str,
    *,
    status: str = "PASS",
    checked: str = "2026-08-19",
    scope: str = "full repository",
    retest: str = "clean-retest",
    findings: str = "release validation bypass fixed",
    codeql_finding: str = "none",
    codeql_changed_paths: str = "none",
    regression_tests: str = "none",
    full_gate: str = "PASS",
) -> None:
    fixture.write(
        f"security/pentest/{release}.md",
        f"# {release} Pentest Record\n\n"
        f"Status: {status}\n"
        f"Date: {checked}\n"
        f"Pentested-Commit: {pentested}\n"
        f"Scope: {scope}\n"
        f"Retest: {retest}\n"
        f"Findings-Resolved: {findings}\n"
        f"CodeQL-Finding: {codeql_finding}\n"
        f"CodeQL-Changed-Paths: {codeql_changed_paths}\n"
        f"Regression-Tests: {regression_tests}\n"
        f"Full-Gate: {full_gate}\n",
    )


def make_release(
    root: Path,
    release: str = "v0.1.0",
    *,
    predecessors: tuple[str, ...] = (),
    **record: str,
) -> tuple[GitFixture, str, str, set[str]]:
    fixture = GitFixture(root)
    declared = set(predecessors) | {release}
    for predecessor in predecessors:
        fixture.commit(predecessor)
        fixture.tag(predecessor)
    pentested = fixture.commit("implementation")
    write_pentest_record(fixture, release, pentested, **record)
    candidate = fixture.commit("release finalization")
    return fixture, pentested, candidate, declared


def validate(
    fixture: GitFixture,
    release: str,
    candidate: str,
    declared: set[str],
    *,
    tagged_release: bool = False,
) -> list[str]:
    return release_validator.validate_release_evidence(
        release,
        fixture.root,
        candidate,
        declared,
        {},
        {},
        "unused",
        today=date(2026, 8, 19),
        tagged_release=tagged_release,
    )
