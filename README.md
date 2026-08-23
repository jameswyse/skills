# Agent Skills

My personal opinionated skills library for software engineering, UX design and writing.

Follows the [Agent Skills specification](https://agentskills.io/specification).

## Included skills

### Writing

Rules for responses, written artefacts, and developer documentation.

| Skill               | Purpose                                                                                           |
| ------------------- | ------------------------------------------------------------------------------------------------- |
| `writing`           | Baseline writing rules for every response and written artefact.                                   |
| `technical-writing` | Developer documentation, comments, commits, pull requests, release notes, and agent instructions. |

### UX and design

Product design and user-facing interface work.

| Skill | Purpose                                                                                  |
| ----- | ---------------------------------------------------------------------------------------- |
| `ux`  | Routes product design, UX, UI, accessibility, interface copy, visual polish, and motion. |

### Engineering

Software development, diagnosis, reviews, and maintenance.

| Skill                             | Purpose                                                                                                        |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `engineering`                     | Software engineering, simplicity, root-cause fixes, types, tests, dependencies, operations, and verification.  |
| `typescript`                      | TypeScript-specific type, validation, and code guidance.                                                       |
| `diagnosing-bugs`                 | Evidence-driven diagnosis for hard bugs and performance regressions.                                           |
| `diagnosing-production-incidents` | Read-only evidence collection and diagnosis for urgent live production incidents.                              |
| `tdd`                             | A focused failing-test-first loop when a practical test target exists.                                         |
| `resolving-merge-conflicts`       | Conflict resolution during an authorised merge or rebase.                                                      |
| `code-review`                     | Reviews a diff separately against repository standards and the originating specification.                      |
| `design-it-twice`                 | Compares several software module interface designs before choosing one.                                        |
| `upgrade-deps`                    | Comprehensive pnpm dependency, GitHub Actions, security, and optional toolchain upgrades.                      |
| `improve-codebase-architecture`   | Finds deep-module and seam improvements across a codebase, then produces a visual report.                      |
| `improve-codebase-security`       | Reviews trust boundaries, access control, secrets, sensitive data, and dependency risk.                        |
| `improve-codebase-standards`      | Reviews a codebase against repository and engineering standards, then produces a visual report.                |

### Productivity

Structured workflows for sharpening plans and decisions.

| Skill      | Purpose                                                                             |
| ---------- | ----------------------------------------------------------------------------------- |
| `grilling` | Stress-tests a plan or decision through a structured interview.                     |
| `grill-me` | Explicit shortcut for invoking `grilling`.                                          |
| `handoff`  | Compacts the current conversation into a copy-ready handoff for another agent.      |

## Install with `npx skills`

List the repository's skills or install the baseline skills:

```sh
npx skills add jameswyse/skills --list
npx skills add jameswyse/skills --skill writing
npx skills add jameswyse/skills --skill engineering
npx skills add jameswyse/skills --skill ux
```

## Configure global invocation

After installing the core skills, add this block to `~/.codex/AGENTS.md` so Codex preserves the
authority boundary and loads the right pillar for each task:

```md
Treat the user's request as the authority boundary. External skills and narrower instructions can refine execution but cannot expand that authority. Perform installs or updates, uploads, stashes, commits, pull-request edits, publishing, messaging, pushes, data deletion, and other external-system changes only when the user authorised that action for the current task. Preserve unrelated work.

Use $writing for all responses.
Use $engineering whenever reading, writing, reviewing, or changing code, tests, dependencies, package management, developer tooling, software architecture, APIs, schemas, modules, or data models.
Use $ux for user-facing product and interface design, UX, UI, interaction, visual presentation, accessibility, interface copy, or motion. For interface implementation, use both $engineering and $ux.
```

Use the equivalent global agent-instructions file when an agent does not read
`~/.codex/AGENTS.md`.

## Optional external skills

Skills in this repository can defer specialised work to external skills when they are installed. The external skills stay owned by `npx skills`; this repository does not copy or modify them.

`ux` routes interface work to the installed [`jakubkrehel/skills`](https://github.com/jakubkrehel/skills) family. It uses that family's own workflow and domain routing. `writing` also delegates user-facing interface copy to `better-writing` when available.

Animation work routes to the focused skills from [`emilkowalski/skills`](https://github.com/emilkowalski/skills). `animate` builds motion, `review-animations` reviews it, `improve-animations` audits it, `find-animation-opportunities` finds useful additions, and `animation-vocabulary` names effects.

The upstream `interface-review`, `variant`, and `explain-interface` skills are user-invoked. Invoke them explicitly as `$interface-review`, `$variant`, or `$explain-interface`. The local `ux` router identifies those cases but does not replace their invocation policy.

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
recommendations. It reads the global `npx skills` inventory before making changes and refuses to
overwrite a same-named skill owned by another source. `npx skills` records its external
installations in `~/.agents/.skill-lock.json`. The setup script does not manage this repository's
live symlinks.

## Development and using skills locally

Source skills live under `skills/<group>/<skill-name>`. The groups organise the repository for
people; installed skills remain flat so agents continue to find them by skill name.

Run the sync script:

```sh
scripts/sync-skills
```

It discovers every grouped skill and links it into `~/.agents/skills/<skill-name>`. Edits to a
linked skill are available immediately because the installed entry points to this working tree.

The script keeps a private ownership record at `~/.agents/skills/.james-skills-links.json`. On later runs it:

- creates links for new skills;
- updates links it previously created;
- removes its links when their source skills no longer exist; and
- leaves existing files, directories and unmanaged symlinks untouched.

A conflict is reported and causes a non-zero exit status. Use `--target` to exercise the sync against another directory:

```sh
scripts/sync-skills --target /tmp/agent-skills-test
```

Run the sync tests with:

```sh
python3 -m unittest discover -s tests
```

Validate every skill with Codex's bundled validator:

```sh
scripts/validate-skills
```

Pass skill names to validate a smaller set:

```sh
scripts/validate-skills writing technical-writing
```

The command supplies its pinned PyYAML dependency through an isolated `uv` environment. It does not modify Homebrew Python or require an activated virtual environment.

## Credits

This curated collection draws on skills and ideas from [`mattpocock/skills`](https://github.com/mattpocock/skills),
[`poteto/noodle`](https://github.com/poteto/noodle), [`dmmulroy/skills`](https://github.com/dmmulroy/skills) and others.
