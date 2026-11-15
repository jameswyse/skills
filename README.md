# Agent Skills

My skills for software engineering, UX, writing and homelab access. They follow the [Agent Skills specification](https://agentskills.io/specification). I use them in Claude Code, Codex, Cursor and Grok Build.

## Install

```sh
npx skills@latest add jameswyse/skills --global --agent claude-code --agent codex --skill '*' --yes
```

This installs to `~/.agents/skills`, which Codex, Cursor and Grok Build read, and links each skill into `~/.claude/skills` for Claude Code. Replace `'*'` with one or more skill names to install fewer. Several skills rely on the global instructions in [`global/AGENTS.md`](global/AGENTS.md). Use it as `~/.codex/AGENTS.md` in Codex, and import it from `~/.claude/CLAUDE.md` in Claude Code. For other agents, add it to their global rules.

## Use

Agents load a skill on their own when the task matches its description. To load one yourself, type `$skill-name` in Codex or `/skill-name` in Claude Code and Cursor. `design-it-twice` loads only when you invoke it.

This repository's `code-review` replaces Claude Code's bundled `/code-review`. Use `/review` for the bundled one.

## Skills

### Writing

| Skill                  | What it does                                                                    |
| ---------------------- | ------------------------------------------------------------------------------- |
| `writing`              | Drafts, edits and reviews prose other people will read.                         |
| `technical-writing`    | Writes developer docs, READMEs, commit messages, skills and agent instructions. |
| `pull-requests`        | Opens pull requests and writes their titles, descriptions and review labels.    |
| `pull-request-reviews` | Reviews someone else's pull request and drafts or posts one comment.            |
| `before-and-after`     | Adds screenshots or recordings to a pull request description.                   |
| `show-me`              | Explains code and code changes, with a diagram when one helps.                  |

### UX

| Skill         | What it does                                           |
| ------------- | ------------------------------------------------------ |
| `ux`          | Designs, builds and reviews user-facing interfaces.    |
| `html-report` | Builds compact HTML reports and shows them in T3 Code. |

### Engineering

| Skill             | What it does                                                                     |
| ----------------- | -------------------------------------------------------------------------------- |
| `engineering`     | Sets the baseline for implementing, debugging, designing and verifying software. |
| `typescript`      | Adds rules for TypeScript types and validation.                                  |
| `diagnosing-bugs` | Finds the cause of hard bugs and performance regressions from evidence.          |
| `tdd`             | Runs a failing-test-first loop.                                                  |
| `code-review`     | Reviews a change for spec, correctness and standards across several models.      |
| `babysit-pr`      | Watches a pull request's CI, reviews and merge conflicts, and fixes what it can. |
| `full-send`       | Takes a task through to a ready pull request with passing checks.                |
| `triage-sentry`   | Investigates a Sentry issue or triages a project's issues.                       |
| `design-it-twice` | Compares several interface designs for a module before choosing one.             |
| `upgrade-deps`    | Upgrades a pnpm project's dependencies, Node.js, pnpm and GitHub Actions.        |

### Productivity

| Skill     | What it does                                        |
| --------- | --------------------------------------------------- |
| `homelab` | Reaches my other machines and self-hosted services. |

## Requirements

- `babysit-pr` needs Python 3 and an authenticated GitHub CLI.
- `before-and-after` needs [agent-browser](https://github.com/vercel-labs/agent-browser) for captures.
- `triage-sentry` works best with the [Sentry CLI](https://cli.sentry.dev/).
- `ux` and `writing` hand some work to the optional skills in [`external-skills.json`](external-skills.json).

## Development

See [docs/development.md](docs/development.md) for local linking, validation, tests, evals and fleet updates.

Credits: [`babysit-pr`](https://github.com/openai/codex/tree/a8c36ca6d265800c1b2c67d19d3583e23dee8382/.codex/skills/babysit-pr) from OpenAI Codex (Apache-2.0), [`before-and-after`](https://github.com/vercel-labs/before-and-after/tree/2880b6799dd9000e65cc476d066abcbb48bce94e/skill) from Vercel Labs (PolyForm Shield 1.0.0) and [`show-me`](https://github.com/humanlayer/skills/blob/main/plugins/show-me/skills/show-me/SKILL.md) from HumanLayer (MIT), each modified and keeping its licence, plus ideas from [`mattpocock/skills`](https://github.com/mattpocock/skills), [`poteto/noodle`](https://github.com/poteto/noodle), [`dmmulroy/skills`](https://github.com/dmmulroy/skills) and others.
