#!/usr/bin/env bash
set -uo pipefail
fixtures="$(cd "$(dirname "$0")" && pwd)"
if [ ! -f oxlint.config.ts ]; then
  cp "$fixtures/lint-configured/repo/oxlint.config.ts" "$fixtures/lint-configured/repo/pnpm-workspace.yaml" .
  pnpm add -D --prefer-offline @jameswyse/oxc-config@0.7.0 oxlint@1.92.0 oxlint-tsgolint@7.0.2006 > /dev/null 2>&1
fi
pnpm exec oxlint . --format=json 2> /dev/null | python3 "$fixtures/count_lint.py"
echo "typecheck: $(pnpm -s typecheck > /dev/null 2>&1 && echo pass || echo fail)"
echo "tests: $(pnpm -s test > /dev/null 2>&1 && echo pass || echo fail)"
echo "suppression directives in src: $(grep -rEc 'oxlint-disable|eslint-disable|@ts-expect-error|@ts-ignore' src | awk -F: '{total += $2} END {print total + 0}')"
