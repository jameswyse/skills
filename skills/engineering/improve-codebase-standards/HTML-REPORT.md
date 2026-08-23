# Standards HTML report format

Render the standards review as one static HTML file in the operating system's temporary directory. Load Tailwind and Mermaid from CDNs when the environment has network access. Otherwise use inline CSS and SVG.

## Scaffold

Use this scaffold when the report can load CDN resources. For an offline report, remove the script tags and use inline CSS and SVG.

```html
<!doctype html>
<html lang="en-AU">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Engineering standards review for {{repo name}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "loose" });
    </script>
    <style>
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
      pre {
        overflow-x: auto;
        border: 1px solid #334155;
        border-radius: 0.5rem;
        background: #020617;
        color: #e2e8f0;
        padding: 1rem;
        box-shadow: inset 0 1px rgb(255 255 255 / 0.08);
      }
      pre code {
        overflow-wrap: normal;
        font-size: 0.8125rem;
        line-height: 1.6;
      }
      .evidence { border-inline-start: 3px solid #4f46e5; }
      .improvement { border-inline-start: 4px solid #4f46e5; background: #eef2ff; }
      .risk { border-inline-start: 3px solid #dc2626; }
    </style>
  </head>
  <body class="bg-stone-50 text-slate-900 font-sans">
    <main class="mx-auto max-w-6xl space-y-10 px-4 py-10 sm:px-6 lg:px-8">
      <header>...</header>
      <section id="review-boundary" class="w-full">...</section>
      <section id="verification-evidence" class="w-full">...</section>
      <section id="findings-summary">...</section>
      <section id="top-recommendation">...</section>
      <section id="candidates" class="space-y-8">...</section>
      <section id="specialist-follow-ups">...</section>
      <section id="coverage-gaps">...</section>
    </main>
  </body>
</html>
```

## Header, review boundary, and verification evidence

Show the repository name, date, reviewed revision, and working-tree state in the header. Follow it with the review boundary and verification before any finding counts or recommendation.

Keep scope because it defines what the review can claim. Drop a separate "method" essay. Render the review boundary and verification evidence as two full-width sections, one after the other. Do not place them in a shared grid or side-by-side columns.

**Review boundary.** Show the requested scope, major areas inspected, and areas sampled or excluded. Use a full-width list or description list. Include a method note only when it limits confidence, such as generated code being sampled or external state being unavailable.

**Verification evidence.** Show the repository's declared Node.js and package-manager versions, whether the active versions matched, and a full-width table or list of checks. Each row names the command or interaction, result, cache state, and what it established. Mark fresh uncached runs explicitly. Include a clear `Not run` row for important runtime, build, browser, or integration coverage that was skipped.

Prefer a fresh build or uncached verification when it is safe and proportionate. Use the repository's uncached entrypoint when it has one. For Turborepo, use that entrypoint or force the relevant task instead of treating cache hits as final evidence. If a fresh run is unavailable, label the cached result and the remaining gap.

Do not present generic actions such as call-site searches, documentation reading, or source inspection as report content. They are review work, not evidence a reader needs. Do not use Turbo task counts as standalone statistics. A result such as `10/10 tasks` is meaningful only when the row also names the command and what those tasks verified. Do not turn partial checks into a `Clean` or codebase-health label.

If the review finds no worthwhile candidates, keep the review boundary and verification, then replace the candidate list with a direct conclusion. Do not invent recommendations to fill the report.

## Findings summary

Use one compact line or small description list for the counts, such as `3 Strong · 3 Worth exploring`. Avoid a row of large dashboard cards. Counts describe the report inventory, not codebase health.

## Top recommendation

Place the recommendation after the review boundary, verification, and compact counts. Keep it horizontal on wide screens and stacked on narrow screens:

```html
<section
  id="top-recommendation"
  aria-labelledby="top-recommendation-title"
  class="grid gap-6 border-s-4 border-indigo-600 bg-white p-6 shadow-sm lg:grid-cols-[minmax(0,2fr)_minmax(16rem,1fr)]"
>
  <div>
    <p class="text-xs font-semibold uppercase tracking-wider text-indigo-700">Top recommendation</p>
    <h2 id="top-recommendation-title" class="mt-2 text-2xl font-semibold tracking-tight">...</h2>
    <p class="mt-3 max-w-3xl text-sm leading-6 text-slate-600">Why this comes first and the source fix.</p>
  </div>
  <div class="grid content-start gap-3 bg-slate-50 p-4 text-sm sm:grid-cols-3 lg:grid-cols-1">
    <p><span class="block text-slate-500">Effort</span>Small</p>
    <p><span class="block text-slate-500">Risk</span>Low</p>
    <a class="font-semibold text-indigo-700 underline" href="#candidate-1">Read the finding</a>
  </div>
</section>
```

Do not put a Mermaid diagram, large illustration, tinted success surface, or repeated current/proposed flow in this section. Put supporting evidence and any useful comparison in the candidate itself.

## Candidate card

Use one `<article>` for each candidate. Keep the evidence and source fix more prominent than decorative elements. On wide screens, use one top-level grid with a two-thirds main column and a one-third supporting column. Stack the columns in reading order on narrow screens.

Each column is one full-width vertical stack. Do not place another grid, multi-column list, or side-by-side comparison inside either column. Put a code comparison, diagram, or other wide visual after the top-level grid so it spans the full article width.

- **Title.** Name the improvement, such as "Derive completion from one state".
- **Badge row.** Show recommendation strength with `Strong` in emerald, `Worth exploring` in amber, or `Speculative` in slate. Add `Small`, `Medium`, or `Large` effort and `Low`, `Medium`, or `High` risk.
- **Files and symbols.** Use a monospaced list with `font-mono text-sm`.
- **Standard.** Name the exact repository rule, `$engineering` section, or linked engineering reference. Do not cite `$engineering` without the rule.
- **Evidence.** Quote only the small code fragment, tool result, or repeated pattern needed to prove the problem.
- **Improvement.** State the smallest coherent source fix.
- **Benefit.** Name what the change removes, prevents, or makes directly verifiable.
- **Verification.** Name the focused command and the observable behaviour.
- **Visual.** Include one only when a relationship or state change is easier to understand visually.

Avoid paragraphs that restate the same evidence. Use short prose around a clear visual or code fragment.

Prefer a list when a section has more than one fact, change, benefit, or verification step. Keep list items short and parallel. Use a sentence for one idea instead of turning it into a one-item list.

### Improvement callout

Make the proposed source fix the strongest content block inside the finding. Use an indigo rule and light indigo background, a clear `Improvement` heading, and a short list when the fix has several parts:

```html
<section class="improvement p-4" aria-labelledby="candidate-1-improvement">
  <h4 id="candidate-1-improvement" class="text-sm font-semibold text-indigo-950">Improvement</h4>
  <ul class="mt-2 list-disc space-y-1 ps-5 text-sm leading-6 text-slate-700">
    <li>Move the production configuration read to the metadata owner.</li>
    <li>Keep the source factory injectable for focused tests.</li>
  </ul>
</section>
```

Use red only for demonstrated risk. The improvement is a proposed action, not a success state, so do not style it as green.

### Direct code comparison

For a local code improvement, prefer a short current-versus-proposed comparison over another paragraph. Place it after the finding's two-column grid so it uses the full article width. Use exact current code. Make the proposed excerpt concrete enough to review, and keep each side to the lines that expose the changed decision. Label both sides in text, not colour alone.

```html
<div class="grid gap-4 lg:grid-cols-2">
  <figure class="min-w-0 overflow-hidden rounded-lg border border-slate-700 bg-slate-950 text-slate-100 shadow-sm">
    <figcaption class="border-b border-slate-700 px-4 py-3 text-xs font-semibold uppercase tracking-wider text-slate-300">Current</figcaption>
    <pre class="rounded-none border-0 shadow-none"><code>...</code></pre>
  </figure>
  <figure class="min-w-0 overflow-hidden rounded-lg border border-indigo-400 bg-slate-950 text-slate-100 shadow-sm">
    <figcaption class="border-b border-indigo-400 px-4 py-3 text-xs font-semibold uppercase tracking-wider text-indigo-200">Proposed</figcaption>
    <pre class="rounded-none border-0 shadow-none"><code>...</code></pre>
  </figure>
</div>
```

Omit the comparison for operational, dependency, cross-cutting, or uncertain changes where a short excerpt would misrepresent the work.

## Visual patterns

Choose the pattern that matches the evidence. Do not force every candidate into a before-and-after architecture diagram.

### Source-of-truth convergence

Show several duplicated values, decisions, or schemas feeding into one authoritative owner. Label the synchronisation paths that disappear.

### State-space reduction

Use a small grid or state diagram to show currently representable invalid combinations. Contrast it with the legal variants in the proposed model.

### Failure path

Use a Mermaid sequence diagram or flowchart to show where context is lost, translated, or duplicated. Show the proposed error owner and the resulting diagnostic path.

### Test observation path

Show the production path beside the path exercised by tests. Highlight a test that bypasses the real behaviour, then show the observable seam or outcome the revised test would use.

### Lifecycle or command flow

Use a sequence diagram for startup, shutdown, retries, scheduling, or concurrent writers. Make duplicated transitions and missing ownership visible.

### Dependency cost

Use a compact dependency graph only when the finding depends on transitive weight, duplicated capability, runtime loading, or an unjustified build step. Preserve exact package and tool names.

## Architecture and organisation follow-ups

Put module-depth, seam, adapter, and substantial interface observations in a separate section. Explain why each belongs in `$improve-codebase-architecture`. Put repository-wide tree, placement, naming, and companion-file observations in the same section and explain why they belong in `$improve-codebase-organisation`. Do not assign these observations a standards rank or let them displace the top standards recommendation.

## Style guidance

- Use a concise editorial layout rather than a corporate dashboard. Let major sections breathe, but keep related facts in compact grids.
- Use indigo as the main accent. Reserve red for demonstrated risk and amber for warnings.
- Reserve emerald for the `Strong` badge or a verified passed result. Do not use a pale green or cyan background for the top recommendation.
- Use colour and diagrams to explain evidence, not to decorate the report.
- Give inline `<code>` a visible neutral surface and border. Give `<pre>` blocks a dark, bordered surface with enough padding to read as code at a glance.
- Keep diagrams near the text they support.
- Use exact repository paths, symbols, commands, frameworks, protocols, and domain terms.
- Limit network dependencies to the Tailwind CDN script and Mermaid ESM import. Keep the rest of the report static.

## Tone

Use plain, concise English. State the observed problem and the proposed source fix. Avoid generic phrases such as "cleaner code", "better practice", and "more maintainable". Name the removed branch, consolidated source of truth, prevented invalid state, improved failure context, or verified behaviour instead.
