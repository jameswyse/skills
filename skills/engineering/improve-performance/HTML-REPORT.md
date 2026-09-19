# Performance HTML report format

Render the performance result as one static HTML file in the operating system's temporary directory. Load Tailwind and Mermaid from CDNs when the environment has network access. Otherwise use inline CSS and SVG. Build quantitative charts with HTML and inline SVG so the exact data remains visible without a charting dependency.

## Visual contract

Use the same editorial system as the architecture and standards reports:

- a light `bg-stone-50` page with `text-slate-900` content;
- one centred `max-w-6xl` document with `space-y-10` vertical rhythm;
- a `text-4xl` title, white major surfaces, restrained slate borders, and small shadows;
- indigo for the final measured state and selected improvement;
- slate for the baseline, emerald for verified passes, amber for inconclusive results, and red only for demonstrated regressions;
- dark surfaces only for code, trace excerpts, or individual diagram nodes.

Do not use a gradient page, glass panels, decorative glow, oversized display title, or a dashboard of metric cards.

## Scaffold

Use this scaffold when the report can load CDN resources. For an offline report, remove the script tags and use inline CSS and SVG.

```html
<!doctype html>
<html lang="en-AU">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Performance improvement for {{target}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "strict" });
    </script>
    <style>
      .grid > * { min-width: 0; }
      a { overflow-wrap: anywhere; }
      code {
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        overflow-wrap: anywhere;
      }
      :not(pre) > code {
        border: 1px solid #cbd5e1;
        border-radius: 0.25rem;
        background: #e2e8f0;
        color: #0f172a;
        padding: 0.125rem 0.35rem;
        font-size: 0.9em;
        font-weight: 600;
      }
      pre:not(.mermaid) {
        overflow-x: auto;
        border: 1px solid #334155;
        border-radius: 0.5rem;
        background: #020617;
        color: #e2e8f0;
        padding: 1rem;
      }
      .mermaid { overflow: visible; border: 0; background: transparent; padding: 0; }
      .result { border-inline-start: 4px solid #4f46e5; background: #eef2ff; }
      .warning { border-inline-start: 4px solid #d97706; background: #fffbeb; }
      .regression { border-inline-start: 4px solid #dc2626; background: #fef2f2; }
    </style>
  </head>
  <body class="bg-stone-50 font-sans text-slate-900 antialiased">
    <main class="mx-auto max-w-6xl space-y-10 px-4 py-10 sm:px-6 lg:px-8">
      <header>...</header>
      <section id="performance-target">...</section>
      <section id="benchmark-method">...</section>
      <section id="result-summary">...</section>
      <section id="before-after">...</section>
      <section id="cost-breakdown">...</section>
      <section id="experiments" class="space-y-8">...</section>
      <section id="verification">...</section>
      <section id="remaining-work">...</section>
    </main>
  </body>
</html>
```

## Keep report data inert

Treat repository names, paths, benchmark labels, command output, traces, source excerpts, URLs, and Mermaid labels as untrusted text. HTML-escape every dynamic value before inserting it into the document. Put dynamic text in text content, quoted attributes, or escaped `<code>` and `<pre>` blocks. Never insert it as raw HTML, inline JavaScript, inline CSS, or an event handler.

Keep Mermaid at `securityLevel: "strict"`. Escape diagram labels as text and omit click callbacks or embedded HTML. A locally opened report must not execute content taken from the reviewed repository or benchmark output.

## Establish what the numbers mean

Show the target, workload, environment, revision, dirty-tree state, build mode, cache state, toolchain, benchmark command, warm-up count, measured sample count, and summary statistic before presenting the result. Keep the performance target and benchmark method as separate full-width sections.

Name the primary metric and whether lower or higher is better. Separate cold and warm paths, cached and uncached paths, or other scenarios with different cost models. Never average unlike scenarios into one result.

Put the exact measurements in a table even when a chart repeats them. Include baseline, final value, absolute change, percentage change when defined, spread, sample count, and status. Use the correct percentage formula:

- For lower-is-better metrics, use `(baseline - final) / baseline * 100`.
- For higher-is-better metrics, use `(final - baseline) / baseline * 100`.

When the baseline is zero, report the absolute change and `N/A` for percentage change. Do not divide by zero or invent an infinite percentage.

Round only to the precision the measurement supports. State when the observed change remains within benchmark variance.

## Result summary

Use one compact horizontal section. Lead with the primary metric, the measured change, and whether the target was met. Put secondary guardrails and the strongest verification beside it. Do not repeat the result as a row of large cards.

Use wording such as `Median warm navigation fell from 820 ms to 560 ms, a 31.7% reduction across 20 measured runs.` Do not write `Performance improved significantly` without the numbers.

## Before-and-after chart

Use a horizontal bar chart or paired dot plot with one shared scale. Label `Baseline` and `Final` in text, print the exact value beside each mark, and state whether lower or higher is better. Use slate for the baseline and indigo for the final state.

When several scenarios share the same unit and conditions, align them on one scale. When units or cost models differ, use separate figures. Do not truncate the scale to exaggerate a small change.

Every chart needs:

- a visible title and concise caption;
- an accessible text alternative or adjacent data table;
- units on the axis or values;
- labels that do not rely on colour;
- enough height and spacing to remain readable at `320px`.

## Cost breakdown

Show where the measured resource went before and after. Choose the form that matches the evidence:

- a stacked bar for mutually exclusive phases that sum to the total;
- a flame-chart excerpt or trace timeline for nested browser or CPU work;
- a request waterfall for network latency and bytes;
- a bundle composition bar for transferred or parsed code;
- an allocation or query table when a chart would hide exact evidence.

Do not turn overlapping samples into a stacked total. State unaccounted time or sampling gaps instead of forcing the parts to add up.

## Experiment ledger

Render one article per hypothesis in the order tested. Each article includes:

- the hypothesis and its supporting profile evidence;
- the exact change tested;
- the previous accepted value, experiment value, spread, and incremental change;
- the cumulative change from the original baseline;
- correctness and secondary-metric results;
- a `Kept`, `Rejected`, or `Inconclusive` badge and the reason.

Use emerald only for a verified kept experiment, amber for inconclusive, slate for a rejected neutral result, and red for a demonstrated regression. A rejected experiment is useful evidence. Do not visually bury it.

State that only `Kept` experiments remain in the final product diff. For every `Rejected` or `Inconclusive` experiment, confirm that its product changes were restored while its measurements remain in the ledger.

## Verification and remaining work

List the focused checks and the observable behaviour each one established. Distinguish fresh results from cache hits. Name important browser, build, integration, load, or production paths that were not exercised.

Separate remaining measured bottlenecks from larger architectural follow-ups. For each architectural follow-up, show the supporting measurement, the approximate ceiling it controls, affected modules, and the authority or scope reason it was not attempted. Do not present an unmeasured redesign as the next optimisation.

If the workflow produced no reliable gain, keep the full method, experiment ledger, and remaining evidence. State `No supported improvement` or `Inconclusive` in the result summary.

## Render check

Apply the "ux" HTML-report verification to the final file, including screenshot inspection at a desktop width and at `320px`. Check these report-specific requirements:

- The page keeps the shared light editorial system and centred `max-w-6xl` document.
- The performance target and benchmark method remain full-width and single-column.
- Charts use one honest scale, exact labels, and a readable text alternative.
- Wide data tables scroll inside their own containers instead of widening the page.
- Experiment articles remain in test order and their badges are understandable without colour.
- Code and trace excerpts scroll inside their own containers; labels wrap and charts fit without widening the page.

Fix observed defects before handoff. If visual inspection is unavailable, deliver the structurally checked report with `Visual verification not run` and the reason.

## Tone

Use plain, concise English. Name the workload, metric, sample count, variance, and observed change. Distinguish measurement from inference. Avoid `faster`, `lighter`, `optimised`, or `significant` when a number can state the result.
