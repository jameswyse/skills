from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SOURCE_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "sync-skills"
STATE_FILENAME = ".james-skills-links.json"


class SyncSkillsTest(unittest.TestCase):
    root: Path
    repository: Path
    target: Path
    skill: Path

    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp(prefix="skills-sync-test-"))
        self.repository = self.root / "repository"
        self.target = self.root / "installed"
        scripts = self.repository / "scripts"
        self.skill = self.repository / "skills" / "writing"
        scripts.mkdir(parents=True)
        self.skill.mkdir(parents=True)
        shutil.copyfile(SOURCE_SCRIPT, scripts / "sync-skills")
        (self.skill / "SKILL.md").write_text(
            "---\nname: writing\ndescription: Always apply.\n---\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        installed_skill = self.target / "writing"
        if installed_skill.is_symlink() or installed_skill.is_file():
            installed_skill.unlink()
        elif installed_skill.is_dir():
            marker = installed_skill / "marker"
            if marker.exists():
                marker.unlink()
            installed_skill.rmdir()

        state = self.target / STATE_FILENAME
        if state.exists():
            state.unlink()
        if self.target.exists():
            self.target.rmdir()

        skill_file = self.skill / "SKILL.md"
        if skill_file.exists():
            skill_file.unlink()
        if self.skill.exists():
            self.skill.rmdir()

        skills = self.repository / "skills"
        if skills.exists():
            skills.rmdir()
        script = self.repository / "scripts" / "sync-skills"
        if script.exists():
            script.unlink()
        scripts = self.repository / "scripts"
        if scripts.exists():
            scripts.rmdir()
        if self.repository.exists():
            self.repository.rmdir()
        self.root.rmdir()

    def run_sync(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(self.repository / "scripts" / "sync-skills"),
                "--target",
                str(self.target),
            ],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_creates_keeps_and_removes_managed_link(self) -> None:
        first = self.run_sync()
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertIn("sync complete: 1 skill present", first.stdout)
        installed = self.target / "writing"
        self.assertTrue(installed.is_symlink())
        self.assertEqual(installed.readlink(), self.skill.resolve())

        second = self.run_sync()
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertIn("current", second.stdout)

        (self.skill / "SKILL.md").unlink()
        self.skill.rmdir()

        third = self.run_sync()
        self.assertEqual(third.returncode, 0, third.stderr)
        self.assertFalse(installed.is_symlink())
        self.assertIn("removed", third.stdout)
        self.assertIn("sync complete: 0 skills present", third.stdout)

    def test_leaves_existing_skill_directory_unchanged(self) -> None:
        installed = self.target / "writing"
        installed.mkdir(parents=True)
        marker = installed / "marker"
        marker.write_text("existing\n", encoding="utf-8")

        result = self.run_sync()

        self.assertEqual(result.returncode, 1)
        self.assertEqual(marker.read_text(encoding="utf-8"), "existing\n")
        state = json.loads((self.target / STATE_FILENAME).read_text(encoding="utf-8"))
        self.assertEqual(state["links"], {})

    def test_leaves_unmanaged_symlink_unchanged(self) -> None:
        self.target.mkdir(parents=True)
        installed = self.target / "writing"
        installed.symlink_to(self.skill, target_is_directory=True)

        result = self.run_sync()

        self.assertEqual(result.returncode, 1)
        self.assertTrue(installed.is_symlink())
        self.assertEqual(installed.readlink(), self.skill)


if __name__ == "__main__":
    unittest.main()
