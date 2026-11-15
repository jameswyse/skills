# Agent Skills

My skills for software engineering, UX, writing and homelab access. They follow the [Agent Skills specification](https://agentskills.io/specification). I use them in Claude Code, Codex, Cursor and Grok Build.

## Install

```sh
npx skills@latest add jameswyse/skills --global --agent claude-code --agent codex --skill '*' --yes
```

This installs to `~/.agents/skills`, which Codex, Cursor and Grok Build read, and links each skill into `~/.claude/skills` for Claude Code. Replace `'*'` with one or more skill names to install fewer. Several skills rely on the global instructions in [`global/AGENTS.md`](global/AGENTS.md). They describe me and my machines, so copy the rules you want into your own `~/.codex/AGENTS.md` for Codex, `~/.claude/CLAUDE.md` for Claude Code, or another agent's global rules.

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

## Development

See [docs/development.md](docs/development.md) for local linking, validation, tests, evals and fleet updates.

## Licence

[MIT](LICENSE). Ideas also come from [`humanlayer/skills`](https://github.com/humanlayer/skills), [`mattpocock/skills`](https://github.com/mattpocock/skills), [`poteto/noodle`](https://github.com/poteto/noodle), [`dmmulroy/skills`](https://github.com/dmmulroy/skills), [`t3dotgg/tstack`](https://github.com/t3dotgg/tstack) and others.
