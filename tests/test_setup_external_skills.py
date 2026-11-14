from __future__ import annotations

import json
import os
import shlex
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "setup-external-skills"


class SetupExternalSkillsTest(unittest.TestCase):
    root: Path
    bin_dir: Path
    state: Path
    log: Path
    environment: dict[str, str]

    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory(prefix="external-skills-test-")
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.bin_dir = self.root / "bin"
        self.bin_dir.mkdir()
        self.state = self.root / "state.json"
        self.log = self.root / "commands.jsonl"
        self.state.write_text("[]\n", encoding="utf-8")

        fake_npx = self.bin_dir / "npx"
        fake_npx.write_text(
            """#!/usr/bin/env python3
import json
import os
import shutil
import sys
from pathlib import Path

state_path = Path(os.environ["FAKE_SKILLS_STATE"])
log_path = Path(os.environ["FAKE_SKILLS_LOG"])
args = sys.argv[1:]

with log_path.open("a", encoding="utf-8") as log:
    log.write(json.dumps(args) + "\\n")

state = json.loads(state_path.read_text(encoding="utf-8"))
command = args[1]

if command == os.environ.get("FAKE_SKILLS_FAILING_COMMAND"):
    raise SystemExit(1)

if command == "list":
    print(json.dumps(state))
    raise SystemExit(0)

if command == "add":
    source = args[2]
    if source == "https://cli.sentry.dev":
        source = "cli.sentry.dev"
    skill_index = args.index("--skill") + 1
    agent_names = {
        "codex": "Codex",
        "claude-code": "Claude Code",
    }
    agents = [
        agent_names[args[index + 1]]
        for index, value in enumerate(args)
        if value == "--agent"
    ]
    names = []
    for value in args[skill_index:]:
        if value.startswith("-"):
            break
        names.append(value)
    known = {record["name"]: record for record in state}
    for name in names:
        known[name] = {"name": name, "source": source, "agents": agents}
    state_path.write_text(json.dumps(list(known.values())), encoding="utf-8")
    raise SystemExit(0)

if command == "update":
    raise SystemExit(0)

if command == "remove":
    names = []
    for value in args[2:]:
        if value.startswith("-"):
            break
        names.append(value)
    for name in names:
        shutil.rmtree(Path.cwd() / "agent" / "skills" / name, ignore_errors=True)
    removed = {name.lower() for name in names}
    remaining = [record for record in state if record["name"].lower() not in removed]
    if "survives-removal" in names:
        remaining.append({"name": "survives-removal", "source": None, "agents": ["Codex"]})
    state_path.write_text(json.dumps(remaining), encoding="utf-8")
    raise SystemExit(0)

raise SystemExit(2)
""",
            encoding="utf-8",
        )
        fake_npx.chmod(0o755)

        self.environment = {
            **os.environ,
            "PATH": f"{self.bin_dir}{os.pathsep}{os.environ['PATH']}",
            "FAKE_SKILLS_STATE": str(self.state),
            "FAKE_SKILLS_LOG": str(self.log),
        }

    def run_setup(
        self, *args: str, cwd: Path | None = None
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(SCRIPT), *args],
            check=False,
            capture_output=True,
            text=True,
            env=self.environment,
            cwd=cwd,
        )

    def commands(self) -> list[list[str]]:
        return [json.loads(line) for line in self.log.read_text().splitlines()]

    def test_installs_missing_skills_then_updates_them_on_the_next_run(self) -> None:
        first = self.run_setup()
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertIn("setup complete", first.stdout)
        installed = json.loads(self.state.read_text(encoding="utf-8"))
        names = {record["name"] for record in installed}
        self.assertIn("animate", names)
        self.assertIn("sentry-cli", names)
        self.assertNotIn("emil-design-eng", names)

        self.log.write_text("", encoding="utf-8")
        second = self.run_setup()
        self.assertEqual(second.returncode, 0, second.stderr)
        commands = self.commands()
        update = next(command for command in commands if command[1] == "update")
        self.assertIn("animate", update)
        self.assertIn("sentry-cli", update)
        self.assertIn("vercel-react-best-practices", update)
        self.assertNotIn("emil-design-eng", update)
        self.assertFalse(any(command[1] == "add" for command in commands))

    def test_refuses_to_overwrite_a_skill_from_another_source(self) -> None:
        self.state.write_text(
            json.dumps(
                [
                    {
                        "name": "animate",
                        "source": "another/source",
                        "agents": ["Codex"],
                    }
                ]
            ),
            encoding="utf-8",
        )

        result = self.run_setup()

        self.assertEqual(result.returncode, 1)
        self.assertIn("Refusing to overwrite existing skills", result.stderr)
        self.assertFalse(
            any(command[1] in {"add", "update"} for command in self.commands())
        )

    def test_adds_missing_claude_binding_for_an_installed_skill(self) -> None:
        self.state.write_text(
            json.dumps(
                [
                    {
                        "name": "animate",
                        "source": "emilkowalski/skills",
                        "agents": ["Codex"],
                    }
                ]
            ),
            encoding="utf-8",
        )

        result = self.run_setup()

        self.assertEqual(result.returncode, 0, result.stderr)
        add = next(
            command
            for command in self.commands()
            if command[1] == "add" and command[2] == "emilkowalski/skills"
        )
        self.assertIn("animate", add)
        self.assertIn("claude-code", add)
        installed = {
            record["name"]: record for record in json.loads(self.state.read_text())
        }
        self.assertIn("Claude Code", installed["animate"]["agents"])

    def test_dry_run_reports_changes_without_installing(self) -> None:
        unlisted = [{"name": "ad-hoc", "source": "someone/skills", "agents": ["Codex"]}]
        self.state.write_text(json.dumps(unlisted), encoding="utf-8")

        result = self.run_setup("--dry-run")

        self.assertEqual(result.returncode, 0, result.stderr)
        printed = [
            shlex.split(line.removeprefix("$ "))
            for line in result.stdout.splitlines()
            if line.startswith("$ ")
        ]
        removal = next(command for command in printed if command[2] == "remove")
        self.assertIn("ad-hoc", removal)
        self.assertIn("--global", removal)
        self.assertIn("npx skills@latest add https://cli.sentry.dev", result.stdout)
        self.assertIn("npx skills@latest add", result.stdout)
        self.assertIn("--agent codex --agent claude-code", result.stdout)
        self.assertEqual(json.loads(self.state.read_text(encoding="utf-8")), unlisted)
        self.assertFalse(
            any(command[1] in {"add", "update", "remove"} for command in self.commands())
        )

    def test_removes_installed_skills_missing_from_the_manifest(self) -> None:
        self.state.write_text(
            json.dumps(
                [
                    {"name": "ad-hoc", "source": "someone/skills", "agents": ["Codex"]},
                    {"name": "writing", "source": None, "agents": ["Codex"]},
                ]
            ),
            encoding="utf-8",
        )

        project_skill = self.root / "project" / "agent" / "skills" / "ad-hoc" / "SKILL.md"
        project_skill.parent.mkdir(parents=True)
        project_skill.write_text("a project skill that shares the removed name\n", encoding="utf-8")

        result = self.run_setup(cwd=self.root / "project")

        self.assertEqual(result.returncode, 0, result.stderr)
        installed = {record["name"] for record in json.loads(self.state.read_text(encoding="utf-8"))}
        self.assertNotIn("ad-hoc", installed)
        self.assertIn("writing", installed)
        self.assertTrue(project_skill.exists())

    def test_fails_when_an_unlisted_skill_survives_removal(self) -> None:
        self.state.write_text(
            json.dumps(
                [{"name": "survives-removal", "source": "someone/skills", "agents": ["Codex"]}]
            ),
            encoding="utf-8",
        )

        result = self.run_setup()

        self.assertEqual(result.returncode, 1)
        self.assertIn("survives-removal", result.stderr)

    def test_fails_when_removal_takes_a_listed_skill_with_it(self) -> None:
        self.state.write_text(
            json.dumps(
                [{"name": "Animate", "source": "emilkowalski/skills", "agents": ["Codex"]}]
            ),
            encoding="utf-8",
        )

        result = self.run_setup()

        self.assertEqual(result.returncode, 1)
        self.assertIn("animate", result.stderr)

    def test_keeps_an_unlisted_skill_when_installing_a_listed_one_fails(self) -> None:
        self.state.write_text(
            json.dumps([{"name": "ad-hoc", "source": "someone/skills", "agents": ["Codex"]}]),
            encoding="utf-8",
        )
        self.environment["FAKE_SKILLS_FAILING_COMMAND"] = "add"

        result = self.run_setup()

        self.assertEqual(result.returncode, 1)
        installed = {record["name"] for record in json.loads(self.state.read_text(encoding="utf-8"))}
        self.assertIn("ad-hoc", installed)

    def test_refuses_to_remove_a_skill_whose_name_reads_as_an_option(self) -> None:
        self.state.write_text(
            json.dumps([{"name": "--all", "source": "someone/skills", "agents": ["Codex"]}]),
            encoding="utf-8",
        )

        result = self.run_setup()

        self.assertEqual(result.returncode, 1)
        self.assertIn("--all", result.stderr)
        self.assertFalse(
            any(command[1] in {"add", "update", "remove"} for command in self.commands())
        )


if __name__ == "__main__":
    unittest.main()
