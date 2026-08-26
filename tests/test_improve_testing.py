from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


INVENTORY_SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "engineering"
    / "improve-testing"
    / "scripts"
    / "collect_test_inventory.py"
)


class ImproveTestingInventoryTest(unittest.TestCase):
    def invoke_inventory(
        self, root: Path, *arguments: str
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(INVENTORY_SCRIPT), str(root), *arguments],
            check=False,
            capture_output=True,
            text=True,
        )

    def run_inventory(self, root: Path, *arguments: str) -> dict[str, object]:
        result = self.invoke_inventory(root, *arguments)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_inventories_cases_tools_support_and_dynamic_declarations(self) -> None:
        with tempfile.TemporaryDirectory(prefix="testing-inventory-test-") as directory:
            root = Path(directory)
            (root / "src").mkdir()
            (root / "scripts").mkdir()
            (root / "tests" / "fixtures").mkdir(parents=True)
            (root / "package.json").write_text(
                json.dumps(
                    {
                        "scripts": {"test": "vitest run"},
                        "devDependencies": {"vitest": "1.2.3", "typescript": "5.6.0"},
                    }
                ),
                encoding="utf-8",
            )
            (root / "playwright.config.ts").write_text(
                "export default {};\n", encoding="utf-8"
            )
            (root / "src" / "widget.test.ts").write_text(
                """test("returns the configured label", () => {});
test.each([[1], [2]])("accepts %s", () => {});
test(dynamicName, () => {});
""",
                encoding="utf-8",
            )
            (root / "src" / "lib.rs").write_text(
                """#[cfg(test)]
mod tests {
    #[test]
    fn normalises_the_value() {}
}
""",
                encoding="utf-8",
            )
            (root / "tests" / "test_widget.py").write_text(
                "def test_rejects_an_empty_label():\n    assert True\n",
                encoding="utf-8",
            )
            (root / "tests" / "fixtures" / "user.json").write_text(
                "{}\n", encoding="utf-8"
            )
            (root / "scripts" / "setup-project").write_text(
                "#!/bin/sh\n", encoding="utf-8"
            )

            inventory = self.run_inventory(root)

            self.assertEqual(
                inventory["summary"],
                {
                    "test_file_count": 3,
                    "declared_case_count": 4,
                    "dynamic_declaration_count": 1,
                    "test_files_without_declared_cases": 0,
                    "manifest_count": 1,
                    "config_file_count": 1,
                    "support_file_count": 1,
                },
            )
            self.assertEqual(
                [case["name"] for case in inventory["declared_cases"]],
                [
                    "normalises_the_value",
                    "returns the configured label",
                    "accepts %s",
                    "test_rejects_an_empty_label",
                ],
            )
            self.assertEqual(
                inventory["manifests"][0]["dependencies"],
                [{"name": "vitest", "version": "1.2.3", "group": "devDependencies"}],
            )
            self.assertEqual(inventory["config_files"], ["playwright.config.ts"])
            self.assertEqual(inventory["support_files"], ["tests/fixtures/user.json"])

    def test_limits_the_inventory_to_the_requested_scope(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="testing-inventory-scope-test-"
        ) as directory:
            root = Path(directory)
            (root / "area-a" / "tests").mkdir(parents=True)
            (root / "area-b" / "tests").mkdir(parents=True)
            (root / "area-a" / "tests" / "alpha_test.py").write_text(
                "def test_alpha():\n    assert True\n",
                encoding="utf-8",
            )
            (root / "area-b" / "tests" / "beta_test.py").write_text(
                "def test_beta():\n    assert True\n",
                encoding="utf-8",
            )

            inventory = self.run_inventory(root, "--scope", "area-a")

            self.assertEqual(inventory["scopes"], ["area-a"])
            self.assertEqual(
                [case["name"] for case in inventory["declared_cases"]],
                ["test_alpha"],
            )

    def test_detects_common_declaration_shapes(self) -> None:
        fixtures = {
            "widget_test.go": "func TestWidget(t *testing.T) {}\n",
            "WidgetTest.java": "@Test void rejectsEmptyValue() {}\n",
            "WidgetTests.cs": "[Fact] public void RejectsEmptyValue() {}\n",
            "widget_spec.rb": 'it "rejects an empty value" do\nend\n',
            "widget_test.cpp": "TEST(Widget, RejectsEmptyValue) {}\n",
            "widget.bats": '@test "rejects an empty value" { true; }\n',
            "widget_test.exs": 'test "rejects an empty value" do\nend\n',
            "WidgetTest.php": "public function testRejectsEmptyValue() {}\n",
            "WidgetTests.swift": "func testRejectsEmptyValue() {}\n",
        }
        with tempfile.TemporaryDirectory(
            prefix="testing-inventory-syntax-test-"
        ) as directory:
            root = Path(directory)
            for name, source in fixtures.items():
                (root / name).write_text(source, encoding="utf-8")

            inventory = self.run_inventory(root)

            self.assertEqual(
                {
                    (case["framework_hint"], case["name"])
                    for case in inventory["declared_cases"]
                },
                {
                    ("Bats", "rejects an empty value"),
                    ("ExUnit", "rejects an empty value"),
                    ("Fact", "RejectsEmptyValue"),
                    ("GoogleTest", "Widget.RejectsEmptyValue"),
                    ("PHPUnit", "testRejectsEmptyValue"),
                    ("RSpec", "rejects an empty value"),
                    ("Test", "rejectsEmptyValue"),
                    ("XCTest", "testRejectsEmptyValue"),
                    ("go test", "TestWidget"),
                },
            )

    def test_detects_javascript_module_test_extensions(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="testing-inventory-modules-test-"
        ) as directory:
            root = Path(directory)
            for suffix in ("cjs", "cts", "mjs", "mts"):
                (root / f"widget.test.{suffix}").write_text(
                    f'test("runs {suffix} tests", () => {{}});\n',
                    encoding="utf-8",
                )

            inventory = self.run_inventory(root)

            self.assertEqual(inventory["summary"]["test_file_count"], 4)
            self.assertEqual(
                {case["name"] for case in inventory["declared_cases"]},
                {
                    "runs cjs tests",
                    "runs cts tests",
                    "runs mjs tests",
                    "runs mts tests",
                },
            )

    def test_uses_paths_relative_to_the_repository_root_for_classification(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="testing-inventory-parent-test-"
        ) as directory:
            root = Path(directory) / "tests" / "project"
            (root / "src").mkdir(parents=True)
            (root / "src" / "production.py").write_text(
                "def calculate_value():\n    return 1\n",
                encoding="utf-8",
            )

            inventory = self.run_inventory(root)

            self.assertEqual(inventory["summary"]["test_file_count"], 0)
            self.assertEqual(inventory["declared_cases"], [])

    def test_keeps_dynamic_tests_in_a_support_named_file(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="testing-inventory-dynamic-test-"
        ) as directory:
            root = Path(directory)
            (root / "test_utils.ts").write_text(
                "test(dynamicName, () => {});\n",
                encoding="utf-8",
            )

            inventory = self.run_inventory(root)

            self.assertEqual(inventory["summary"]["test_file_count"], 1)
            self.assertEqual(inventory["summary"]["dynamic_declaration_count"], 1)
            self.assertEqual(inventory["support_files"], [])

    def test_writes_the_inventory_to_the_requested_output_file(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="testing-inventory-output-test-"
        ) as directory:
            root = Path(directory)
            (root / "example_test.py").write_text(
                "def test_example():\n    assert True\n",
                encoding="utf-8",
            )
            output = root / "inventory.json"

            result = self.invoke_inventory(root, "--output", str(output))

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            inventory = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(inventory["summary"]["declared_case_count"], 1)

    def test_rejects_a_scope_outside_the_repository_root(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="testing-inventory-root-test-"
        ) as root_directory:
            with tempfile.TemporaryDirectory(
                prefix="testing-inventory-outside-test-"
            ) as outside_directory:
                result = self.invoke_inventory(
                    Path(root_directory), "--scope", outside_directory
                )

            self.assertEqual(result.returncode, 2)
            self.assertIn("scope is outside the repository root", result.stderr)


if __name__ == "__main__":
    unittest.main()
