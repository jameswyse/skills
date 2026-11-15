from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


FORMAT_SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "before-and-after"
    / "scripts"
    / "format.mjs"
)
MARKED_BLOCK = "<!-- before-and-after:start -->\nold evidence\n<!-- before-and-after:end -->"


class BeforeAndAfterFormatTest(unittest.TestCase):
    directory: Path

    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="before-and-after-test-")
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        (self.directory / "after.png").write_bytes(b"image")

    def format(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["node", str(FORMAT_SCRIPT), *arguments],
            check=False,
            capture_output=True,
            text=True,
            cwd=self.directory,
        )

    def test_replacing_the_block_keeps_the_surrounding_description(self) -> None:
        before_block = "Summary with a hard break  \nsecond line\n\n\n"
        after_block = "\n\n\n    indented code  \n    more code  \n\nClosing paragraph.  "
        (self.directory / "body.md").write_text(
            f"{before_block}{MARKED_BLOCK}{after_block}", encoding="utf-8"
        )

        result = self.format("--body-file", "body.md", "--after", "after.png")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(result.stdout.startswith(f"{before_block}<!-- before-and-after:start -->"))
        self.assertTrue(result.stdout.endswith(f"<!-- before-and-after:end -->{after_block}"))
        self.assertNotIn("old evidence", result.stdout)

    def test_a_pipe_in_a_label_stays_inside_its_table_cell(self) -> None:
        result = self.format("--after", "after.png", "--label", "Light | dark")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("| Preview (Light \\| dark) |", result.stdout)

    def test_a_video_table_label_is_shown_as_text(self) -> None:
        result = self.format(
            "--after-video-url",
            "https://github.com/user-attachments/assets/example",
            "--label",
            "<b>Light</b> & dark",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("<th>Preview (&lt;b&gt;Light&lt;/b&gt; &amp; dark)</th>", result.stdout)

    def test_rejects_a_file_name_that_gh_would_split_at_a_hash(self) -> None:
        (self.directory / "chart#1.png").write_bytes(b"image")

        result = self.format("--after", "chart#1.png", "--attach-list")

        self.assertEqual(result.returncode, 1)
        self.assertIn("chart#1.png", result.stderr)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
