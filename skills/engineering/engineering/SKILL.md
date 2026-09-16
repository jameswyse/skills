---
name: engineering
description: "Implement, debug, design, or assess software and developer tooling. Load for code changes and engineering reviews. Skip straightforward code explanations, read-only lookups, and routine Git operations."
---

# Engineering

Use this baseline for implementation and engineering judgement. Repository conventions and the user's task govern the work. For interface implementation, also use "ux".

## Keep these rules in scope

- Follow the governing authority rules and preserve unrelated work. Resolve routine choices from evidence and continue within the user's request.
- Fix the source problem and update necessary consumers. Prefer the simplest complete design across the affected system. Avoid speculative guards, fallbacks, layers, and compatibility paths.
- Use strict types that express valid states. Validate untrusted inputs at their entry point, then trust established invariants. Never use `any`.
- Enforce authorisation at the protected operation. Keep secrets and sensitive data out of source, client output, logs, and fixtures.
- Add a test only for observable behaviour, through a caller's interface, with an independent expected result and a plausible defect it catches. Existing coverage may be sufficient.
- Match repository runtime and package-manager declarations before commands. Prefer pnpm when unspecified, named exports, and direct imports from the owning module.
- Use reversible deletion such as `trash` only within explicit authority. Never recursively delete without explicit consent.

## Load guidance at the decision

Read the matching reference before making the relevant decision. Use the needed sections and retain already-read guidance. A routine command, conventional companion file, or small local edit does not require the full reference set.

- Unclear fix placement or repeated workarounds: [Root-cause fixes](references/root-causes.md). Use "diagnosing-bugs" for hard bugs and performance regressions.
- Substantial architecture, state, schema, or type decisions: [Design and maintainability](references/design.md). Also read its security or dependency section before changing a security boundary or selecting a dependency.
- Module ownership, interface compression, or a new test seam: [Deep modules](references/deep-modules.md).
- Substantial moves, splits, renames, or uncertain file ownership: [Organisation and naming](references/organisation-and-naming.md).
- New error representations, recovery, or translation across boundaries: [Failures and diagnostics](references/errors.md).
- Designing test cases, choosing an oracle or test double, or assessing a suite: [Testing](references/testing.md). Running existing checks alone does not trigger it.
- Coordinated migrations, delegation, pending jobs, or corrections affecting ongoing work: [Execution and migration](references/execution.md).
- Lifecycle behaviour, retries, scheduling, or concurrent state: [Reliable operations](references/operations.md). For a toolchain mismatch, read only its toolchain section first.

## Finish with evidence

Run required repository checks and observe the changed behaviour. Inspect the diff. Stop when that evidence is sufficient; repeat checks only after relevant changes, failures, stale results, or unresolved uncertainty. State unverified paths honestly.

For substantial changes, security boundaries, public interfaces, stored data, dependency migrations, consequential tooling, or unresolved verification, read [Verification, review, and learning](references/verification.md) and use "code-review" when its review criteria apply. Small, well-covered local changes may finish with direct diff inspection. Detailed standards remain available during review even when implementation did not need them.
