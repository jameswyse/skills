---
name: improve-performance
description: Measure and improve performance in a user-selected codebase, application, feature, function, or critical path through reproducible benchmarks, profiling, controlled experiments, and a before-and-after HTML report. Use only when the user explicitly requests a measured performance optimisation workflow.
---

# Improve performance

Make the selected path measurably faster without changing its required behaviour or moving the cost somewhere unmeasured.

Apply `$engineering`. Apply `$diagnosing-bugs` as well when the work concerns an unexpected performance regression or the measurements conflict with expectations. Apply an available framework or runtime performance skill only after the repository and the diagnosed bottleneck justify it. For example, use a matching Next.js cache skill for a confirmed Next.js caching problem rather than for every slow Next.js page.

## Choose the intake and set the target

Use the user's named codebase, application, feature, function, command, or critical path as the scope.

For a broad or exploratory request, work from repository evidence with little user input. If the user names a codebase or application, derive a small set of representative critical paths from its entrypoints, existing performance budgets, documented flows, and read-only telemetry when available. If the user does not name a target, inspect the current repository, available project context, and recent work without changing it. Offer two to four concrete suggestions, such as a recently changed browser flow, a slow build or test command, a server endpoint, or a hot function. Ask the user to choose one before instrumentation. Do not offer generic areas that the evidence does not support.

For a specific improvement request, resolve consequential unknowns before building the laboratory. Find repository facts yourself. Ask only for decisions that the code and existing evidence cannot answer, including:

- the slow action, input, or data size that represents the real workload;
- the environment and mode that matter, such as local, CI, or production and cold or warm;
- the result that would count as useful;
- required behaviour and unacceptable trade-offs;
- constraints on dependencies, architecture, compatibility, memory, cost, or delivery time.

Ask a compact set of direct questions when the unknowns are independent and few. When several consequential decisions remain, their answers depend on each other, or the acceptable solution could change substantially, apply `$grilling`. Use its design tree and recommended answers until the user confirms the shared understanding. Do not start instrumentation or implementation before that confirmation.

Write a short performance brief before changing product code:

- the target and the user-visible or operational outcome;
- the representative workload, inputs, and environment;
- one primary metric with its direction, such as lower latency or higher throughput;
- the target or minimum change that would count as useful;
- secondary guardrails for correctness, memory, CPU, network weight, tail latency, or another affected resource;
- the selected scope, relevant exclusions, and current working-tree state.

Infer and state any detail that the request and repository make clear so the user can correct it. The performance brief is ready when no unstated assumption can change the workload, success criterion, or acceptable solution.

The request to improve the named target authorises product and benchmark changes inside that scope. It does not authorise tool installation, dependency upgrades, production instrumentation, production configuration changes, or a larger architectural redesign. Ask before any of those actions.

## Phase 1: Build the laboratory

Establish a reproducible baseline before changing product code.

1. Read the repository instructions and find existing benchmarks, profiling tools, performance budgets, telemetry, tests, and verification commands. Compare the active toolchain with repository declarations once before relevant commands.
2. Choose the smallest workload that reproduces the real critical path. Separate scenarios that have different cost models, including cold and warm starts, cached and uncached requests, or development and production builds.
3. Create a benchmark command or harness that records structured results such as JSON or CSV. Put disposable probes and traces in the operating system's temporary directory. Add a lasting benchmark to the repository only when it protects an important path and fits the repository's test or benchmark conventions.
4. Add the least intrusive instrumentation that reveals where the time or resources go:
   - For browser work, use the available collaborative browser, Chrome DevTools MCP, or Chrome skill to capture a performance trace. Prefer `performance.mark()` and `performance.measure()` when trace-aligned markers help. Use `console.time()` when it fits the existing code or toolchain.
   - For page loading, measure the relevant Core Web Vitals, network requests, page weight, and bundle output. Use Lighthouse only with a fixed build, profile, throttling configuration, and repeated runs.
   - For scripts, servers, databases, or native code, use the repository's timing, CPU, allocation, query, I/O, or sampling profiler that matches the suspected resource. Use installed tools before proposing another dependency.
5. Run enough warm-ups and measured repetitions to expose normal variance. Keep the machine, toolchain, build mode, configuration, input data, and cache state consistent. Record the median and a useful tail or spread such as p95, interquartile range, or the observed range. Do not compare one-off timings.
6. Before the first experiment, define a checkable acceptance rule from the useful-change target and the baseline distribution. Record the statistic, threshold, and comparison method. Use a confidence interval, repeated batches, or another method the benchmark supports. Use `Inconclusive` only when the evidence cannot decide the rule. Use `Rejected` when the evidence establishes that the experiment misses it or fails a guardrail.
7. Record the reviewed revision, dirty-tree state, environment, sample count, raw results, and benchmark command. Keep secrets, authentication data, personal data, and complete request or response bodies out of traces and results.
8. Capture the current output or required behaviour through focused tests, fixtures, checksums, or observable browser behaviour so performance work cannot silently change the result.

The laboratory is ready when one command can reproduce the workload, record the primary metric, expose the main cost breakdown, and confirm the required output. If the benchmark remains too noisy to distinguish useful changes, improve the laboratory before diagnosing the code.

## Phase 2: Diagnose the bottlenecks

Use the measurements and profiles to identify the dominant costs. Name up to five bottlenecks, but do not fill a quota. One supported bottleneck is better than five guesses.

For each bottleneck, record:

- the trace, profile, query plan, bundle analysis, or benchmark evidence;
- a falsifiable hypothesis about the cause;
- the smallest intervention that would test the hypothesis;
- the metric expected to move and the approximate part of the cost it can affect;
- correctness risks and secondary metrics that could regress;
- the focused verification required after the experiment.

Rank hypotheses by their share of the measured cost, confidence, likely user impact, experiment size, and risk. Reject work that cannot affect the primary metric enough to rise above the benchmark's variance.

Before testing a library-specific hypothesis, confirm the repository's installed version. Search current primary sources such as official documentation, release notes, source code, and maintainers' issue trackers for known performance behaviour or gotchas that could change the experiment. Record the relevant source beside the hypothesis. Do not replace local measurement with generic advice from the web.

## Phase 3: Run controlled experiments

Work through the ranked hypotheses one at a time.

1. Start from the last accepted state and make one coherent change that tests one cause.
2. Run the focused correctness check and the same benchmark under the same conditions.
3. Compare the experiment with the previous accepted state for its incremental effect and with the original baseline for its cumulative effect.
4. Keep the change only when it passes the predeclared acceptance rule, required behaviour still passes, and secondary metrics do not reveal an unacceptable cost transfer.
5. Record the result and its raw values, spread, percentage change, correctness evidence, and reason:
   - `Kept` means the experiment passed the acceptance rule and every guardrail.
   - `Rejected` means it demonstrated no useful gain, regressed a metric, or failed a guardrail.
   - `Inconclusive` means the evidence could not distinguish the change from noise or another uncontrolled effect.
6. Restore the experiment's product changes after every `Rejected` or `Inconclusive` result. Retain its benchmark evidence for the report. Preserve unrelated work and accepted experiments.

Re-profile after a kept change when the cost distribution can have shifted. The original top bottleneck may no longer be the next useful target.

Flag a larger architectural change when the evidence shows that it owns the remaining bottleneck but exceeds the selected scope or authority. Record the measured ceiling, affected modules, expected gain, and why the change is larger. Then continue with the next independent hypothesis. Do not hide the architectural work inside a local workaround.

Stop when one of these conditions holds:

- the target or agreed performance budget is met;
- no evidence-backed safe hypothesis remains;
- further changes fall within measurement noise or fail the guardrails;
- every remaining bottleneck requires broader architecture, external-system access, a new dependency, or user input.

## Phase 4: Report the measured result

Before writing the report, read [HTML-REPORT.md](HTML-REPORT.md) in full. Write one static HTML file to the operating system's temporary directory. Resolve the directory from `$TMPDIR`, falling back to `/tmp` on Unix or `%TEMP%` on Windows. Use `<tmpdir>/performance-improvement-<timestamp>.html` so each run gets a fresh file.

The report must include:

- the target, workload, environment, revision, working-tree state, and benchmark method;
- the original baseline and final result with sample counts and spread;
- accessible before-and-after charts and a table of exact values;
- a breakdown that shows where the measured time, bytes, allocations, or other resource went;
- every experiment and its `Kept`, `Rejected`, or `Inconclusive` result;
- correctness checks and secondary-metric guardrails;
- remaining bottlenecks, measurement gaps, and larger architectural follow-ups.

Report an inconclusive or negative result honestly. Do not select the fastest run, hide rejected experiments, combine unlike scenarios, or imply causation that the controlled experiment did not establish.

Inspect the rendered report at a desktop width and at `320px`. Confirm that the charts, labels, tables, and experiment order remain legible and that the page has no horizontal overflow. Open the report with `xdg-open <path>` on Linux, `open <path>` on macOS, or `start <path>` on Windows. Tell the user the absolute path and summarise the measured outcome.

## Finish the code change

Remove disposable instrumentation and profiling artefacts from the product diff. Keep a benchmark or marker only when it has continuing value, stable overhead, and a clear owner. Run the repository's proportionate verification, inspect the complete diff and untracked files, and apply the finished-diff review required by `$engineering`.
