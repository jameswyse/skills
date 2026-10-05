#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path


ASSETS = Path(__file__).resolve().parent.parent / "assets"
DOCUMENT_TAG = re.compile(r"<(?:!doctype|html|head|body|style|link)\b", re.IGNORECASE)
MERMAID_BLOCK = re.compile(r"class=\"[^\"]*\bmermaid\b", re.IGNORECASE)
FILTER_CONTROLS = re.compile(r"\bdata-filter-for=", re.IGNORECASE)


def build(title: str, body: str) -> str:
    misplaced = DOCUMENT_TAG.search(body)
    if misplaced:
        raise ValueError(
            f"The body fragment contains {misplaced.group(0)}. "
            "Write only the report content; the script adds the document and styles."
        )
    scripts = []
    if FILTER_CONTROLS.search(body):
        scripts.append(f"<script>\n{(ASSETS / 'report-filter.js').read_text()}</script>")
    if MERMAID_BLOCK.search(body):
        scripts.append(f'<script type="module">\n{(ASSETS / "report-mermaid.js").read_text()}</script>')
    return "\n".join(
        [
            "<!doctype html>",
            '<html lang="en-AU">',
            "<head>",
            '<meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            f"<title>{html.escape(title)}</title>",
            f"<style>\n{(ASSETS / 'report.css').read_text()}</style>",
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
    arguments = parser.parse_args()

    body = sys.stdin.read() if str(arguments.input) == "-" else arguments.input.read_text()
    try:
        document = build(arguments.title, body)
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
