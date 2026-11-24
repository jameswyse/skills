# Agent Skills

## Install

```sh
npx skills@latest add jameswyse/skills
```

## Use

Agents load a skill on their own when the task matches its description. To load one yourself, type `$skill-name` in Codex or `/skill-name` in Claude Code and Cursor. `design-it-twice` loads only when you invoke it.

This repository's `code-review` replaces Claude Code's bundled `/code-review`. Use `/review` for the bundled one.

## Skills

| Skill             | What it does                                                                                                     |
| ----------------- | ---------------------------------------------------------------------------------------------------------------- |
| `engineering`     | Sets the baseline for implementing, debugging, designing and verifying software, including test-first bug fixes. |
| `typescript`      | Adds rules for TypeScript types and validation.                                                                  |
| `design-it-twice` | Compares several interface designs for a module before choosing one.                                             |
| `debugging`       | Finds the cause of hard bugs and performance regressions from evidence.                                          |
| `triage-sentry`   | Investigates a Sentry issue or triages a project's issues.                                                       |
| `upgrade-deps`    | Upgrades a pnpm project's dependencies, Node.js, pnpm and GitHub Actions.                                        |
| `code-review`     | Reviews a change for spec, correctness and standards across several models.                                      |
| `open-pr`         | Opens pull requests and writes their titles, descriptions, screenshots and review labels.                        |
| `babysit-pr`      | Watches a pull request's CI, reviews and merge conflicts, and fixes what it can.                                 |
| `full-send`       | Takes a task through to a ready pull request with passing checks.                                                |
| `jira`            | Reads, files and splits Jira issues, and ties branches, commits and pull requests to them.                       |
| `timesheet`       | Logs time and meetings to Productive.                                                                            |
| `review-pr`       | Reviews someone else's pull request and drafts or posts one comment.                                             |
| `explain-code`    | Explains code and code changes, with a diagram when one helps.                                                   |
| `writing`         | Drafts, edits and reviews prose, docs, commit messages, skills and agent instructions.                           |
| `ux`              | Designs, builds and reviews user-facing interfaces.                                                              |
| `html-report`     | Builds compact HTML reports and shows them in T3 Code.                                                           |
| `homelab`         | Reaches my machines and self-hosted services. Personal, so skip it.                                              |

## Requirements

- `babysit-pr` and `open-pr` need an authenticated GitHub CLI. Attaching screenshots needs a version whose `gh pr edit` has `--attach`.
- `triage-sentry` works best with the [Sentry CLI](https://cli.sentry.dev/).
- `ux` and `writing` hand some work to the optional skills in [`external-skills.json`](external-skills.json).
- `code-review` and `engineering` delegate to other models through T3 Code when it's available, and use the current agent's subagents otherwise.
- Several skills rely on rules in [`global/AGENTS.md`](global/AGENTS.md), which describes me and my machines. Copy the rules you want into your agent's global instructions.

## Development

| Command                               | What it does                                                                                                                   |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `scripts/sync-skills`                 | Links every skill and the global instructions into `~/.agents`, `~/.claude` and the Codex homes, so edits apply straight away. |
| `scripts/validate-skills [skill ...]` | Checks each skill's frontmatter against the Agent Skills specification and Claude Code's extensions.                           |
| `scripts/test-skills`                 | Runs the repository's tooling tests.                                                                                           |
| `scripts/eval-skills [skill ...]`     | Probes skills on Opus and Sol with no skill text, the committed text and the working tree's text, and reports regressions.     |
| `scripts/setup-external-skills`       | Installs and updates the skills in `external-skills.json`, and removes ones it no longer lists.                                |
| `scripts/update-fleet-skills`         | Rolls the pushed commit out to my machines.                                                                                    |

[`external-skills.json`](external-skills.json) lists the third-party skills every machine installs, keyed by their `npx skills` source. Add or remove a name there, then run `scripts/setup-external-skills`.

See [docs/development.md](docs/development.md) for details.

## Licence

[MIT](LICENSE). Ideas also come from [`humanlayer/skills`](https://github.com/humanlayer/skills), [`mattpocock/skills`](https://github.com/mattpocock/skills), [`poteto/noodle`](https://github.com/poteto/noodle), [`dmmulroy/skills`](https://github.com/dmmulroy/skills), [`t3dotgg/tstack`](https://github.com/t3dotgg/tstack) and others.
