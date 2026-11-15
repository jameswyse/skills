#!/usr/bin/env python3
"""Freeze a code review's scope as one diff from its base to a snapshot of the working tree."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


SCOPE_FILE = "scope.json"
PLAIN_DIFF = ("diff", "--no-color", "--no-ext-diff", "--no-textconv")


class ScopeError(Exception):
    pass


def git_bytes(*arguments: str, environment: dict[str, str] | None = None) -> bytes:
    completed = subprocess.run(["git", *arguments], capture_output=True, env=environment)
    if completed.returncode != 0:
        message = completed.stderr.decode(errors="replace").strip()
        raise ScopeError(message or f"git {' '.join(arguments)} failed")
    return completed.stdout


def git(*arguments: str, environment: dict[str, str] | None = None) -> str:
    return git_bytes(*arguments, environment=environment).decode(errors="replace")


def verified(ref: str) -> str:
    try:
        return git("rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}").strip()
    except ScopeError:
        raise ScopeError(f"'{ref}' is not a commit. Ask for a valid fixed point.") from None


def merge_base(base_ref: str, required: bool) -> str | None:
    try:
        return git("merge-base", verified(base_ref), "HEAD").strip()
    except ScopeError:
        if required:
            raise
        return None


def pull_request_base() -> str | None:
    if shutil.which("gh") is None:
        return None
    completed = subprocess.run(
        ["gh", "pr", "view", "--json", "baseRefName", "--jq", ".baseRefName"],
        capture_output=True,
        text=True,
    )
    branch = completed.stdout.strip()
    if completed.returncode != 0 or not branch:
        return None
    matches = git("for-each-ref", "--format=%(refname:short)", f"refs/remotes/*/{branch}").split()
    return matches[0] if len(matches) == 1 else None


def remote_default_branch() -> str | None:
    heads = git("for-each-ref", "--format=%(symref:short)", "refs/remotes/*/HEAD").split()
    return heads[0] if len(heads) == 1 else None


def resolve_base(explicit: str | None) -> str:
    if explicit:
        return explicit
    if git("status", "--porcelain").strip():
        return "HEAD"
    base = pull_request_base() or remote_default_branch()
    if base is None:
        raise ScopeError(
            "The working tree is clean and no pull request or single remote default branch"
            " names a base. Ask for a fixed point."
        )
    return base


def packet_object_store(packet: Path) -> dict[str, str]:
    objects = packet / "objects"
    objects.mkdir(exist_ok=True)
    repository_objects = Path(git("rev-parse", "--git-path", "objects").strip()).resolve()
    return {
        **os.environ,
        "GIT_OBJECT_DIRECTORY": str(objects),
        "GIT_ALTERNATE_OBJECT_DIRECTORIES": str(repository_objects),
    }


def submodules_with_uncommitted_changes() -> list[str]:
    staged_entries = git("ls-files", "--stage", "-z").split("\0")
    submodules = sorted({entry.split("\t", 1)[1] for entry in staged_entries if entry.startswith("160000 ")})
    return [
        path
        for path in submodules
        if (Path(path) / ".git").exists() and git("-C", path, "status", "--porcelain").strip()
    ]


def snapshot_working_tree(environment: dict[str, str]) -> str:
    with tempfile.TemporaryDirectory() as scratch:
        index = Path(scratch) / "index"
        current_index = Path(git("rev-parse", "--git-path", "index").strip())
        if current_index.exists():
            shutil.copyfile(current_index, index)
        environment = {**environment, "GIT_INDEX_FILE": str(index)}
        git("add", "-A", environment=environment)
        return git("write-tree", environment=environment).strip()


def freeze(base: str | None, packet: Path | None) -> dict[str, object]:
    previous = None
    if packet:
        packet = packet.resolve()
        if not (packet / SCOPE_FILE).is_file():
            raise ScopeError(f"{packet} holds no {SCOPE_FILE}. Run without --packet to start a review.")
        previous = json.loads((packet / SCOPE_FILE).read_text())
    os.chdir(git("rev-parse", "--show-toplevel").strip())
    base_ref = previous["base"] if previous else resolve_base(base)
    start = None if previous and base_ref == "HEAD" else merge_base(base_ref, required=previous is None)
    if start is None:
        start = previous["from"]
    packet = packet or Path(tempfile.mkdtemp(prefix="code-review-"))
    snapshot_store = packet_object_store(packet)
    tree = snapshot_working_tree(snapshot_store)

    (packet / "scope.diff").write_bytes(git_bytes(*PLAIN_DIFF, start, tree, environment=snapshot_store))
    changed_files = git(*PLAIN_DIFF, "--name-status", start, tree, environment=snapshot_store)
    (packet / "files.txt").write_text(changed_files)
    commits = git("log", "--oneline", "--no-color", "--no-show-signature", f"{start}..HEAD")
    (packet / "commits.txt").write_text(commits)

    scope: dict[str, object] = {
        "packet": str(packet),
        "base": base_ref,
        "from": start,
        "head": git("rev-parse", "HEAD").strip(),
        "tree": tree,
        "round": previous["round"] + 1 if previous else 1,
        "changed_files": len(changed_files.splitlines()),
        "commits": len(commits.splitlines()),
        "diff": str(packet / "scope.diff"),
        "dirty_submodules": submodules_with_uncommitted_changes(),
    }
    if previous:
        (packet / "fixes.diff").write_bytes(
            git_bytes(*PLAIN_DIFF, previous["tree"], tree, environment=snapshot_store)
        )
        scope["fixes_diff"] = str(packet / "fixes.diff")
    (packet / SCOPE_FILE).write_text(json.dumps(scope, indent=2) + "\n")
    return scope


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base",
        help="Fixed point to review from. Defaults to HEAD for a dirty tree, otherwise the pull"
        " request's base or the remote default branch.",
    )
    parser.add_argument(
        "--packet",
        type=Path,
        help="Packet directory from an earlier round. Refreshes scope.diff and writes fixes.diff"
        " with only the changes since that round.",
    )
    return parser.parse_args()


def main() -> int:
    arguments = parse_args()
    try:
        scope = freeze(arguments.base, arguments.packet)
    except ScopeError as error:
        print(str(error), file=sys.stderr)
        return 2
    print(json.dumps(scope, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
