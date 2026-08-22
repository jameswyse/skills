# Skills

Personal skills following the [Agent Skills specification](https://agentskills.io/specification).

## Install with `npx skills`

List or install skills with:

```sh
npx skills add jameswyse/skills --list
npx skills add jameswyse/skills --skill writing
```

## Optional external skills

Skills in this repository can defer specialised work to external skills when they are installed. The external skills stay owned by `npx skills`; this repository does not copy or modify them.

`interface-design` routes interface work to the installed [`jakubkrehel/skills`](https://github.com/jakubkrehel/skills) family. It uses that family's own workflow and domain routing. `writing` also delegates user-facing interface copy to `better-writing` when available.

Animation work routes to the focused skills from [`emilkowalski/skills`](https://github.com/emilkowalski/skills). `animate` builds motion, `review-animations` reviews it, `improve-animations` audits it, `find-animation-opportunities` finds useful additions, and `animation-vocabulary` names effects.

The upstream `interface-review`, `variant`, and `explain-interface` skills are user-invoked. Invoke them explicitly as `$interface-review`, `$variant`, or `$explain-interface`. The local `interface-design` router identifies those cases but does not replace their invocation policy.

## Recommended specialist skills

The recommended global set groups related skills by their upstream source:

| Area | Source | Skills |
| --- | --- | --- |
| Interface design | `jakubkrehel/skills` | `better-accessibility`, `better-colors`, `better-interface`, `better-layout`, `better-typography`, `better-ui`, `better-writing`, `explain-interface`, `interface-review`, `variant` |
| Animation | `emilkowalski/skills` | `animate`, `animation-vocabulary`, `find-animation-opportunities`, `improve-animations`, `review-animations` |
| Apollo and GraphQL | `apollographql/skills` | `apollo-client`, `apollo-server`, `graphql-operations`, `graphql-schema` |
| Sanity | `sanity-io/agent-toolkit` | `content-experimentation-best-practices`, `content-modeling-best-practices`, `portable-text-conversion`, `portable-text-serialization`, `sanity-best-practices`, `sanity-migration`, `seo-aeo-best-practices` |
| Sanity with Next.js | `sanity-io/next-sanity` | `sanity-live-cache-components` |
| React | `vercel-labs/agent-skills` | `vercel-composition-patterns`, `vercel-react-best-practices`, `vercel-react-view-transitions` |
| Components | `vercel/components.build` | `building-components` |
| Visual verification | `vercel-labs/before-and-after` | `before-and-after` |
| Next.js guidance | `vercel-labs/openreview` | `next-best-practices`, `next-cache-components` |
| Next.js workflows | `vercel/next.js` | `next-cache-components-adoption`, `next-cache-components-optimizer`, `next-dev-loop` |
| Turborepo | `vercel/turborepo` | `turborepo` |
| Browser automation | `openai/skills` | `playwright` |
| Stacked pull requests | `github/gh-stack` | `gh-stack` |

Install missing recommendations and update the installed recommendations with:

```sh
scripts/setup-external-skills
```

Inspect the commands without changing the global installation:

```sh
scripts/setup-external-skills --dry-run
```

The setup script reads the global `npx skills` inventory before making changes. It refuses to overwrite a same-named skill owned by another source. `npx skills` records the external installations in `~/.agents/.skill-lock.json`; the setup script does not manage this repository's live symlinks.

## Development and using skills locally

Run the sync script:

```sh
scripts/sync-skills
```

It links every skill in this repository into `~/.agents/skills`. Edits to a linked skill are available immediately because the installed entry points to this working tree.

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