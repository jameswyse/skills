---
name: code-review
description: Review a branch, PR, working-tree diff, or changes since a fixed point against standards and the request.
---

# Two-axis code review

Review two axes separately. **Standards** covers repository rules and code smells. **Spec** covers
the originating request, issue, or PRD. A change can pass either axis and fail the other. Do not
merge or rerank their findings.

Use the "engineering" skill as the baseline for code, tests, dependencies, package
management, and developer tooling. This skill owns the detailed standards. Choose them from the
reviewed behaviour. The author does not need to have read them for the result to meet them:

- For code, read the sections of [Code standards](references/code-standards.md) that the diff
  touches: simplicity and reader load, domain modelling, types, seams, failures, reliable
  operations, migrations, security and dependencies, and named smells. For ownership, interface
  compression, or seam placement, also read the engineering [Design](../engineering/references/design.md)
  reference.
- When the scope contains tests, read [Testing](references/testing.md) and use its named test smells.
- When the scope adds, moves, renames, splits, merges, or deletes files or directories, read
  [Codebase organisation and naming](references/organisation-and-naming.md). Apply it to the
  affected subtree, authoritative imports, naming patterns, and companion-file ownership.

Do not load every section for a small diff.

Treat security as part of Standards when the diff changes a trust boundary, authentication,
authorisation, sensitive data, secret handling, permissions, security configuration, or the
dependency graph. Keep this check scoped to the diff and the context needed to verify it. Recommend
the user-invoked "improve-security" skill only when the user requests a dedicated security review.

## 1. Fix the scope

- When the user supplies a fixed point, verify it with `git rev-parse`, capture
  `git diff <ref>...HEAD` once, and note `git log <ref>..HEAD --oneline`. If the working tree is
  dirty, also capture `git diff HEAD` and the complete contents of untracked files from
  `git status --short`. Review the committed and working-tree diffs as one scope without
  double-counting overlapping findings.
- When no fixed point exists and the working tree is dirty, use `git diff HEAD` plus the complete
  contents of untracked files from `git status --short`.
- When no fixed point exists and the working tree is clean, resolve the comparison branch from
  current PR metadata when available. Otherwise use the remote default branch from
  `refs/remotes/*/HEAD` when exactly one is available. Verify the resolved ref, then capture
  `git diff <base>...HEAD` and
  `git log <base>..HEAD --oneline` once. If no unambiguous base exists, ask for a fixed point.
- For a bad ref or ambiguous base, stop and ask for a valid scope. For a verified empty diff, report
  that there are no changes to review and stop.

For working-tree reviews, the user request is the spec. Otherwise find it in order from issue
references in commit messages, a user-supplied path, then a matching Markdown file under `docs/` or
`specs/`. If none exists, skip the Spec agent and report "no spec available".

Standards sources are repository files that define how code is written, the engineering skill,
and the triggered standards references above. Repository rules override the baseline. Treat named
smells as leads and report only a concrete cost in the scoped diff.

## 2. Choose review execution

This workflow requests bounded, read-only delegation when independent review adds useful confidence and the user and runtime permit it. Delegate the applicable axes for substantial, uncertain, or consequential changes. For a small diff whose scope and checks are clear, inspect the Standards and Spec axes sequentially in the primary agent. Also use the sequential path when delegation is unavailable or restricted. Preserve both axes and the same evidence threshold in either mode; state which mode was used.

For the sequential path, use the captured scope from step 1 and the axis prompts below directly. Keep findings separate, then perform step 3. No review packet or subagent is required. References to agent reports in step 3 mean your candidate notes in this mode.

For a delegated review, read [Delegated review](references/delegated-review.md) before preparing the packet. Use the axis prompts below in either mode.

### Standards agent

When the scope affects React code, read the React Doctor section of [Code standards](references/code-standards.md) for tool use, diagnostic evidence, and configuration candidates.

Ask:

> Report by file and hunk:
> 1. Every documented-standard violation, citing the rule and its source.
> 2. Every named smell from the Code standards reference, naming it and quoting the hunk.
> 3. Every named test smell from the Testing reference when the scope contains tests.
> Separate hard documented breaches from baseline judgement calls. Repository rules override the
> baseline. Skip other tooling-enforced issues.
> Prioritise by severity. Return all supported findings concisely. If the tool output limit would
> truncate the report, return the first batch and state how many supported findings remain.

### Spec agent

Ask:

> Report missing or partial requirements, unrequested behaviour or scope creep, and apparently
> implemented requirements whose implementation looks wrong. Quote the relevant spec
> line for every finding. Return all supported findings concisely. If the tool output limit would
> truncate the report, return the first batch and state how many supported findings remain.

## 3. Verify and report

Treat both reports as leads, not proof. Request any remaining batches, then verify every candidate
finding yourself:

1. Re-open the cited hunk and its surrounding context.
2. Read the cited rule or spec line from its source.
3. Confirm the concrete correctness, maintenance, or requirement impact.
4. Reject findings that are unsupported, duplicated, outside the fixed scope, or already handled.

Make one final pass over the complete scope for high-risk correctness or security issues the agents
missed. Present only verified findings, in your own words, under `## Standards` and `## Spec`. Merge
duplicates within an axis, but do not merge or rerank findings across the two axes.

End with one line giving each axis's verified finding count and worst issue, if any.
