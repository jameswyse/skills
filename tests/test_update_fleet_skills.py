from __future__ import annotations

import os
import re
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

    def run_script(
        self, *args: str, environment: dict[str, str] | None = None
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(self.repository / "scripts" / "update-fleet-skills"), *args],
            capture_output=True,
            text=True,
            env={
                **os.environ,
                "HOMELAB_DIR": str(self.root / "missing-homelab"),
                **(environment or {}),
            },
        )

    def test_help_exits_without_running_the_rollout(self) -> None:
        (self.repository / "draft.md").write_text("draft\n", encoding="utf-8")

        result = self.run_script("--help")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("update-fleet-skills", result.stdout)
        self.assertNotIn("uncommitted changes", result.stderr)

    def test_rejects_an_unknown_argument_without_running_the_rollout(self) -> None:
        (self.repository / "draft.md").write_text("draft\n", encoding="utf-8")

        result = self.run_script("--no-such-option")

        self.assertEqual(result.returncode, 2)
        self.assertIn("--no-such-option", result.stderr)
        self.assertNotIn("uncommitted changes", result.stderr)

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

    def test_fast_forwards_each_remote_checkout_under_its_home(self) -> None:
        for step in ("validate-skills", "setup-external-skills", "sync-skills"):
            script = self.repository / "scripts" / step
            script.write_text("#!/bin/sh\n", encoding="utf-8")
            script.chmod(0o755)
        self.commit("Add rollout steps")
        git(self.repository, "push", "--quiet")
        rollout = self.repository / "scripts" / "update-fleet-skills"
        configured, settings_changed = re.subn(
            r"(?m)^REMOTE_CHECKOUT_UNDER_HOME = .*$",
            'REMOTE_CHECKOUT_UNDER_HOME = "Code/my skills"',
            rollout.read_text(encoding="utf-8"),
        )
        self.assertEqual(settings_changed, 1)
        rollout.write_text(configured, encoding="utf-8")
        remote_home = self.root / "remote-home"
        remote_checkout = remote_home / "Code" / "my skills"
        remote_checkout.parent.mkdir(parents=True)
        git(self.root, "clone", "--quiet", str(self.root / "origin.git"), str(remote_checkout))
        self.commit("Change a skill")
        git(self.repository, "push", "--quiet")
        fleet = self.root / "homelab" / "scripts" / "fleet"
        fleet.parent.mkdir(parents=True)
        fleet.write_text(
            "#!/bin/sh\n"
            "shift\n"
            'while [ "$1" = -o ]; do shift 2; done\n'
            "shift\n"
            'HOME="$REMOTE_HOME" exec sh -c "$*"\n',
            encoding="utf-8",
        )
        fleet.chmod(0o755)

        result = self.run_script(
            environment={
                "HOMELAB_DIR": str(self.root / "homelab"),
                "REMOTE_HOME": str(remote_home),
            }
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(
            git(remote_checkout, "rev-parse", "HEAD"),
            git(self.repository, "rev-parse", "HEAD"),
        )


if __name__ == "__main__":
    unittest.main()
