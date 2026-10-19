from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


COLLECT_SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "engineering"
    / "code-review"
    / "scripts"
    / "collect_bot_comments.py"
)

FAKE_GH = """#!{python}
import json
import sys
from pathlib import Path

fixtures = json.loads(Path({fixtures!r}).read_text())
arguments = sys.argv[1:]
with Path({log!r}).open("a") as log:
    log.write(json.dumps(arguments) + "\\n")
if arguments[:2] == ["search", "prs"]:
    print(json.dumps(fixtures["search"]))
elif arguments[0] == "api":
    key = arguments[-1]
    if key not in fixtures["comments"]:
        print("HTTP 404: Not Found", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(fixtures["comments"][key]))
"""


def pull_request(repository: str, number: int, merged_at: str) -> dict[str, object]:
    return {
        "repository": {"nameWithOwner": repository},
        "number": number,
        "title": f"Change {number}",
        "closedAt": merged_at,
    }


def comment(user: dict[str, object] | None, body: str = "Finding", reply_to: int | None = None) -> dict[str, object]:
    return {
        "user": user,
        "body": body,
        "path": "src/app.ts",
        "line": 12,
        "created_at": "2026-10-01T00:00:00Z",
        "html_url": "https://github.com/acme/app/pull/1#discussion_r1",
        "in_reply_to_id": reply_to,
    }


def bot(login: str) -> dict[str, object]:
    return {"login": login, "type": "Bot"}


def human(login: str) -> dict[str, object]:
    return {"login": login, "type": "User"}


def comments_endpoint(repository: str, number: int) -> str:
    return f"repos/{repository}/pulls/{number}/comments"


def single_pull_request(*comments: dict[str, object]) -> dict[str, object]:
    return {
        "search": [pull_request("acme/app", 1, "2026-10-02T00:00:00Z")],
        "comments": {comments_endpoint("acme/app", 1): [list(comments)]},
    }


class CollectBotCommentsTest(unittest.TestCase):
    def run_collect(
        self, fixtures: dict[str, object], *arguments: str
    ) -> tuple[subprocess.CompletedProcess[str], list[list[str]]]:
        with tempfile.TemporaryDirectory(prefix="bot-comments-test-") as directory:
            root = Path(directory)
            fixtures_path = root / "fixtures.json"
            fixtures_path.write_text(json.dumps(fixtures))
            log_path = root / "gh.log"
            log_path.touch()
            gh = root / "gh"
            gh.write_text(
                FAKE_GH.format(
                    python=sys.executable, fixtures=str(fixtures_path), log=str(log_path)
                )
            )
            gh.chmod(0o755)
            result = subprocess.run(
                [sys.executable, str(COLLECT_SCRIPT), *arguments],
                check=False,
                capture_output=True,
                text=True,
                env={**os.environ, "PATH": f"{root}{os.pathsep}{os.environ['PATH']}"},
            )
            calls = [json.loads(line) for line in log_path.read_text().splitlines()]
            return result, calls

    def report(self, fixtures: dict[str, object], *arguments: str) -> dict[str, object]:
        result, _ = self.run_collect(fixtures, *arguments)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_searches_only_pull_requests_merged_since_the_date(self) -> None:
        _, calls = self.run_collect({"search": [], "comments": {}}, "--since", "2026-09-01")

        self.assertIn("--merged", calls[0])
        self.assertEqual(calls[0][calls[0].index("--merged-at") + 1], ">=2026-09-01")

    def test_counts_only_pull_requests_in_repositories_with_bot_comments(self) -> None:
        fixtures = {
            "search": [
                pull_request("acme/app", 1, "2026-10-01T00:00:00Z"),
                pull_request("acme/app", 2, "2026-10-02T00:00:00Z"),
                pull_request("acme/docs", 3, "2026-10-03T00:00:00Z"),
            ],
            "comments": {
                comments_endpoint("acme/app", 1): [[comment(bot("Copilot"))]],
                comments_endpoint("acme/app", 2): [[]],
                comments_endpoint("acme/docs", 3): [[comment(human("jameswyse"))]],
            },
        }

        summary = self.report(fixtures)["summary"]

        self.assertEqual(summary["merged_pull_requests"], 3)
        self.assertEqual(summary["bot_commented_repositories"], ["acme/app"])
        self.assertEqual(summary["counted_pull_requests"], 2)
        self.assertEqual(summary["pull_requests_with_comments"], 1)

    def test_groups_comments_by_merge_month(self) -> None:
        fixtures = {
            "search": [
                pull_request("acme/app", 1, "2026-09-30T00:00:00Z"),
                pull_request("acme/app", 2, "2026-10-02T00:00:00Z"),
            ],
            "comments": {
                comments_endpoint("acme/app", 1): [
                    [comment(bot("Copilot"))],
                    [comment(bot("chatgpt-codex-connector[bot]"))],
                ],
                comments_endpoint("acme/app", 2): [[]],
            },
        }

        by_month = self.report(fixtures)["summary"]["by_month"]

        self.assertEqual(
            by_month,
            [
                {"month": "2026-09", "pull_requests": 1, "comments": 2, "comments_per_pull_request": 2.0},
                {"month": "2026-10", "pull_requests": 1, "comments": 0, "comments_per_pull_request": 0.0},
            ],
        )

    def test_counts_comments_by_bot(self) -> None:
        fixtures = single_pull_request(
            comment(bot("Copilot")),
            comment(bot("Copilot")),
            comment(bot("chatgpt-codex-connector[bot]")),
        )

        by_bot = self.report(fixtures)["summary"]["by_bot"]

        self.assertEqual(by_bot, {"Copilot": 2, "chatgpt-codex-connector[bot]": 1})

    def test_skips_replies_human_comments_and_deleted_accounts(self) -> None:
        fixtures = single_pull_request(
            comment(bot("Copilot"), "Top level"),
            comment(bot("Copilot"), "Follow-up", reply_to=10),
            comment(human("jameswyse"), "Human note"),
            comment(None, "Deleted account"),
        )

        comments = self.report(fixtures)["comments"]

        self.assertEqual([entry["body"] for entry in comments], ["Top level"])

    def test_includes_every_bot_account_by_default(self) -> None:
        comments = self.report(single_pull_request(comment(bot("macroscopeapp[bot]"))))["comments"]

        self.assertEqual([entry["bot"] for entry in comments], ["macroscopeapp[bot]"])

    def test_bot_option_selects_trimmed_logins_case_insensitively(self) -> None:
        fixtures = single_pull_request(comment(bot("Copilot")), comment(bot("other[bot]")))

        comments = self.report(fixtures, "--bot", " OTHER[bot] ")["comments"]

        self.assertEqual([entry["bot"] for entry in comments], ["other[bot]"])

    def test_keeps_code_in_bodies_and_collapses_whitespace(self) -> None:
        fixtures = single_pull_request(
            comment(bot("Copilot"), "Reject `x < 1 || x > 3`\n\n  in   `Map<string, number>`")
        )

        body = self.report(fixtures)["comments"][0]["body"]

        self.assertEqual(body, "Reject `x < 1 || x > 3` in `Map<string, number>`")

    def test_truncates_long_bodies(self) -> None:
        long_body = "x" * 5000

        body = self.report(single_pull_request(comment(bot("Copilot"), long_body)))["comments"][0]["body"]

        self.assertLess(len(body), len(long_body))
        self.assertTrue(body.endswith("…"))

    def test_rejects_blank_bot_logins(self) -> None:
        result, _ = self.run_collect(single_pull_request(), "--bot", "  ")

        self.assertEqual(result.returncode, 2)
        self.assertIn("must not be blank", result.stderr)

    def test_reports_when_the_limit_is_reached(self) -> None:
        fixtures = single_pull_request()

        self.assertTrue(self.report(fixtures, "--limit", "1")["summary"]["limit_reached"])
        self.assertFalse(self.report(fixtures, "--limit", "2")["summary"]["limit_reached"])

    def test_rejects_limits_outside_the_search_range(self) -> None:
        for limit in ("0", "1001"):
            with self.subTest(limit=limit):
                result, _ = self.run_collect(single_pull_request(), "--limit", limit)

                self.assertEqual(result.returncode, 2)
                self.assertIn("between 1 and 1000", result.stderr)

    def test_reports_gh_failure(self) -> None:
        fixtures = {"search": [pull_request("acme/gone", 9, "2026-10-02T00:00:00Z")], "comments": {}}

        result, _ = self.run_collect(fixtures)

        self.assertEqual(result.returncode, 1)
        self.assertIn("HTTP 404", result.stderr)

    def test_rejects_unparseable_merge_dates(self) -> None:
        fixtures = {"search": [pull_request("acme/app", 1, "yesterday")], "comments": {}}

        result, _ = self.run_collect(fixtures)

        self.assertEqual(result.returncode, 1)
        self.assertIn("invalid closedAt", result.stderr)

    def test_rejects_unexpected_gh_output(self) -> None:
        result, _ = self.run_collect({"search": [{"number": 1}], "comments": {}})

        self.assertEqual(result.returncode, 1)
        self.assertIn("repository", result.stderr)


if __name__ == "__main__":
    unittest.main()
