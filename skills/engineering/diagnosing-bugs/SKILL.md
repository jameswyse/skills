---
name: diagnosing-bugs
description: Diagnose hard bugs and performance regressions from symptoms, reproduction, and evidence.
---

# Diagnosing bugs

Use "engineering" and its source-fix rules when choosing a fix.

## Authority

A diagnosis-only, debugging-only, or explanation request doesn't authorise a fix or persistent repository changes. Use existing commands, runtime inspection, or temporary files outside the repository, and get authority before adding repository instrumentation or touching production. A request that includes a fix authorises continuing through the fix and verification.

Redact secrets before showing commands, output, or captures. For a possible active outage or an urgent recovery request, suggest the explicitly invoked "diagnosing-production-incidents" workflow without blocking the investigation.

## Investigate

- Reproduce the actual symptom with a focused existing check where you can. Code inspection alone can't verify a runtime fix. To build or minimise a reproduction, or for intermittent behaviour, read [Reproduction techniques](references/reproduction.md).
- When reproduction isn't practical, state the missing access, inputs, or setup cost and continue from source, traces, configuration, and history. Never claim an unexecuted reproduction or an inferred fix was verified.
- Rank plausible causes, each with a prediction an available observation could test, and share the ranking as a non-blocking update so the user can correct assumptions.
- Give agent-added diagnostic logs a unique prefix such as `[DEBUG-a4f2]`, and remove them before completion.
- When something fails after a restart, inspect persistent state first, such as configuration files, caches, lock files, and serialised state.
- For a performance regression, measure the workload before choosing an optimisation.

## Finish

Stop when the evidence separates the cause from realistic alternatives, or no available observation can reduce the uncertainty. Report the cause or ranked causes, confidence, distinguishing evidence, affected scope, and smallest coherent fix, with the relevant redacted output or the remaining verification gap.

For diagnosis-only work, remove agent-created diagnostics and temporary artefacts and stop before fixing. When a fix is authorised, read [Fix and verify](references/fix-and-verify.md) and continue without asking again.
