# Development

## Prerequisites

- Python 3 for `sync-skills` and `setup-external-skills`.
- [uv](https://docs.astral.sh/uv/) for `validate-skills`, `test-skills` and `eval-skills`, which run on Python 3.11 or newer.
- Node.js and npx for `setup-external-skills` and the `before-and-after` tests.
- The `claude` and `codex` CLIs, signed in, for `eval-skills`.

## Layout

- `skills/<skill-name>` holds each skill.
- `global/` holds the global `AGENTS.md` and `CLAUDE.md`.
- `evals/` holds the model probes and fixture repositories.
- `archive/` mirrors the repository for retired skills. Scripts ignore it.
- `external-skills.json` lists the third-party skills every machine installs.

## Link this working tree

```sh
scripts/sync-skills
```

This links every skill into `~/.agents/skills` and `~/.claude/skills`, so edits apply immediately. It also links `global/AGENTS.md` to `~/.agents/AGENTS.md`, `global/CLAUDE.md` to `~/.claude/CLAUDE.md`, and `AGENTS.md` in `~/.codex` and `~/.codex-t3` to the shared copy.

- It creates, updates and removes only links it owns.
- It moves an existing `AGENTS.md` or `CLAUDE.md` file to a timestamped `.backup-` file before linking.
- It reports a conflict and exits non-zero for anything else in the way.
- `--target`, `--claude-target` and `--codex-home` redirect it for a dry test.

Don't manage the same skill with both `npx skills` and `scripts/sync-skills`.

## External skills

```sh
scripts/setup-external-skills [--dry-run]
```

This installs and updates every skill in `external-skills.json` for Claude Code and Codex. It then removes any skill `npx skills` tracks that the file doesn't list. It leaves skills `npx skills` doesn't track alone, and refuses to overwrite a same-named skill from another source.

When a skill moves from `external-skills.json` into this repository, run this before `scripts/sync-skills`.

## Validate and test

```sh
scripts/validate-skills [skill-name ...]
scripts/test-skills
```

`validate-skills` checks Agent Skills fields and the supported Claude Code extensions. `test-skills` runs the repository tooling tests and the `babysit-pr` watcher tests. Both use isolated `uv` environments. The watcher tests never contact GitHub.

`disable-model-invocation: true` is a Claude Code extension. Strict Agent Skills tools may reject it.

## Evals

```sh
scripts/eval-skills code-review babysit-pr
scripts/eval-skills --kinds live --arms before,after engineering
scripts/eval-skills --audit code-review
```

Each probe is a short scenario with one correct course of action. The script sends it to Opus and Sol through the `claude` and `codex` CLIs in three arms, and a judge marks each answer.

- `none` has only the global instructions.
- `before` adds the skill's text from the base ref, `HEAD` unless `--base` says otherwise.
- `after` adds the working tree's text.

An edit holds when `after` passes every probe `before` passes, on both models. A probe `none` passes on both models marks a rule that is a candidate to delete. A probe `before` fails marks text that isn't working.

- `--kinds live` runs a probe with shell and edit access in a copy of its fixture. A fixture's `check.sh` runs on the result.
- `--audit` asks each model which requirements the working tree dropped.
- Answers are cached by prompt under `$TMPDIR/skill-evals`.
- `evals/lint.toml` compares one task with and without [`@jameswyse/oxc-config`](https://github.com/jameswyse/oxc-config). Run it with `scripts/eval-skills lint --kinds live --arms before,after --runs 3`.

Add a probe when a skill gains a rule a model wouldn't follow unprompted.

## Update the fleet

```sh
scripts/update-fleet-skills
```

Run this after pushing. It exits with status 2 if this checkout is dirty or out of step with its upstream. It validates the skills, then runs external setup and sync here and on each machine in `FLEET`. Remote machines fast-forward their checkout first. A machine with local changes, unpushed commits or another branch is reported as failed and left unchanged.

The script reaches machines through the homelab repository's `scripts/fleet`, read from `~/Projects/homelab` unless `HOMELAB_DIR` is set. Edit `FLEET` and `REMOTE_CHECKOUT_UNDER_HOME` at the top of the script for other machines.

## Archive a skill

Move its paths under `archive/` with `git mv`, such as `skills/homelab` to `archive/skills/homelab` and its test to `archive/tests/`. Reverse the move to restore it. Run `scripts/sync-skills` either way. Relative links in an archived skill point to where it lives once restored, so they only resolve after the move back.
