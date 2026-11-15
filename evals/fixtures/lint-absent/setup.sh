#!/usr/bin/env bash
set -euo pipefail
pnpm install --frozen-lockfile --prefer-offline > /dev/null
git init -q -b main
git add -A
git -c user.name=eval -c user.email=eval@example.invalid commit -q -m "feat: join URLs and log structured records"
