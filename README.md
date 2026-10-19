# Agent Skills

My personal opinionated skills library for software engineering, UX design, writing and productivity.

Follows the [Agent Skills specification](https://agentskills.io/specification).

## Included skills

### Writing

Drafting, editing, and developer documentation. The hard writing rules for every response live in `global/AGENTS.md`.

| Skill               | Purpose                                                                                           |
| ------------------- | ------------------------------------------------------------------------------------------------- |
| `writing`           | Drafting and editing guidance for documents, reports, and substantial prose.                      |
| `technical-writing` | Developer documentation, comments, commits, release notes, and agent instructions.                |
| `pull-requests`     | Pull-request creation, titles, and descriptions with visual change outlines.                      |
| `show-me`           | Visual explanations for code questions, code changes, and pull-request descriptions.              |

### UX and design

Product design and user-facing interface work.

| Skill | Purpose                                                                                  |
| ----- | ---------------------------------------------------------------------------------------- |
| `ux`  | Routes product design, UX, UI, accessibility, interface copy, visual polish, and motion. |

### Engineering

Software development, diagnosis, reviews, and maintenance.

| Skill                             | Purpose                                                                                                        |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `engineering`                     | Implementation baseline for source fixes, toolchain checks, design decisions, delegation, and verification.    |
| `typescript`                      | TypeScript-specific type, validation, and code guidance.                                                       |
| `diagnosing-bugs`                 | Evidence-driven diagnosis for hard bugs and performance regressions.                                           |
| `diagnosing-production-incidents` | Read-only evidence collection and diagnosis for urgent live production incidents.                              |
| `tdd`                             | A focused failing-test-first loop when a practical test target exists.                                         |
| `code-review`                     | Reviews a diff on Sol and Opus for standards, spec, and correctness, and calibrates against bot comments.      |
| `babysit-pr`                      | Monitors pull-request reviews, CI, and mergeability, with authorised fixes and bounded flaky retries.            |
| `design-it-twice`                 | Compares several software module interface designs before choosing one.                                        |
| `upgrade-deps`                    | Comprehensive pnpm dependency, GitHub Actions, security, and Node.js and pnpm toolchain upgrades.              |
| `improve-architecture`            | Finds deep-module and seam improvements across a codebase, then produces a visual report.                      |
| `improve-organisation`            | Reviews codebase structure, ownership, filenames, shallow paths, and companion-file ownership.                 |
| `improve-performance`             | Benchmarks and improves a selected critical path, then produces a measured before-and-after report.            |
| `improve-security`                | Reviews trust boundaries, access control, secrets, sensitive data, and dependency risk.                        |
| `improve-standards`               | Reviews a codebase against repository and engineering standards, then produces a visual report.                |
| `improve-testing`                 | Ranks every test by value, maps behavioural guarantees, and produces a visual testing report.                  |

### Productivity

Access to the homelab.

| Skill     | Purpose                                                                                   |
| --------- | ----------------------------------------------------------------------------------------- |
| `homelab` | Routes access to fleet computers and self-hosted services through the homelab repository. |

## Install with `npx skills`

List the repository's skills or install the baseline skills globally for Codex and Claude Code:

```sh
npx skills@latest add jameswyse/skills --list
npx skills@latest add jameswyse/skills --global --agent codex --agent claude-code --skill writing --skill engineering --skill ux --skill show-me --yes
```

With Codex and Claude Code selected together, `npx skills` keeps a canonical copy under
`~/.agents/skills` and symlinks it into Claude Code. A single non-universal agent target is copied
by the current CLI even when `--copy` is omitted. Pass `--copy` explicitly only when independent
copies are wanted or the target filesystem cannot use symlinks.

## Configure global invocation

The global instructions live in this repository.

`scripts/sync-skills` links `~/.agents/AGENTS.md` and `~/.claude/CLAUDE.md` to these files and
points `AGENTS.md` in both Codex homes, `~/.codex` and T3 Code's `~/.codex-t3`, at
`~/.agents/AGENTS.md`. Edit the repository copies, then commit them and update the fleet. Without
the sync script, copy the two files into place instead.

Skills with `disable-model-invocation: true` remain available through `/skill-name`, but Claude does
not load or call them automatically. This is a Claude Code extension to the Agent Skills
frontmatter. Strict Agent Skills packaging and upload tools may reject it.

## Monitor pull requests with `babysit-pr`

`babysit-pr` is included in this repository. It requires Python 3 and an authenticated GitHub CLI
with access to the target repository. Invoke `$babysit-pr` in Codex or `/babysit-pr` in Claude Code
from the repository that owns the pull request. Supply a PR number or URL, or let it infer the PR
from the current branch.

The skill watches review feedback, CI, and mergeability until the PR closes or needs your input.
In T3 Code it hands wake-ups to T3's PR watching instead of running a long-lived watcher. Fixes, pushes, retries, and GitHub comments stay within the authority you give for that task.
The watcher, reference notes, and tests live in
[`skills/engineering/babysit-pr`](skills/engineering/babysit-pr).

## Optional external skills

Skills in this repository can defer specialised work to external skills when they are installed. The external skills stay owned by `npx skills`; this repository does not copy or modify them.

`ux` routes interface work to the installed [`jakubkrehel/skills`](https://github.com/jakubkrehel/skills) family. It uses that family's own workflow and domain routing. `writing` also delegates user-facing interface copy to `better-writing` when available.

Animation work routes to the focused skills from [`emilkowalski/skills`](https://github.com/emilkowalski/skills). `animate` builds motion, `review-animations` reviews it, `improve-animations` audits it, `find-animation-opportunities` finds useful additions, and `animation-vocabulary` names effects.

The upstream `interface-review`, `variant`, and `explain-interface` skills are user-invoked. Invoke them explicitly with the syntax supported by the current agent, such as `$interface-review` in Codex or `/interface-review` in Claude Code. The local `ux` router identifies those cases but does not replace their invocation policy.

## Recommended specialist skills

[`external-skills.json`](external-skills.json) lists every external skill to install globally,
keyed by install source. The `aws agent-toolkit` entry lists the AWS skills; every other key is an
`npx skills` source. To add a skill to every machine, add its name under its source, commit and
push, then run `scripts/update-fleet-skills`.

Install missing skills and update installed ones on this machine with:

```sh
scripts/setup-external-skills
```

Inspect the commands without changing the global installation:

```sh
scripts/setup-external-skills --dry-run
```

The script installs the `npx skills` entries for both Codex and Claude Code and manages the AWS
entries with `aws agent-toolkit add-skill` and `update-skill`. It reads the global inventories
before making changes, refuses to overwrite a same-named skill owned by another source, and lists
installed `npx skills` skills that the file does not mention. It never removes a skill. `npx skills`
records its installations in `~/.agents/.skill-lock.json`. The script does not manage this
repository's live symlinks.

The AWS skills need an up-to-date AWS CLI, as described in the
[AWS CLI setup for Agent Toolkit](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/aws-cli.html#aws-cli-setup).
The script does not configure the AWS MCP server. Run `aws configure agent-toolkit` interactively
when a machine needs it. The Sentry skill needs an up-to-date
[Sentry CLI](https://cli.sentry.dev/).

## Development and using skills locally

Source skills live under `skills/<group>/<skill-name>`. The groups organise the repository for
people; installed skills remain flat so agents continue to find them by skill name.

Run the sync script:

```sh
scripts/sync-skills
```

It discovers every grouped skill, links it into `~/.agents/skills/<skill-name>`, then links
`~/.claude/skills/<skill-name>` to that canonical entry. Edits are available immediately because
the canonical entry points to this working tree.

It also links `AGENTS.md` beside the canonical skills directory and `CLAUDE.md` beside Claude
Code's skills directory to the files in `global/`, then links `AGENTS.md` in each Codex home to the
shared `AGENTS.md`. Pass `--codex-home` once per home to override the default `~/.codex` and
`~/.codex-t3`. When one of these paths already holds a different file, the script moves it to a
timestamped `.backup-` file before linking. It leaves a symlink to anywhere else unchanged and
reports a conflict.

The script keeps a private ownership record in both managed skills directories. On later runs it:

- creates links for new skills;
- updates links it previously created;
- removes its links when their source skills no longer exist; and
- leaves existing files, directories and unmanaged symlinks untouched.

A conflict is reported and causes a non-zero exit status. Pass every target to exercise the sync
without changing the global installation:

```sh
scripts/sync-skills --target /tmp/agent-skills-test --claude-target /tmp/claude-skills-test \
  --codex-home /tmp/codex-test
```

Do not let `npx skills` and `scripts/sync-skills` manage the same local skill. Use `npx skills` for
released installations and the sync script for this working tree.

Run the repository tooling tests and the imported PR watcher tests with:

```sh
scripts/test-skills
```

The command uses an isolated `uv` environment with pinned pytest. The watcher tests replace GitHub
calls with local test data and do not contact or modify pull requests. To run only the repository
tooling tests, use `python3 -m unittest discover -s tests`.

Validate every skill against the Agent Skills fields and the supported Claude Code extensions:

```sh
scripts/validate-skills
```

Pass skill names to validate a smaller set:

```sh
scripts/validate-skills writing technical-writing
```

The command supplies its pinned PyYAML dependency through an isolated `uv` environment. It does
not require Codex, modify Homebrew Python, or require an activated virtual environment.

In Claude Code, run `/skills` to confirm discovery. This repository's `code-review` skill overrides
Claude Code's bundled `/code-review`; use Claude's `/review` alias when you want the bundled review.

## Update the fleet

After committing and pushing skill or global instruction changes, roll them out to every
development machine:

```sh
scripts/update-fleet-skills
```

The script exits with status 2 before contacting the fleet when this checkout has uncommitted
changes, unpushed commits, or upstream commits it has not pulled. Otherwise it validates the skills,
runs `scripts/sync-skills` and `scripts/setup-external-skills` locally, then connects to each
other machine in its fleet list through the homelab repository's `scripts/fleet`. On each machine
it fast-forwards `~/Projects/skills` to the validated commit, runs the sync script and sets up the
external skills. A machine with local changes, commits, or a different branch is reported as failed
and left unchanged. Successful steps print only changes, conflicts and summaries; a failed step
prints its full output. The script reads the homelab checkout from `~/Projects/homelab` unless
`HOMELAB_DIR` is set.

## Credits

`babysit-pr` is imported from [OpenAI's Codex skill](https://github.com/openai/codex/tree/a8c36ca6d265800c1b2c67d19d3583e23dee8382/.codex/skills/babysit-pr)
at commit `a8c36ca6d265800c1b2c67d19d3583e23dee8382`. It retains the upstream Apache-2.0
[licence](skills/engineering/babysit-pr/LICENSE) and [notices](skills/engineering/babysit-pr/NOTICE).
Local changes adapt installation paths and consolidate the workflow and authority rules. They retain
the safeguards from the upstream [review monitoring](https://github.com/openai/codex/commit/0fe873ad5f4d),
[CI diagnostics](https://github.com/openai/codex/commit/c39824c2fd47),
[GitHub mutation policy](https://github.com/openai/codex/commit/f3a807497590), and
[pending review](https://github.com/openai/codex/commit/a770e5b8470d) fixes. The watcher and its
tests are unchanged.

`show-me` is adapted from [HumanLayer's source skill](https://github.com/humanlayer/skills/blob/main/plugins/show-me/skills/show-me/SKILL.md) and retains its MIT licence.

This curated collection also draws on skills and ideas from [`mattpocock/skills`](https://github.com/mattpocock/skills),
[`poteto/noodle`](https://github.com/poteto/noodle), [`dmmulroy/skills`](https://github.com/dmmulroy/skills) and others.
