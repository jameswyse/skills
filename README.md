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

| Skill                  | What it does                                                                     |
| ---------------------- | -------------------------------------------------------------------------------- |
| `engineering`          | Sets the baseline for implementing, debugging, designing and verifying software. |
| `typescript`           | Adds rules for TypeScript types and validation.                                  |
| `design-it-twice`      | Compares several interface designs for a module before choosing one.             |
| `tdd`                  | Runs a failing-test-first loop.                                                  |
| `diagnosing-bugs`      | Finds the cause of hard bugs and performance regressions from evidence.          |
| `triage-sentry`        | Investigates a Sentry issue or triages a project's issues.                       |
| `upgrade-deps`         | Upgrades a pnpm project's dependencies, Node.js, pnpm and GitHub Actions.        |
| `code-review`          | Reviews a change for spec, correctness and standards across several models.      |
| `pull-requests`        | Opens pull requests and writes their titles, descriptions and review labels.     |
| `before-and-after`     | Adds screenshots or recordings to a pull request description.                    |
| `babysit-pr`           | Watches a pull request's CI, reviews and merge conflicts, and fixes what it can. |
| `full-send`            | Takes a task through to a ready pull request with passing checks.                |
| `pull-request-reviews` | Reviews someone else's pull request and drafts or posts one comment.             |
| `show-me`              | Explains code and code changes, with a diagram when one helps.                   |
| `writing`              | Drafts, edits and reviews prose other people will read.                          |
| `technical-writing`    | Writes developer docs, READMEs, commit messages, skills and agent instructions.  |
| `ux`                   | Designs, builds and reviews user-facing interfaces.                              |
| `html-report`          | Builds compact HTML reports and shows them in T3 Code.                           |
| `homelab`              | Reaches my machines and self-hosted services. Personal, so skip it.              |

## Requirements

- `babysit-pr` needs Python 3 and an authenticated GitHub CLI.
- `before-and-after` needs [agent-browser](https://github.com/vercel-labs/agent-browser) for captures.
- `triage-sentry` works best with the [Sentry CLI](https://cli.sentry.dev/).
- `ux` and `writing` hand some work to the optional skills in [`external-skills.json`](external-skills.json).
- `code-review` and `engineering` delegate to other models through T3 Code when it's available, and use the current agent's subagents otherwise.

## Development

See [docs/development.md](docs/development.md) for local linking, validation, tests, evals and fleet updates.

Licensed [MIT](LICENSE), except the imported skills [`babysit-pr`](https://github.com/openai/codex/tree/a8c36ca6d265800c1b2c67d19d3583e23dee8382/.codex/skills/babysit-pr) from OpenAI Codex (Apache-2.0), [`before-and-after`](https://github.com/vercel-labs/before-and-after/tree/2880b6799dd9000e65cc476d066abcbb48bce94e/skill) from Vercel Labs (PolyForm Shield 1.0.0) and [`show-me`](https://github.com/humanlayer/skills/blob/main/plugins/show-me/skills/show-me/SKILL.md) from HumanLayer (MIT), each modified and keeping its own licence. Ideas also come from [`mattpocock/skills`](https://github.com/mattpocock/skills), [`poteto/noodle`](https://github.com/poteto/noodle), [`dmmulroy/skills`](https://github.com/dmmulroy/skills) and others.
