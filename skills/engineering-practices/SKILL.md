---
name: engineering-practices
description: "Baseline engineering rules for code, tests, dependencies, package management, and developer tooling. Apply whenever reading, writing, reviewing, or changing them. Specialised skills may refine these rules within their scope."
---

# Engineering practices

Apply these rules as the baseline for engineering work. When a narrower skill also applies, use both. The narrower skill may strengthen or refine these rules within its scope, but must not weaken them.

## Safety

- Never run or implement recursive deletion without explicit user consent.

## Design and types

- Prefer simple, strictly typed code that makes invalid states unrepresentable.
- Validate untrusted or untyped data at system seams, then trust established typed invariants. Never use `any`.
- Do not add speculative guards, fallbacks, or compatibility paths. Implement only behaviour required by the current system or request.

## Tests

- Write durable tests that protect observable behaviour or reproduce a regression.
- Do not add tests that merely prove an edit, an implementation detail, or a static type guarantee.

## Repository conventions

- Prefer pnpm for JavaScript and TypeScript package management.
- Prefer named exports. Use barrels for types only.

## Dependencies

- Add a dependency only when its maintenance, security, licence, transitive dependency, and runtime costs are justified.
