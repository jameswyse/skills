---
name: typescript
description: Use when writing, changing, or reviewing TypeScript code. Skip read-only lookups.
---

# TypeScript

For implementation, design, debugging, or review, also use "engineering".

- Model variants as a discriminated union on a `kind` field instead of a boolean with optional fields.
- Brand semantic primitives as `string & { readonly __brand: "AgentId" }`, created only by a function that validates them.
- Keep `T[]` while every operation on it stays total. Use `[T, ...T[]]` only where the loose type forces `!`, a cast, or a "should never happen" throw.
- Treat external data as `unknown` and parse it with a schema into a named domain type where it enters. `Record<string, unknown>` stops at that parse.
- Prefer narrowing or `satisfies` to `as`. Assert only after validation, and put a proof TypeScript can't follow in a named guard, parser, or assertion function. Name guards `isX` or `hasX`, and make them check what they claim.
- End a switch over a union with `const _exhaustive: never = value;` in the default arm, followed by `return _exhaustive;` when the switch returns a value or `void _exhaustive;` when it doesn't.
- Derive types with `Pick`, `Omit`, `Parameters`, `ReturnType`, `Awaited`, and `typeof` before declaring a parallel shape.
- Pass an options object instead of positional arguments, except on hot paths such as render loops and parsers.
- Avoid boolean control parameters and `Partial<T>` inputs unless that shape is the domain.
- For a new project, enable `strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noImplicitOverride`, and `noFallthroughCasesInSwitch`. Treat enabling them in an existing project as a deliberate migration.
- Don't mock what you can run. Mock only what can't run locally.
- Log through the repository's structured logger instead of `console.log` in shipped code.
