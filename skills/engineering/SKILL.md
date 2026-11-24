---
name: engineering
description: Use when implementing, debugging, designing, or reviewing software or tooling, including TDD and test-first bug fixes. Skip simple code explanations, lookups, and routine Git operations.
---

# Engineering

Repository conventions and the user's task govern the work. Load "ux" before the first interface decision, including while planning. Load "typescript" before writing or reviewing TypeScript. Load "debugging" when a bug's cause isn't clear from the code, a first fix didn't work, a failure is intermittent, or performance has regressed. Read [Design](references/design.md) before planning a substantial change to architecture, state, a schema or stored data shape, a module or interface boundary, or a test seam, and whenever a new requirement challenges the current design. Sending it to a reviewer afterwards doesn't count.

## Rules

- Prefer the simplest complete design across the affected system. Avoid speculative guards, fallbacks, layers, and compatibility paths.
- Never use `any`. Validate untrusted input where it enters, then trust the types inside.
- Keep secrets, tokens, and sensitive data out of source, client output, errors, logs, traces, snapshots, and fixtures.
- Add a dependency only when no established repository tool covers the behaviour, and the behaviour justifies its maintenance, security, licence, and install-time costs.
- Before creating a file, type, adapter, or helper, search for an existing owner. Choose a path that predicts the new responsibility.
- Prefer pnpm when unspecified, named exports, and direct imports from the owning module.
- Use `trash` instead of `rm` when available.
- Before the first JavaScript or TypeScript command, compare the active runtime and package manager with the repository's declarations. On a mismatch, switch once through repository setup or a version manager. Output from a different runtime is diagnostic evidence, not verification.

## Fix at the source

Fix the cause where invalid state enters. Correct the authoritative type, structure, or configuration instead of adding a downstream guard that silences the failure, and make the consumer, test, type, configuration, or fixture changes the fix needs instead of a workaround that keeps the diff narrow. Fix minor instances of the same pattern and report larger ones. Pause only when the fix exceeds your authority or opens a decision about public interfaces, data, dependencies, infrastructure, or product behaviour.

## Test gate

Don't add a test because production code changed or coverage feels expected. Existing coverage may be enough. Before adding one, complete this statement with concrete details:

> This test fails when [observable runtime behaviour] breaks at [caller or user seam], and its
> expected result comes from [independent requirement, specification, known result, or maintained fixture].

Also name a plausible defect it would catch. If you can't, improve the design or don't add the test. A check for file contents, source shape, an export, a mocked helper call, a current snapshot, or a guarantee the type system already enforces doesn't count. Prefer no new test over one with a weak signal.

The one type-level exception is a public type that ordinary callers would keep compiling against if it were weakened, such as a prop widened from `boolean` to `boolean | string`. Protect it with a few negative examples in one strict compile, and assert only that each example fails to compile, never the diagnostic text or position.

Ask before encoding an unresolved choice that would set product policy or narrow supported behaviour.

Before writing a test that passes the gate, read the code-review [Testing](../code-review/references/testing.md) reference for how to design it.

## Test-first bug fixes

When the user asks for TDD, or a bug fix has a clear, cheap regression-test path, write the smallest test that would have caught the bug before fixing it. This includes defects found by review, verification, or a check while the change is in progress. Put the test at the closest existing test seam for the broken path, and make it encode the intended behaviour, not the current implementation.

1. Run the test before fixing and confirm it fails for the intended reason. If it passes or fails for another reason, correct the test first.
2. Make the smallest production change that fixes the behaviour, then rerun the test and the adjacent checks.
3. When the fix covers several behaviours, work in vertical slices: one failing test, the code that makes it pass, then the next.

When a failing test would need broad harness setup, brittle mocks, slow end-to-end infrastructure, production-only state, or large fixture churn, say why before fixing and use the closest executable check instead, such as a targeted script or a scripted reproduction. Don't build test infrastructure for a small fix. Report the failing-before check and the failure it produced, the passing-after run, and any check you used instead of a test and why.

## Delegate

Keep small, coherent changes local. Delegate only independent investigations, distinct designs, or substantial review areas inside the task, except that "code-review" decides how its own review delegates. Give each worker the objective, scope, relevant paths, authority limits, an isolated write target, and the evidence it must return, and leave out your expected verdict. Inspect a worker's artefacts before accepting its summary.

## Finish with evidence

Prove the changed behaviour on the real artefact: run the changed path and read its actual output. A build, a cached copy, or a self-report isn't proof. For an interface change, run the app and look at the changed screen, because passing tests with mocks don't show that the experience works. Remove state, branches, and paths the finished design no longer needs, run the repository's required checks, and inspect the diff. State any path you couldn't exercise and why.

Then follow the repository's review requirements and run "code-review" as the global rule requires. Fix the actionable findings within the authorised change, rerun the checks they affect, and report the rest.

Keep a list of problems you found outside the task, such as pre-existing bugs and "code-review" findings that predate the change, each with its evidence. When the repository's instructions record a Jira project, end your report by asking which of them to file, with your recommendation for each, and file the chosen ones with "jira". A subagent or delegated task returns the list to its parent instead of asking.
