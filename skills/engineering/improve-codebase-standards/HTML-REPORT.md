# Standards HTML report format

Render the standards review as one HTML file in the operating system's temporary directory. The report is single-file, not offline. Load Tailwind and Mermaid from CDNs when the environment has network access. Otherwise use inline CSS and SVG.

## Scaffold

Use this scaffold when the report can load CDN resources. For an offline report, remove the script tags and use inline CSS and SVG.

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Engineering standards review for {{repo name}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "loose" });
    </script>
    <style>
      .evidence { border-left: 4px solid #4f46e5; }
      .risk { border-left: 4px solid #dc2626; }
      .improvement { background: linear-gradient(135deg, #eef2ff, #ffffff); }
    </style>
  </head>
  <body class="bg-stone-50 text-slate-900 font-sans">
    <main class="max-w-5xl mx-auto px-6 py-12 space-y-12">
      <header>...</header>
      <section id="coverage">...</section>
      <section id="candidates" class="space-y-10">...</section>
      <section id="architecture-follow-ups">...</section>
      <section id="top-recommendation">...</section>
    </main>
  </body>
</html>
```

## Header and coverage

Show the repository name, date, reviewed revision, working-tree state, and requested scope. Follow the header with a compact coverage map of the major repository areas inspected. Mark uninspected or partially inspected areas as coverage gaps. Do not calculate a codebase health score.

If the review finds no worthwhile candidates, keep the coverage section and replace the candidate list with a direct conclusion. Do not invent recommendations to fill the report.

## Candidate card

Use one `<article>` for each candidate. Keep the evidence and source fix more prominent than the decorative elements.

- **Title.** Name the improvement, such as "Derive completion from one state".
- **Badge row.** Show recommendation strength with `Strong` in emerald, `Worth exploring` in amber, or `Speculative` in slate. Add `Small`, `Medium`, or `Large` effort and `Low`, `Medium`, or `High` risk.
- **Files and symbols.** Use a monospaced list with `font-mono text-sm`.
- **Standard.** Name the repository rule or the relevant section of `$engineering`.
- **Evidence.** Quote only the small code fragment, tool result, or repeated pattern needed to prove the problem.
- **Improvement.** State the smallest coherent source fix.
- **Benefit.** Name what the change removes, prevents, or makes directly verifiable.
- **Verification.** Name the focused command and the observable behaviour.
- **Visual.** Include one only when a relationship or state change is easier to understand visually.

Avoid paragraphs that restate the same evidence. Use short prose around a clear visual or code fragment.

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

### Direct code comparison

For a local simplification, place short code excerpts side by side. Fade branches, state, or indirection that the improvement removes. Keep excerpts short enough to read without horizontal scrolling.

## Architecture follow-ups

Put module-depth, seam, adapter, and substantial interface observations in a separate section. Explain why each belongs in `$improve-codebase-architecture`. Do not assign them a standards rank or let them displace the top standards recommendation.

## Style guidance

- Use an editorial layout with generous whitespace rather than a corporate dashboard.
- Use indigo as the main accent. Reserve red for demonstrated risk and amber for warnings.
- Use colour and diagrams to explain evidence, not to decorate the report.
- Keep diagrams near the text they support.
- Use exact repository paths, symbols, commands, frameworks, protocols, and domain terms.
- Limit network dependencies to the Tailwind CDN script and Mermaid ESM import. Keep the rest of the report static.

## Top recommendation

Use one larger card. Include the candidate name, one sentence explaining why it comes first, its effort and risk, and an anchor link to the candidate card.

## Tone

Use plain, concise English. State the observed problem and the proposed source fix. Avoid generic phrases such as "cleaner code", "better practice", and "more maintainable". Name the removed branch, consolidated source of truth, prevented invalid state, improved failure context, or verified behaviour instead.
