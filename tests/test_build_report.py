from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


UX_SKILL = Path(__file__).resolve().parents[1] / "skills" / "ux" / "ux"
BUILD_SCRIPT = UX_SKILL / "scripts" / "build_report.py"


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
        self.assertIn((UX_SKILL / "assets" / "report.css").read_text(), document)
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

    def test_adds_scripts_only_for_mermaid_blocks_and_filters(self) -> None:
        body = (
            '<pre class="mermaid">flowchart LR\n  A --> B</pre>'
            '<div class="filter" data-filter-for="inventory" hidden></div>'
        )
        result, output = self.build("Review", body)

        self.assertEqual(result.returncode, 0, result.stderr)
        document = output.read_text()
        self.assertIn("mermaid.esm.min.mjs", document)
        self.assertIn("data-filter-text", document)

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
