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
    claude_target: Path
    skill: Path
    created_skills: list[Path]
    instructions: Path
    installed_agents: Path
    installed_claude: Path
    codex_homes: list[Path]

    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp(prefix="skills-sync-test-"))
        self.repository = self.root / "repository"
        self.target = self.root / "installed"
        self.claude_target = self.root / "claude" / "skills"
        scripts = self.repository / "scripts"
        self.skill = self.repository / "skills" / "writing"
        self.created_skills = [self.skill]
        scripts.mkdir(parents=True)
        self.skill.mkdir(parents=True)
        shutil.copyfile(SOURCE_SCRIPT, scripts / "sync-skills")
        self.instructions = self.repository / "global"
        self.instructions.mkdir()
        (self.instructions / "AGENTS.md").write_text("# Global rules\n", encoding="utf-8")
        (self.instructions / "CLAUDE.md").write_text("@~/.agents/AGENTS.md\n", encoding="utf-8")
        self.installed_agents = self.root / "AGENTS.md"
        self.installed_claude = self.root / "claude" / "CLAUDE.md"
        self.codex_homes = [self.root / "codex", self.root / "codex-t3"]
        (self.skill / "SKILL.md").write_text(
            "---\nname: writing\ndescription: Always apply.\n---\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        for home in self.codex_homes:
            if (home / "AGENTS.md").is_symlink():
                (home / "AGENTS.md").unlink()
            if home.exists():
                home.rmdir()
        for installed in (self.installed_agents, self.installed_claude):
            for leftover in installed.parent.glob(f"{installed.name}*"):
                leftover.unlink()
        for name in ("AGENTS.md", "CLAUDE.md"):
            (self.instructions / name).unlink()
        self.instructions.rmdir()

        for target in (self.claude_target, self.target):
            installed_skill = target / "writing"
            if installed_skill.is_symlink() or installed_skill.is_file():
                installed_skill.unlink()
            elif installed_skill.is_dir():
                marker = installed_skill / "marker"
                if marker.exists():
                    marker.unlink()
                installed_skill.rmdir()

            state = target / STATE_FILENAME
            if state.exists():
                state.unlink()
            if target.exists():
                target.rmdir()

        claude_root = self.root / "claude"
        if claude_root.exists():
            claude_root.rmdir()

        for skill in self.created_skills:
            skill_file = skill / "SKILL.md"
            if skill_file.exists():
                skill_file.unlink()
            if skill.exists():
                skill.rmdir()

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
                "--claude-target",
                str(self.claude_target),
                *(argument for home in self.codex_homes for argument in ("--codex-home", str(home))),
            ],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_links_global_instruction_files_beside_the_skill_directories(self) -> None:
        first = self.run_sync()
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(self.installed_agents.readlink(), (self.instructions / "AGENTS.md").resolve())
        self.assertEqual(self.installed_claude.readlink(), (self.instructions / "CLAUDE.md").resolve())

        second = self.run_sync()
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertIn(f"current  {self.installed_agents}", second.stdout)

    def test_points_each_codex_home_at_the_shared_agents_file(self) -> None:
        result = self.run_sync()

        self.assertEqual(result.returncode, 0, result.stderr)
        for home in self.codex_homes:
            self.assertEqual((home / "AGENTS.md").readlink(), self.installed_agents)
            self.assertEqual((home / "AGENTS.md").read_text(encoding="utf-8"), "# Global rules\n")

    def test_replaces_an_identical_instruction_file_without_a_backup(self) -> None:
        self.installed_agents.write_text("# Global rules\n", encoding="utf-8")

        result = self.run_sync()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(self.installed_agents.is_symlink())
        self.assertEqual(list(self.root.glob("AGENTS.md.backup-*")), [])

    def test_backs_up_a_different_instruction_file_before_linking(self) -> None:
        self.installed_agents.write_text("# Local rules\n", encoding="utf-8")

        result = self.run_sync()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(self.installed_agents.is_symlink())
        backups = list(self.root.glob("AGENTS.md.backup-*"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(encoding="utf-8"), "# Local rules\n")

    def test_leaves_an_instruction_link_owned_elsewhere_unchanged(self) -> None:
        elsewhere = self.root / "AGENTS.md.elsewhere"
        elsewhere.write_text("# Other rules\n", encoding="utf-8")
        self.installed_agents.symlink_to(elsewhere)

        result = self.run_sync()

        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.installed_agents.readlink(), elsewhere)
        self.assertIn("left unchanged", result.stderr)

    def test_creates_keeps_and_removes_managed_link(self) -> None:
        first = self.run_sync()
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertIn("sync complete: 1 skill present", first.stdout)
        installed = self.target / "writing"
        self.assertTrue(installed.is_symlink())
        self.assertEqual(installed.readlink(), self.skill.resolve())
        claude_installed = self.claude_target / "writing"
        self.assertTrue(claude_installed.is_symlink())
        self.assertEqual(
            (self.claude_target / claude_installed.readlink()).resolve(),
            installed.resolve(),
        )

        second = self.run_sync()
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertIn("current", second.stdout)

        (self.skill / "SKILL.md").unlink()
        self.skill.rmdir()

        third = self.run_sync()
        self.assertEqual(third.returncode, 0, third.stderr)
        self.assertFalse(installed.is_symlink())
        self.assertFalse(claude_installed.is_symlink())
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

    def test_leaves_existing_claude_skill_directory_unchanged(self) -> None:
        installed = self.claude_target / "writing"
        installed.mkdir(parents=True)
        marker = installed / "marker"
        marker.write_text("existing\n", encoding="utf-8")

        result = self.run_sync()

        self.assertEqual(result.returncode, 1)
        self.assertEqual(marker.read_text(encoding="utf-8"), "existing\n")
        state = json.loads(
            (self.claude_target / STATE_FILENAME).read_text(encoding="utf-8")
        )
        self.assertEqual(state["links"], {})

    def test_rejects_identical_canonical_and_claude_targets(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(self.repository / "scripts" / "sync-skills"),
                "--target",
                str(self.target),
                "--claude-target",
                str(self.target),
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("must be different directories", result.stderr)
        self.assertFalse(self.target.exists())

    def test_updates_managed_link_whose_source_moved(self) -> None:
        first = self.run_sync()
        self.assertEqual(first.returncode, 0, first.stderr)

        earlier_source = str(self.repository / "skills" / "writing" / "writing")
        installed = self.target / "writing"
        installed.unlink()
        installed.symlink_to(earlier_source)
        state_path = self.target / STATE_FILENAME
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["links"]["writing"] = earlier_source
        state_path.write_text(json.dumps(state), encoding="utf-8")

        second = self.run_sync()

        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertIn("updated", second.stdout)
        self.assertEqual(installed.readlink(), self.skill.resolve())

if __name__ == "__main__":
    unittest.main()
