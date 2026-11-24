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

    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp(prefix="skills-validation-test-"))
        self.repository = self.root / "repository"
        self.skills = []

        scripts = self.repository / "scripts"
        scripts.mkdir(parents=True)
        self.skill = self.add_skill("writing")
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

    def add_skill(self, name: str) -> Path:
        skill = self.repository / "skills" / name
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: Test skill.\n---\n",
            encoding="utf-8",
        )
        self.skills.append(skill)
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

    def test_validates_skill_by_name_without_codex(self) -> None:
        result = self.run_validation("writing")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("skills/writing", result.stdout)
        self.assertIn("validation complete", result.stdout)

    def test_validates_every_skill_in_name_order(self) -> None:
        self.add_skill("typescript")

        result = self.run_validation()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertLess(
            result.stdout.index("skills/typescript"),
            result.stdout.index("skills/writing"),
        )

    def test_accepts_repository_relative_path(self) -> None:
        result = self.run_validation("skills/writing")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("skills/writing", result.stdout)

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

    def write_skill_of_length(self, characters: int) -> None:
        frontmatter = "---\nname: writing\ndescription: Test skill.\n---\n"
        (self.skill / "SKILL.md").write_text(
            frontmatter + "a" * (characters - len(frontmatter)),
            encoding="utf-8",
        )

    def test_accepts_skill_file_at_the_character_limit(self) -> None:
        self.write_skill_of_length(17_000)

        result = self.run_validation("writing")

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_rejects_skill_file_over_the_character_limit(self) -> None:
        self.write_skill_of_length(17_001)

        result = self.run_validation("writing")

        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "SKILL.md has 17,001 characters, over the 17,000-character limit",
            result.stderr,
        )
        self.assertIn(
            "first 5,000 tokens of an invoked skill after compaction", result.stderr
        )


if __name__ == "__main__":
    unittest.main()
