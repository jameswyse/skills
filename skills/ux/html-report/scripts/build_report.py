#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


ASSETS = Path(__file__).resolve().parent.parent / "assets"
STYLESHEET = (ASSETS / "report.css").read_text()
STYLESHEET_CLASSES = frozenset(re.findall(r"\.([a-z][a-z0-9-]*)", STYLESHEET))
FORBIDDEN_TAGS = frozenset(
    {
        "html", "head", "body", "style", "link", "meta", "base",
        "script", "iframe", "frame", "frameset", "object", "embed",
    }
)
SCRIPT_URL = re.compile(r"^[\x00-\x20]*javascript:", re.IGNORECASE)
URL_ATTRIBUTES = ("href", "src", "action", "formaction", "xlink:href")
BAR_VALUE = re.compile(r"\s*--value:\s*\d+(?:\.\d+)?%\s*;?\s*")
FILTER_CONTROLS = re.compile(r"\bdata-filter-for=", re.IGNORECASE)


class ComponentChecker(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.problems: list[str] = []

    def handle_decl(self, decl: str) -> None:
        self.problems.append(f"<!{decl}> declaration")

    def unknown_decl(self, data: str) -> None:
        self.problems.append("<![...]> section")

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in FORBIDDEN_TAGS:
            self.problems.append(f"<{tag}> element")
        names = [name for name, _ in attrs]
        self.problems.extend(
            f"duplicate {name} attribute on <{tag}>"
            for name in dict.fromkeys(names)
            if names.count(name) > 1
        )
        values = dict(attrs)
        self.problems.extend(
            f"{name} attribute on <{tag}>" for name in values if name.startswith("on")
        )
        self.problems.extend(
            f"javascript: URL in {name} on <{tag}>"
            for name in URL_ATTRIBUTES
            if SCRIPT_URL.match(re.sub(r"[\t\n\r]", "", values.get(name) or ""))
        )
        classes = (values.get("class") or "").split()
        self.problems.extend(
            f'class "{class_name}"' for class_name in classes if class_name not in STYLESHEET_CLASSES
        )
        style = values.get("style")
        if "style" in values and not ("bar" in classes and BAR_VALUE.fullmatch(style or "")):
            self.problems.append(f'style="{style or ""}" on <{tag}>')


def check_components(body: str) -> None:
    checker = ComponentChecker()
    checker.feed(body)
    checker.close()
    if checker.problems:
        raise ValueError(
            "The body fragment uses markup outside the report components: "
            + ", ".join(dict.fromkeys(checker.problems))
            + ". Write only the report content with the components in the html-report skill;"
            " the script adds the document and styles."
        )


def build(title: str, body: str, inline: bool = False) -> str:
    check_components(body)
    scripts = []
    if FILTER_CONTROLS.search(body):
        scripts.append(f"<script>\n{(ASSETS / 'report-filter.js').read_text()}</script>")
    return "\n".join(
        [
            "<!doctype html>",
            '<html lang="en-AU" class="report-inline">' if inline else '<html lang="en-AU">',
            "<head>",
            '<meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            f"<title>{html.escape(title)}</title>",
            f"<style>\n{STYLESHEET}</style>",
            "</head>",
            "<body>",
            '<main class="report">',
            body.strip(),
            "</main>",
            *scripts,
            "</body>",
            "</html>",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Wrap a report body fragment in the shared report document and styles."
    )
    parser.add_argument("--title", required=True, help="Document title shown in the browser tab")
    parser.add_argument("--input", required=True, type=Path, help="Body fragment file, or - for stdin")
    parser.add_argument("--output", required=True, type=Path, help="HTML file to write")
    parser.add_argument(
        "--inline",
        action="store_true",
        help="Follow the host's theme and drop page margins for T3 Code's html_render",
    )
    arguments = parser.parse_args()

    body = sys.stdin.read() if str(arguments.input) == "-" else arguments.input.read_text()
    try:
        document = build(arguments.title, body, arguments.inline)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1

    output = arguments.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    encoded = document.encode()
    output.write_bytes(encoded)
    print(
        json.dumps(
            {
                "path": str(output),
                "name": output.name,
                "mimeType": "text/html",
                "sizeBytes": len(encoded),
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
