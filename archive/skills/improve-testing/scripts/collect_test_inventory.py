#!/usr/bin/env python3
"""Collect a reviewable test inventory without executing repository code."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


SKIP_DIRECTORIES = {
    ".cache",
    ".git",
    ".gradle",
    ".idea",
    ".next",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".turbo",
    ".venv",
    ".vscode",
    "__pycache__",
    "build",
    "coverage",
    "deriveddata",
    "dist",
    "node_modules",
    "out",
    "target",
    "venv",
}
SOURCE_SUFFIXES = {
    ".bats",
    ".c",
    ".cc",
    ".cjs",
    ".clj",
    ".cljs",
    ".cpp",
    ".cts",
    ".cs",
    ".ex",
    ".exs",
    ".go",
    ".java",
    ".js",
    ".jsx",
    ".kt",
    ".kts",
    ".mjs",
    ".mts",
    ".php",
    ".py",
    ".rb",
    ".rs",
    ".scala",
    ".sh",
    ".swift",
    ".ts",
    ".tsx",
}
TEST_DIRECTORY_NAMES = {"__tests__", "spec", "specs", "test", "tests"}
SUPPORT_DIRECTORY_NAMES = {
    "factories",
    "fixtures",
    "mocks",
    "snapshots",
    "stubs",
    "test-data",
    "testdata",
}
SUPPORT_NAME = re.compile(
    r"(?:^|[._-])(?:fixture|fixtures|mock|mocks|setup|snapshot|snapshots|stub|stubs|"
    r"testdata|test-data|test-helper|test-helpers|factory|factories)(?:[._-]|$)",
    re.IGNORECASE,
)
TEST_SUPPORT_BASENAME = re.compile(
    r"^(?:conftest|setup_tests?|setuptests|"
    r"test[_-](?:factories|fixtures|helpers|mocks|setup|stubs|utils))$",
    re.IGNORECASE,
)
TEST_BASENAME = re.compile(
    r"(?:^test_.+|.+_test|.+[._-](?:test|tests|spec|specs))$", re.IGNORECASE
)
CONFIG_BASENAME = re.compile(
    r"^(?:ava\.config|cypress\.config|jest\.config|karma\.conf|mocha\.config|"
    r"playwright\.config|testcafe\.config|vitest\.config)(?:\..+)?$|"
    r"^(?:phpunit\.xml(?:\.dist)?|pytest\.ini|tox\.ini|\.coveragerc|\.rspec|\.mocharc(?:\..+)?)$",
    re.IGNORECASE,
)
MANIFEST_NAMES = {
    "build.gradle",
    "build.gradle.kts",
    "Cargo.toml",
    "composer.json",
    "deps.edn",
    "Directory.Packages.props",
    "Gemfile",
    "go.mod",
    "mix.exs",
    "package.json",
    "Package.swift",
    "Pipfile",
    "pom.xml",
    "project.clj",
    "pyproject.toml",
    "requirements-dev.txt",
    "requirements-test.txt",
    "requirements.txt",
    "setup.cfg",
    "build.sbt",
}
MANIFEST_SUFFIXES = {".csproj", ".fsproj", ".vbproj"}
TEST_TOOL_TERMS = re.compile(
    r"(?:@playwright|@testing-library|\bava\b|\bbats\b|\bc8\b|\bchai\b|"
    r"\bcoverage\b|\bcucumber\b|\bcypress\b|\bdoctest\b|\bfactory-boy\b|"
    r"\bfast-check\b|\bfreezegun\b|\bgo-cmp\b|\bginkgo\b|\bgomega\b|"
    r"\bhamcrest\b|\bhypothesis\b|\bistanbul\b|\bjasmine\b|\bjest\b|"
    r"\bjsdom\b|\bjunit\b|\bkarma\b|\bmockall\b|\bmocha\b|\bmockito\b|"
    r"\bmsw\b|\bmutmut\b|\bnock\b|\bnunit\b|\bnyc\b|\bpact\b|\bphpunit\b|"
    r"\bplaywright\b|\bproptest\b|\bpuppeteer\b|\bpytest\b|\bquickcheck\b|"
    r"\bresponses\b|\brespx\b|\brspec\b|\bselenium\b|\bsinon\b|\bstryker\b|"
    r"\bsupertest\b|\btap\b|\btape\b|\btestcafe\b|\btestcontainers\b|"
    r"\btestify\b|\btesting-library\b|\btestng\b|\btox\b|\bunittest\b|"
    r"\bvitest\b|\bwebdriverio\b|\bwiremock\b|\bxunit\b)",
    re.IGNORECASE,
)
MAX_TEXT_BYTES = 2_000_000


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Inventory test files, declared cases, test support, and test-related "
            "manifest entries without running repository code."
        )
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        type=Path,
        help="repository root (default: current directory)",
    )
    parser.add_argument(
        "--scope",
        action="append",
        default=[],
        type=Path,
        help="path inside the root to inventory; repeat for several paths",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="write JSON to this file instead of standard output",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="write compact JSON",
    )
    return parser.parse_args()


def relative_path(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def resolve_scopes(root: Path, requested: list[Path]) -> list[Path]:
    scopes = requested or [Path(".")]
    resolved: list[Path] = []
    for scope in scopes:
        candidate = scope.resolve() if scope.is_absolute() else (root / scope).resolve()
        try:
            candidate.relative_to(root)
        except ValueError as error:
            raise ValueError(
                f"scope is outside the repository root: {scope}"
            ) from error
        if not candidate.exists():
            raise ValueError(f"scope does not exist: {scope}")
        if candidate not in resolved:
            resolved.append(candidate)
    return resolved


def is_within_scope(path: Path, scopes: list[Path]) -> bool:
    for scope in scopes:
        if path == scope:
            return True
        try:
            path.relative_to(scope)
            return True
        except ValueError:
            continue
    return False


def has_skipped_directory(path: Path, root: Path) -> bool:
    return any(
        part.lower() in SKIP_DIRECTORIES for part in path.relative_to(root).parts[:-1]
    )


def git_files(root: Path, scopes: list[Path]) -> list[Path] | None:
    scope_arguments = [relative_path(scope, root) or "." for scope in scopes]
    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "ls-files",
                "-co",
                "--exclude-standard",
                "-z",
                "--",
                *scope_arguments,
            ],
            check=False,
            capture_output=True,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None

    files: list[Path] = []
    for raw_path in result.stdout.split(b"\0"):
        if not raw_path:
            continue
        path = (root / os.fsdecode(raw_path)).resolve()
        if (
            path.is_file()
            and is_within_scope(path, scopes)
            and not has_skipped_directory(path, root)
        ):
            files.append(path)
    return sorted(set(files))


def filesystem_files(root: Path, scopes: list[Path]) -> list[Path]:
    files: set[Path] = set()
    for scope in scopes:
        if scope.is_file():
            files.add(scope)
            continue
        for current_root, directories, filenames in os.walk(scope):
            directories[:] = sorted(
                directory
                for directory in directories
                if directory.lower() not in SKIP_DIRECTORIES
            )
            base = Path(current_root)
            for filename in sorted(filenames):
                path = (base / filename).resolve()
                if is_within_scope(path, scopes) and not has_skipped_directory(
                    path, root
                ):
                    files.add(path)
    return sorted(files)


def collect_files(root: Path, scopes: list[Path]) -> tuple[str, list[Path]]:
    files = git_files(root, scopes)
    if files is not None:
        return "git ls-files -co --exclude-standard", files
    return "filesystem walk with generated-directory exclusions", filesystem_files(
        root, scopes
    )


def read_text(path: Path) -> tuple[str | None, str | None]:
    try:
        if path.stat().st_size > MAX_TEXT_BYTES:
            return None, f"file exceeds {MAX_TEXT_BYTES} bytes"
        raw = path.read_bytes()
    except OSError as error:
        return None, str(error)
    if b"\0" in raw:
        return None, "binary file"
    try:
        return raw.decode("utf-8"), None
    except UnicodeDecodeError:
        return raw.decode("utf-8", errors="replace"), "invalid UTF-8 replaced"


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def case_entry(
    path: str,
    line: int,
    name: str,
    kind: str,
    framework_hint: str,
    status: str = "active",
) -> dict[str, Any]:
    return {
        "id": f"{path}:{line}:{name}",
        "path": path,
        "line": line,
        "name": name,
        "kind": kind,
        "framework_hint": framework_hint,
        "status": status,
    }


def extract_javascript_cases(path: str, text: str) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    patterns = [
        re.compile(
            r"(?<![\w$])(?P<call>it|test)(?P<mods>(?:\.(?:concurrent|fails|only|skip|todo))*)"
            r"\s*\(\s*(?P<quote>['\"`])(?P<name>[^\n'\"`]+)(?P=quote)",
        ),
        re.compile(
            r"(?<![\w$])(?P<call>it|test)(?P<mods>(?:\.(?:concurrent|only|skip))*)"
            r"\.each(?:<[^>]+>)?\s*(?:\([^;]{0,2000}?\)|`[^`]{0,2000}`)\s*"
            r"\(\s*(?P<quote>['\"`])(?P<name>[^\n'\"`]+)(?P=quote)",
            re.DOTALL,
        ),
    ]
    seen: set[tuple[int, str]] = set()
    for pattern in patterns:
        for match in pattern.finditer(text):
            name = match.group("name").strip()
            line = line_number(text, match.start())
            key = (line, name)
            if key in seen:
                continue
            seen.add(key)
            modifiers = match.group("mods") or ""
            status = (
                "todo"
                if ".todo" in modifiers
                else "skipped"
                if ".skip" in modifiers
                else "active"
            )
            cases.append(
                case_entry(path, line, name, "test", match.group("call"), status)
            )
    return sorted(cases, key=lambda case: (case["line"], case["name"]))


def extract_python_cases(path: str, text: str) -> list[dict[str, Any]]:
    pattern = re.compile(
        r"^[ \t]*(?:async[ \t]+)?def[ \t]+(test_[A-Za-z0-9_]+)[ \t]*\(", re.MULTILINE
    )
    return [
        case_entry(
            path,
            line_number(text, match.start()),
            match.group(1),
            "test",
            "pytest or unittest",
        )
        for match in pattern.finditer(text)
    ]


def extract_go_cases(path: str, text: str) -> list[dict[str, Any]]:
    pattern = re.compile(
        r"^func[ \t]+(Test|Benchmark|Example)([A-Za-z0-9_]*)[ \t]*\(", re.MULTILINE
    )
    cases = []
    for match in pattern.finditer(text):
        prefix = match.group(1)
        kind = {"Test": "test", "Benchmark": "benchmark", "Example": "example"}[prefix]
        cases.append(
            case_entry(
                path,
                line_number(text, match.start()),
                f"{prefix}{match.group(2)}",
                kind,
                "go test",
            )
        )
    return cases


def extract_rust_cases(path: str, text: str) -> list[dict[str, Any]]:
    pattern = re.compile(
        r"#\[(?P<attribute>(?:[A-Za-z0-9_:]+::)?test)\][\s\S]{0,240}?"
        r"(?:async\s+)?fn\s+(?P<name>[A-Za-z0-9_]+)\s*\(",
    )
    return [
        case_entry(
            path,
            line_number(text, match.start()),
            match.group("name"),
            "test",
            match.group("attribute"),
        )
        for match in pattern.finditer(text)
    ]


def extract_annotated_cases(path: str, text: str) -> list[dict[str, Any]]:
    lines = text.splitlines()
    cases: list[dict[str, Any]] = []
    pending: tuple[int, str] | None = None
    annotation = re.compile(
        r"@(?P<kind>Test|ParameterizedTest|RepeatedTest|TestFactory)\b|\[(?P<kind_cs>(?:Fact|Theory|Test))\b"
    )
    method = re.compile(
        r"\b(?:fun|func|void|public|private|protected|internal|static|async|Task|[A-Za-z0-9_<>,?\[\]]+)"
        r"(?:\s+[A-Za-z0-9_<>,?\[\]]+){0,5}\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*\("
    )
    for index, line in enumerate(lines, start=1):
        annotation_match = annotation.search(line)
        if annotation_match:
            pending = (
                index,
                annotation_match.group("kind") or annotation_match.group("kind_cs"),
            )
        if pending is None:
            continue
        method_match = method.search(line)
        if method_match:
            cases.append(
                case_entry(path, index, method_match.group("name"), "test", pending[1])
            )
            pending = None
        elif index - pending[0] > 8:
            pending = None
    return cases


def extract_ruby_cases(path: str, text: str) -> list[dict[str, Any]]:
    patterns = [
        (
            re.compile(
                r"^[ \t]*(?:it|specify|example)[ \t]*(?:\([ \t]*)?['\"]([^'\"\n]+)['\"]",
                re.MULTILINE,
            ),
            "RSpec",
        ),
        (
            re.compile(
                r"^[ \t]*test[ \t]+['\"]([^'\"\n]+)['\"][ \t]+do\b", re.MULTILINE
            ),
            "Minitest",
        ),
        (
            re.compile(r"^[ \t]*def[ \t]+(test_[A-Za-z0-9_!?]+)", re.MULTILINE),
            "Minitest",
        ),
    ]
    cases = []
    for pattern, framework in patterns:
        for match in pattern.finditer(text):
            cases.append(
                case_entry(
                    path,
                    line_number(text, match.start()),
                    match.group(1),
                    "test",
                    framework,
                )
            )
    return sorted(cases, key=lambda case: (case["line"], case["name"]))


def extract_macro_cases(path: str, text: str) -> list[dict[str, Any]]:
    patterns = [
        (
            re.compile(r"\bTEST(?:_F|_P)?\s*\(\s*([^,\n]+)\s*,\s*([^\)\n]+)\)"),
            "GoogleTest",
        ),
        (re.compile(r"\bTEST_CASE\s*\(\s*['\"]([^'\"\n]+)['\"]"), "Catch2"),
        (re.compile(r"^[ \t]*@test[ \t]+['\"]([^'\"\n]+)['\"]", re.MULTILINE), "Bats"),
        (
            re.compile(
                r"^[ \t]*test[ \t]+['\"]([^'\"\n]+)['\"][ \t]+do\b", re.MULTILINE
            ),
            "ExUnit",
        ),
        (
            re.compile(
                r"^[ \t]*(?:public[ \t]+)?function[ \t]+(test[A-Za-z0-9_]+)[ \t]*\(",
                re.MULTILINE,
            ),
            "PHPUnit",
        ),
        (
            re.compile(
                r"^[ \t]*func[ \t]+(test[A-Za-z0-9_]+)[ \t]*\(",
                re.MULTILINE | re.IGNORECASE,
            ),
            "XCTest",
        ),
    ]
    cases: list[dict[str, Any]] = []
    for pattern, framework in patterns:
        for match in pattern.finditer(text):
            if framework == "GoogleTest":
                name = f"{match.group(1).strip()}.{match.group(2).strip()}"
            else:
                name = match.group(1).strip()
            cases.append(
                case_entry(
                    path, line_number(text, match.start()), name, "test", framework
                )
            )
    return sorted(cases, key=lambda case: (case["line"], case["name"]))


def extract_cases(
    path: str, suffix: str, text: str
) -> tuple[bool, list[dict[str, Any]]]:
    if suffix in {".cjs", ".cts", ".js", ".jsx", ".mjs", ".mts", ".ts", ".tsx"}:
        return True, extract_javascript_cases(path, text)
    if suffix == ".py":
        return True, extract_python_cases(path, text)
    if suffix == ".go":
        return True, extract_go_cases(path, text)
    if suffix == ".rs":
        return True, extract_rust_cases(path, text)
    if suffix in {".java", ".kt", ".kts", ".cs"}:
        return True, extract_annotated_cases(path, text)
    if suffix == ".rb":
        return True, extract_ruby_cases(path, text)
    if suffix in {".bats", ".c", ".cc", ".cpp", ".ex", ".exs", ".php", ".swift"}:
        return True, extract_macro_cases(path, text)
    return False, []


def is_test_file(path: Path, root: Path) -> bool:
    if path.suffix.lower() not in SOURCE_SUFFIXES:
        return False
    stem = path.stem
    if TEST_SUPPORT_BASENAME.match(stem):
        return False
    if TEST_BASENAME.search(stem):
        return True
    relative_parts = path.relative_to(root).parts[:-1]
    if any(part.lower() in SUPPORT_DIRECTORY_NAMES for part in relative_parts):
        return False
    if SUPPORT_NAME.search(path.name):
        return False
    return any(part.lower() in TEST_DIRECTORY_NAMES for part in relative_parts)


def is_config_file(path: Path) -> bool:
    return bool(CONFIG_BASENAME.match(path.name))


def is_manifest(path: Path) -> bool:
    return path.name in MANIFEST_NAMES or path.suffix.lower() in MANIFEST_SUFFIXES


def is_support_file(path: Path, root: Path) -> bool:
    if is_config_file(path) or is_test_file(path, root):
        return False
    parent_names = {part.lower() for part in path.relative_to(root).parts[:-1]}
    return (
        bool(TEST_SUPPORT_BASENAME.match(path.stem))
        or bool(parent_names & SUPPORT_DIRECTORY_NAMES)
        or bool(parent_names & TEST_DIRECTORY_NAMES and SUPPORT_NAME.search(path.name))
        or path.suffix.lower() in {".snap", ".snapshot"}
    )


def package_json_evidence(path: str, text: str) -> dict[str, Any]:
    evidence: dict[str, Any] = {
        "path": path,
        "kind": "package.json",
        "dependencies": [],
        "scripts": {},
    }
    try:
        package = json.loads(text)
    except json.JSONDecodeError as error:
        evidence["parse_error"] = str(error)
        return evidence

    for group in (
        "dependencies",
        "devDependencies",
        "optionalDependencies",
        "peerDependencies",
    ):
        dependencies = package.get(group, {})
        if not isinstance(dependencies, dict):
            continue
        for name, version in dependencies.items():
            if isinstance(name, str) and TEST_TOOL_TERMS.search(name):
                evidence["dependencies"].append(
                    {"name": name, "version": str(version), "group": group}
                )

    scripts = package.get("scripts", {})
    if isinstance(scripts, dict):
        for name, command in scripts.items():
            if isinstance(command, str) and (
                TEST_TOOL_TERMS.search(command)
                or re.search(
                    r"(?:^|[:_-])(?:test|spec|e2e)(?:$|[:_-])", name, re.IGNORECASE
                )
            ):
                evidence["scripts"][name] = command
    return evidence


def generic_manifest_evidence(path: str, text: str) -> dict[str, Any]:
    matches = []
    for line_index, line in enumerate(text.splitlines(), start=1):
        if TEST_TOOL_TERMS.search(line):
            matches.append({"line": line_index, "text": line.strip()[:300]})
    return {"path": path, "kind": "manifest", "test_related_lines": matches}


def find_dynamic_declarations(
    text: str, suffix: str, case_lines: set[int]
) -> list[dict[str, Any]]:
    patterns: list[re.Pattern[str]] = []
    if suffix in {".cjs", ".cts", ".js", ".jsx", ".mjs", ".mts", ".ts", ".tsx"}:
        patterns = [re.compile(r"\b(?:it|test)(?:\.[A-Za-z]+)*\s*\(")]
    elif suffix == ".py":
        patterns = [re.compile(r"^[ \t]*(?:async[ \t]+)?def[ \t]+test_", re.MULTILINE)]
    declarations = []
    for line_index, line in enumerate(text.splitlines(), start=1):
        if line_index in case_lines:
            continue
        if any(pattern.search(line) for pattern in patterns):
            declarations.append({"line": line_index, "text": line.strip()[:300]})
    return declarations


def inventory(root: Path, scopes: list[Path]) -> dict[str, Any]:
    discovery_method, files = collect_files(root, scopes)
    test_files: list[dict[str, Any]] = []
    cases: list[dict[str, Any]] = []
    manifests: list[dict[str, Any]] = []
    config_files: list[str] = []
    support_files: list[str] = []
    warnings: list[dict[str, str]] = []

    for path in files:
        display_path = relative_path(path, root)
        named_test_file = is_test_file(path, root)
        source_file = path.suffix.lower() in SOURCE_SUFFIXES
        if is_config_file(path):
            config_files.append(display_path)

        needs_text = source_file or is_manifest(path)
        if not needs_text:
            if is_support_file(path, root):
                support_files.append(display_path)
            continue
        text, read_warning = read_text(path)
        if text is None:
            warnings.append(
                {"path": display_path, "reason": read_warning or "unreadable"}
            )
            if named_test_file:
                test_files.append(
                    {
                        "path": display_path,
                        "lines": None,
                        "parser_supported": path.suffix.lower() in SOURCE_SUFFIXES,
                        "declared_case_count": None,
                        "dynamic_declarations": [],
                    }
                )
            elif is_support_file(path, root):
                support_files.append(display_path)
            continue
        if read_warning:
            warnings.append({"path": display_path, "reason": read_warning})

        if is_manifest(path):
            manifests.append(
                package_json_evidence(display_path, text)
                if path.name == "package.json"
                else generic_manifest_evidence(display_path, text)
            )

        supported, file_cases = (
            extract_cases(display_path, path.suffix.lower(), text)
            if source_file
            else (False, [])
        )
        dynamic = find_dynamic_declarations(
            text, path.suffix.lower(), {case["line"] for case in file_cases}
        )
        content_test_file = bool(file_cases or dynamic)
        if named_test_file or content_test_file:
            test_files.append(
                {
                    "path": display_path,
                    "lines": len(text.splitlines()),
                    "parser_supported": supported,
                    "declared_case_count": len(file_cases),
                    "dynamic_declarations": dynamic,
                }
            )
            cases.extend(file_cases)
        elif is_support_file(path, root):
            support_files.append(display_path)

    test_files.sort(key=lambda item: item["path"])
    cases.sort(key=lambda item: (item["path"], item["line"], item["name"]))
    manifests.sort(key=lambda item: item["path"])
    config_files.sort()
    support_files.sort()
    warnings.sort(key=lambda item: (item["path"], item["reason"]))

    files_without_cases = [
        item["path"] for item in test_files if item["declared_case_count"] == 0
    ]
    dynamic_count = sum(len(item["dynamic_declarations"]) for item in test_files)
    return {
        "schema_version": 1,
        "root": str(root),
        "scopes": [relative_path(scope, root) or "." for scope in scopes],
        "collection": {
            "method": discovery_method,
            "file_count": len(files),
            "excluded_directory_names": sorted(SKIP_DIRECTORIES),
        },
        "summary": {
            "test_file_count": len(test_files),
            "declared_case_count": len(cases),
            "dynamic_declaration_count": dynamic_count,
            "test_files_without_declared_cases": len(files_without_cases),
            "manifest_count": len(manifests),
            "config_file_count": len(config_files),
            "support_file_count": len(support_files),
        },
        "test_files": test_files,
        "declared_cases": cases,
        "manifests": manifests,
        "config_files": config_files,
        "support_files": support_files,
        "files_without_declared_cases": files_without_cases,
        "read_warnings": warnings,
        "limitations": [
            "Declared cases are source declarations, not runtime-expanded parameterised cases.",
            "Dynamic, generated, inherited, macro-based, and unsupported test declarations may be incomplete.",
            "Confirm completeness with the repository's native test collector when it provides a read-only list mode.",
            "The inventory records test-tool evidence but does not judge whether a dependency or test is useful.",
        ],
    }


def write_result(result: dict[str, Any], output: Path | None, compact: bool) -> None:
    if compact:
        rendered = json.dumps(result, ensure_ascii=False, separators=(",", ":")) + "\n"
    else:
        rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if output is None:
        sys.stdout.write(rendered)
        return
    output.write_text(rendered, encoding="utf-8")


def main() -> int:
    arguments = parse_args()
    root = arguments.root.resolve()
    if not root.is_dir():
        print(f"repository root is not a directory: {root}", file=sys.stderr)
        return 2
    try:
        scopes = resolve_scopes(root, arguments.scope)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 2
    try:
        result = inventory(root, scopes)
        write_result(result, arguments.output, arguments.compact)
    except OSError as error:
        print(f"inventory failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
