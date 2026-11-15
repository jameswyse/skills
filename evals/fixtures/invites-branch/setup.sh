#!/usr/bin/env bash
set -euo pipefail
change="$(cd "$(dirname "$0")" && pwd)/change"
commit() { git -c user.name=eval -c user.email=eval@example.invalid commit -q "$@"; }
git init -q -b main
git add -A
commit -m "chore: teams and member roles"
git checkout -q -b feature/invites
cp -R "$change/." .
git add -A
commit -m "feat(invites): invite, revoke and accept team invites" -m "Implements docs/specs/invites.md."
