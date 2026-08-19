#!/usr/bin/env python3
"""Real GnuPG integration tests for release evidence and predecessor tags."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

REPOSITORY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY / "scripts"))

import validate_release_evidence as validator  # noqa: E402
import release_evidence_testkit as fixtures  # noqa: E402


def run(
    arguments: list[str], *, directory: Path | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        arguments,
        cwd=directory,
        check=True,
        capture_output=True,
        text=True,
    )


class ReleaseSignatureIntegrationTests(unittest.TestCase):
    def create_key(self, home: Path) -> str:
        home.mkdir(mode=0o700)
        with patch.dict(os.environ, {"GNUPGHOME": str(home)}):
            run(
                [
                    "gpg",
                    "--batch",
                    "--pinentry-mode",
                    "loopback",
                    "--passphrase",
                    "",
                    "--quick-generate-key",
                    "Gestur Release Test <release-test@example.invalid>",
                    "ed25519",
                    "sign",
                    "0",
                ]
            )
            listing = run(
                ["gpg", "--batch", "--with-colons", "--list-secret-keys"]
            ).stdout
        return next(
            line.split(":")[9]
            for line in listing.splitlines()
            if line.startswith("fpr:")
        )

    def test_detached_evidence_signature_and_tamper_detection(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fingerprint = self.create_key(root / "gnupg")
            record = root / "review.md"
            signature = root / "review.md.asc"
            record.write_text("reviewed evidence\n", encoding="utf-8")
            with patch.dict(os.environ, {"GNUPGHOME": str(root / "gnupg")}):
                run(
                    [
                        "gpg",
                        "--batch",
                        "--armor",
                        "--detach-sign",
                        "--local-user",
                        fingerprint,
                        "--output",
                        str(signature),
                        str(record),
                    ]
                )
                self.assertEqual(
                    validator.default_signature_verifier(signature, record),
                    fingerprint,
                )
                record.write_text("tampered evidence\n", encoding="utf-8")
                self.assertIsNone(
                    validator.default_signature_verifier(signature, record)
                )

    def test_signed_annotated_tag_and_unsigned_tag_rejection(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fingerprint = self.create_key(root / "gnupg")
            repository = root / "repository"
            repository.mkdir()
            with patch.dict(os.environ, {"GNUPGHOME": str(root / "gnupg")}):
                run(["git", "init", "-q"], directory=repository)
                run(["git", "config", "user.name", "Gestur Test"], directory=repository)
                run(
                    ["git", "config", "user.email", "gestur-test@example.invalid"],
                    directory=repository,
                )
                run(
                    ["git", "commit", "-q", "--allow-empty", "-m", "candidate"],
                    directory=repository,
                )
                run(
                    ["git", "tag", "-s", "-u", fingerprint, "-m", "v0.1.0", "v0.1.0"],
                    directory=repository,
                )
                run(["git", "tag", "-a", "-m", "unsigned", "v0.1.1"], directory=repository)
                self.assertEqual(
                    validator.default_tag_verifier(repository, "v0.1.0"),
                    fingerprint,
                )
                self.assertIsNone(
                    validator.default_tag_verifier(repository, "v0.1.1")
                )

    def test_arbitrary_valid_tag_key_is_not_release_authority(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fingerprint = self.create_key(root / "gnupg")
            with patch.dict(os.environ, {"GNUPGHOME": str(root / "gnupg")}):
                repository = root / "repository"
                repository.mkdir()
                fixture = fixtures.GitFixture(repository)
                fixture.commit("v0.1.0")
                fixture.run("tag", "-s", "-u", fingerprint, "-m", "v0.1.0", "v0.1.0")
                candidate = fixture.commit("candidate")
                fixtures.write_source_evidence(fixture, "v0.1.1", candidate)
                fixture.commit("evidence")
                errors = fixtures.validate(
                    fixture,
                    "v0.1.1",
                    candidate,
                    {"v0.1.0", "v0.1.1"},
                    tag_verifier=validator.default_tag_verifier,
                )
        self.assertTrue(any("signer is not authorized" in error for error in errors))

    def test_authorized_external_pentest_signature_passes_full_gate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fingerprint = self.create_key(root / "gnupg")
            repository = root / "repository"
            repository.mkdir()
            fixture = fixtures.GitFixture(repository)
            fixture.write(
                "security/external-pentesters.txt",
                f"{fingerprint} | Independent Pentester\n",
            )
            candidate = fixture.commit("candidate")
            fixtures.write_source_evidence(fixture, "v0.1.0", candidate)
            fixtures.write_pentest_evidence(
                fixture,
                "v0.1.0",
                candidate,
                tester_key=fingerprint,
                signature="placeholder\n",
            )
            attestation = repository / "security/pentest/v0.1.0.md"
            signature = repository / "security/pentest/v0.1.0.md.asc"
            signature.unlink()
            with patch.dict(os.environ, {"GNUPGHOME": str(root / "gnupg")}):
                run(
                    [
                        "gpg",
                        "--batch",
                        "--armor",
                        "--detach-sign",
                        "--local-user",
                        fingerprint,
                        "--output",
                        str(signature),
                        str(attestation),
                    ]
                )
                fixture.commit("evidence")

                def verify(selected: Path, record: Path) -> str | None:
                    if "pentest" in record.parts:
                        return validator.default_signature_verifier(selected, record)
                    return fixtures.valid_signature(selected, record)

                errors = fixtures.validate(
                    fixture,
                    "v0.1.0",
                    candidate,
                    {"v0.1.0"},
                    signature_verifier=verify,
                )
        self.assertEqual(errors, [])

    def test_merge_evidence_commit_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = fixtures.GitFixture(Path(directory))
            candidate = fixture.commit("candidate")
            main = fixture.run("branch", "--show-current")
            fixture.run("switch", "-q", "-c", "evidence-side")
            fixtures.write_source_evidence(fixture, "v0.1.0", candidate)
            fixture.commit("side evidence")
            fixture.run("switch", "-q", main)
            fixture.run("merge", "-q", "--no-ff", "-m", "evidence", "evidence-side")
            errors = fixtures.validate(
                fixture, "v0.1.0", candidate, {"v0.1.0"}
            )
        self.assertTrue(any("exactly one parent" in error for error in errors))

    def test_self_declared_untrusted_reviewer_key_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = fixtures.GitFixture(Path(directory))
            fixture.write("security/release-reviewers.txt", "# nobody authorized\n")
            candidate = fixture.commit("candidate")
            fixtures.write_source_evidence(fixture, "v0.1.0", candidate)
            fixture.commit("evidence")
            errors = fixtures.validate(
                fixture, "v0.1.0", candidate, {"v0.1.0"}
            )
        self.assertTrue(any("not authorized by the candidate" in error for error in errors))

    def test_ambiguous_reviewer_key_authorization_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fixture = fixtures.GitFixture(Path(directory))
            fixture.write(
                "security/release-reviewers.txt",
                f"{fixtures.REVIEWER_KEY} | Release Reviewer\n"
                f"{fixtures.REVIEWER_KEY} | Another Identity\n",
            )
            candidate = fixture.commit("candidate")
            fixtures.write_source_evidence(fixture, "v0.1.0", candidate)
            fixture.commit("evidence")
            errors = fixtures.validate(
                fixture, "v0.1.0", candidate, {"v0.1.0"}
            )
        self.assertTrue(any("duplicate fingerprint" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
