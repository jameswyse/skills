# AGENTS

- Validate skill changes with `scripts/validate-skills [skill-name ...]`. The repository command validates Agent Skills fields and the supported Claude Code extensions through an isolated `uv` environment with pinned PyYAML.
- Run `scripts/test-skills` for script changes. It includes the repository tooling tests and the imported `babysit-pr` watcher tests.
- Run the sync script after all changes are completed and validated.
- After skill changes are committed and pushed, run `scripts/update-fleet-skills` only when asked to update the fleet. It changes other machines.
