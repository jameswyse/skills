# AGENTS

- Validate skill changes with `scripts/validate-skills [skill-name ...]`. The repository command validates Agent Skills fields and the supported Claude Code extensions through an isolated `uv` environment with pinned PyYAML.
- After rewording or cutting a skill that has a probe file in `evals/`, run `scripts/eval-skills <skill-name ...>`. It calls Opus and Sol through the `claude` and `codex` CLIs, and the edit holds when `after` passes every probe that `before` passes.
- Run `scripts/test-skills` for script changes. It includes the repository tooling tests and the imported `babysit-pr` watcher tests.
- Run the sync script after all changes are completed and validated. When a change moves a skill from `external-skills.json` into this repository, run `scripts/setup-external-skills` first, because the sync script reports a conflict while the external copy is installed.
- After skill changes are committed and pushed, run `scripts/update-fleet-skills` only when asked to update the fleet. It changes other machines.
