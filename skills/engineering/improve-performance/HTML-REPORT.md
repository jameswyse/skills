# Performance HTML report format

Build the report with the "html-report" skill. This file owns what the performance report says. Write the body to `<tmpdir>/performance-improvement-<timestamp>.body.html` and build `<tmpdir>/performance-improvement-<timestamp>.html`.

## Sections

1. **Header.** Eyebrow `Performance improvement`, the target as the title, then date, revision, working-tree state, and build mode.
2. **Summary.** The measured result in one sentence, such as `Median warm navigation fell from 820 ms to 560 ms, a 31.7% reduction across 20 measured runs.` Add whether the target or budget was met, and name the workload, environment, and summary statistic. Counts: experiments kept, rejected, and inconclusive.
3. **Result.** A `figure.chart` of baseline and final values for each scenario, then a two-column table: the scenario with a note giving baseline, final, absolute change, spread, and sample count, then the percentage change and a status badge.
4. **Where the time went.** One breakdown of the measured resource before and after.
5. **Experiments.** One `.item` per hypothesis, in the order tested, however many there are.
6. **Remaining work.** Measured bottlenecks that remain, then architectural follow-ups.
7. **How this was checked.** The benchmark method and the correctness and guardrail checks.

If the workflow produced no reliable gain, state `No supported improvement` or `Inconclusive` in the summary and keep the experiments and method.

## Numbers

Name the primary metric and whether lower or higher is better. Separate cold and warm, cached and uncached, or other scenarios with different cost models. Never average unlike scenarios.

Calculate percentage change as `(baseline - final) / baseline * 100` for lower-is-better metrics and `(final - baseline) / baseline * 100` for higher-is-better metrics. When the baseline is zero, report the absolute change and `N/A`. Round only to the precision the measurement supports, and state when a change is within benchmark variance.

## Charts

Use `.bars` with one shared scale per unit and condition. Label rows `Baseline` and `Final` in text, give the final row `accent`, print each exact value, and put the unit and direction in the caption. Do not truncate the scale to exaggerate a change. Use separate charts when units or cost models differ.

For the breakdown, choose the form that matches the evidence:

- `.bars` for mutually exclusive phases, one row per phase with before and after values;
- a table for nested trace work, request waterfalls, bundle composition, allocations, or queries;
- a short `pre` trace excerpt when one frame or request explains the cost.

Do not stack overlapping samples into a total. State unaccounted time or sampling gaps.

## Experiment

- **Title.** The hypothesis, such as "Defer the analytics bundle until idle".
- **Badges.** `Kept` as `good`, `Inconclusive` as `warn`, `Rejected` as neutral, and a demonstrated regression as `risk`.
- **Result callout.** The previous accepted value, experiment value, spread, incremental change, and cumulative change from the original baseline.
- **Fields.**
  - `Evidence`: the profile result that suggested it.
  - `Change`: the exact change tested.
  - `Checks`: correctness and secondary-metric results.
  - `Reason`: why it was kept, rejected, or left inconclusive.

Show rejected experiments at the same weight as kept ones. Only `Kept` experiments remain in the product diff. For each other experiment, state that its product changes were restored.

## Remaining work and checks

For each architectural follow-up, give the supporting measurement, the ceiling it controls, the affected modules, and why it was out of scope. Do not present an unmeasured redesign as the next optimisation.

In the checks section, use a `.fields` list for target, workload, environment, toolchain, benchmark command, warm-up count, sample count, statistic, and cache state. Follow it with the checks table, noting what each check established when the name does not show it and `Cached` when a result came from cache. Add `Not run` rows for important browser, build, integration, load, or production paths.

## Wording

Name the workload, metric, sample count, variance, and change. Distinguish measurement from inference. Avoid `faster`, `lighter`, `optimised`, and `significant` when a number can state the result.
