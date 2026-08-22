---
name: typescript-best-practices
description: TypeScript best practices. Use when reading or editing any .ts or .tsx file.
---

# TypeScript best practices

Apply `$engineering` first. This skill grounds its type and seam rules in TypeScript syntax.

| Rule | Summary |
|------|---------|
| Discriminated unions | Model variants with a `kind` literal discriminant so impossible states can't be represented. No optional-field bags. |
| Branded types | Brand primitives with `& { readonly __brand: "X" }` so they can't be mixed up. Validate once at creation. |
| Constructive modelling | Choose representations that remove invalid combinations. Use `[T, ...T[]]` for non-empty, `[T, T][]` for pairs, and `start` plus a validated duration for a range. Type structure owns structural invariants. Runtime validation owns numeric constraints TypeScript cannot express. |
| Simplest total type | Keep `T[]` while every operation on it stays total. Strengthen to `NonEmpty<T>` only where the loose type forces `!`, a cast, or a "should never happen" throw. |
| `unknown` over `any` | External data is `unknown`. `any` disables type checking everywhere it touches. |
| Avoid unchecked `as` assertions | An assertion bypasses type checking and can hide a runtime bug. Prefer narrowing or `satisfies`. Assert only after validation or when expressing a proven invariant TypeScript cannot infer. |
| Narrowing hierarchy | Discriminant switch > `in` operator > `typeof`/`instanceof` > user-defined type guard > `as`. |
| Type guards | Must verify the claim. A lying guard is worse than `as` because the bug hides behind a name that says it's safe. Name them `isX` or `hasX`. |
| Exhaustiveness | Inline `const _exhaustive: never = x;` in default arms so the compiler errors when a new variant is added. |
| `satisfies` over `as` | Validates the value without widening literal types. |
| Seam validation | Parse where data crosses in, into a named domain type. `Record<string, unknown>` (however spelt) stops at that parse. Trust types inside. Read `$engineering`'s design reference for seam placement. |
| Schema-derived types | Reach for `Pick`/`Omit`/`Parameters`/`ReturnType`/`Awaited`/`typeof` before declaring a new interface. |
| Object args | Pass objects, not positional, so argument order is self-documenting. Skip on hot paths (per-frame render, tokenisers, parsers). |
| Real tests | Don't mock what you can run. Prefer the framework's real test primitives with leak checks and disposable resources. Verify UI in a running build. Mock only what you can't run locally. |
| Structured telemetry | Prefer structured logger diagnostics with enough context to debug from an id. No `console.log` in shipped code. |

Examples: `references/patterns.md`.
