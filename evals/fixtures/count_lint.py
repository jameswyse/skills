import json
import sys
from collections import Counter

FORMATTING_RULES = {"wyse(statement-spacing)"}

diagnostics = json.load(sys.stdin).get("diagnostics", [])
source = [item for item in diagnostics if not item["filename"].endswith(".config.ts")]
errors = [item for item in source if item["severity"] == "error"]
formatting = [item for item in errors if item["code"] in FORMATTING_RULES]
by_rule = Counter(f'{item["code"]} ({item["severity"]})' for item in source)
print(f"lint errors: {len(errors) - len(formatting)}")
print(f"lint formatting errors: {len(formatting)}")
print(f"lint warnings: {len(source) - len(errors)}")
for rule, count in by_rule.most_common():
    print(f"  {count} x {rule}")
