#!/usr/bin/env python3
"""Externally pinned, role-separated release trust policy helpers."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import subprocess
from pathlib import Path

POLICY_DIGEST_ENV = "GESTUR_RELEASE_TRUST_POLICY_SHA256"
REGISTRIES = {
    "reviewer": "security/release-reviewers.txt",
    "pentester": "security/external-pentesters.txt",
    "tag-signer": "security/release-tag-signers.txt",
}
FINGERPRINT_RE = re.compile(r"^[0-9A-F]{40}(?:[0-9A-F]{24})?$")
DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")


def git_blob(repository: Path, revision: str, relative: str) -> bytes | None:
    result = subprocess.run(
        ["git", "-C", str(repository), "show", f"{revision}:{relative}"],
        check=False,
        capture_output=True,
    )
    return result.stdout if result.returncode == 0 else None


def registry_entries(
    repository: Path, revision: str, role: str, errors: list[str] | None = None
) -> list[tuple[str, str]]:
    selected_errors = errors if errors is not None else []
    path = REGISTRIES[role]
    raw = git_blob(repository, revision, path)
    if raw is None:
        selected_errors.append(f"release trust policy: missing {path} at {revision}")
        return []
    try:
        content = raw.decode("utf-8")
    except UnicodeDecodeError:
        selected_errors.append(f"release trust policy: {path} is not UTF-8")
        return []
    entries: list[tuple[str, str]] = []
    for line_number, line in enumerate(content.splitlines(), start=1):
        if not line or line.startswith("#"):
            continue
        parts = [part.strip() for part in line.split("|")]
        if len(parts) != 2 or not FINGERPRINT_RE.fullmatch(parts[0]) or not parts[1]:
            selected_errors.append(
                f"release trust policy: malformed {path} line {line_number}"
            )
            continue
        entries.append((parts[0], parts[1]))
    fingerprints = [fingerprint for fingerprint, _identity in entries]
    identities = [identity for _fingerprint, identity in entries]
    if len(fingerprints) != len(set(fingerprints)):
        selected_errors.append(f"release trust policy: duplicate fingerprint in {path}")
    if len(identities) != len(set(identities)):
        selected_errors.append(f"release trust policy: duplicate identity in {path}")
    return entries


def trust_policy_digest(repository: Path, revision: str) -> str | None:
    digest = hashlib.sha256(b"gestur-release-trust-policy-v1\0")
    for role, relative in REGISTRIES.items():
        raw = git_blob(repository, revision, relative)
        if raw is None:
            return None
        for field in (role.encode(), relative.encode(), raw):
            digest.update(len(field).to_bytes(8, "big"))
            digest.update(field)
    return digest.hexdigest()


def validate_trust_policy(
    repository: Path,
    revision: str,
    expected_digest: str | None = None,
) -> list[str]:
    errors: list[str] = []
    entries_by_role = {
        role: registry_entries(repository, revision, role, errors) for role in REGISTRIES
    }
    roles_by_fingerprint: dict[str, set[str]] = {}
    for role, entries in entries_by_role.items():
        for fingerprint, _identity in entries:
            roles_by_fingerprint.setdefault(fingerprint, set()).add(role)
    for fingerprint, roles in roles_by_fingerprint.items():
        if len(roles) > 1:
            errors.append(
                "release trust policy: fingerprint "
                f"{fingerprint} crosses roles: {', '.join(sorted(roles))}"
            )

    expected = expected_digest or os.environ.get(POLICY_DIGEST_ENV)
    if expected is None:
        errors.append(f"release trust policy: missing external {POLICY_DIGEST_ENV}")
        return errors
    if not DIGEST_RE.fullmatch(expected):
        errors.append("release trust policy: external digest is malformed")
        return errors
    actual = trust_policy_digest(repository, revision)
    if actual is None:
        errors.append("release trust policy: cannot calculate candidate policy digest")
    elif actual != expected:
        errors.append("release trust policy: candidate policy differs from external pin")
    return errors


def identity_is_authorized(
    repository: Path,
    revision: str,
    role: str,
    fingerprint: str,
    identity: str | None = None,
) -> bool:
    entries = registry_entries(repository, revision, role)
    if identity is None:
        return sum(key == fingerprint for key, _name in entries) == 1
    return entries.count((fingerprint, identity)) == 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("revision", nargs="?", default="HEAD")
    parser.add_argument("--repository", type=Path, default=Path("."))
    args = parser.parse_args()
    digest = trust_policy_digest(args.repository.resolve(), args.revision)
    if digest is None:
        parser.error("revision lacks one or more release trust registries")
    print(digest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
