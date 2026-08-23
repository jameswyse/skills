---
name: improve-codebase-standards
description: Review an entire codebase against its repository rules and $engineering, then present evidence-backed improvements in a visual HTML report. Use recent changes or a specific repository area only when the user explicitly requests that scope.
---

# Improve codebase standards

Find concrete opportunities to improve an existing codebase's correctness, simplicity, maintainability, testability, tooling, and operations. Present the evidence before changing code.

Apply `$engineering` as the baseline. Repository instructions and established conventions take precedence. Read each engineering reference when its trigger appears. Apply `$ux` when a candidate concerns the user-facing experience.

Keep this review distinct from narrower workflows:

- Use `$code-review` when the task is to approve or find defects in a specific change. Keep an explicitly requested recent-history standards scan in this workflow.
- Use `$diagnosing-bugs` for a known failure or performance regression.
- Recommend `$upgrade-deps` for a comprehensive dependency refresh.
- Use `$improve-codebase-security` for a dedicated security review. Report a concrete security flaw discovered here, but do not expand this workflow into a general security audit.
- Recommend `$improve-codebase-architecture` when the primary improvement requires deeper modules, a different seam, or a substantial interface redesign. Do not include that work in the standards ranking.

## Process

### 1. Establish the scope

Review the entire codebase by default. Inventory the repository's projects, packages, entrypoints, domain areas, tests, configuration, scripts, and operational code. Inspect every major area at a useful level before ranking candidates. State any area that the review could not inspect as a coverage gap.

Use a narrower scope only when the user explicitly requests one:

- If the user asks to review recent changes or commits, inspect the requested history and the affected paths.
- If the user names a repository area, module, subsystem, or problem, inspect that area and the callers or dependencies needed to judge it.

Do not use Git history, the current issue, or the working tree to narrow an unqualified invocation. Inspect the working tree only to preserve unrelated work and describe the reviewed state.

Read the project's instructions and documentation before exploring the code. Identify the repository's verification commands and the tools that already enforce its standards. Use repository-provided inspection or verification commands when they do not require source or configuration changes.

### 2. Find candidates

Use the engineering rules as search directions, not quotas. Follow evidence across the repository:

- Find unnecessary concepts, state, branches, layers, dependencies, execution paths, and sources of truth.
- Trace repeated workarounds, defensive checks, and special cases to their source.
- Look for domain rules weakened by loose types, duplicated models, or validation in the wrong place.
- Check whether important behaviour can be verified through observable outcomes.
- Inspect failure context, error translation, commands, lifecycle handling, retries, scheduling, and concurrent writes where those concerns exist.
- Review dependency and tooling choices only when the repository shows a concrete maintenance, security, licence, or runtime cost.

When delegation is available and authorised, divide exploration by repository area. Treat delegated findings as leads. Reopen the cited code, rule, callers, and tests before including a candidate.

### 3. Validate and rank

Include a candidate only when the repository provides evidence of a correctness, maintenance, verification, or operational cost. For each candidate:

1. Reopen the affected files and symbols in context.
2. Identify the repository rule or engineering guidance that applies.
3. Confirm the current cost through callers, tests, configuration, logs, or repeated implementation.
4. Describe the smallest coherent improvement that fixes the source problem.
5. Name the focused check and the observable behaviour that would verify the change.

Do not repeat formatter, linter, compiler, or test output as a recommendation. Use that output as evidence for a source problem. Exclude generic best-practice advice, speculative abstractions, unverified dependency claims, and tests that would protect only implementation details.

Rank candidates as `Strong`, `Worth exploring`, or `Speculative`. Prefer high-confidence improvements with a clear verification path. Do not pad the report. A review may conclude that the codebase has no worthwhile standards improvements.

### 4. Present the HTML report

Write one HTML file to the operating system's temporary directory so nothing enters the repository. Resolve the directory from `$TMPDIR`, falling back to `/tmp` on Unix or `%TEMP%` on Windows. Write to `<tmpdir>/standards-review-<timestamp>.html` so each run gets a fresh file. Open it with `xdg-open <path>` on Linux, `open <path>` on macOS, or `start <path>` on Windows. Tell the user the absolute path.

The report is single-file, not offline. Use Tailwind via CDN for layout and styling. Use Mermaid via CDN when a graph, flow, or sequence clarifies a finding. If the environment has no network access, use inline CSS and SVG instead.

Show the reviewed revision, working-tree state, requested scope, coverage, and coverage gaps. For each candidate, include:

- **Files and symbols.** Name the inspected code.
- **Standard.** Cite the repository rule or engineering guidance.
- **Evidence.** Show the current cost or risk.
- **Improvement.** Describe the source fix in plain English.
- **Benefit.** Name the concrete reduction in complexity, risk, or verification effort.
- **Effort and risk.** Use relative labels without invented precision.
- **Verification.** Name the checks and observable behaviour.
- **Recommendation strength.** Render `Strong`, `Worth exploring`, or `Speculative` as a badge.

Use a visual only when it makes the evidence or proposed change easier to understand. See [HTML-REPORT.md](HTML-REPORT.md) for the report scaffold and visual patterns.

End with a top recommendation. Put architectural observations in a separate follow-up section that suggests `$improve-codebase-architecture` without ranking them against standards candidates.

After writing the report, ask the user, "Which of these would you like to improve?"

### 5. Continue after selection

Treat the report as a snapshot. Revalidate the selected candidate against the current working tree before designing or implementing a change.

Selection does not authorise file changes. Make changes only when the user asks for implementation. Within that authority, apply `$engineering`, make the smallest coherent source fix, and verify the real behaviour before reporting completion.
