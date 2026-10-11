---
name: diagnosing-bugs
description: Diagnose hard bugs and performance regressions from symptoms, reproduction, and evidence.
---

# Diagnosing bugs

Choose the next investigation from the evidence. Use "engineering" and apply its source-fix rules when choosing a fix. Read relevant repository guidance and ADRs when they can explain the affected path.

## Authority and sensitive data

A diagnosis-only, debugging-only, or explanation request does not authorise a fix or persistent repository changes. Use existing commands, runtime inspection, or temporary files outside the repository. Temporary repository instrumentation or changes to production need authority covering those actions. A request that includes a fix authorises continuing through the fix and verification within its scope.

Redact secrets before showing commands, output, or captures. Keep credentials in environment variables and quote only diagnostic evidence. If safe redacted evidence cannot distinguish the cause, name the missing observation and request only what is needed.

An ordinary production bug stays in this workflow. For a possible active outage, major unusable production feature, or urgent recovery request, suggest the explicitly invoked "diagnosing-production-incidents" workflow without blocking current investigation. If the user invokes it, let that skill own diagnosis rather than running both processes.

## Establish the evidence

Identify the reported symptom, expected behaviour, affected path, and available observations. Prefer a focused existing check that reproduces the actual symptom. Code inspection alone cannot verify a runtime fix.

When constructing or improving a reproduction, investigating intermittent behaviour, or minimising a scenario will help distinguish causes, read [Reproduction techniques](references/reproduction.md). Keep the original scenario for final verification. Choose the cheapest reliable signal that exercises the relevant path; do not require an elaborate reproduction for a straightforward diagnosis.

If reproduction is unavailable or disproportionate, state the missing access, inputs, or setup cost and continue from source, captured traces, configuration, history, and relevant documentation. Rank provisional explanations and name the observation that would distinguish them. Continue independent investigation while waiting for necessary evidence. Never claim an unexecuted reproduction or inferred fix was verified.

## Distinguish causes

While uncertainty remains, rank plausible explanations and realistic alternatives. Each hypothesis needs a prediction that an available observation could support or weaken. Do not fill a quota or delay a decisive check to complete a phase.

Share a useful hypothesis ranking as a non-blocking update so the user can correct assumptions. Choose the next probe for its ability to distinguish causes. Change one variable at a time when testing a causal prediction.

Prefer debugger or REPL inspection, then targeted logs where needed. For diagnosis-only work, add logs only through existing runtime controls or authorised instrumentation. Give agent-added diagnostic logs a unique prefix such as `[DEBUG-a4f2]` and remove them before completion. Avoid indiscriminate captures.

When something fails after a restart, inspect persistent state first, such as configuration files, caches, lock files, and serialised state. If clearing state restores behaviour, fix state validation or reconciliation.

For performance regressions, measure the relevant workload with timing, profiling, or a query plan before choosing an optimisation. Record variance and limits of intermittent evidence.

## Complete the requested outcome

Stop investigating when evidence distinguishes the cause from realistic alternatives or no available observation can reduce uncertainty. Report the cause or ranked probable causes, confidence, distinguishing evidence, affected scope, and smallest coherent fix. Include the command and relevant redacted output, or the evidence fallback and remaining verification gap.

For diagnosis-only work, remove agent-created diagnostics and temporary artefacts with targeted operations, preserve the original working tree, state what changed, and stop before fixing.

When a fix is already authorised, read [Fix and verify](references/fix-and-verify.md) and continue through the practical regression check, source fix, verification, and cleanup. Do not require renewed approval solely because diagnosis ended.
