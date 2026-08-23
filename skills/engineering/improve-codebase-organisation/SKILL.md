---
name: improve-codebase-organisation
description: Review an entire codebase's tree, module placement, filenames, companion-file ownership, and shallow filesystem structure. Use when the user explicitly requests a codebase organisation, naming, locality, or repository-structure audit rather than a general architecture or standards review.
---

# Improve codebase organisation

Review the repository tree as an interface for maintainers. Find structures that make a capability difficult to locate or follow, then present evidence before changing files.

Apply `$engineering`. Read [Codebase organisation and naming](../engineering/references/organisation-and-naming.md) before inspecting the tree. Read [Deep modules](../engineering/references/deep-modules.md) before judging whether a file, directory, or interface is shallow.

Keep this workflow distinct from broader reviews:

- Use `$code-review` to approve or find defects in a particular diff.
- Use `$improve-codebase-architecture` when the main problem requires a deeper module, a different seam, or substantial interface redesign.
- Use `$improve-codebase-standards` for correctness, types, tests, tooling, operations, and general maintenance standards.

## Establish the scope

Review the entire codebase by default. Inventory its projects, packages, entrypoints, capabilities, shared mechanisms, tests, stories, styles, fixtures, and generated code. Derive major areas from the repository's own vocabulary. Give every major area one coverage verdict:

- a supported organisation candidate;
- inspected with no supported candidate; or
- a named coverage gap.

Use a narrower scope only when the user names a repository area, subsystem, recent change, branch, or fixed point. Inspect the callers and neighbouring ownership needed to judge that scope.

Read the repository instructions, architecture guidance, domain glossary, and framework conventions before treating a layout as accidental. Inspect the working tree to preserve unrelated work and describe the reviewed state. Do not let recent changes narrow an unqualified whole-codebase review.

## Inspect how a maintainer navigates

Start from entrypoints and the tree, not from a symbol search result. For each major area, trace representative maintenance questions and record where the tree stops predicting the next location.

Follow evidence from paths, imports, exports, callers, tests, stories, styles, fixtures, documentation, and change history. Look for:

- one capability scattered across unrelated technical directories;
- shared directories containing code with one real owner;
- vague names that do not predict contents or responsibility, including catch-all directories whose children have clearer owners;
- sibling modules that express the same pattern with inconsistent names;
- re-export-only files, one-caller forwarding modules, and dispatchers that own no choice;
- tiny type or helper files without independent meaning;
- directories that add a navigation step without grouping a coherent set;
- tests, stories, styles, fixtures, or generated artefacts without an obvious owner;
- obsolete paths or parallel naming retained after a migration;
- public entrypoints that expose internal layout or internal entrypoints that imitate a public package interface.

Treat file size, child count, and search matches as leads. Reopen each candidate and inspect its callers before reporting it.

## Require a concrete navigation cost

Include a candidate only when current evidence supports these points:

1. **Prediction failure.** Show what a maintainer would reasonably expect from the path or name and where the code actually lives.
2. **Ownership or locality.** Show the knowledge that changes together, the current places a maintainer must visit, or the file that has no independent owner.
3. **Deletion test.** For a shallow path, show whether deleting it removes the concept or scatters decisions back into callers.
4. **Coherent target.** Show the exact rename, move, merge, deletion, or grouping that would make the tree more predictive.
5. **Net reduction.** Confirm that the proposal removes navigation and concepts rather than moving them or adding another taxonomy.
6. **Verification.** Name the imports, builds, tests, documentation, and companion-owner checks that would prove the reorganisation complete.

Reject personal naming preferences without a maintenance cost, speculative taxonomies, public API changes without authority, and large moves justified only by symmetry. Preserve framework filenames and generated layouts unless the framework permits a clearer supported structure.

Rank supported candidates as `Strong`, `Worth exploring`, or `Speculative`. Do not fill a quota.

## Present the review

Return a concise Markdown report with:

1. the requested scope, repository state, coverage verdicts, and gaps;
2. the strongest candidate and why it ranks first;
3. ranked candidates with current paths, evidence, the proposed tree, benefit, risk, and verification;
4. confirmed clean checks for companion ownership, naming families, forwarding paths, and obsolete locations.

Use a small current-versus-proposed tree when it explains a candidate faster than prose. Name exact files and symbols. Distinguish confirmed orphans from candidates that need a framework or cross-module exception.

Do not change files during a review-only request. When the user authorises implementation, revalidate the selected candidates against the current tree, make the coherent moves, migrate imports and companions, remove obsolete paths, update affected documentation, and run the repository's real verification commands.
