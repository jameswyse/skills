from __future__ import annotations

import importlib.machinery
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "eval-skills"


def load_eval_skills():
    loader = importlib.machinery.SourceFileLoader("eval_skills", str(SCRIPT))
    spec = importlib.util.spec_from_loader("eval_skills", loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules["eval_skills"] = module
    loader.exec_module(module)
    return module


class EvalSkillsExitStatusTest(unittest.TestCase):
    def setUp(self) -> None:
        self.eval_skills = load_eval_skills()
        self.out = tempfile.TemporaryDirectory(prefix="eval-skills-test-")
        self.addCleanup(self.out.cleanup)
        self.evals = tempfile.TemporaryDirectory(prefix="eval-skills-probes-")
        self.addCleanup(self.evals.cleanup)
        Path(self.evals.name, "sample.toml").write_text(
            'skill = "sample"\n\n[[probe]]\nid = "only-probe"\nkind = "decision"\n'
            "prompt = 'Question.'\nexpect = 'Pass: answer.'\n"
        )

    def run_main(self, passes: dict[str, bool], *arguments: str) -> int:
        def evaluate(cell, base, out) -> dict:
            return {
                "skill": cell.probe.skill,
                "probe": cell.probe.id,
                "arm": cell.arm,
                "model": cell.model,
                "run": cell.run,
                "pass": passes[cell.arm],
                "score": None,
            }

        argv = ["eval-skills", *arguments, "--models", "opus", "--out", self.out.name]
        with (
            mock.patch.object(self.eval_skills, "evaluate", evaluate),
            mock.patch.object(self.eval_skills, "EVALS", Path(self.evals.name)),
            mock.patch.object(sys, "argv", argv),
        ):
            with mock.patch("sys.stdout"):
                return self.eval_skills.main()

    def test_fails_when_a_probe_passes_before_and_fails_after(self) -> None:
        status = self.run_main({"none": False, "before": True, "after": False}, "sample", "--probe", "only-probe")

        self.assertEqual(status, 1)

    def test_succeeds_when_after_keeps_every_pass(self) -> None:
        status = self.run_main({"none": False, "before": True, "after": True}, "sample", "--probe", "only-probe")

        self.assertEqual(status, 0)

    def test_fails_when_no_probe_matches_the_selection(self) -> None:
        with self.assertRaises(SystemExit) as raised:
            self.run_main({}, "sample", "--probe", "sample/only-probe")

        self.assertNotEqual(raised.exception.code, 0)


class RunCodexToolUseTest(unittest.TestCase):
    def setUp(self) -> None:
        self.eval_skills = load_eval_skills()

    def run_codex(self, *events: dict) -> dict:
        completed = subprocess.CompletedProcess(
            args=["codex"],
            returncode=0,
            stdout="\n".join(json.dumps(event) for event in events),
            stderr="",
        )
        with mock.patch.object(self.eval_skills.subprocess, "run", return_value=completed):
            return self.eval_skills.run_codex("Question.", Path("."), "gpt-6.1-sol", live=False)

    def test_feature_warning_is_not_tool_use(self) -> None:
        result = self.run_codex(
            {
                "type": "item.completed",
                "item": {
                    "id": "item_0",
                    "type": "error",
                    "message": "Under-development features enabled: default_mode_request_user_input.",
                },
            },
            {"type": "item.completed", "item": {"id": "item_1", "type": "agent_message", "text": "Answer."}},
        )

        self.assertEqual(result, {"answer": "Answer.", "used_tools": False})

    def test_command_execution_is_tool_use(self) -> None:
        result = self.run_codex(
            {
                "type": "item.completed",
                "item": {"id": "item_0", "type": "command_execution", "command": "ls", "exit_code": 0},
            },
            {"type": "item.completed", "item": {"id": "item_1", "type": "agent_message", "text": "Answer."}},
        )

        self.assertEqual(result, {"answer": "Answer.", "used_tools": True})


if __name__ == "__main__":
    unittest.main()
