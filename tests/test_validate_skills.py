from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


SOURCE_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate-skills"


class ValidateSkillsTest(unittest.TestCase):
    root: Path
    repository: Path
    skills: list[Path]
    groups: list[Path]

    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp(prefix="skills-validation-test-"))
        self.repository = self.root / "repository"
        self.skills = []
        self.groups = []

        scripts = self.repository / "scripts"
        scripts.mkdir(parents=True)
        self.skill = self.add_skill("writing", "writing")
        repository_script = scripts / "validate-skills"
        shutil.copyfile(SOURCE_SCRIPT, repository_script)
        repository_script.chmod(0o755)

    def tearDown(self) -> None:
        for skill in self.skills:
            skill_file = skill / "SKILL.md"
            if skill_file.exists():
                skill_file.unlink()
            if skill.exists():
                skill.rmdir()

        for group in self.groups:
            if group.exists():
                group.rmdir()

        skills_root = self.repository / "skills"
        if skills_root.exists():
            skills_root.rmdir()
        repository_script = self.repository / "scripts" / "validate-skills"
        if repository_script.exists():
            repository_script.unlink()
        repository_scripts = self.repository / "scripts"
        if repository_scripts.exists():
            repository_scripts.rmdir()
        if self.repository.exists():
            self.repository.rmdir()
        self.root.rmdir()

    def add_skill(self, group: str, name: str) -> Path:
        skill = self.repository / "skills" / group / name
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: Test skill.\n---\n",
            encoding="utf-8",
        )
        self.skills.append(skill)
        self.groups.append(skill.parent)
        return skill

    def run_validation(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                str(self.repository / "scripts" / "validate-skills"),
                *arguments,
            ],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_validates_grouped_skill_by_name_without_codex(self) -> None:
        result = self.run_validation("writing")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("skills/writing/writing", result.stdout)
        self.assertIn("validation complete", result.stdout)

    def test_validates_every_grouped_skill_in_name_order(self) -> None:
        self.add_skill("engineering", "typescript")

        result = self.run_validation()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertLess(
            result.stdout.index("skills/engineering/typescript"),
            result.stdout.index("skills/writing/writing"),
        )

    def test_accepts_repository_relative_grouped_path(self) -> None:
        result = self.run_validation("skills/writing/writing")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("skills/writing/writing", result.stdout)

    def test_accepts_claude_code_frontmatter(self) -> None:
        (self.skill / "SKILL.md").write_text(
            "---\n"
            "name: writing\n"
            "description: Test skill.\n"
            "disable-model-invocation: true\n"
            "argument-hint: '[file]'\n"
            "---\n",
            encoding="utf-8",
        )

        result = self.run_validation("writing")

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_rejects_unknown_frontmatter_and_mismatched_name(self) -> None:
        (self.skill / "SKILL.md").write_text(
            "---\n"
            "name: another-name\n"
            "description: Test skill.\n"
            "unknown-field: true\n"
            "---\n",
            encoding="utf-8",
        )

        result = self.run_validation("writing")

        self.assertEqual(result.returncode, 1)
        self.assertIn("Unexpected frontmatter fields: unknown-field", result.stderr)
        self.assertIn("must match field 'name'", result.stderr)

    def test_rejects_non_string_frontmatter_field_name(self) -> None:
        (self.skill / "SKILL.md").write_text(
            "---\nname: writing\ndescription: Test skill.\n1: invalid\n---\n",
            encoding="utf-8",
        )

        result = self.run_validation("writing")

        self.assertEqual(result.returncode, 1)
        self.assertIn("Frontmatter field names must be strings", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_rejects_unfinished_description(self) -> None:
        (self.skill / "SKILL.md").write_text(
            "---\nname: writing\ndescription: '[TODO: finish this]'\n---\n",
            encoding="utf-8",
        )

        result = self.run_validation("writing")

        self.assertEqual(result.returncode, 1)
        self.assertIn("unfinished TODO placeholder", result.stderr)

    def test_rejects_duplicate_skill_names_across_groups(self) -> None:
        self.add_skill("productivity", "writing")

        result = self.run_validation()

        self.assertEqual(result.returncode, 1)
        self.assertIn("Duplicate skill directory name: writing", result.stderr)


if __name__ == "__main__":
    unittest.main()
