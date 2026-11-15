---
name: improve-standards
description: Audit a codebase or named area against repository and engineering standards.
disable-model-invocation: true
---

# Improve standards

Find concrete opportunities to improve an existing codebase's correctness, simplicity, maintainability, testability, tooling, and operations. Present the evidence before changing code.

Use the "engineering" skill as the baseline. Repository instructions and established conventions take precedence. Read each engineering reference when its trigger appears. Use the "ux" skill when a candidate concerns the user-facing experience.

Keep this review distinct from narrower workflows:

- Use the "code-review" skill when the task is to approve or find defects in a specific change. Keep an explicitly requested recent-history standards scan in this workflow.
- Use the "debugging" skill for a known failure or performance regression.
- Recommend the "upgrade-deps" skill for a comprehensive dependency refresh.
- Recommend the user-invoked "improve-security" skill for a dedicated security review. Report a concrete security flaw discovered here, but do not expand this workflow into a general security audit.
- Recommend the user-invoked "improve-architecture" skill when the primary improvement requires deeper modules, a different seam, or a substantial interface redesign. Do not include that work in the standards ranking.
- Recommend the user-invoked "improve-organisation" skill when the primary improvement requires a repository-wide tree, placement, filename, or companion-file audit. Report a concrete organisation problem discovered here, but do not expand this workflow into that audit.

## Process

### 1. Establish the scope

Review the entire codebase by default. Inventory the repository's projects, packages, entrypoints, domain areas, tests, configuration, scripts, and operational code. Inspect every major area at a useful level before ranking candidates. State any area that the review could not inspect as a coverage gap.

Use a narrower scope only when the user explicitly requests one:

- If the user asks to review recent changes or commits, inspect the requested history and the affected paths.
- If the user names a repository area, module, subsystem, or problem, inspect that area and the callers or dependencies needed to judge it.

Do not use Git history, the current issue, or the working tree to narrow an unqualified invocation. Inspect the working tree only to preserve unrelated work and describe the reviewed state.

Read the project's instructions and documentation before exploring the code. Identify the repository's verification commands and the tools that already enforce its standards. Use repository-provided inspection or verification commands when they do not require source or configuration changes.

Before verification, apply the engineering skill's toolchain check once for the task. Record the active versions and whether they satisfy the repository declarations. Report affected checks as not verified when no compatible toolchain is available.

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

Prefer fresh verification when it is safe and proportionate. Use the repository's uncached verification entrypoint when one exists. For Turborepo, prefer the repository's uncached command or force the relevant tasks instead of relying on cache hits. Run a fresh build for a candidate whose behaviour depends on build output. Cached results can guide exploration, but they do not replace fresh evidence when an uncached check is available. When fresh verification is too costly or unavailable, run the narrowest useful uncached check and state what remains unverified.

### 4. Present the HTML report

Use the "html-report" skill to build and deliver the report. Before writing HTML, read [HTML-REPORT.md](HTML-REPORT.md) in full. It owns the report's sections, finding content, and output location in the temporary directory, so nothing enters the repository.

Lead with the recommended improvement and the ranked findings. Keep follow-ups for "improve-architecture" and "improve-organisation" separate and unranked. End with the toolchain, the checks with their cache state, and the paths not exercised. Omit method narration such as searches performed or files opened.

After a review-only request, ask which candidates the user wants to improve. If the user already authorised implementation, continue with candidates covered by that request and resolve routine priorities from the evidence. Ask only when the selection changes the intended outcome or exceeds that authority.

### 5. Continue after selection

Treat the report as a snapshot. Revalidate the selected candidate against the current working tree before designing or implementing a change.

Selecting an item for further discussion does not authorise file changes. An instruction to implement selected candidates, including one given before the review, does. Apply the governing authority rules, make the smallest coherent source fix, and verify the real behaviour before reporting completion.
