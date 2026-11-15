from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REVIEW_SCOPE_SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "engineering"
    / "code-review"
    / "scripts"
    / "review_scope.py"
)


class ReviewScopeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        root = Path(self.scratch.name)
        self.repository = root / "repository"
        self.repository.mkdir()
        tools = root / "tools"
        tools.mkdir()
        fake_gh = tools / "gh"
        fake_gh.write_text("#!/bin/sh\nexit 1\n")
        fake_gh.chmod(0o755)
        self.environment = {
            **os.environ,
            "PATH": f"{tools}{os.pathsep}{os.environ['PATH']}",
            "TMPDIR": str(root),
            "GIT_AUTHOR_NAME": "Test",
            "GIT_AUTHOR_EMAIL": "test@example.invalid",
            "GIT_COMMITTER_NAME": "Test",
            "GIT_COMMITTER_EMAIL": "test@example.invalid",
        }
        self.git("init", "-q", "-b", "main")
        self.write("kept.txt", "kept\n")
        self.commit("initial")

    def git(self, *arguments: str) -> str:
        return subprocess.run(
            ["git", *arguments],
            cwd=self.repository,
            env=self.environment,
            check=True,
            capture_output=True,
            text=True,
        ).stdout

    def write(self, name: str, content: str) -> None:
        (self.repository / name).write_text(content)

    def commit(self, message: str) -> None:
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)

    def freeze(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(REVIEW_SCOPE_SCRIPT), *arguments],
            cwd=self.repository,
            env=self.environment,
            capture_output=True,
            text=True,
        )

    def scope(self, *arguments: str) -> dict[str, object]:
        completed = self.freeze(*arguments)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        return json.loads(completed.stdout)

    def test_dirty_tree_scope_includes_untracked_files_and_leaves_the_index_alone(self) -> None:
        self.write("kept.txt", "changed\n")
        self.write("new.txt", "untracked\n")

        scope = self.scope()

        diff = Path(scope["diff"]).read_text()
        self.assertIn("+changed", diff)
        self.assertIn("+untracked", diff)
        self.assertEqual(scope["base"], "HEAD")
        self.assertEqual(scope["changed_files"], 2)
        self.assertEqual(self.git("diff", "--cached", "--name-only"), "")
        self.assertIn("?? new.txt", self.git("status", "--porcelain"))

    def test_snapshot_objects_stay_out_of_the_repository(self) -> None:
        self.write("new.txt", "untracked\n")
        objects_before = self.git("count-objects", "-v")

        scope = self.scope()

        self.assertEqual(self.git("count-objects", "-v"), objects_before)
        completed = subprocess.run(
            ["git", "cat-file", "-e", str(scope["tree"])], cwd=self.repository, env=self.environment
        )
        self.assertNotEqual(completed.returncode, 0)

    def test_fixed_point_scope_joins_commits_and_working_tree_changes_from_the_merge_base(self) -> None:
        self.git("checkout", "-q", "-b", "feature")
        self.write("feature.txt", "committed\n")
        self.commit("feature")
        self.git("checkout", "-q", "main")
        self.write("main-only.txt", "moved on\n")
        self.commit("main moves on")
        self.git("checkout", "-q", "feature")
        self.write("kept.txt", "uncommitted\n")

        scope = self.scope("--base", "main")

        diff = Path(scope["diff"]).read_text()
        self.assertIn("+committed", diff)
        self.assertIn("+uncommitted", diff)
        self.assertNotIn("main-only.txt", diff)
        self.assertEqual(scope["commits"], 1)
        self.assertEqual(Path(scope["packet"], "commits.txt").read_text().split()[1:], ["feature"])

    def test_later_round_writes_only_the_changes_since_the_previous_round(self) -> None:
        self.write("kept.txt", "first attempt\n")
        first = self.scope()
        self.write("fix.txt", "the fix\n")

        second = self.scope("--packet", str(first["packet"]))

        fixes = Path(second["fixes_diff"]).read_text()
        self.assertIn("+the fix", fixes)
        self.assertNotIn("first attempt", fixes)
        self.assertIn("+first attempt", Path(second["diff"]).read_text())
        self.assertEqual(second["round"], 2)
        self.assertEqual(second["from"], first["from"])

    def test_text_that_is_not_utf8_reaches_the_diff_unchanged(self) -> None:
        (self.repository / "kept.txt").write_bytes("caf\u00e9\n".encode("latin-1"))

        scope = self.scope()

        self.assertIn(b"+caf\xe9\n", Path(scope["diff"]).read_bytes())

    def test_submodule_with_uncommitted_changes_is_named(self) -> None:
        library = Path(self.scratch.name) / "library"
        library.mkdir()
        for arguments in (["init", "-q", "-b", "main"], ["commit", "-q", "--allow-empty", "-m", "initial"]):
            subprocess.run(["git", *arguments], cwd=library, env=self.environment, check=True)
        self.git("-c", "protocol.file.allow=always", "submodule", "add", "-q", str(library), "vendor/library")
        self.commit("add library")
        (self.repository / "vendor" / "library" / "local.txt").write_text("uncommitted\n")

        scope = self.scope("--base", "HEAD")

        self.assertEqual(scope["dirty_submodules"], ["vendor/library"])
        self.assertEqual(scope["changed_files"], 0)

    def test_moved_submodule_with_uncommitted_changes_is_named(self) -> None:
        library = Path(self.scratch.name) / "library"
        library.mkdir()
        for arguments in (["init", "-q", "-b", "main"], ["commit", "-q", "--allow-empty", "-m", "initial"]):
            subprocess.run(["git", *arguments], cwd=library, env=self.environment, check=True)
        self.git("-c", "protocol.file.allow=always", "submodule", "add", "-q", str(library), "vendor/library")
        self.commit("add library")
        self.git("mv", "vendor/library", "vendor/moved")
        (self.repository / "vendor" / "moved" / "local.txt").write_text("uncommitted\n")

        scope = self.scope()

        self.assertEqual(scope["dirty_submodules"], ["vendor/moved"])

    def test_later_round_follows_a_rebase_onto_the_moved_base(self) -> None:
        self.git("checkout", "-q", "-b", "feature")
        self.write("feature.txt", "committed\n")
        self.commit("feature")
        first = self.scope("--base", "main")
        self.git("checkout", "-q", "main")
        self.write("main-only.txt", "moved on\n")
        self.commit("main moves on")
        self.git("checkout", "-q", "feature")
        self.git("rebase", "-q", "main")

        second = self.scope("--packet", str(first["packet"]))

        self.assertNotEqual(second["from"], first["from"])
        self.assertNotIn("main-only.txt", Path(second["diff"]).read_text())
        self.assertIn("+committed", Path(second["diff"]).read_text())

    def test_diff_ignores_color_and_external_diff_configuration(self) -> None:
        self.git("config", "color.diff", "always")
        self.git("config", "diff.external", "false")
        self.write("kept.txt", "changed\n")

        scope = self.scope()

        self.assertTrue(Path(scope["diff"]).read_text().startswith("diff --git "))

    def test_later_round_survives_deletion_of_the_base_branch(self) -> None:
        self.git("branch", "base")
        self.git("checkout", "-q", "-b", "feature")
        self.write("feature.txt", "committed\n")
        self.commit("feature")
        first = self.scope("--base", "base")
        self.git("branch", "-D", "base")

        second = self.scope("--packet", str(first["packet"]))

        self.assertEqual(second["from"], first["from"])

    def test_renamed_file_with_a_status_like_name_does_not_break_the_scope(self) -> None:
        self.write("1 old", "content\n")
        self.commit("add oddly named file")
        self.git("mv", "1 old", "new")

        scope = self.scope()

        self.assertEqual(scope["dirty_submodules"], [])
        self.assertEqual(scope["changed_files"], 1)

    def test_text_converter_configuration_does_not_empty_the_diff(self) -> None:
        self.write(".gitattributes", "*.txt diff=hidden\n")
        self.commit("attributes")
        self.git("config", "diff.hidden.textconv", "true")
        self.write("kept.txt", "changed\n")

        scope = self.scope()

        self.assertIn("+changed", Path(scope["diff"]).read_text())

    def test_unchanged_scope_reports_no_changed_files(self) -> None:
        scope = self.scope("--base", "HEAD")

        self.assertEqual(scope["changed_files"], 0)
        self.assertEqual(scope["dirty_submodules"], [])
        self.assertEqual(Path(scope["diff"]).read_text(), "")

    def test_clean_tree_without_a_pull_request_or_remote_asks_for_a_fixed_point(self) -> None:
        completed = self.freeze()

        self.assertEqual(completed.returncode, 2)
        self.assertIn("Ask for a fixed point", completed.stderr)

    def test_clean_tree_uses_the_single_remote_default_branch(self) -> None:
        self.git("update-ref", "refs/remotes/origin/main", "HEAD")
        self.git("symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main")
        self.git("checkout", "-q", "-b", "feature")
        self.write("feature.txt", "committed\n")
        self.commit("feature")

        scope = self.scope()

        self.assertEqual(scope["base"], "origin/main")
        self.assertIn("+committed", Path(scope["diff"]).read_text())

    def test_unknown_fixed_point_is_rejected(self) -> None:
        completed = self.freeze("--base", "no-such-ref")

        self.assertEqual(completed.returncode, 2)
        self.assertIn("not a commit", completed.stderr)


if __name__ == "__main__":
    unittest.main()
