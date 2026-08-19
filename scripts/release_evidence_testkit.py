"""Shared real-Git fixtures for release-evidence tests."""

from __future__ import annotations

import hashlib
import subprocess
from datetime import date
from pathlib import Path

import validate_release_evidence as release_validator
from release_trust_policy import trust_policy_digest

REVIEWER_KEY = "A" * 40
BOUNDARY_REVIEWER_KEY = "B" * 40
TAG_SIGNER_KEY = "C" * 40
PENTESTER_KEY = "D" * 40
SOURCE_DIGEST = "b" * 64
BOUNDARY_DIGEST = "c" * 64


class GitFixture:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.run("init", "-q")
        self.run("config", "user.name", "Gestur Test")
        self.run("config", "user.email", "gestur-test@example.invalid")
        self.write("docs/scope.md", "initial scope\n")
        self.write(
            "security/release-reviewers.txt",
            f"{REVIEWER_KEY} | Release Reviewer\n"
            f"{BOUNDARY_REVIEWER_KEY} | Boundary Reviewer\n",
        )
        self.write(
            "security/release-tag-signers.txt",
            f"{TAG_SIGNER_KEY} | Release Tag Signer\n",
        )
        self.write(
            "security/external-pentesters.txt",
            f"{PENTESTER_KEY} | Independent Pentester\n",
        )
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


def valid_signature(signature: Path, record: Path) -> str | None:
    if signature.read_text(encoding="utf-8") != "valid\n":
        return None
    if "pentest" in record.parts:
        return PENTESTER_KEY
    return BOUNDARY_REVIEWER_KEY if "feasibility" in record.parts else REVIEWER_KEY


def valid_tag(_repository: Path, _tag: str) -> str | None:
    return TAG_SIGNER_KEY


def write_pentest_evidence(
    fixture: GitFixture,
    release: str,
    candidate: str,
    *,
    tester: str = "Independent Pentester",
    tester_key: str = PENTESTER_KEY,
    reviewed: str | None = None,
    status: str = "PASS",
    report_path: str | None = None,
    report_digest: str | None = None,
    evidence_digest: str | None = None,
    signature: str = "valid\n",
) -> None:
    report_relative = report_path or f"security/pentest/reports/{release}/report.md"
    report = "Independent penetration-test report\n"
    fixture.write(report_relative, report)
    support_relative = f"security/pentest/support/{release}/provider-evidence.txt"
    support = "Provider scope and clean-retest evidence\n"
    fixture.write(support_relative, support)
    attestation_relative = f"security/pentest/{release}.md"
    fixture.write(
        attestation_relative,
        f"Status: {status}\n"
        "Date: 2026-08-19\n"
        f"Reviewed-Commit: {reviewed or candidate}\n"
        "Scope: full release candidate\n"
        f"Tester: {tester}\n"
        f"Tester-Key: {tester_key}\n"
        f"Report: {report_relative}\n"
        f"Report-Digest: {report_digest or hashlib.sha256(report.encode()).hexdigest()}\n"
        f"Evidence: {support_relative}\n"
        f"Evidence-Digest: {evidence_digest or hashlib.sha256(support.encode()).hexdigest()}\n"
        f"Signature: {attestation_relative}.asc\n",
    )
    fixture.write(f"{attestation_relative}.asc", signature)


def write_source_evidence(
    fixture: GitFixture,
    release: str,
    candidate: str,
    *,
    reviewed: str | None = None,
    source_digest: str = SOURCE_DIGEST,
    signature: str = "valid\n",
) -> None:
    support_relative = f"evidence/source-freshness/reviews/{release}.md"
    support = "Primary-source review details\n"
    fixture.write(support_relative, support)
    support_digest = hashlib.sha256(support.encode()).hexdigest()
    record_relative = f"evidence/source-freshness/{release}.md"
    fixture.write(
        record_relative,
        "Status: PASS\n"
        "Date: 2026-08-19\n"
        f"Reviewed-Commit: {reviewed or candidate}\n"
        f"Source-Lock-Digest: {source_digest}\n"
        "Reviewer: Release Reviewer\n"
        f"Reviewer-Key: {REVIEWER_KEY}\n"
        f"Evidence: {support_relative}\n"
        f"Evidence-Digest: {support_digest}\n"
        f"Signature: {record_relative}.asc\n",
    )
    fixture.write(f"{record_relative}.asc", signature)
    write_pentest_evidence(fixture, release, candidate)


def write_boundary_evidence(
    fixture: GitFixture,
    candidate: str,
    *,
    reviewed: str | None = None,
    scope: str = "docs/scope.md",
    plan_digest: str = BOUNDARY_DIGEST,
    support_digest: str | None = None,
    signature: str = "valid\n",
) -> dict[str, str]:
    boundary = "sqlite"
    support_relative = f"evidence/feasibility/support/{boundary}.md"
    support = "SQLite boundary review details\n"
    fixture.write(support_relative, support)
    actual_support_digest = hashlib.sha256(support.encode()).hexdigest()
    record_relative = f"evidence/feasibility/{boundary}.md"
    fixture.write(
        record_relative,
        f"Boundary: {boundary}\n"
        "Status: QUALIFIED\n"
        f"Reviewed-Commit: {reviewed or candidate}\n"
        f"Boundary-Plan-Digest: {plan_digest}\n"
        f"Scope: {scope}\n"
        "Reviewer: Boundary Reviewer\n"
        f"Reviewer-Key: {BOUNDARY_REVIEWER_KEY}\n"
        f"Evidence: {support_relative}\n"
        f"Evidence-Digest: {support_digest or actual_support_digest}\n"
        f"Signature: {record_relative}.asc\n",
    )
    fixture.write(f"{record_relative}.asc", signature)
    return {
        "decision_by": "v0.1.0",
        "required_by": "v0.12.1",
        "status": "qualified",
        "evidence": record_relative,
    }


def validate(
    fixture: GitFixture,
    release: str,
    candidate: str,
    declared: set[str],
    *,
    boundaries: dict[str, dict[str, str]] | None = None,
    boundary_digest: str = BOUNDARY_DIGEST,
    signature_verifier=valid_signature,
    tag_verifier=valid_tag,
    expected_trust_policy_digest: str | None = None,
    tagged_release: bool = False,
) -> list[str]:
    selected = boundaries or {}
    return release_validator.validate_release_evidence(
        release,
        fixture.root,
        candidate,
        declared,
        selected,
        {boundary: boundary_digest for boundary in selected},
        SOURCE_DIGEST,
        today=date(2026, 8, 19),
        signature_verifier=signature_verifier,
        tag_verifier=tag_verifier,
        expected_trust_policy_digest=(
            expected_trust_policy_digest
            or trust_policy_digest(fixture.root, candidate)
        ),
        tagged_release=tagged_release,
    )
