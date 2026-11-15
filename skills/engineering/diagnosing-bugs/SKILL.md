---
name: diagnosing-bugs
description: Use when a bug's cause isn't clear from the code, a first fix didn't work, a failure is intermittent, or performance has regressed.
---

# Diagnosing bugs

A diagnosis-only, debugging-only, or explanation request authorises no fix and no lasting repository change. Work from existing commands, runtime inspection, and throwaway files in the operating system's temporary directory, and get authority before adding repository instrumentation or touching production. A request that includes a fix carries through the fix and its verification. Redact secrets in commands, output, and captures.

## Investigate

- Reproduce the user's exact symptom, not a nearby failure or a run that merely doesn't crash, with a focused existing check where you can, otherwise the cheapest loop that drives the real bug path. Capture the error, wrong output, or timing so verification can show the fix addresses it. When a person must act, guide them with the [human-assisted loop template](scripts/hitl-loop.template.sh).
- For an intermittent failure, record the conditions, attempt count, and failure rate, and stop adding attempts when more are unlikely to distinguish causes.
- Minimise a failing reproduction one cut at a time, rerunning after each, until further cuts won't change the diagnosis. Keep the original scenario for final verification.
- When reproduction isn't practical, state the missing access, inputs, or setup cost and continue from source, traces, configuration, and history. Ask only for evidence that would change the diagnosis. Never report an unexecuted reproduction or an inferred fix as verified.
- Rank the plausible causes, each with a prediction an available observation could test, and share the ranking as a non-blocking update so the user can correct assumptions.
- Give diagnostic logs you add a unique prefix such as `[DEBUG-a4f2]`, and remove them before finishing.
- When something fails after a restart, inspect persistent state first, such as configuration files, caches, lock files, and serialised state.
- For a performance regression, measure the workload before choosing an optimisation.

## Finish

Stop when the evidence separates the cause from realistic alternatives, or no available observation can reduce the uncertainty. Report the cause or ranked causes, confidence, distinguishing evidence, affected scope, and smallest coherent fix under the "engineering" skill's source-fix rules, with the relevant redacted output or the remaining verification gap.

For diagnosis-only work, remove your diagnostics and temporary artefacts and stop before fixing. When a fix is authorised, read [Fix and verify](references/fix-and-verify.md) and continue without asking again.
