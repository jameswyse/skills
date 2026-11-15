#!/usr/bin/env python3
"""Collect inline bot review comments from a user's recently merged pull requests."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import date, datetime, timedelta
from pathlib import Path


EXCERPT_LENGTH = 600
GH_SEARCH_LIMIT = 1000

JsonObject = dict[str, object]


class CollectionError(Exception):
    pass


@dataclass(frozen=True)
class PullRequest:
    repository: str
    number: int
    title: str
    merged_month: str


@dataclass(frozen=True)
class Author:
    login: str
    is_bot: bool


@dataclass(frozen=True)
class ReviewComment:
    author: Author
    is_reply: bool
    path: str | None
    line: int | None
    created_at: str
    url: str
    body: str


@dataclass(frozen=True)
class BotComment:
    repository: str
    pull_request: int
    title: str
    bot: str
    path: str | None
    line: int | None
    created_at: str
    url: str
    body: str


@dataclass(frozen=True)
class MonthSummary:
    month: str
    pull_requests: int
    comments: int
    comments_per_pull_request: float


def gh_json(*arguments: str) -> object:
    result = subprocess.run(
        ["gh", *arguments], check=False, capture_output=True, text=True
    )
    if result.returncode != 0:
        raise CollectionError(f"gh {' '.join(arguments)} failed: {result.stderr.strip()}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise CollectionError(f"gh {' '.join(arguments)} returned invalid JSON: {error}") from error


def as_object(value: object, context: str) -> JsonObject:
    if not isinstance(value, dict):
        raise CollectionError(f"{context}: expected an object")
    return value


def as_list(value: object, context: str) -> list[object]:
    if not isinstance(value, list):
        raise CollectionError(f"{context}: expected a list")
    return value


def optional_text(value: JsonObject, key: str) -> str | None:
    item = value.get(key)
    return item if isinstance(item, str) else None


def optional_integer(value: JsonObject, key: str) -> int | None:
    item = value.get(key)
    return item if isinstance(item, int) and not isinstance(item, bool) else None


def required_text(value: JsonObject, key: str, context: str) -> str:
    item = optional_text(value, key)
    if item is None:
        raise CollectionError(f"{context}: expected text in {key!r}")
    return item


def required_integer(value: JsonObject, key: str, context: str) -> int:
    item = optional_integer(value, key)
    if item is None:
        raise CollectionError(f"{context}: expected an integer in {key!r}")
    return item


def merge_month(closed_at: str) -> str:
    try:
        return datetime.fromisoformat(closed_at.replace("Z", "+00:00")).strftime("%Y-%m")
    except ValueError as error:
        raise CollectionError(f"gh search prs result: invalid closedAt {closed_at!r}") from error


def parse_pull_request(raw: object) -> PullRequest:
    context = "gh search prs result"
    item = as_object(raw, context)
    repository = as_object(item.get("repository"), f"{context} repository")
    return PullRequest(
        repository=required_text(repository, "nameWithOwner", f"{context} repository"),
        number=required_integer(item, "number", context),
        title=required_text(item, "title", context),
        merged_month=merge_month(required_text(item, "closedAt", context)),
    )


def parse_author(item: JsonObject) -> Author | None:
    user = item.get("user")
    if not isinstance(user, dict):
        return None
    login = optional_text(user, "login")
    if login is None:
        return None
    return Author(login=login, is_bot=user.get("type") == "Bot")


def parse_review_comment(raw: object) -> ReviewComment | None:
    context = "pull request review comment"
    item = as_object(raw, context)
    author = parse_author(item)
    if author is None:
        return None
    return ReviewComment(
        author=author,
        is_reply=item.get("in_reply_to_id") is not None,
        path=optional_text(item, "path"),
        line=optional_integer(item, "line") or optional_integer(item, "original_line"),
        created_at=required_text(item, "created_at", context),
        url=required_text(item, "html_url", context),
        body=required_text(item, "body", context),
    )


def search_merged_pull_requests(author: str, since: str, limit: int) -> list[PullRequest]:
    results = gh_json(
        "search",
        "prs",
        "--author",
        author,
        "--merged",
        "--merged-at",
        f">={since}",
        "--limit",
        str(limit),
        "--json",
        "repository,number,title,closedAt",
    )
    return [parse_pull_request(item) for item in as_list(results, "gh search prs")]


def review_comments(pull_request: PullRequest) -> list[ReviewComment]:
    endpoint = f"repos/{pull_request.repository}/pulls/{pull_request.number}/comments"
    pages = as_list(gh_json("api", "--paginate", "--slurp", endpoint), endpoint)
    parsed = (
        parse_review_comment(comment)
        for page in pages
        for comment in as_list(page, endpoint)
    )
    return [comment for comment in parsed if comment is not None]


def is_selected_bot(author: Author, selected_logins: frozenset[str] | None) -> bool:
    if selected_logins is None:
        return author.is_bot
    return author.login.casefold() in selected_logins


def excerpt(body: str) -> str:
    collapsed = re.sub(r"\s+", " ", body).strip()
    if len(collapsed) <= EXCERPT_LENGTH:
        return collapsed
    return collapsed[: EXCERPT_LENGTH - 1].rstrip() + "…"


def bot_comments(
    pull_request: PullRequest,
    comments: list[ReviewComment],
    selected_logins: frozenset[str] | None,
) -> list[BotComment]:
    return [
        BotComment(
            repository=pull_request.repository,
            pull_request=pull_request.number,
            title=pull_request.title,
            bot=comment.author.login,
            path=comment.path,
            line=comment.line,
            created_at=comment.created_at,
            url=comment.url,
            body=excerpt(comment.body),
        )
        for comment in comments
        if is_selected_bot(comment.author, selected_logins) and not comment.is_reply
    ]


def summarize_months(
    pull_requests: list[PullRequest], comments: list[BotComment]
) -> list[MonthSummary]:
    month_of = {
        (pull_request.repository, pull_request.number): pull_request.merged_month
        for pull_request in pull_requests
    }
    pull_requests_by_month = Counter(month_of.values())
    comments_by_month = Counter(
        month_of[(comment.repository, comment.pull_request)] for comment in comments
    )
    return [
        MonthSummary(
            month=month,
            pull_requests=pull_requests_by_month[month],
            comments=comments_by_month[month],
            comments_per_pull_request=round(
                comments_by_month[month] / pull_requests_by_month[month], 2
            ),
        )
        for month in sorted(pull_requests_by_month)
    ]


def build_report(
    author: str,
    since: str,
    limit: int,
    pull_requests: list[PullRequest],
    comments: list[BotComment],
) -> JsonObject:
    commented_repositories = sorted({comment.repository for comment in comments})
    counted = [
        pull_request
        for pull_request in pull_requests
        if pull_request.repository in commented_repositories
    ]
    commented = {(comment.repository, comment.pull_request) for comment in comments}
    return {
        "summary": {
            "author": author,
            "merged_since": since,
            "merged_pull_requests": len(pull_requests),
            "limit_reached": len(pull_requests) >= limit,
            "bot_commented_repositories": commented_repositories,
            "counted_pull_requests": len(counted),
            "pull_requests_with_comments": len(commented),
            "comments": len(comments),
            "by_bot": dict(Counter(comment.bot for comment in comments).most_common()),
            "by_month": [asdict(month) for month in summarize_months(counted, comments)],
        },
        "comments": [asdict(comment) for comment in comments],
    }


def collect(
    author: str, since: str, limit: int, selected_logins: frozenset[str] | None
) -> JsonObject:
    pull_requests = search_merged_pull_requests(author, since, limit)
    comments = [
        comment
        for pull_request in pull_requests
        for comment in bot_comments(
            pull_request, review_comments(pull_request), selected_logins
        )
    ]
    return build_report(author, since, limit, pull_requests, comments)


def bot_login(value: str) -> str:
    login = value.strip().casefold()
    if not login:
        raise argparse.ArgumentTypeError("must not be blank")
    return login


def search_limit(value: str) -> int:
    limit = int(value)
    if not 1 <= limit <= GH_SEARCH_LIMIT:
        raise argparse.ArgumentTypeError(f"must be between 1 and {GH_SEARCH_LIMIT}")
    return limit


def parse_arguments(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--since",
        type=date.fromisoformat,
        default=date.today() - timedelta(days=30),
        help="earliest merge date, YYYY-MM-DD (default: 30 days ago)",
    )
    parser.add_argument(
        "--author", default="@me", help="pull request author (default: @me)"
    )
    parser.add_argument(
        "--limit",
        type=search_limit,
        default=GH_SEARCH_LIMIT,
        help=f"maximum pull requests, 1 to {GH_SEARCH_LIMIT} (default: {GH_SEARCH_LIMIT})",
    )
    parser.add_argument(
        "--bot",
        action="append",
        dest="bots",
        type=bot_login,
        help="inline comment login to include, such as Copilot; repeat for each (default: every bot account)",
    )
    parser.add_argument("--output", type=Path, help="write JSON here instead of stdout")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    arguments = parse_arguments(argv)
    try:
        report = collect(
            arguments.author,
            arguments.since.isoformat(),
            arguments.limit,
            frozenset(arguments.bots) if arguments.bots else None,
        )
    except CollectionError as error:
        print(error, file=sys.stderr)
        return 1
    output = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if arguments.output:
        arguments.output.write_text(output)
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
