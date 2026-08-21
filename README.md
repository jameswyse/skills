# Skills

Personal skills following the [Agent Skills specification](https://agentskills.io/specification).

## Structure

```text
skills/
  <skill-name>/
    SKILL.md
    agents/
      openai.yaml  # Codex invocation policy
    scripts/       # optional
    references/    # optional
    assets/        # optional
scripts/
  sync-skills
```

Each skill lives directly under `skills/`. Its directory name must match the `name` in its `SKILL.md` frontmatter.

Each skill declares its Codex invocation policy in `agents/openai.yaml`. Set `allow_implicit_invocation` to `true` only when the description gives Codex a clear, reliable automatic trigger. Set it to `false` for skills that should run only when explicitly invoked as `$skill-name`.

## Use skills locally

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

## Install with `npx skills`

List or install skills with:

```sh
npx skills add jameswyse/skills --list
npx skills add jameswyse/skills --skill writing
```
