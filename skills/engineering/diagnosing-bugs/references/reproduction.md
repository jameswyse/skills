# Reproduction techniques

Use when selecting or improving a reproduction, investigating intermittent failures, or minimising a scenario would distinguish causes. Respect the authority and evidence fallback in the [entrypoint](../SKILL.md).

## Choose a reproduction technique

Choose a loop that fits the authorised scope. For diagnosis-only work, prefer an existing test or a command that needs no repository changes. Keep throwaway scripts, fixtures, and captures in the operating system's temporary directory unless the user authorised adding them to the repository.

1. **Failing test** at whichever seam reaches the bug, whether unit, integration, or end to end.
2. **Curl or HTTP script** against a running development server.
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot.
4. **Headless browser script.** Use Playwright or Puppeteer to drive the UI and assert on the DOM, console, and network.
5. **Replay a captured trace.** Save a real network request, payload, or event log to disk. Replay it through the code path in isolation.
6. **Throwaway harness.** Start a minimal subset of the system, such as one service with mocked dependencies, that exercises the bug path with one function call.
7. **Property or fuzz loop.** If the bug sometimes returns the wrong output, run a bounded set of random inputs justified by the failure rate and cost and look for the failure mode.
8. **Bisection harness.** If the bug appeared between two known states (commit, dataset, version), automate "boot at state X, check, repeat" so you can `git bisect run` it.
9. **Differential loop.** Run the same input through old and new versions, or through two configurations, and compare the outputs.
10. **Human-in-the-loop script.** Use this as a last resort. If a human must click, guide _them_ with the [human-assisted loop template](../scripts/hitl-loop.template.sh) so the loop remains structured. Use their captured output as the next input.

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
- [ ] **Runnable.** Prefer unattended execution. When human participation is necessary, use a structured procedure such as the [human-assisted loop template](../scripts/hitl-loop.template.sh) and record the observed result.

Proceed with the loop or the explicitly recorded evidence fallback. Keep the original symptom as the target in either mode.

## Reproduce and minimise

When a reproduction is available, run it and confirm the reported failure. In fallback mode, skip executable minimisation and narrow the affected path from the available evidence.

Confirm:

- [ ] The loop produces the failure mode the **user** described, not a different nearby failure. Reproducing the wrong bug leads to the wrong fix.
- [ ] Repeated runs support the failure, or the intermittent reproduction's limits are recorded.
- [ ] You have captured the exact symptom (error message, wrong output, slow timing) so verification can establish whether the fix actually addresses it.

### Minimise

Once it is red, shrink the reproduction to the **smallest scenario that still goes red**. Cut inputs, callers, configuration, data, and steps **one at a time**. Run the loop after each cut and keep only what the failure requires.

A minimal reproduction reduces the plausible causes because fewer moving parts remain. It also becomes a focused regression test when a fix is authorised.

Stop minimising when the scenario isolates the relevant behaviour and further reduction is unlikely to change the diagnosis or make the next check more useful. Preserve the original reproduction for final verification. Exhaustive minimality is not a completion requirement.

