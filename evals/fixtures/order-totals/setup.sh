#!/usr/bin/env bash
set -euo pipefail
git init -q -b main
git add -A
git -c user.name=eval -c user.email=eval@example.invalid commit -q -m "feat: import orders from the supplier feed"
