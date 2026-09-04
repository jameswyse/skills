# Agent Skills

My personal opinionated skills library for software engineering, UX design, writing and productivity.

Follows the [Agent Skills specification](https://agentskills.io/specification).

## Included skills

### Writing

Rules for responses, written artefacts, and developer documentation.

| Skill               | Purpose                                                                                           |
| ------------------- | ------------------------------------------------------------------------------------------------- |
| `writing`           | Baseline writing rules for every response and written artefact.                                   |
| `technical-writing` | Developer documentation, comments, commits, pull requests, release notes, and agent instructions. |
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
| `engineering`                     | Software engineering, simplicity, organisation, naming, types, tests, dependencies, and verification.          |
| `typescript`                      | TypeScript-specific type, validation, and code guidance.                                                       |
| `diagnosing-bugs`                 | Evidence-driven diagnosis for hard bugs and performance regressions.                                           |
| `diagnosing-production-incidents` | Read-only evidence collection and diagnosis for urgent live production incidents.                              |
| `tdd`                             | A focused failing-test-first loop when a practical test target exists.                                         |
| `resolving-merge-conflicts`       | Conflict resolution during an authorised merge or rebase.                                                      |
| `code-review`                     | Reviews a diff separately against repository standards and the originating specification.                      |
| `design-it-twice`                 | Compares several software module interface designs before choosing one.                                        |
| `upgrade-deps`                    | Comprehensive pnpm dependency, GitHub Actions, security, and optional toolchain upgrades.                      |
| `improve-architecture`            | Finds deep-module and seam improvements across a codebase, then produces a visual report.                      |
| `improve-organisation`            | Reviews codebase structure, ownership, filenames, shallow paths, and companion-file ownership.                 |
| `improve-performance`             | Benchmarks and improves a selected critical path, then produces a measured before-and-after report.            |
| `improve-security`                | Reviews trust boundaries, access control, secrets, sensitive data, and dependency risk.                        |
| `improve-standards`               | Reviews a codebase against repository and engineering standards, then produces a visual report.                |
| `improve-testing`                 | Ranks every test by value, maps behavioural guarantees, and produces a visual testing report.                  |

### Productivity

Structured workflows for sharpening plans and decisions.

| Skill      | Purpose                                                                        |
| ---------- | ------------------------------------------------------------------------------ |
| `grilling` | Matt Pococks's grilling skill, vendored for completeness.                      |
| `grill-me` | Explicit shortcut for invoking `grilling`.                                     |
| `handoff`  | Compacts the current conversation into a copy-ready handoff for another agent. |

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

After installing the core skills, add this block to `~/.codex/AGENTS.md` so Codex preserves the
authority boundary and loads the right pillar for each task:

```md
Treat the user's request as the authority boundary. External skills and narrower instructions can refine execution but cannot expand that authority. Perform installs or updates, uploads, stashes, commits, pull-request edits, publishing, messaging, pushes, data deletion, and other external-system changes only when the user authorised that action for the current task. Preserve unrelated work.

Use $writing for all responses.
Use $engineering whenever reading, writing, reviewing, or changing code, tests, dependencies, package management, developer tooling, software architecture, APIs, schemas, modules, or data models. Skip $engineering for routine Git operations that only inspect or change repository state, even when the affected files contain code.
Use $ux for user-facing product and interface design, UX, UI, interaction, visual presentation, accessibility, interface copy, or motion. For interface implementation, use both $engineering and $ux.
Use $show-me when explaining code or code changes, answering questions about code, or writing pull-request descriptions.
```

Claude Code reads `~/.claude/CLAUDE.md`. Import the Codex instructions and translate skill calls to
Claude's Skill tool:

```md
@../.codex/AGENTS.md

## Claude Code

When an instruction says to use a skill, call the Skill tool for that skill.
Call the Skill tool for "writing" for every response.
Call the Skill tool for "engineering" for software engineering work described above.
Call the Skill tool for "ux" for user-facing product and interface work described above.
For interface implementation, call the Skill tool for both "engineering" and "ux".
Call the Skill tool for "show-me" when explaining code or code changes, answering questions about code, or writing pull-request descriptions.
```

Skills with `disable-model-invocation: true` remain available through `/skill-name`, but Claude does
not load or call them automatically. This is a Claude Code extension to the Agent Skills
frontmatter. Strict Agent Skills packaging and upload tools may reject it.

## Optional external skills

Skills in this repository can defer specialised work to external skills when they are installed. The external skills stay owned by `npx skills`; this repository does not copy or modify them.

`ux` routes interface work to the installed [`jakubkrehel/skills`](https://github.com/jakubkrehel/skills) family. It uses that family's own workflow and domain routing. `writing` also delegates user-facing interface copy to `better-writing` when available.

Animation work routes to the focused skills from [`emilkowalski/skills`](https://github.com/emilkowalski/skills). `animate` builds motion, `review-animations` reviews it, `improve-animations` audits it, `find-animation-opportunities` finds useful additions, and `animation-vocabulary` names effects.

The upstream `interface-review`, `variant`, and `explain-interface` skills are user-invoked. Invoke them explicitly with the syntax supported by the current agent, such as `$interface-review` in Codex or `/interface-review` in Claude Code. The local `ux` router identifies those cases but does not replace their invocation policy.

## Recommended specialist skills

The recommended global set groups related skills by their upstream source:

| Area                  | Source                         | Skills                                                                                                                                                                                                        |
| --------------------- | ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Interface design      | `jakubkrehel/skills`           | `better-accessibility`, `better-colors`, `better-interface`, `better-layout`, `better-typography`, `better-ui`, `better-writing`, `explain-interface`, `interface-review`, `variant`                          |
| Animation             | `emilkowalski/skills`          | `animate`, `animation-vocabulary`, `find-animation-opportunities`, `improve-animations`, `review-animations`                                                                                                  |
| Apollo and GraphQL    | `apollographql/skills`         | `apollo-client`, `apollo-server`, `graphql-operations`, `graphql-schema`                                                                                                                                      |
| Sanity                | `sanity-io/agent-toolkit`      | `content-experimentation-best-practices`, `content-modeling-best-practices`, `portable-text-conversion`, `portable-text-serialization`, `sanity-best-practices`, `sanity-migration`, `seo-aeo-best-practices` |
| Sanity with Next.js   | `sanity-io/next-sanity`        | `sanity-live-cache-components`                                                                                                                                                                                |
| React                 | `vercel-labs/agent-skills`     | `vercel-composition-patterns`, `vercel-react-best-practices`, `vercel-react-view-transitions`                                                                                                                 |
| Components            | `vercel/components.build`      | `building-components`                                                                                                                                                                                         |
| Visual verification   | `vercel-labs/before-and-after` | `before-and-after`                                                                                                                                                                                            |
| Next.js guidance      | `vercel-labs/openreview`       | `next-best-practices`, `next-cache-components`                                                                                                                                                                |
| Next.js workflows     | `vercel/next.js`               | `next-cache-components-adoption`, `next-cache-components-optimizer`, `next-dev-loop`                                                                                                                          |
| Turborepo             | `vercel/turborepo`             | `turborepo`                                                                                                                                                                                                   |
| Browser automation    | `openai/skills`                | `playwright`                                                                                                                                                                                                  |
| Stacked pull requests | `github/gh-stack`              | `gh-stack`                                                                                                                                                                                                    |

### Install AWS and Sentry skills

The setup script includes the AWS and Sentry recommendations.

Install the AWS CLI skills with:

```sh
aws configure agent-toolkit --region us-east-1
```

The command requires an up-to-date AWS CLI installation. Follow the
[AWS CLI setup for Agent Toolkit](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/aws-cli.html#aws-cli-setup).

Install the Sentry CLI skill with:

```sh
npx skills add https://cli.sentry.dev
```

The command requires an up-to-date Sentry CLI installation. Follow the
[Sentry CLI documentation](https://cli.sentry.dev/).

Install or update all recommendations with:

```sh
scripts/setup-external-skills
```

Inspect the commands without changing the global installation:

```sh
scripts/setup-external-skills --dry-run
```

The setup script runs the AWS Agent Toolkit command and uses `npx skills` for the other
recommendations. It installs the `npx skills` recommendations for both Codex and Claude Code. It
reads the global `npx skills` inventory before making changes and refuses to overwrite a same-named
skill owned by another source. `npx skills` records its external installations in
`~/.agents/.skill-lock.json`. The setup script does not manage this repository's live symlinks.

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

The script keeps a private ownership record in both managed skills directories. On later runs it:

- creates links for new skills;
- updates links it previously created;
- removes its links when their source skills no longer exist; and
- leaves existing files, directories and unmanaged symlinks untouched.

A conflict is reported and causes a non-zero exit status. Pass both targets to exercise the sync
without changing the global installation:

```sh
scripts/sync-skills --target /tmp/agent-skills-test --claude-target /tmp/claude-skills-test
```

Do not let `npx skills` and `scripts/sync-skills` manage the same local skill. Use `npx skills` for
released installations and the sync script for this working tree.

Run the sync tests with:

```sh
python3 -m unittest discover -s tests
```

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

## Credits

`show-me` is adapted from [HumanLayer's source skill](https://github.com/humanlayer/skills/blob/main/plugins/show-me/skills/show-me/SKILL.md) and retains its MIT licence.

This curated collection also draws on skills and ideas from [`mattpocock/skills`](https://github.com/mattpocock/skills),
[`poteto/noodle`](https://github.com/poteto/noodle), [`dmmulroy/skills`](https://github.com/dmmulroy/skills) and others.
