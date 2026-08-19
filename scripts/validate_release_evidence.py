#!/usr/bin/env python3
"""Git- and signature-bound release evidence validation for Gestur."""

from __future__ import annotations

import hashlib
import re
import subprocess
from datetime import date
from pathlib import Path, PurePosixPath
from typing import Callable

SignatureVerifier = Callable[[Path, Path], str | None]
TagVerifier = Callable[[Path, str], bool]

IMPLEMENTATION_SCOPES = {
    "sqlite": "crates/gestur-db-sqlite",
    "postgresql": "crates/gestur-db-postgres",
    "mysql": "crates/gestur-db-mysql",
    "unicode-security": "crates/gestur-unicode-security",
    "tls": "crates/gestur-tls-host",
    "oidc": "crates/gestur-identity-oidc",
    "webauthn": "crates/gestur-identity-webauthn",
    "wasm": "crates/gestur-plugin-host",
    "pkcs11": "crates/gestur-key-provider-pkcs11",
}

HEX_40_RE = re.compile(r"^[0-9a-f]{40}$")
KEY_RE = re.compile(r"^[0-9A-F]{40}(?:[0-9A-F]{24})?$")
DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")


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


def default_signature_verifier(signature: Path, record: Path) -> str | None:
    result = subprocess.run(
        [
            "gpg",
            "--batch",
            "--status-fd",
            "1",
            "--verify",
            str(signature),
            str(record),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    match = re.search(r"^\[GNUPG:\] VALIDSIG ([0-9A-F]+) ", result.stdout, re.MULTILINE)
    return match.group(1) if match else None


def default_tag_verifier(repository: Path, tag: str) -> bool:
    return git(repository, "verify-tag", "--raw", tag).returncode == 0


def safe_path(
    repository: Path,
    relative: str,
    errors: list[str],
    label: str,
    *,
    prefix: str | None = None,
) -> Path | None:
    pure = PurePosixPath(relative)
    if (
        not relative
        or "\\" in relative
        or pure.is_absolute()
        or ".." in pure.parts
        or "." in pure.parts
        or (prefix is not None and not relative.startswith(prefix))
    ):
        errors.append(f"{label}: unsafe evidence path {relative!r}")
        return None
    root = repository.resolve()
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        errors.append(f"{label}: evidence path escapes repository")
        return None
    return candidate


def metadata(content: str, name: str, errors: list[str], label: str) -> str | None:
    values = re.findall(rf"^{re.escape(name)}: (.+)$", content, re.MULTILINE)
    if len(values) != 1:
        errors.append(f"{label}: expected exactly one {name} field")
        return None
    return values[0]


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reviewer_is_trusted(
    repository: Path, candidate: str, reviewer: str, reviewer_key: str
) -> bool:
    content = git_output(
        repository, "show", f"{candidate}:security/release-reviewers.txt"
    )
    if content is None:
        return False
    entries = [
        tuple(part.strip() for part in line.split("|", 1))
        for line in content.splitlines()
        if line and not line.startswith("#") and "|" in line
    ]
    return entries.count((reviewer_key, reviewer)) == 1 and sum(
        key == reviewer_key for key, _name in entries
    ) == 1


def verify_support_and_signature(
    repository: Path,
    candidate: str,
    record_path: Path,
    content: str,
    errors: list[str],
    label: str,
    allowed_paths: set[str],
    signature_verifier: SignatureVerifier,
    *,
    support_prefix: str,
) -> None:
    reviewer = metadata(content, "Reviewer", errors, label)
    reviewer_key = metadata(content, "Reviewer-Key", errors, label)
    support_relative = metadata(content, "Evidence", errors, label)
    expected_digest = metadata(content, "Evidence-Digest", errors, label)
    signature_relative = metadata(content, "Signature", errors, label)
    if reviewer is not None and not reviewer.strip():
        errors.append(f"{label}: reviewer identity is empty")
    if reviewer_key is not None and not KEY_RE.fullmatch(reviewer_key):
        errors.append(f"{label}: reviewer key fingerprint is invalid")
    if (
        reviewer is not None
        and reviewer_key is not None
        and KEY_RE.fullmatch(reviewer_key)
        and not reviewer_is_trusted(repository, candidate, reviewer, reviewer_key)
    ):
        errors.append(f"{label}: reviewer key is not authorized by the candidate")

    if support_relative is not None:
        support = safe_path(
            repository,
            support_relative,
            errors,
            label,
            prefix=support_prefix,
        )
        if support is None or not support.is_file():
            errors.append(f"{label}: supporting evidence file is missing")
        else:
            allowed_paths.add(support_relative)
            if expected_digest is None or not DIGEST_RE.fullmatch(expected_digest):
                errors.append(f"{label}: supporting evidence digest is invalid")
            elif file_digest(support) != expected_digest:
                errors.append(f"{label}: supporting evidence digest does not match")

    expected_signature = record_path.relative_to(repository.resolve()).as_posix() + ".asc"
    if signature_relative is not None:
        signature = safe_path(repository, signature_relative, errors, label)
        if signature_relative != expected_signature:
            errors.append(f"{label}: signature must be {expected_signature}")
        if signature is None or not signature.is_file():
            errors.append(f"{label}: detached signature is missing")
        elif reviewer_key is not None and KEY_RE.fullmatch(reviewer_key):
            allowed_paths.add(signature_relative)
            signer = signature_verifier(signature, record_path)
            if signer != reviewer_key:
                errors.append(f"{label}: detached signature is invalid or from the wrong key")


def validate_predecessors(
    release: str,
    repository: Path,
    candidate: str,
    declared_versions: set[str],
    errors: list[str],
    tag_verifier: TagVerifier,
) -> None:
    predecessors = sorted(
        (item for item in declared_versions if version_key(item) < version_key(release)),
        key=version_key,
    )
    prior_commit: str | None = None
    for tag in predecessors:
        tag_type = git_output(repository, "cat-file", "-t", f"refs/tags/{tag}")
        if tag_type != "tag":
            errors.append(f"{release}: missing annotated predecessor tag {tag}")
            continue
        tagged_commit = git_output(repository, "rev-parse", f"refs/tags/{tag}^{{commit}}")
        if tagged_commit is None:
            errors.append(f"{release}: predecessor tag {tag} has no commit")
            continue
        if not tag_verifier(repository, tag):
            errors.append(f"{release}: predecessor tag {tag} has no valid signature")
        if prior_commit is not None:
            if tagged_commit == prior_commit:
                errors.append(f"{release}: predecessor tag {tag} reuses a release commit")
            elif not is_ancestor(repository, prior_commit, tagged_commit):
                errors.append(f"{release}: predecessor tag {tag} is out of ancestry order")
        if not is_ancestor(repository, tagged_commit, candidate):
            errors.append(f"{release}: predecessor tag {tag} is not an ancestor")
        prior_commit = tagged_commit
    if prior_commit == candidate:
        errors.append(f"{release}: candidate reuses the last predecessor commit")


def validate_boundary_record(
    boundary: str,
    entry: dict[str, str],
    plan_digest: str,
    release: str,
    repository: Path,
    candidate: str,
    errors: list[str],
    allowed_paths: set[str],
    signature_verifier: SignatureVerifier,
) -> None:
    label = f"{boundary} feasibility evidence"
    relative = entry["evidence"]
    path = safe_path(
        repository, relative, errors, label, prefix="evidence/feasibility/"
    )
    if path is None or not path.is_file():
        errors.append(f"{label}: record is missing")
        return
    allowed_paths.add(relative)
    content = path.read_text(encoding="utf-8")
    expected = {
        "Boundary": boundary,
        "Status": entry["status"].upper(),
        "Boundary-Plan-Digest": plan_digest,
    }
    for name, expected_value in expected.items():
        if metadata(content, name, errors, label) != expected_value:
            errors.append(f"{label}: {name} does not match")

    reviewed = metadata(content, "Reviewed-Commit", errors, label)
    scopes_raw = metadata(content, "Scope", errors, label)
    if reviewed is not None:
        if not HEX_40_RE.fullmatch(reviewed) or not commit_exists(repository, reviewed):
            errors.append(f"{label}: reviewed commit does not exist")
        elif not is_ancestor(repository, reviewed, candidate):
            errors.append(f"{label}: reviewed commit is not a candidate ancestor")
    scopes = [] if scopes_raw is None else scopes_raw.split(",")
    if not scopes or any(not item for item in scopes):
        errors.append(f"{label}: scope is empty or malformed")
    for scope in scopes:
        if safe_path(repository, scope, errors, label) is None:
            continue
        if reviewed is not None and commit_exists(repository, reviewed):
            if git(repository, "cat-file", "-e", f"{reviewed}:{scope}").returncode != 0:
                errors.append(f"{label}: reviewed scope does not exist at reviewed commit")
            elif git(repository, "diff", "--quiet", reviewed, candidate, "--", scope).returncode:
                errors.append(f"{label}: reviewed scope changed after review")

    if version_key(release) >= version_key(entry["required_by"]):
        required_scope = IMPLEMENTATION_SCOPES[boundary]
        if required_scope not in scopes:
            errors.append(f"{label}: consuming release must cover {required_scope}")

    verify_support_and_signature(
        repository,
        candidate,
        path,
        content,
        errors,
        label,
        allowed_paths,
        signature_verifier,
        support_prefix="evidence/feasibility/support/",
    )


def validate_source_attestation(
    release: str,
    repository: Path,
    candidate: str,
    source_digest: str,
    current_date: date,
    errors: list[str],
    allowed_paths: set[str],
    signature_verifier: SignatureVerifier,
) -> None:
    relative = f"evidence/source-freshness/{release}.md"
    label = f"{release} source-freshness attestation"
    path = safe_path(repository, relative, errors, label)
    if path is None or not path.is_file():
        errors.append(f"{label}: record is missing")
        return
    allowed_paths.add(relative)
    content = path.read_text(encoding="utf-8")
    if metadata(content, "Status", errors, label) != "PASS":
        errors.append(f"{label}: status is not PASS")
    if metadata(content, "Reviewed-Commit", errors, label) != candidate:
        errors.append(f"{label}: reviewed commit is not the exact candidate")
    if metadata(content, "Source-Lock-Digest", errors, label) != source_digest:
        errors.append(f"{label}: source-lock digest does not match")
    checked_raw = metadata(content, "Date", errors, label)
    if checked_raw is not None:
        try:
            checked = date.fromisoformat(checked_raw)
        except ValueError:
            errors.append(f"{label}: invalid ISO date")
        else:
            age = (current_date - checked).days
            if age < 0 or age > 7:
                errors.append(f"{label}: attestation is not within seven days")
    verify_support_and_signature(
        repository,
        candidate,
        path,
        content,
        errors,
        label,
        allowed_paths,
        signature_verifier,
        support_prefix="evidence/source-freshness/reviews/",
    )


def validate_release_evidence(
    release: str,
    repository: Path,
    candidate: str | None,
    declared_versions: set[str],
    boundaries: dict[str, dict[str, str]],
    boundary_digests: dict[str, str],
    source_digest: str,
    *,
    today: date | None = None,
    signature_verifier: SignatureVerifier = default_signature_verifier,
    tag_verifier: TagVerifier = default_tag_verifier,
) -> list[str]:
    errors: list[str] = []
    root = repository.resolve()
    candidate_commit = candidate or git_output(root, "rev-parse", "HEAD^")
    if candidate_commit is None or not HEX_40_RE.fullmatch(candidate_commit):
        return ["release evidence: candidate commit is missing or invalid"]
    if not commit_exists(root, candidate_commit):
        return ["release evidence: candidate commit does not exist"]
    if git_output(root, "status", "--porcelain", "--untracked-files=all"):
        errors.append("release evidence: worktree is not clean")
    if git_output(root, "rev-parse", "HEAD^") != candidate_commit:
        errors.append("release evidence: candidate must be the parent of the evidence commit")
    head_line = git_output(root, "rev-list", "--parents", "-n", "1", "HEAD")
    if head_line is None or len(head_line.split()) != 2:
        errors.append("release evidence: evidence commit must have exactly one parent")
    if git_output(root, "rev-parse", f"refs/tags/{release}") is not None:
        errors.append(f"{release}: tag already exists")

    validate_predecessors(
        release,
        root,
        candidate_commit,
        declared_versions,
        errors,
        tag_verifier,
    )
    allowed_paths = {f"security/pentest/{release}.md"}
    release_key = version_key(release)
    for boundary, entry in boundaries.items():
        if release_key < version_key(entry["decision_by"]) or entry["status"] == "pending":
            continue
        validate_boundary_record(
            boundary,
            entry,
            boundary_digests[boundary],
            release,
            root,
            candidate_commit,
            errors,
            allowed_paths,
            signature_verifier,
        )
    validate_source_attestation(
        release,
        root,
        candidate_commit,
        source_digest,
        today or date.today(),
        errors,
        allowed_paths,
        signature_verifier,
    )

    changed_output = git_output(root, "diff", "--name-only", candidate_commit, "HEAD")
    changed = set() if not changed_output else set(changed_output.splitlines())
    required = {f"security/pentest/{release}.md"} | {
        path for path in allowed_paths if path.startswith("evidence/source-freshness/")
    }
    if not required.issubset(changed):
        errors.append(f"{release}: evidence commit lacks pentest or source attestation")
    unexpected = sorted(changed - allowed_paths)
    if unexpected:
        errors.append(
            f"{release}: evidence commit changes unauthorized paths: {', '.join(unexpected)}"
        )
    return errors
