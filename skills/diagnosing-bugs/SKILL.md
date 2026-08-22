---
name: diagnosing-bugs
description: Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose" or "debug this", or reports something broken, throwing, failing, or slow.
---

# Diagnosing bugs

A discipline for hard bugs. Skip phases only when explicitly justified.

Read [Root-cause fixes](../engineering-practices/references/root-causes.md) before choosing a fix. This skill owns the diagnostic loop. The reference owns fix placement, necessary consumer updates, and when a source fix needs approval.

When exploring the codebase, read `CONTEXT.md` (if it exists) to get a clear mental model of the relevant modules, and check ADRs in the area you're touching.

## Redact

This skill requires visible commands, outputs, and captured artefacts. **Redact every secret first.** Write `<REDACTED>` in its place. Build loops against environment variables so credentials stay in the environment rather than in visible output. Captured artefacts can contain authentication headers. Quote only the lines that carry the signal.

If the redacted output is not enough to diagnose the bug, say so and ask the user.

## Phase 1: Build a feedback loop

**This is the skill.** Everything else supports it. If you have a **tight** binary signal that goes red on _this_ bug, you can find the cause. Bisection, hypothesis testing, and instrumentation all consume that signal. Code reading alone cannot replace it.

Spend disproportionate effort here. **Be aggressive. Be creative. Refuse to give up.**

### Ways to construct one, in roughly this order

1. **Failing test** at whichever seam reaches the bug, whether unit, integration, or end to end.
2. **Curl or HTTP script** against a running development server.
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot.
4. **Headless browser script.** Use Playwright or Puppeteer to drive the UI and assert on the DOM, console, and network.
5. **Replay a captured trace.** Save a real network request, payload, or event log to disk. Replay it through the code path in isolation.
6. **Throwaway harness.** Start a minimal subset of the system, such as one service with mocked dependencies, that exercises the bug path with one function call.
7. **Property or fuzz loop.** If the bug sometimes returns the wrong output, run 1000 random inputs and look for the failure mode.
8. **Bisection harness.** If the bug appeared between two known states (commit, dataset, version), automate "boot at state X, check, repeat" so you can `git bisect run` it.
9. **Differential loop.** Run the same input through old and new versions, or through two configurations, and compare the outputs.
10. **Human-in-the-loop script.** Use this as a last resort. If a human must click, guide _them_ with `scripts/hitl-loop.template.sh` so the loop remains structured. Use their captured output as the next input.

Build the right feedback loop before investigating the cause.

### Tighten the loop

Treat the loop as a product. Once you have _a_ loop, **tighten** it:

- Can setup be cached, unrelated initialisation skipped, or the test scope narrowed?
- Can the loop assert the specific symptom instead of merely checking that it did not crash?
- Can it pin time, seed random generation, isolate the filesystem, or freeze the network?

A 30-second flaky loop is barely better than no loop. A 2-second deterministic loop is tight enough for rapid diagnosis.

### Non-deterministic bugs

The goal is not a clean reproduction but a **higher reproduction rate**. Loop the trigger 100 times, parallelise it, add stress, narrow timing windows, or inject delays. A bug that appears in 50% of runs is practical to diagnose. A 1% rate is not, so keep raising the rate until diagnosis is practical.

### When you genuinely cannot build a loop

Stop and say so explicitly. List what you tried. Ask the user for one of the following:

- Access to an environment that reproduces the problem.
- A redacted captured artefact, such as a HAR file, log dump, core dump, or screen recording with timestamps.
- Permission to add temporary production instrumentation.

Do **not** proceed to hypotheses without a loop.

### Completion criterion: a tight loop that goes red

Phase 1 is done when the loop is **tight** and **red-capable**. Name **one command**, such as a script path, test invocation, or curl command, that you have **already run at least once**. Show the invocation and its redacted output. The command must meet these conditions:

- [ ] **Red-capable.** It drives the actual bug path and asserts the **user's exact symptom**, so it can go red on this bug and green once fixed. "Runs without erroring" is insufficient. The command must catch this specific bug.
- [ ] **Deterministic.** It returns the same verdict every run. For flaky bugs, pin a high reproduction rate as described above.
- [ ] **Fast.** It takes seconds, not minutes.
- [ ] **Agent-runnable.** You can run it unattended. A human participates only through `scripts/hitl-loop.template.sh`.

If you catch yourself reading code to build a theory before this command exists, stop. **Jumping straight to a hypothesis is the exact failure this skill prevents.** Do not start Phase 2 without a red-capable command.

## Phase 2: Reproduce and minimise

Run the loop. Watch it go red as the bug appears.

Confirm:

- [ ] The loop produces the failure mode the **user** described, not a different nearby failure. Reproducing the wrong bug leads to the wrong fix.
- [ ] The failure is reproducible across multiple runs (or, for non-deterministic bugs, reproducible at a high enough rate to debug against).
- [ ] You have captured the exact symptom (error message, wrong output, slow timing) so later phases can verify the fix actually addresses it.

### Minimise

Once it is red, shrink the reproduction to the **smallest scenario that still goes red**. Cut inputs, callers, configuration, data, and steps **one at a time**. Run the loop after each cut and keep only what the failure requires.

A minimal reproduction reduces the hypotheses in Phase 3 because fewer moving parts remain. It also becomes the focused regression test in Phase 5.

This phase is done when **every remaining element is necessary**. Removing any one of them makes the loop go green.

Do not proceed until you have reproduced **and** minimised.

## Phase 3: Hypothesise

Generate **3 to 5 ranked hypotheses** before testing any of them. Single-hypothesis generation anchors on the first plausible idea.

Each hypothesis must be **falsifiable**: state the prediction it makes.

> Format: "If <X> is the cause, then <changing Y> will make the bug disappear, or <changing Z> will make it worse."

If you cannot state the prediction, the hypothesis is an unsupported guess. Discard or sharpen it.

**Show the ranked list to the user before testing.** The user may have domain knowledge that immediately changes the ranking, such as "we just deployed a change to #3". They may also know which hypotheses have already been ruled out. Do not block on their reply. Continue with the current ranking while waiting.

## Phase 4: Instrument

Each probe must map to a specific prediction from Phase 3. **Change one variable at a time.**

Tool preference:

1. **Debugger or REPL inspection** when the environment supports it. Prefer one breakpoint to ten logs.
2. **Targeted logs** at the seams that distinguish hypotheses.
3. Never "log everything and grep".

**Tag every debug log** with a unique prefix, such as `[DEBUG-a4f2]`. Cleanup then becomes a single grep. Remove every tagged log before completion.

**Performance branch.** Logs usually provide weak evidence for performance regressions. Establish a baseline with a timing harness, `performance.now()`, a profiler, or a query plan. Then bisect. Measure first and fix second.

## Phase 5: Fix and add a regression test

Write the regression test **before the fix**, but only if there is a **correct seam** for it.

A correct seam lets the test exercise the **real bug pattern** as it occurs at the call site. The available seam may be too shallow. Examples include a single-caller test for a bug that needs several callers, or a unit test that cannot reproduce the chain that triggered the bug. A regression test at that seam gives false confidence.

**If no correct seam exists, that itself is the finding.** Note it. The codebase architecture is preventing the bug from being locked down. Flag this for the next phase.

If a correct seam exists:

1. Turn the minimised repro into a failing test at that seam.
2. Watch it fail.
3. Apply the fix.
4. Watch it pass.
5. Re-run the Phase 1 feedback loop against the original (un-minimised) scenario.

## Phase 6: Cleanup

Required before declaring done:

- [ ] The original reproduction no longer fails. Run the Phase 1 loop again.
- [ ] The regression test passes, or the absence of a suitable seam is documented.
- [ ] All `[DEBUG-...]` instrumentation is removed. Search for the prefix.
- [ ] Throwaway prototypes are deleted or moved to a clearly marked debug location.
- [ ] The correct hypothesis is stated in the commit or PR description so the next debugger can use it.
