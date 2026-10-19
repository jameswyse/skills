---
name: engineering
description: Implement, debug, design, or review software and tooling. Skip simple code explanations, lookups, and routine Git operations.
---

# Engineering

Use this baseline for implementation and engineering judgement. Repository conventions and the user's task govern the work. For interface implementation, also use "ux". The "code-review" skill holds the detailed code and test standards used to judge a finished change.

## Keep these rules in scope

- Follow the governing authority rules and preserve unrelated work. Resolve routine choices from evidence and continue within the user's request.
- Prefer the simplest complete design across the affected system. Avoid speculative guards, fallbacks, layers, and compatibility paths.
- Use strict types that express valid states. Validate untrusted inputs at their entry point, then trust established invariants. Never use `any`.
- Enforce authorisation at the protected operation. Keep secrets and sensitive data out of source, client output, logs, and fixtures.
- Add a dependency only when the required behaviour justifies its maintenance, security, licence, and runtime costs and no established repository tool already covers it.
- Never add code comments. Carry intent in names, types, tests, and validating functions, and put a reason the code cannot show in the commit message. Tool directives such as `oxlint-disable-next-line`, `@ts-expect-error`, and `#__PURE__` are not comments for this rule; give a suppression its reason after `--`. In JavaScript files, JSDoc that declares types, such as `@param {string}` or `@typedef`, is a type annotation and stays. Existing comments may be agent-written, so check those in code you change against the code and remove wrong ones rather than treating them as requirements.
- Add a test only for observable behaviour, through a caller's interface, with an independent expected result and a plausible defect it catches. Existing coverage may be sufficient.
- Before creating a file, directory, type, adapter, or helper, search for an existing owner. Choose a path that predicts the new responsibility.
- Prefer pnpm when unspecified, named exports, and direct imports from the owning module.
- Use reversible deletion such as `trash` when available. Double check the path is correct (especially when variable expansion occurs) before running any `rm` command.

For TypeScript implementation or review, use "typescript". For substantial architecture, state, schema, module-boundary, or test-seam decisions, read [Design](references/design.md) before choosing. A small local edit does not need it.

## Run the repository's toolchain

Before the first JavaScript or TypeScript command in a task, compare the active runtime and package manager with the repository's declarations. Treat exact pins as exact and ranges as constraints. On a mismatch, select a compatible toolchain once through repository setup or a version manager, before starting parallel checks. If the declared toolchain is unavailable, report the affected checks as not verified. Output from a different runtime is diagnostic evidence, not verification.

## Fix at the source

Let the requested outcome define the scope. When a source fix needs adjacent consumer, test, type, configuration, or fixture changes, make them instead of a local workaround that keeps the diff narrow. Pause only when the fix exceeds your authority or opens a decision about public interfaces, data, dependencies, infrastructure, or product behaviour. Then explain the root cause and why a narrower workaround would leave it unresolved.

- Do not add a guard that only silences a crash. Validate and repair where invalid state enters, and correct the authoritative type, structure, or configuration instead of adding downstream exceptions.
- Search for the same pattern. Fix equivalent minor instances now and report those that need a larger change.
- If a workaround needs a paragraph of explanation, fix the code instead.
- When stuck, instrument and read the actual error and state. Use "diagnosing-bugs" for hard bugs and performance regressions.

## Delegate bounded work

Delegate only work inside the user's task, when an independent investigation, distinct design, or substantial review area benefits from separate judgement and the runtime permits it. Keep small, coherent changes local. The "code-review" skill decides when its own review delegates. Give each worker the objective, bounded scope, completion evidence, relevant paths, authority limits, and an isolated write target. Use a fresh context when independent judgement matters, and omit your expected verdict. A worker's summary reports intent, not proof, so inspect its artefacts before accepting its findings.

## Finish with evidence

Prove the changed behaviour on the real artefact. Run the changed path and read its actual output or value. A build, cached copy, or self-report is not proof. Before final checks, remove concepts, state, branches, and parallel paths the finished design no longer needs. Run required repository checks and inspect the diff. Repeat checks only after a relevant change, failure, or stale result. State any path you could not exercise and why.

Follow repository review requirements and the global instructions' rule for "code-review" before reporting completion. Fix actionable findings, as "code-review" defines them, within the authorised change, rerun the checks they affect, and report the rest.
