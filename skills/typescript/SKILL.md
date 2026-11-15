---
name: typescript
description: Use when writing, changing, or reviewing TypeScript code. Skip read-only lookups.
---

# TypeScript

- Model variants as a discriminated union on a `kind` field instead of a boolean with optional fields. When the type already has a field that names the variant, such as an existing `status`, discriminate on that field instead of adding `kind`.
- Brand semantic primitives as `string & { readonly __brand: "AgentId" }`, created only by a function that validates them.
- Parse external data from `unknown` with a schema into a named domain type where it enters. `Record<string, unknown>` stops at that parse.
- Assert only after validation, and put a proof TypeScript can't follow in a named guard, parser, or assertion function. Name guards `isX` or `hasX`, and make them check what they claim.
- End a switch over a union with `const _exhaustive: never = value;` in the default arm, followed by `return _exhaustive;` when the switch returns a value or `void _exhaustive;` when it doesn't.
- Avoid boolean control parameters and `Partial<T>` inputs unless that shape is the domain.
- Don't mock what you can run. Mock only what can't run locally.
