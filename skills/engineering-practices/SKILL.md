---
name: engineering-practices
description: "Baseline engineering rules for code, tests, dependencies, package management, and developer tooling. Apply whenever reading, writing, reviewing, or changing them. Fix problems at their source and route design, execution, operations, and verification guidance from this skill."
---

# Engineering practices

Apply these rules as the baseline for engineering work. When a narrower skill also applies, use both. The narrower skill may strengthen or refine these rules within its scope, but must not weaken them.

## Fight for simplicity

Complexity inhibits understanding and robustness. Simplicity makes change easier. Actively seek the simplest complete design throughout design, implementation, and review.

- Minimise the total number of concepts, states, branches, layers, dependencies, execution paths, and sources of truth required by the behaviour and its constraints.
- Judge simplicity across the affected system, not by local line count. Moving complexity into callers or hiding it behind an abstraction is not simplification.
- At each meaningful step, ask what can be deleted, combined, derived, moved to its source, or made unnecessary before proceeding.
- Reconsider the design when implementation requires repeated coordination, special cases, defensive checks, or signals threaded through several layers.
- Include small, adjacent simplifications when they make the result coherent, remove compensating complexity, or prevent a decision from remaining scattered. Report unrelated opportunities instead. Pause when simplification would significantly change the intended result, a public or external interface, dependencies, risk, or the size of the work.

## Keep moving and fix at source

- Continue safe, reversible work covered by the requested outcome. Infer ordinary implementation details from the request, repository conventions, and current evidence.
- Scope follows the root cause, not the initially expected file list. Prefer a small source fix and the necessary consumer, test, or type updates over local exceptions, fallback paths, or compensating complexity.
- Search for the same defect elsewhere. Fix minor, clearly equivalent instances when leaving them would preserve inconsistent behaviour.
- Pause when the correct fix significantly changes the intended result, a public or external contract, data, dependencies, infrastructure, product risk, or the size of the work. Explain why the broader source fix is preferable to a local workaround.
- Preserve unrelated work. Do not publish, message, commit, push, delete data, or affect external systems unless the user authorised that action.

## Safety

- Never run or implement recursive deletion without explicit user consent.

## Design and types

- Prefer simple, strictly typed code that makes invalid states unrepresentable.
- Validate untrusted or untyped data at system seams, then trust established typed invariants. Never use `any`.
- Do not add speculative guards, fallbacks, or compatibility paths. Implement only behaviour required by the current system or request.

## Tests

- Write durable tests that protect observable behaviour or reproduce a regression.
- Do not add tests that merely prove an edit, an implementation detail, or a static type guarantee.

## Repository conventions

- Prefer pnpm for JavaScript and TypeScript package management.
- Prefer named exports. Use barrels for types only.

## Dependencies

- Add a dependency only when its maintenance, security, licence, transitive dependency, and runtime costs are justified.

## Read the relevant reference

Read each reference when its trigger first appears, including when the task changes phase later in a long thread.

- For an unexpected problem, a tempting guard or workaround, or a reported bug, read [Root-cause fixes](references/root-causes.md). For a hard bug or performance regression, also apply `$diagnosing-bugs`; it owns the diagnostic loop, while the reference owns fix placement.
- Before substantial type, state, data-structure, module, interface, or refactor decisions, or when a new requirement does not fit the current design, read [Design and maintainability](references/design.md).
- For a sweep, migration, internal interface transition, or other multi-step change, read [Execution and migration](references/execution.md).
- For commands, lifecycle work, retries, restarts, scheduling, or concurrent writers, read [Reliable operations](references/operations.md).
- Before declaring any engineering change complete, read [Verification and learning](references/verification.md).
