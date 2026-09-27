from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


SOURCE_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "update-fleet-skills"


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(
        ("git", *args), cwd=cwd, check=True, capture_output=True, text=True
    ).stdout.strip()


class UpdateFleetSkillsPreflightTest(unittest.TestCase):
    root: Path
    repository: Path

    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory(prefix="skills-fleet-test-")
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        origin = self.root / "origin.git"
        self.repository = self.root / "repository"
        git(self.root, "init", "--quiet", "--bare", "--initial-branch=master", str(origin))
        git(self.root, "clone", "--quiet", str(origin), str(self.repository))
        git(self.repository, "config", "user.name", "Test")
        git(self.repository, "config", "user.email", "test@example.com")
        scripts = self.repository / "scripts"
        scripts.mkdir()
        shutil.copy2(SOURCE_SCRIPT, scripts / "update-fleet-skills")
        self.commit("Initial commit")
        git(self.repository, "push", "--quiet", "-u", "origin", "master")

    def commit(self, message: str) -> None:
        git(self.repository, "add", "--all")
        git(self.repository, "commit", "--quiet", "--allow-empty", "-m", message)

    def run_script(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(self.repository / "scripts" / "update-fleet-skills")],
            capture_output=True,
            text=True,
            env={**os.environ, "HOMELAB_DIR": str(self.root / "missing-homelab")},
        )

    def test_refuses_uncommitted_changes(self) -> None:
        (self.repository / "draft.md").write_text("draft\n", encoding="utf-8")

        result = self.run_script()

        self.assertEqual(result.returncode, 2)
        self.assertIn("uncommitted changes", result.stderr)
        self.assertIn("draft.md", result.stderr)

    def test_refuses_unpushed_commits(self) -> None:
        self.commit("Local only")

        result = self.run_script()

        self.assertEqual(result.returncode, 2)
        self.assertIn("1 unpushed commit(s)", result.stderr)
        self.assertIn("Local only", result.stderr)

    def test_refuses_checkout_behind_upstream(self) -> None:
        other = self.root / "other"
        git(self.root, "clone", "--quiet", str(self.root / "origin.git"), str(other))
        git(other, "-c", "user.name=Test", "-c", "user.email=test@example.com",
            "commit", "--quiet", "--allow-empty", "-m", "Elsewhere")
        git(other, "push", "--quiet")

        result = self.run_script()

        self.assertEqual(result.returncode, 2)
        self.assertIn("1 commit(s) behind origin/master", result.stderr)

    def test_published_checkout_passes_preflight(self) -> None:
        result = self.run_script()

        self.assertEqual(result.returncode, 2)
        self.assertIn("missing-homelab/scripts/fleet not found", result.stderr)


if __name__ == "__main__":
    unittest.main()
