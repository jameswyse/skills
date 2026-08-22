---
name: code-review
description: Review working-tree changes or a diff from a fixed point on separate Standards and Spec axes. Use for branch, PR or work-in-progress reviews and "review since X".
---

# Two-axis code review

Review two axes separately. **Standards** covers repository rules and code smells. **Spec** covers
the originating request, issue, or PRD. A change can pass either axis and fail the other. Do not
merge or rerank their findings.

Apply `$engineering` as the baseline for code, tests, dependencies, package management,
and developer tooling. When the scope contains tests, read its
[Testing](../engineering/references/testing.md) reference and use its named test smells.
When a finding depends on design, module depth, interface compression, seam placement, or
simplicity, read the relevant engineering reference before reporting it.

## 1. Fix the scope

- When the user supplies a fixed point, verify it with `git rev-parse`, capture `git diff <ref>...HEAD` once, and
  note `git log <ref>..HEAD --oneline`. If the working tree is dirty, also capture `git diff HEAD`
  and the complete contents of untracked files from `git status --short`. Review the committed and
  working-tree diffs as one scope without double-counting overlapping findings.
- When no fixed point exists and the working tree is dirty, use `git diff HEAD` plus the complete contents of untracked
  files from `git status --short`.
- When no fixed point exists and the working tree is clean, resolve the comparison branch from current PR metadata when
  available. Otherwise use the remote default branch from `refs/remotes/*/HEAD` when exactly one is
  available. Verify the resolved ref, then capture `git diff <base>...HEAD` and
  `git log <base>..HEAD --oneline` once. If no unambiguous base exists, ask for a fixed point.
- For a bad ref or ambiguous base, stop and ask for a valid scope. For a verified empty diff, report
  that there are no changes to review and stop.

For working-tree reviews, the user request is the spec. Otherwise find it in order from issue
references in commit messages, a user-supplied path, then a matching Markdown file under `docs/` or
`specs/`. If none exists, skip the Spec agent and report "no spec available".

Standards sources are repository files that define how code is written, `$engineering`
and its triggered references, plus this smell baseline. Repository rules override the baseline.
Tooling-enforced issues are out of scope. Smells are evidence to investigate, not automatic
refactoring instructions. Confirm the concrete maintenance or correctness cost in the diff, then
report the smallest coherent response. Every baseline finding is a labelled judgement call:

- **Mysterious Name.** A name hides what it does or holds. Rename it. If no honest name exists,
  clarify the design.
- **Duplicated Code.** The same logic shape recurs. Share one owner when the copies express the same
  stable rule and must change together. Keep repetition when an abstraction would encode guesses.
- **Feature Envy.** A method reaches into another object's data more than its own. Move the behaviour
  only when the other module owns the knowledge it needs.
- **Data Clumps.** The same fields or parameters travel together. Introduce one type when they form
  a domain concept or share an invariant.
- **Primitive Obsession.** Interchangeable primitives represent distinct domain concepts. Add a
  semantic type when it prevents invalid mixing or centralises validation.
- **Repeated Switches.** The same decision over one domain type recurs. Put the rule in one owner,
  such as a domain model, map, registry, or polymorphic implementation.
- **Ternaryception.** A ternary is nested inside a ternary that is already nested. One level of
  nesting is fine. Beyond that, replace the expression with named branches, a lookup, or a switch.
- **Shotgun Surgery.** One logical change requires scattered edits. Gather what changes together.
- **Divergent Change.** One module changes for unrelated bodies of knowledge. Split it only when the
  result has stronger cohesion and less total reader load.
- **Speculative Generality.** Unused abstraction, parameters, or hooks anticipate unasked needs.
  Delete or inline them.
- **Message Chains.** Callers must understand a long `a.b().c().d()` chain. Move the required
  knowledge to its owner or expose a direct operation when that reduces coupling.
- **Middle Man.** A module mainly delegates. Apply the deletion test. Remove it when its complexity
  disappears, but keep an interface that hides real decisions or coordination.
- **Refused Bequest.** A subtype ignores inherited behaviour or violates the base type's
  expectations. Prefer composition when inheritance does not describe a valid substitution.
- **Unnecessary Complexity.** The change adds concepts, state, branches, layers, dependencies, or
  execution paths that its behaviour and constraints do not require. Name the concrete maintenance
  or correctness cost and the smallest coherent alternative. Do not flag essential domain complexity
  or mere line count.

## 2. Run independent reviews

Spawn the applicable agents in parallel. Do not let them edit files.

### Standards agent

Provide the scope command, commit list when applicable, complete untracked file contents, every
standards-source path, the triggered engineering references, and the full baseline above.
Ask:

> Report by file and hunk:
> 1. Every documented-standard violation, citing the rule and its source.
> 2. Every baseline smell, naming it and quoting the hunk.
> 3. Every named test smell from the Testing reference when the scope contains tests.
> Separate hard documented breaches from
> baseline judgement calls. Repository rules override the baseline. Skip tooling-enforced issues.
> Stay under 400 words.

### Spec agent

Provide the same scope information and the spec path or contents. Ask:

> Report missing or partial requirements, unrequested behaviour or scope creep, and apparently
> implemented requirements whose implementation looks wrong. Quote the relevant spec
> line for every finding. Stay under 400 words.

## 3. Report

Present the reports, verbatim or lightly cleaned, under `## Standards` and `## Spec`. Do not merge
or rerank them. End with one line giving each axis's finding count and worst issue, if any.
