---
name: diagnosing-bugs
description: Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose" or "debug this", or reports something broken, throwing, failing, or slow. For a possible urgent live production incident, suggest diagnosing-production-incidents and continue unless the user invokes it.
---

# Diagnosing bugs

A discipline for hard bugs. Choose the next investigation from the evidence. Use a reproduction when practical and the evidence fallback below when it is not.

Read [Root-cause fixes](../engineering/references/root-causes.md) before choosing a fix. This skill owns the diagnostic loop. The reference owns fix placement, necessary consumer updates, and when a source fix needs approval.

When exploring the codebase, read `CONTEXT.md` (if it exists) to get a clear mental model of the relevant modules, and check ADRs in the area you're touching.

## Flag possible live production incidents

An ordinary bug found in production remains in this workflow. If the report may describe an urgent live production incident, mention that the user-invoked "diagnosing-production-incidents" skill is available for an evidence-first incident workflow. Signals include an active outage, a major production feature being unusable, or an explicit need for immediate recovery.

Make this a non-blocking suggestion. Continue the current diagnostic workflow without waiting for a response. Do not classify a report as an incident merely because production is mentioned.

If the user explicitly invokes "diagnosing-production-incidents", that skill owns the workflow. Do not run both diagnostic processes in parallel.

## Set the authority boundary

Diagnosis does not authorise a fix or persistent repository changes. When the user asks only for diagnosis, debugging, or an explanation, keep the working tree unchanged. Build the feedback loop from existing commands, runtime inspection, or temporary artefacts outside the repository. Ask before adding repository instrumentation or changing a production environment.

Continue through Phase 5 only when the user asked for a fix. A request to investigate a problem authorises Phases 1 to 4 and the diagnosis completion gate below.

## Redact

This skill requires visible commands, outputs, and captured artefacts. **Redact every secret first.** Write `<REDACTED>` in its place. Build loops against environment variables so credentials stay in the environment rather than in visible output. Captured artefacts can contain authentication headers. Quote only the lines that carry the signal.

If the redacted output is not enough to diagnose the bug, say so and ask the user.

## Phase 1: Build a feedback loop

Prefer a focused signal that goes red on the reported bug. Bisection, hypothesis testing, and instrumentation can use that signal to distinguish causes. Read relevant code, traces, configuration, and history when they help construct the reproduction or identify the next discriminating observation. Code inspection alone does not establish that a runtime fix works.

Spend effort in proportion to the evidence value of a reproduction. Use the fallback below when further setup would add little useful evidence or needs unavailable access.

### Ways to construct one, in roughly this order

Choose a loop that fits the authorised scope. For diagnosis-only work, prefer an existing test or a command that needs no repository changes. Keep throwaway scripts, fixtures, and captures in the operating system's temporary directory unless the user authorised adding them to the repository.

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

Use what the investigation reveals to improve the feedback loop. Keep provisional explanations distinct from a confirmed cause.

### Tighten the loop

Treat the loop as a product. Once you have _a_ loop, **tighten** it:

- Can setup be cached, unrelated initialisation skipped, or the test scope narrowed?
- Can the loop assert the specific symptom instead of merely checking that it did not crash?
- Can it pin time, seed random generation, isolate the filesystem, or freeze the network?

Prefer a fast, repeatable loop. Keep a slower check when the bug's actual path requires it; execution time alone does not disqualify useful evidence.

### Non-deterministic bugs

For intermittent failures, record the conditions, attempt count, and observed failure rate. Use bounded repetitions or controlled timing changes when they improve diagnostic value within the authorised environment and load. A low reproduction rate can still be useful evidence. Stop expanding the run when additional attempts are unlikely to distinguish causes.

### When a reproduction is unavailable or disproportionate

State what you tried and the missing access, inputs, or disproportionate setup. Continue read-only investigation using source, captured traces, configuration, history, and relevant documentation. Rank provisional explanations and identify the observation that would distinguish each one. Request only missing evidence that would change the diagnosis, such as:

- Access to an environment that reproduces the problem.
- A redacted captured artefact, such as a HAR file, log dump, core dump, or screen recording with timestamps.
- Permission to add temporary production instrumentation.

Continue independent investigation while waiting. Stop the affected branch when no available observation can reduce uncertainty. Report a probable cause or unresolved diagnosis when that is all the evidence supports. Never present an unexecuted reproduction or inferred fix as verified.

### Completion criterion: a tight loop that goes red

When a loop is practical, name a command you have run and show the relevant redacted output. Use these criteria to judge its evidence:

- [ ] **Red-capable.** It drives the actual bug path and asserts the **user's exact symptom**, so it can go red on this bug and green once fixed. "Runs without erroring" is insufficient. The command must catch this specific bug.
- [ ] **Repeatable.** It returns a consistent verdict, or records the conditions and failure rate for an intermittent bug.
- [ ] **Proportionate.** Its execution cost is justified by the symptom it observes.
- [ ] **Runnable.** Prefer unattended execution. When human participation is necessary, use a structured procedure such as `scripts/hitl-loop.template.sh` and record the observed result.

Proceed with the loop or the explicitly recorded evidence fallback. Keep the original symptom as the target in either mode.

## Phase 2: Reproduce and minimise

When a reproduction is available, run it and confirm the reported failure. In fallback mode, skip executable minimisation and narrow the affected path from the available evidence.

Confirm:

- [ ] The loop produces the failure mode the **user** described, not a different nearby failure. Reproducing the wrong bug leads to the wrong fix.
- [ ] Repeated runs support the failure, or the intermittent reproduction's limits are recorded.
- [ ] You have captured the exact symptom (error message, wrong output, slow timing) so later phases can verify the fix actually addresses it.

### Minimise

Once it is red, shrink the reproduction to the **smallest scenario that still goes red**. Cut inputs, callers, configuration, data, and steps **one at a time**. Run the loop after each cut and keep only what the failure requires.

A minimal reproduction reduces the hypotheses in Phase 3 because fewer moving parts remain. It also becomes the focused regression test in Phase 5.

Stop minimising when the scenario isolates the relevant behaviour and further reduction is unlikely to change the diagnosis or make the next check more useful. Preserve the original reproduction for final verification. Exhaustive minimality is not a completion requirement.

## Phase 3: Hypothesise

While the cause remains uncertain, rank the plausible explanations supported by current evidence. Consider realistic alternatives to the leading explanation. Do not invent hypotheses to fill a quota or delay a decisive check when the evidence already identifies one.

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

For diagnosis-only work, add logs only through existing runtime controls or after the user authorises temporary instrumentation.

**Tag every debug log** with a unique prefix, such as `[DEBUG-a4f2]`. Cleanup then becomes a single grep. Remove every tagged log before completion.

**Performance branch.** Logs usually provide weak evidence for performance regressions. Establish a baseline with a timing harness, `performance.now()`, a profiler, or a query plan. Then bisect. Measure first and fix second.

## Diagnosis completion gate

Once the evidence identifies the root cause, state the cause, the evidence that distinguishes it from the rejected hypotheses, the affected scope, and the smallest coherent fix.

If the user requested diagnosis only:

- Remove all `[DEBUG-...]` instrumentation and temporary artefacts.
- Report the feedback-loop command and its redacted failing output, or the evidence fallback, confidence, and remaining verification gap.
- State that the working tree was not changed and no fix was applied.
- Stop without entering Phase 5.

## Phase 5: Fix and add a regression test when authorised

Write the regression test **before the fix**, but only if there is a **correct seam** for it.

A correct seam lets the test exercise the **real bug pattern** as it occurs at the call site. The available seam may be too shallow. Examples include a single-caller test for a bug that needs several callers, or a unit test that cannot reproduce the chain that triggered the bug. A regression test at that seam gives false confidence.

If no practical test seam exists, record the limitation and use the closest useful check under the engineering testing reference. Distinguish architectural constraints from missing access, tooling, or an expensive test environment. Do not infer an architecture defect merely because no test was added.

If a correct seam exists:

1. Turn the minimised repro into a failing test at that seam.
2. Watch it fail.
3. Apply the fix.
4. Watch it pass.
5. Re-run the Phase 1 feedback loop against the original (un-minimised) scenario.

## Phase 6: Verify and clean up the authorised fix

Required before declaring the fix done:

- [ ] The original reproduction no longer fails, or the closest available check and the unexercised original symptom are stated explicitly. An inaccessible runtime remains unverified even when source evidence supports the fix.
- [ ] The regression test passes, or the absence of a suitable seam is documented.
- [ ] All `[DEBUG-...]` instrumentation is removed. Search for the prefix.
- [ ] Throwaway artefacts are removed from the temporary directory or kept only at a location the user requested.
- [ ] The confirmed cause and its evidence are stated plainly.
- [ ] The correct hypothesis is stated in the commit or PR description when the task includes writing one.
