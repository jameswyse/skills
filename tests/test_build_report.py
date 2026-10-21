from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILLS = Path(__file__).resolve().parents[1] / "skills"
REPORT_SKILL = SKILLS / "ux" / "html-report"
BUILD_SCRIPT = REPORT_SKILL / "scripts" / "build_report.py"
DOCUMENTED_TEMPLATES = (
    REPORT_SKILL / "SKILL.md",
    SKILLS / "engineering" / "upgrade-deps" / "references" / "html-report.md",
)
HTML_BLOCK = re.compile(r"```html\n(.*?)```", re.DOTALL)


class BuildReportTest(unittest.TestCase):
    def build(
        self, title: str, body: str, *options: str
    ) -> tuple[subprocess.CompletedProcess[str], Path]:
        directory = Path(tempfile.mkdtemp())
        source = directory / "body.html"
        source.write_text(body)
        output = directory / "report.html"
        result = subprocess.run(
            [
                sys.executable,
                str(BUILD_SCRIPT),
                "--title",
                title,
                "--input",
                str(source),
                "--output",
                str(output),
                *options,
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        return result, output

    def test_wraps_the_body_in_a_self_contained_document(self) -> None:
        result, output = self.build("Review <acme> & co", '<p class="lead">Ship it.</p>')

        self.assertEqual(result.returncode, 0, result.stderr)
        document = output.read_text()
        self.assertIn("<title>Review &lt;acme&gt; &amp; co</title>", document)
        self.assertIn((REPORT_SKILL / "assets" / "report.css").read_text(), document)
        self.assertIn('<main class="report">\n<p class="lead">Ship it.</p>\n</main>', document)
        self.assertNotIn("<script", document)
        self.assertIn('<html lang="en-AU">', document)

    def test_marks_an_inline_document_so_it_follows_the_host_theme(self) -> None:
        result, output = self.build("Review", "<p>Ship it.</p>", "--inline")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('<html lang="en-AU" class="report-inline">', output.read_text())

    def test_reports_the_attachment_metadata_of_the_written_file(self) -> None:
        result, output = self.build("Review", "<p>Résumé</p>")

        metadata = json.loads(result.stdout)
        self.assertEqual(
            metadata,
            {
                "path": str(output.resolve()),
                "name": "report.html",
                "mimeType": "text/html",
                "sizeBytes": len(output.read_bytes()),
            },
        )

    def test_adds_the_filter_script_for_filter_controls(self) -> None:
        result, output = self.build(
            "Review", '<div class="filter" data-filter-for="inventory" hidden></div>'
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("data-filter-text", output.read_text())

    def test_rejects_markup_outside_the_report_components(self) -> None:
        fragments = {
            '<div class="grid-cols-2">x</div>': 'class "grid-cols-2"',
            '<p style="color: red">x</p>': 'style="color: red" on <p>',
            '<span class="bar-track" style="--value: 40%"></span>': 'style="--value: 40%" on <span>',
            '<span class="bar" style="inset: 0" style="--value: 40%"></span>': "duplicate style",
            "<script>alert(1)</script>": "<script> element",
            '<p onclick="go()">x</p>': "onclick attribute on <p>",
            '<a href=" JavaScript:go()">x</a>': "javascript: URL in href on <a>",
            '<a href="java&#9;script:go()">x</a>': "javascript: URL in href on <a>",
            '<svg><a xlink:href="javascript:go()">x</a></svg>': "javascript: URL in xlink:href",
            "<![CDATA[><style>p{}</style>]]>": "<![...]> section",
            '<meta http-equiv="refresh" content="0">': "<meta> element",
        }
        for fragment, problem in fragments.items():
            with self.subTest(fragment=fragment):
                result, output = self.build("Review", fragment)

                self.assertEqual(result.returncode, 1)
                self.assertIn(problem, result.stderr)
                self.assertFalse(output.exists())

    def test_accepts_a_bar_value(self) -> None:
        result, _ = self.build("Review", '<span class="bar" style="--value: 62.5%"></span>')

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_builds_every_documented_template(self) -> None:
        for path in DOCUMENTED_TEMPLATES:
            blocks = HTML_BLOCK.findall(path.read_text())
            self.assertTrue(blocks, f"{path} has no html block")
            for index, block in enumerate(blocks):
                with self.subTest(path=path.name, block=index):
                    result, _ = self.build("Review", block)

                    self.assertEqual(result.returncode, 0, result.stderr)

    def test_rejects_a_fragment_that_brings_its_own_document_or_styles(self) -> None:
        for fragment in ("<!doctype html><p>x</p>", "<body><p>x</p></body>", "<style>p{}</style>"):
            with self.subTest(fragment=fragment):
                result, output = self.build("Review", fragment)

                self.assertEqual(result.returncode, 1)
                self.assertIn("only the report content", result.stderr)
                self.assertFalse(output.exists())

    def test_accepts_header_elements(self) -> None:
        result, _ = self.build("Review", '<header class="report-header"><h1>acme</h1></header>')

        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
