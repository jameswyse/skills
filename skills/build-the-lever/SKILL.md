---
name: build-the-lever
description: "Build the smallest rerunnable tool or check that performs non-trivial work and proves the result."
---

# Build the lever

Create a file-backed, rerunnable lever for the requested work. Use a codemod or script for edits, a generator for repetitive files, a query for analysis, or an executable check for verification.

## Build it

- Work through one representative unit manually when needed to discover the recipe.
- Encode the smallest deterministic tool that performs or proves that recipe. Do not turn it into a framework.
- Limit its inputs and write scope to the user's task. Make repeated runs safe.
- If work is delegated, put the shared recipe, checks and write boundaries in one file outside delegates' write scope.

## Prove it

- Compare the lever's result with the representative manual result.
- Run it across the intended scope, then rerun it to prove that it is safe and stable.
- Leave the lever in the deliverable so a reviewer can inspect and rerun it. Invoking this skill must produce a codemod, script, generator, query, executable check or delegate instruction file.

Use `$principle-laziness-protocol` to keep the lever small, `$principle-encode-lessons-in-structure` when the lesson should become a lasting guardrail, and `$principle-prove-it-works` to verify the result.
