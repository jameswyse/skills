import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";

mermaid.initialize({
  startOnLoad: false,
  securityLevel: "strict",
  theme: matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "neutral",
  fontFamily: getComputedStyle(document.body).fontFamily,
});
await mermaid.run({ querySelector: ".mermaid" });
