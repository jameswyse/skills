# HTML report format

Render the architectural review as one HTML file in the operating system's temporary directory. The report is single-file, not offline. Load Tailwind and Mermaid from CDNs when the environment has network access. Otherwise use inline CSS and SVG. In network-backed reports, use Mermaid for graph-shaped diagrams. Use hand-built elements and inline SVG for mass diagrams, cross-sections, and other custom visuals. Mix both approaches when they are available so the report does not look generic.

## Scaffold

Use this scaffold when the report can load CDN resources. For an offline report, remove the script tags and use inline CSS and SVG.

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Architecture review for {{repo name}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "loose" });
    </script>
    <style>
      /* Small custom layer for details Tailwind does not cover cleanly,
         such as dashed seam lines and custom arrow heads. */
      .seam { stroke-dasharray: 4 4; }
      .leak { stroke: #dc2626; }
      .deep { background: linear-gradient(135deg, #0f172a, #1e293b); }
    </style>
  </head>
  <body class="bg-stone-50 text-slate-900 font-sans">
    <main class="max-w-5xl mx-auto px-6 py-12 space-y-12">
      <header>...</header>
      <section id="candidates" class="space-y-10">...</section>
      <section id="top-recommendation">...</section>
    </main>
  </body>
</html>
```

## Header

Show the repository name, date, and a compact legend. A solid box means module, a dashed line means seam, a red arrow means leakage, and a thick dark box means deep module. Omit an introduction and begin with the candidates.

## Candidate card

Make the diagrams explain the structure. Keep prose sparse and plain. Use the terms from [Deep modules](../engineering/references/deep-modules.md) directly.

Each candidate is one `<article>`:

- **Title.** Use a short name for the deepening, such as "Collapse the Order intake pipeline".
- **Badge row.** Show recommendation strength with `Strong` in emerald, `Worth exploring` in amber, or `Speculative` in slate. Add a dependency tag for `in-process`, `local-substitutable`, `remote and owned`, or `external and unowned`.
- **Files.** Use a monospaced list with `font-mono text-sm`.
- **Before-and-after diagram.** Use two side-by-side columns as the centrepiece. See the patterns below.
- **Problem.** Use one sentence to name what is difficult.
- **Solution.** Use one sentence to name what changes.
- **Wins.** Use bullets of six words or fewer, such as "Tests hit one interface", "Pricing logic stops leaking", or "Delete 4 shallow wrappers".
- **Documentation or ADR callout.** When applicable, use an amber-tinted box.

No paragraphs of explanation. If the diagram needs a paragraph to be understood, redraw the diagram.

## Diagram patterns

Pick the pattern that fits the candidate. Mix them. Don't make every diagram look the same. Variety is part of the point.

### Mermaid graph for dependencies and call flow

Use a Mermaid `flowchart` or `graph` to show a chain such as "X calls Y, then Y calls Z". Put it in a Tailwind-styled card that matches the report. Use `classDef` to colour leakage edges red and the deep module dark. Sequence diagrams work well when six round trips become one.

```html
<div class="rounded-lg border border-slate-200 bg-white p-4">
  <pre class="mermaid">
    flowchart LR
      A[OrderHandler] --> B[OrderValidator]
      B --> C[OrderRepo]
      C -.leak.-> D[PricingClient]
      classDef leak stroke:#dc2626,stroke-width:2px;
      class C,D leak
  </pre>
</div>
```

### Hand-built boxes and arrows

Render modules as bordered and labelled `<div>` elements. Render arrows as inline SVG `<line>` or `<path>` elements positioned over a relative container. Use this pattern when the "after" diagram needs one thick-bordered deep module with greyed-out internals and Mermaid cannot produce the layout.

### Cross-section for layered shallowness

Stack horizontal bands with `h-12 border-l-4` to show layers a call passes through. The before view has six thin layers that add no useful work. The after view has one thick band labelled with the consolidated responsibility.

### Mass diagram for interface and implementation size

Use two rectangles per module, one for interface size and one for implementation size. In the before view, both rectangles are nearly the same height, which indicates a shallow module. In the after view, the interface rectangle is short and the implementation rectangle is tall, which indicates a deep module.

### Call-graph collapse

In the before view, render a tree of function calls as nested boxes. In the after view, collapse the tree into one box and fade the calls that are now internal.

## Style guidance

- Use an editorial layout rather than a corporate dashboard. Leave generous whitespace. A serif heading font is optional. `font-serif` works well with stone and slate.
- Use colour sparingly. Choose one accent, either emerald or indigo. Reserve red for leakage and amber for warnings.
- Keep diagrams approximately 320px tall so the before-and-after views fit side by side without scrolling.
- Use `text-xs uppercase tracking-wider` for module labels inside diagrams, so they read as schematic, not as UI.
- In a network-backed report, limit external dependencies to the Tailwind CDN script and Mermaid ESM import. In an offline report, keep CSS and SVG inline. Keep the rest of the report static, with no application code or interactivity beyond Mermaid's rendering.

## Top recommendation section

One larger card. Candidate name, one sentence on why, anchor link to its card. That's it.

## Tone

Use plain, concise English. Take the architectural nouns and verbs from [Deep modules](../engineering/references/deep-modules.md). Concision is not an excuse to drift.

Use these terms exactly when they name the deep-module concepts:

`module`, `interface`, `implementation`, `depth`, `deep`, `shallow`, `seam`, `adapter`, `leverage`, and `locality`.

Preserve established framework, protocol, code, and domain terms when they are exact. A React component remains a component, an HTTP API remains an API, and a repository type or symbol keeps its real name. Use `module`, `interface`, and `seam` for the architectural concepts instead of renaming exact terms to fit the glossary.

These phrasings fit the style:

- "Order intake module is shallow. Its interface nearly matches the implementation."
- "Pricing leaks across the seam."
- "Deepen it. Use one interface and one place to test."
- "Two adapters justify the seam. Use HTTP in production and an in-memory adapter in tests."

Use glossary terms in the wins bullets. Examples include *"locality keeps bugs in one module"*, *"leverage gives N call sites one interface"*, and *"the interface shrinks while the implementation absorbs the wrappers"*. Do not write *"easier to maintain"* or *"cleaner code"* because those terms do not name the mechanism.

Do not hedge or preface a point with phrases such as "it is worth noting that". Turn a sentence into a bullet when that makes it easier to scan. Cut bullets that add nothing. Before inventing a term, look for one in the deep-module glossary.
