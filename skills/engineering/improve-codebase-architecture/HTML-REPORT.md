# Architecture HTML report format

Render the architecture review as one static HTML file in the operating system's temporary directory. Load Tailwind and Mermaid from CDNs when the environment has network access. Otherwise use inline CSS and SVG. Use Mermaid for graph-shaped diagrams. Use hand-built elements and inline SVG for mass diagrams, cross-sections, and other custom visuals.

## Scaffold

Use this scaffold when the report can load CDN resources. For an offline report, remove the script tags and use inline CSS and SVG.

```html
<!doctype html>
<html lang="en-AU">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Architecture review for {{repo name}}</title>
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
      pre:not(.mermaid) {
        overflow-x: auto;
        border: 1px solid #334155;
        border-radius: 0.5rem;
        background: #020617;
        color: #e2e8f0;
        padding: 1rem;
        box-shadow: inset 0 1px rgb(255 255 255 / 0.08);
      }
      pre:not(.mermaid) code {
        overflow-wrap: normal;
        font-size: 0.8125rem;
        line-height: 1.6;
      }
      .mermaid {
        overflow: visible;
        border: 0;
        background: transparent;
        padding: 0;
        box-shadow: none;
      }
      .proposal { border-inline-start: 4px solid #4f46e5; background: #eef2ff; }
      .warning { border-inline-start: 4px solid #d97706; background: #fffbeb; }
      .seam { stroke-dasharray: 4 4; }
      .leak { stroke: #dc2626; }
      .deep { background: #0f172a; color: #f8fafc; }
    </style>
  </head>
  <body class="bg-stone-50 font-sans text-slate-900 antialiased">
    <main class="mx-auto max-w-6xl space-y-10 px-4 py-10 sm:px-6 lg:px-8">
      <header>...</header>
      <section id="review-boundary" class="w-full">...</section>
      <section id="evidence" class="w-full">...</section>
      <section id="candidate-summary">...</section>
      <section id="top-recommendation">...</section>
      <section id="candidates" class="space-y-8">...</section>
      <section id="coverage-gaps">...</section>
    </main>
  </body>
</html>
```

## Header, review boundary, and evidence

Show the repository name, date, reviewed revision, and working-tree state in the header. Follow it with the review boundary and evidence before candidate counts or recommendations.

Render the review boundary and evidence as two full-width sections, one after the other. Do not place them in a shared grid or side-by-side columns.

**Review boundary.** Show the requested scope, major areas inspected, and areas sampled or excluded. Use a full-width list or description list. Include a method detail only when it limits confidence.

**Evidence and verification.** Show the concrete evidence used to assess depth. Name the relevant callers, tests, documented ownership or ADRs, and the deletion-test result. List commands or runtime paths only when they affect confidence. Mark anything not exercised as `Not verified`.

Do not calculate an architecture-health score. If the review finds no credible candidates, keep these two sections and replace the candidate list with a direct conclusion.

## Candidate summary

Use one compact line or small description list for the counts, such as `2 Strong · 1 Worth exploring`. Counts describe the report inventory, not the codebase's health.

## Top recommendation

Place the recommendation after the review boundary, evidence, and compact counts. Keep it horizontal on wide screens and stacked on narrow screens:

```html
<section
  id="top-recommendation"
  aria-labelledby="top-recommendation-title"
  class="grid gap-6 border-s-4 border-indigo-600 bg-white p-6 shadow-sm lg:grid-cols-[minmax(0,2fr)_minmax(16rem,1fr)]"
>
  <div>
    <p class="text-xs font-semibold uppercase tracking-wider text-indigo-700">Top recommendation</p>
    <h2 id="top-recommendation-title" class="mt-2 text-2xl font-semibold tracking-tight">...</h2>
    <p class="mt-3 max-w-3xl text-sm leading-6 text-slate-600">Why this candidate comes first and what the deepening absorbs.</p>
  </div>
  <div class="grid content-start gap-3 bg-slate-50 p-4 text-sm sm:grid-cols-3 lg:grid-cols-1">
    <p><span class="block text-slate-500">Strength</span>Strong</p>
    <p><span class="block text-slate-500">Dependency</span>In-process</p>
    <a class="font-semibold text-indigo-700 underline underline-offset-4" href="#candidate-1">Read the candidate</a>
  </div>
</section>
```

Keep diagrams and detailed evidence in the candidate card. Do not turn the recommendation into a second candidate card.

## Candidate card

Make the before-and-after diagram the centrepiece. Keep prose sparse and use the terms from [Deep modules](../engineering/references/deep-modules.md) directly.

Each candidate is one `<article>`. On wide screens, use one top-level grid with a two-thirds main column and a one-third supporting column. Each column is one full-width vertical stack. Do not place another grid or multi-column list inside either column. Stack the columns in reading order on narrow screens.

- **Title.** Use a short name for the deepening, such as "Collapse the Order intake pipeline".
- **Badge row.** Show `Strong` in emerald, `Worth exploring` in amber, or `Speculative` in slate. Add one dependency tag: `in-process`, `local-substitutable`, `remote and owned`, or `external and unowned`.
- **Problem.** Name the current coordination, leaked decision, or shallow interface.
- **Proposed deepening.** Highlight what the module absorbs and what its callers stop knowing.
- **Files.** Use a monospaced list of exact files, modules, and symbols.
- **Wins.** Use short bullets naming locality, leverage, interface reduction, or testing gains.
- **Documentation or ADR callout.** When applicable, use an amber warning with the conflicting rule and why it merits reconsideration.
- **Before-and-after diagram.** Place it after the top-level grid so it spans the full article width.

Prefer a list when a section contains more than one fact, change, or win. Keep a sentence when it carries one idea. No paragraphs of explanation. If the diagram needs a paragraph to be understood, redraw it.

### Proposed deepening callout

Make the proposed deepening the strongest text block inside the candidate. Use an indigo rule and light indigo background. Use a short list when the module absorbs several decisions:

```html
<section class="proposal p-4" aria-labelledby="candidate-1-proposal">
  <h4 id="candidate-1-proposal" class="text-sm font-semibold text-indigo-950">Proposed deepening</h4>
  <ul class="mt-2 list-disc space-y-1 ps-5 text-sm leading-6 text-slate-700">
    <li>Move restoration, validation, and persistence behind one interface.</li>
    <li>Leave feature-owned outcomes outside the module.</li>
  </ul>
</section>
```

The proposal is not a success state. Keep it indigo, not green. Reserve red for demonstrated leakage and amber for documentation conflicts or uncertainty.

### Full-width before and after

Place the comparison below the candidate's two-column summary so it uses the full article width. Use visible `Current` and `Proposed` labels rather than colour alone. Stack the two figures on narrow screens.

```html
<div class="mt-6 grid gap-4 lg:grid-cols-2">
  <figure class="min-w-0 overflow-hidden rounded-lg border border-slate-300 bg-white shadow-sm">
    <figcaption class="border-b border-slate-200 px-4 py-3 text-xs font-semibold uppercase tracking-wider text-slate-600">Current</figcaption>
    <div class="min-h-80 p-4">...</div>
  </figure>
  <figure class="min-w-0 overflow-hidden rounded-lg border border-indigo-300 bg-white shadow-sm">
    <figcaption class="border-b border-indigo-200 px-4 py-3 text-xs font-semibold uppercase tracking-wider text-indigo-700">Proposed</figcaption>
    <div class="min-h-80 p-4">...</div>
  </figure>
</div>
```

Give every diagram a visible label and a concise text alternative beside it or in its `<figcaption>`. Do not rely on line style or colour alone to communicate leakage, seams, or depth.

## Diagram patterns

Pick the pattern that matches the evidence. Mix them when that clarifies different candidates. Variety is useful only when the diagram type fits the relationship.

### Mermaid graph for dependencies and call flow

Use a Mermaid `flowchart`, `graph`, or sequence diagram for dependencies and call order. Put it inside the full-width before-and-after figure. Keep the containing surface and labels in HTML so Mermaid does not control the report hierarchy.

```html
<figure aria-labelledby="current-flow-title" class="rounded-lg border border-slate-300 bg-white shadow-sm">
  <figcaption id="current-flow-title" class="border-b border-slate-200 px-4 py-3 font-semibold">Current call flow</figcaption>
  <div class="p-4">
    <pre class="mermaid">
      flowchart LR
        A[OrderHandler] --> B[OrderValidator]
        B --> C[OrderRepo]
        C -. leakage .-> D[PricingClient]
    </pre>
    <p class="mt-3 text-sm text-slate-600">Pricing decisions cross the repository seam.</p>
  </div>
</figure>
```

### Hand-built boxes and arrows

Render modules as bordered and labelled `<div>` elements. Render arrows as inline SVG positioned over a relative container. Use this when the proposed view needs one thick-bordered deep module with faded internals and Mermaid cannot produce the layout.

### Cross-section for layered shallowness

Stack horizontal bands to show layers a call passes through. The current view has several thin layers that add no useful work. The proposed view has one deeper band labelled with the consolidated responsibility.

### Mass diagram for interface and implementation size

Use two rectangles per module, one for interface size and one for implementation size. The diagram is qualitative. Do not turn source-line counts into a depth score.

### Call-graph collapse

In the current view, render a tree of function calls as nested boxes. In the proposed view, collapse the tree into one module and fade the calls that become implementation details.

## Style guidance

- Use the same concise editorial shell as the standards report: stone page, slate text, white evidence surfaces, indigo accent, restrained borders, and small shadows.
- Use indigo for the proposal and selected architecture. Reserve red for demonstrated leakage and amber for warnings or documentation conflicts.
- Reserve emerald for the `Strong` badge or verified passed result. Do not use a green-tinted recommendation or proposal surface.
- Give inline `<code>` a visible neutral surface and border. Give non-Mermaid `<pre>` blocks a dark, bordered surface with enough padding to read as code at a glance.
- Keep before-and-after diagrams near `320px` tall when the content permits. Let them grow rather than clipping labels or content.
- Use `text-xs uppercase tracking-wider` for schematic module labels.
- Keep exact repository paths, symbols, frameworks, protocols, and domain terms.
- Limit network dependencies to the Tailwind CDN script and Mermaid ESM import. Keep the rest of the report static.

## Tone

Use plain, concise English. Take the architectural nouns and verbs from [Deep modules](../engineering/references/deep-modules.md). Concision is not an excuse to drift.

Use these terms exactly when they name the deep-module concepts:

`module`, `interface`, `implementation`, `depth`, `deep`, `shallow`, `seam`, `adapter`, `leverage`, and `locality`.

Preserve established framework, protocol, code, and domain terms when they are exact. A React component remains a component, an HTTP API remains an API, and a repository type or symbol keeps its real name.

These phrasings fit the style:

- "Order intake module is shallow. Its interface nearly matches the implementation."
- "Pricing leaks across the seam."
- "Deepen it. Use one interface and one place to test."
- "Two adapters justify the seam. Use HTTP in production and an in-memory adapter in tests."

Use glossary terms in the wins bullets. Examples include "Locality keeps bugs in one module", "Leverage gives 12 callers one interface", and "The interface shrinks while the implementation absorbs four wrappers". Do not write "easier to maintain" or "cleaner code" because those phrases do not name the mechanism.

Do not hedge or preface a point with filler. Turn a sentence into a bullet when that makes it easier to scan. Cut bullets that add nothing. Before inventing a term, look for one in the deep-module glossary.
