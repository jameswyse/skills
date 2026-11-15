#!/usr/bin/env bash
set -euo pipefail
fixtures="$(cd "$(dirname "$0")" && pwd)"
cp "$fixtures/lint-configured/repo/oxlint.config.ts" "$fixtures/lint-configured/repo/pnpm-workspace.yaml" .
pnpm add -D --prefer-offline @jameswyse/oxc-config@0.7.0 oxlint@1.92.0 oxlint-tsgolint@7.0.2006 > /dev/null
{ pnpm exec oxlint . --format=json || true; } | python3 "$fixtures/count_lint.py"
echo "typecheck: $(pnpm -s typecheck > /dev/null 2>&1 && echo pass || echo fail)"
echo "tests: $(pnpm -s test > /dev/null 2>&1 && echo pass || echo fail)"
suppressions="$(git grep -cE 'oxlint-disable|eslint-disable|@ts-expect-error|@ts-ignore' -- '*.ts' '*.tsx' '*.mts' '*.cts' '*.js' '*.jsx' '*.mjs' '*.cjs' || [ $? -eq 1 ])"
echo "suppression directives: $(awk -F: '{total += $NF} END {print total + 0}' <<< "$suppressions")"
