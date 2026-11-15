---
name: engineering
description: Use when implementing, debugging, designing, or reviewing software or tooling, including TDD and test-first bug fixes. Skip simple code explanations, lookups, and routine Git operations.
---

# Engineering

Repository conventions and the user's task govern the work. For interface implementation also use "ux", for TypeScript "typescript", and for hard bugs and performance regressions "debugging". Before a substantial architecture, state, schema, module-boundary, or test-seam decision, read [Design](references/design.md).

## Rules

- Prefer the simplest complete design across the affected system. Avoid speculative guards, fallbacks, layers, and compatibility paths.
- Never use `any`. Validate untrusted input where it enters, then trust the types inside.
- Keep secrets, tokens, and sensitive data out of source, client output, errors, logs, traces, snapshots, and fixtures.
- Add a dependency only when no established repository tool covers the behaviour, and the behaviour justifies its maintenance, security, licence, and install-time costs.
- Before adding a test, apply the test gate in the code-review [Testing](../code-review/references/testing.md) reference. Existing coverage may be enough.
- Before creating a file, type, adapter, or helper, search for an existing owner. Choose a path that predicts the new responsibility.
- Prefer pnpm when unspecified, named exports, and direct imports from the owning module.
- Use `trash` instead of `rm` when available.
- Before the first JavaScript or TypeScript command, compare the active runtime and package manager with the repository's declarations. On a mismatch, switch once through repository setup or a version manager. Output from a different runtime is diagnostic evidence, not verification.

## Fix at the source

Fix the cause where invalid state enters. Correct the authoritative type, structure, or configuration instead of adding a downstream guard that silences the failure, and make the consumer, test, type, configuration, or fixture changes the fix needs instead of a workaround that keeps the diff narrow. Fix minor instances of the same pattern and report larger ones. Pause only when the fix exceeds your authority or opens a decision about public interfaces, data, dependencies, infrastructure, or product behaviour.

## Test-first bug fixes

When the user asks for TDD, or a bug fix has a clear, cheap regression-test path, write the smallest test that would have caught the bug before fixing it. Put it at the closest existing test seam for the broken path, and make it encode the intended behaviour, not the current implementation. Read the code-review [Testing](../code-review/references/testing.md) reference first.

1. Run the test before fixing and confirm it fails for the intended reason. If it passes or fails for another reason, correct the test first.
2. Make the smallest production change that fixes the behaviour, then rerun the test and the adjacent checks.
3. When the fix covers several behaviours, work in vertical slices: one failing test, the code that makes it pass, then the next.

When a failing test would need broad harness setup, brittle mocks, slow end-to-end infrastructure, production-only state, or large fixture churn, say why before fixing and use the closest executable check instead, such as a targeted script or a scripted reproduction. Don't build test infrastructure for a small fix. Report the failing-before check and the failure it produced, the passing-after run, and any check you used instead of a test and why.

## Delegate

Keep small, coherent changes local. Delegate only independent investigations, distinct designs, or substantial review areas inside the task, except that "code-review" decides how its own review delegates. Give each worker the objective, scope, relevant paths, authority limits, an isolated write target, and the evidence it must return, and leave out your expected verdict. Inspect a worker's artefacts before accepting its summary.

## Finish with evidence

Prove the changed behaviour on the real artefact: run the changed path and read its actual output. A build, a cached copy, or a self-report isn't proof. Remove state, branches, and paths the finished design no longer needs, run the repository's required checks, and inspect the diff. State any path you couldn't exercise and why.

Then follow the repository's review requirements and run "code-review" as the global rule requires. Fix the actionable findings within the authorised change, rerun the checks they affect, and report the rest.
