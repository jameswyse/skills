# TypeScript patterns

Code examples for each rule in `SKILL.md`. The language-agnostic type and seam rules live in `$engineering`'s design reference.

## Branded types

Brand primitives so they cannot be mixed up. Validate once at creation. Downstream code trusts the type.

```ts
type AgentId = string & { readonly __brand: "AgentId" };

function parseAgentId(input: string): AgentId {
  if (!isUUID(input)) throw new Error(`Invalid agent id: ${input}`);
  return input as AgentId;
}

function focusAgent(id: AgentId): void {
  /* input is trusted */
}
```

Match the `readonly __brand: 'X'` shape. Do not invent a new convention.

## Discriminated unions

If a bug makes a field combination questionable, the type is too loose. Model variants with a literal discriminant. Every variant shares the field name and each variant's value is unique, so impossible combinations cannot be represented.

```ts
// Don't. Boolean + optionals lets contradictory states exist.
type DiffState = { loading: boolean; diff?: GitDiff; error?: string };

// Do. Only valid states exist.
type DiffState =
  | { kind: "loading" }
  | { kind: "ready"; diff: GitDiff }
  | { kind: "error"; error: string };
```

Pick one discriminant name (`kind`, `type`, `tag`) and stick to it.

## Constructive modelling

Build the type from parts that are all legal instead of restricting a loose type with runtime checks. Adding is easier than subtracting.

Non-empty, via a variadic tuple:

```ts
type NonEmpty<T> = [T, ...T[]];

// Don't: T[] plus a length check every caller must repeat
function pickWinner(entries: string[]): string {
  if (entries.length === 0) throw new Error("no entries");
  return entries[Math.floor(Math.random() * entries.length)];
}

// Do: an empty value of the type can't exist
function pickWinner(entries: NonEmpty<string>): string {
  return entries[Math.floor(Math.random() * entries.length)];
}
```

Where a plain `T[]` arrives, narrow once with a guard. The fact then travels in the type:

```ts
const isNonEmpty = <T>(arr: T[]): arr is NonEmpty<T> => arr.length > 0;
```

Represent even length as pairs. TypeScript has no refinement types for facts such as `arr.length % 2 === 0` at the type level. You do not need one:

```ts
type Pairs<T> = [T, T][];
```

A time range, as start plus duration:

```ts
// Don't: a comment holds the invariant
type TimeRange = { start: Date; end: Date }; // start <= end

// Do. A negative range cannot be written. Derive the end when needed.
type TimeRange = { start: Date; durationMs: number };
```

Keep `durationMs` a plain number. Brand it (per Branded types) only if a raw number could be passed where a duration is expected, not by reflex. A `Pairs<T>` is an even-length list under the interpretation you give it, the same way `{ start, durationMs }` is a range. Pick the representation that makes the bad state unconstructable, then expose the reading you need on top (`pairs.flat()`, a `rangeEnd()` helper).

## Simplest total type

Don't strengthen everything. Keep `T[]` when every operation on it is total:

```ts
const sum = (xs: number[]) => xs.reduce((a, b) => a + b, 0); // [] is 0, fine
```

Strengthen when the loose type forces a lie at a use site. The tells are `!`, `arr[0] as T`, and a "should never happen" throw:

```ts
// Don't. The assertion hides partiality from the compiler.
function newestSession(sessions: Session[]): Session {
  return sessions.at(0)!;
}

// Do. Strengthen the input so the assertion disappears.
function newestSession(sessions: NonEmpty<Session>): Session {
  return sessions[0];
}
```

Weakening the result to `Session | undefined` is the other total signature. Either way, the call site handles the empty case because it knows what empty means.

## `unknown` over `any`

`any` disables type checking for everything it touches. External data is always `unknown`. Narrow before use.

```ts
// Don't
function handle(input: any) {
  return input.foo.bar;
}

// Do
function handle(input: unknown) {
  if (typeof input === "object" && input !== null && "foo" in input) {
    // Narrowed. The compiler verifies access.
  }
}
```

External sources include RPC payloads, `JSON.parse`, `postMessage`, IPC, file contents, environment variables, database results.

## No `as` casts

An unchecked `as` cast can cause a runtime crash. Cast only after the type system has verified the claim.

```ts
// Don't
const user = data as User;

// Do. Earn the cast at the input seam.
function parseUser(data: unknown): User {
  if (typeof data !== "object" || data === null) {
    throw new Error("expected object");
  }
  if (!("id" in data) || typeof (data as Record<string, unknown>).id !== "string") {
    throw new Error("expected id");
  }
  // ... validate all fields
  return data as User; // OK, earned cast after full validation
}
```

When refactoring an `as` out of existing code, identify why TypeScript can't infer:

- Missing discriminant: add one, switch to a discriminated union.
- Overly wide source type (e.g. `Record<string, unknown>`): narrow it.
- Untyped input seam: add a parse function or schema.
- Genuinely inexpressible: use a branded type or `satisfies`.

## Narrowing hierarchy

From best to last-resort:

1. **Discriminated union switch or `if`.** The compiler narrows automatically.
2. **`in` operator.** `"key" in obj` narrows to variants containing that key.
3. **`typeof` or `instanceof`.** Use these for primitives and class instances.
4. **User-defined type guard.** When the above aren't enough.
5. **`as` cast.** Only after validation.

```ts
function area(s: Shape): number {
  if ("radius" in s) return Math.PI * s.radius ** 2; // narrowed to circle
  return s.width * s.height; // narrowed to rect
}
```

## Type guards

A guard must verify its claim. A false guard is worse than `as` because its misleading name makes the bug harder to find.

```ts
function isCircle(s: Shape): s is Shape & { kind: "circle" } {
  return s.kind === "circle";
}
```

Prefer discriminant narrowing when possible. The guard adds a layer the reader has to follow.

## Exhaustiveness

In default arms, assign the discriminant to a `never`-typed local. The compiler errors if a new variant is added without handling.

```ts
// Value-returning switch
function area(s: Shape): number {
  switch (s.kind) {
    case "circle":
      return Math.PI * s.radius ** 2;
    case "rect":
      return s.width * s.height;
    default: {
      const _exhaustive: never = s;
      return _exhaustive;
    }
  }
}

// Void switch
function handle(s: Shape): void {
  switch (s.kind) {
    case "circle":
      drawCircle(s);
      break;
    case "rect":
      drawRect(s);
      break;
    default: {
      const _exhaustive: never = s;
      void _exhaustive;
    }
  }
}
```

Use the return style in value-returning switches. Use the void style in statement switches.

## `satisfies` over `as`

`satisfies` validates without widening literal types.

```ts
// Don't. Widens, loses literal types.
const config = { theme: "dark", cols: 3 } as Config;

// Do. Validates AND preserves literal types.
const config = { theme: "dark", cols: 3 } satisfies Config;
// config.theme is "dark" (literal), not string
```

## Seam validation

Validate once where data enters. Trust types inside. Read `$engineering`'s design reference for seam placement.

- **Wire formats** (proto, JSON-RPC): parse with `ignoreUnknownFields` so forward-compatible changes don't break old clients.
- **Persisted JSON.** Use a versioned blob with `try` and `catch` around the parse.
- **Don't re-validate** deep in call chains.

## Schema-derived types

When a `.proto`, OpenAPI spec, GraphQL schema, or database migration already defines a shape, derive from the generated types instead of duplicating them.

```ts
// Don't. Duplicate shape, drifts when the schema changes.
type CheckSummary = {
  totalCount: number;
  checks: { name: string; status: string }[];
};
function renderChecks(s: CheckSummary) {
  /* ... */
}

// Do. Derive from the generated schema type.
import type { ChecksMessage } from "<generated module>";
function renderChecks(s: Pick<ChecksMessage, "totalCount" | "checks">) {
  /* ... */
}
```

Reach for `Pick`, `Omit`, `Parameters`, `ReturnType`, `Awaited`, or `typeof` before writing a new interface.

## Object args

```ts
// Don't. Swap two args, still compiles.
openFile(uri, {
  startLineNumber: 10,
  startColumn: 1,
  endLineNumber: 10,
  endColumn: 1,
});

// Do. Order-independent, self-documenting.
openFile({
  uri,
  selection: {
    startLineNumber: 10,
    startColumn: 1,
    endLineNumber: 10,
    endColumn: 1,
  },
});
```

Skip on hot paths: per-frame render, tokenisers, parsers, anything in a tight loop where the allocation cost matters.
