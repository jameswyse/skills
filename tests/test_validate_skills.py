from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SOURCE_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate-skills"


class ValidateSkillsTest(unittest.TestCase):
    root: Path
    repository: Path
    codex_home: Path
    log: Path
    skills: list[Path]
    groups: list[Path]

    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp(prefix="skills-validation-test-"))
        self.repository = self.root / "repository"
        self.codex_home = self.root / "codex"
        self.log = self.root / "validator.log"
        self.skills = []
        self.groups = []

        scripts = self.repository / "scripts"
        scripts.mkdir(parents=True)
        shutil.copyfile(SOURCE_SCRIPT, scripts / "validate-skills")

        validator = (
            self.codex_home
            / "skills"
            / ".system"
            / "skill-creator"
            / "scripts"
            / "quick_validate.py"
        )
        validator.parent.mkdir(parents=True)
        validator.write_text(
            """from __future__ import annotations

import os
import sys
from pathlib import Path

with Path(os.environ["VALIDATOR_LOG"]).open("a", encoding="utf-8") as log:
    log.write(f"{sys.argv[1]}\\n")
""",
            encoding="utf-8",
        )
        self.add_skill("writing", "writing")

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

        validator = (
            self.codex_home
            / "skills"
            / ".system"
            / "skill-creator"
            / "scripts"
            / "quick_validate.py"
        )
        if validator.exists():
            validator.unlink()
        for directory in (
            validator.parent,
            validator.parent.parent,
            validator.parent.parent.parent,
            validator.parent.parent.parent.parent,
            self.codex_home,
        ):
            if directory.exists():
                directory.rmdir()

        if self.log.exists():
            self.log.unlink()
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
                sys.executable,
                str(self.repository / "scripts" / "validate-skills"),
                *arguments,
            ],
            check=False,
            capture_output=True,
            text=True,
            env={
                **os.environ,
                "CODEX_HOME": str(self.codex_home),
                "VALIDATOR_LOG": str(self.log),
            },
        )

    def validated_paths(self) -> list[Path]:
        if not self.log.exists():
            return []
        return [Path(line) for line in self.log.read_text().splitlines()]

    def test_validates_grouped_skill_by_name(self) -> None:
        result = self.run_validation("writing")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            self.validated_paths(),
            [(self.repository / "skills" / "writing" / "writing").resolve()],
        )

    def test_validates_every_grouped_skill_in_name_order(self) -> None:
        typescript = self.add_skill("engineering", "typescript")

        result = self.run_validation()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            self.validated_paths(),
            [typescript.resolve(), self.skills[0].resolve()],
        )

    def test_accepts_repository_relative_grouped_path(self) -> None:
        result = self.run_validation("skills/writing/writing")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.validated_paths(), [self.skills[0].resolve()])

    def test_rejects_duplicate_skill_names_across_groups(self) -> None:
        self.add_skill("productivity", "writing")

        result = self.run_validation()

        self.assertEqual(result.returncode, 1)
        self.assertIn("Duplicate skill directory name: writing", result.stderr)
        self.assertEqual(self.validated_paths(), [])


if __name__ == "__main__":
    unittest.main()
