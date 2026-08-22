---
name: code-review
description: Review working-tree changes or a diff from a fixed point on separate Standards and Spec axes. Use for branch, PR or work-in-progress reviews and “review since X”.
---

# Two-axis code review

Review **Standards** (repository rules and code smells) separately from **Spec** (the originating
request, issue or PRD). A change can pass either axis and fail the other; do not merge or rerank
their findings.

## 1. Fix the scope

- Supplied fixed point: verify it with `git rev-parse`, capture `git diff <ref>...HEAD` once and
  note `git log <ref>..HEAD --oneline`. If the working tree is dirty, also capture `git diff HEAD`
  and the complete contents of untracked files from `git status --short`. Review the committed and
  working-tree diffs as one scope without double-counting overlapping findings.
- No fixed point and a dirty tree: use `git diff HEAD` plus the complete contents of untracked
  files from `git status --short`.
- No fixed point and a clean tree: resolve the comparison branch from current PR metadata when
  available. Otherwise use the remote default branch from `refs/remotes/*/HEAD` when exactly one is
  available. Verify the resolved ref, then capture `git diff <base>...HEAD` and
  `git log <base>..HEAD --oneline` once. If no unambiguous base exists, ask for a fixed point.
- Bad ref or ambiguous base: stop here and ask for a valid scope. For a verified empty diff, report
  that there are no changes to review and stop.

For working-tree reviews, the user request is the spec. Otherwise find it in order from issue
references in commit messages, a user-supplied path, then a matching Markdown file under `docs/` or
`specs/`. If none exists, skip the Spec agent and report “no spec available”.

Standards sources are repository files that define how code is written, plus this smell baseline.
Repository rules override the baseline; tooling-enforced issues are out of scope. Every baseline
finding is a labelled judgement call:

- **Mysterious Name** — a name hides what it does or holds. Rename it; if no honest name exists,
  clarify the design.
- **Duplicated Code** — the same logic shape recurs. Extract and share it.
- **Feature Envy** — a method reaches into another object's data more than its own. Move it to the
  data it envies.
- **Data Clumps** — the same fields or parameters travel together. Give them one type.
- **Primitive Obsession** — a primitive represents a domain concept. Introduce a small type.
- **Repeated Switches** — the same conditional over one type recurs. Use polymorphism or one shared
  map.
- **Ternaryception** — a ternary is nested inside a ternary that is already nested. One level of
  nesting is fine; beyond that, replace the expression with named branches, a lookup or a switch.
- **Shotgun Surgery** — one logical change requires scattered edits. Gather what changes together.
- **Divergent Change** — one module changes for unrelated reasons. Split its responsibilities.
- **Speculative Generality** — unused abstraction, parameters or hooks anticipate unasked needs.
  Delete or inline them.
- **Message Chains** — callers navigate a long `a.b().c().d()` chain. Hide it behind the first
  object.
- **Middle Man** — a module mainly delegates. Call the actual owner directly.
- **Refused Bequest** — a subtype ignores most inherited behaviour. Prefer composition.
- **Unnecessary Complexity.** The change adds concepts, state, branches, layers, dependencies, or
  execution paths that its behaviour and constraints do not require. Name the concrete maintenance
  or correctness cost and the smallest coherent alternative. Do not flag essential domain complexity
  or mere line count.

## 2. Run independent reviews

Spawn the applicable agents in parallel. Do not let them edit files.

### Standards agent

Provide the scope command, commit list when applicable, complete untracked file contents, every
standards-source path, and the full baseline above. Ask:

> Report by file/hunk: (a) every documented-standard violation, citing the rule and its source;
> (b) every baseline smell, naming it and quoting the hunk. Separate hard documented breaches from
> baseline judgement calls. Repository rules override the baseline. Skip tooling-enforced issues.
> Stay under 400 words.

### Spec agent

Provide the same scope information and the spec path or contents. Ask:

> Report: (a) missing or partial requirements; (b) unrequested behaviour or scope creep; (c)
> apparently implemented requirements whose implementation looks wrong. Quote the relevant spec
> line for every finding. Stay under 400 words.

## 3. Report

Present the reports, verbatim or lightly cleaned, under `## Standards` and `## Spec`. Do not merge
or rerank them. End with one line giving each axis's finding count and worst issue, if any.
