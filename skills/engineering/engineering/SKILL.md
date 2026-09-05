---
name: engineering
description: "Baseline software engineering rules for code, tests, dependencies, package management, developer tooling, architecture, APIs, schemas, modules, and data models. Apply when reading, changing, or assessing those subjects. Skip the engineering skill for routine Git operations that only inspect or change repository state, even when the affected files contain code. Route design, execution, operations, and verification guidance from this skill. For user-facing interface decisions, also apply the ux skill."
---

# Engineering

Apply these rules as the baseline for software engineering. When a narrower skill also applies, use both. The narrower skill may strengthen or refine these rules within its scope, but must not weaken them.

- This skill owns implementation quality, architecture, data, types, tests, dependencies, and tooling.
- For user-facing interface implementation that isn't well defined, use the "ux" skill. It owns experience, interaction, visual presentation, accessibility, interface copy, and motion decisions.
- When explaining code or code changes, or answering questions about code, also use the "show-me" skill. It owns the smallest useful diagram or code-shape sketch.

## Test work requires the testing reference

Before planning, proposing, writing, changing, or reviewing any test, read [Testing](references/testing.md). Read it before making test decisions, even when tests are a small part of the task or appear only after implementation has started.

Do not add a test merely because production code changed or because adding a test feels expected. A new test needs all of these:

- An observable runtime behaviour or invariant that it protects.
- The caller or user seam where that behaviour can be observed.
- An independent source for the expected result.
- A plausible defect in runtime behaviour that the test would catch.

If any item is missing, improve the test design or do not add the test. File-content checks, source-shape assertions, export-presence checks, mock choreography, snapshots accepted only because they are current, and guarantees already enforced by types or static analysis do not satisfy this gate.

## Fight for simplicity

Complexity inhibits understanding and robustness. Simplicity makes change easier. Actively seek the simplest complete design throughout design, implementation, and review.

- Minimise the total number of concepts, states, branches, layers, dependencies, execution paths, and sources of truth required by the behaviour and its constraints.
- Judge simplicity across the affected system, not by local line count. Moving complexity into callers or hiding it behind an abstraction is not simplification.
- Treat the repository tree and filenames as part of each module's interface. A reader should be able to predict where a capability lives and what a file contains without following forwarding layers.
- Before changing a module, inspect its surrounding tree and naming patterns. After changing it, confirm that every affected path still has a clear owner, name, and purpose.
- At each meaningful step, ask what can be deleted, combined, derived, moved to its source, or made unnecessary before proceeding.
- Reconsider the design when implementation requires repeated coordination, special cases, defensive checks, or signals threaded through several layers.
- Include small, adjacent simplifications when they make the result coherent, remove compensating complexity, or prevent a decision from remaining scattered. Report unrelated opportunities instead. Pause when simplification would significantly change the intended result, a public or external interface, dependencies, risk, or the size of the work.

## Keep moving and fix at source

- Carry forward authorisation already given for the current task. A narrower workflow cannot require renewed approval for an action the user already authorised. Review-only requests remain review-only; a request to review and implement includes both phases within its stated scope.
- Resolve routine choices from repository evidence. Ask only for missing decisions that change the intended outcome or exceed the existing authority. Continue independent authorised work while waiting, and prepare a concrete, reviewable result before requesting approval for the remaining action.
- When a skill causes a pause or leaves requested work unfinished, cite its exact file and instruction. Explain whether the pause follows an explicit requirement or your interpretation, and check the user's existing authorisation before asking again.
- Continue safe, reversible work covered by the requested outcome. Infer ordinary implementation details from the request, repository conventions, and current evidence.
- Scope follows the root cause, not the initially expected file list. Prefer a small source fix and the necessary consumer, test, or type updates over local exceptions, fallback paths, or compensating complexity.
- Search for the same defect elsewhere. Fix minor, clearly equivalent instances when leaving them would preserve inconsistent behaviour.
- Pause when the correct fix significantly changes the intended result, a public or external interface, data, dependencies, infrastructure, product risk, or the size of the work. Explain why the broader source fix is preferable to a local workaround.
- Preserve unrelated work. Do not publish, message, commit, push, delete data, or affect external systems unless the user authorised that action.

## Safety

- Never run or implement recursive deletion without explicit user consent.
- Use `trash` or equivalent for data deletion. Do not delete data without a clear, explicit, and reversible user action.

## Security

- For security-sensitive changes, identify the protected assets, attacker-controlled inputs, trust boundaries, and credible misuse paths before choosing the design.
- Treat authentication and authorisation as separate decisions. Enforce authorisation at the server-side operation or data boundary that owns the protected action.
- Keep secrets and sensitive data out of source code, client bundles, logs, errors, traces, metrics, snapshots, and fixtures. Give credentials and permissions only the scope they need.
- Test representative allowed and denied paths for sensitive operations, including object or tenant isolation when it applies.

## Design and types

- Prefer simple, strictly typed code that makes invalid states unrepresentable.
- Validate untrusted or untyped data at system seams, then trust established typed invariants. Never use `any`.
- Do not add speculative guards, fallbacks, or compatibility paths. Implement only behaviour required by the current system or request.

## Tests

- Write durable tests that protect observable behaviour or reproduce a regression.
- Do not add tests that merely prove an edit, an implementation detail, or a static type guarantee.
- Prefer no new test over one that cannot pass the test-work gate above.

## Repository conventions

- Prefer pnpm for JavaScript and TypeScript package management.
- Prefer named exports and direct imports from the authoritative module. Keep a re-exporting entrypoint only when it defines a deliberate supported interface.

## Dependencies

- Add a dependency only when its maintenance, security, licence, provenance, transitive dependency, install-time code, and runtime costs are justified.

## Read the relevant reference

Read each reference when its trigger first appears, including when the task changes phase later in a long thread.

- For an unexpected problem, a tempting guard or workaround, or a reported bug, read [Root-cause fixes](references/root-causes.md). For a hard bug or performance regression, also use the "diagnosing-bugs" skill. It owns the diagnostic loop, while the reference owns fix placement.
- Before substantial type, state, data-structure, module, interface, or refactor decisions, or when a new requirement does not fit the current design, read [Design and maintainability](references/design.md).
- Before assessing module depth, compressing an interface, placing a seam, choosing adapters, or deciding where tests should observe behaviour, read [Deep modules](references/deep-modules.md).
- Before adding, moving, renaming, splitting, merging, or reviewing files or directories, read [Codebase organisation and naming](references/organisation-and-naming.md).
- Before designing, changing, or reviewing failure handling, error types, error translation, or diagnostic context, read [Failures and diagnostics](references/errors.md).
- For multi-step work, pending tools or questions, mid-task corrections, delegation, sweeps, or migrations, read [Execution and migration](references/execution.md).
- For commands, lifecycle work, retries, restarts, scheduling, or concurrent writers, read [Reliable operations](references/operations.md).
- Before declaring any engineering change complete, read [Verification, review, and learning](references/verification.md).
