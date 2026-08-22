# Design and maintainability

Choose structures, seams, and types that make the requested behaviour straightforward. Aim for the most result with the least code and reader effort.

## Design for the people who use the work

The user is whoever consumes the work. For a library or internal interface, that is the colleague who imports it. The engineer who maintains the code next is a user too. Weigh their experience alongside implementation cost, and explain impact from their seat.

Foundations should serve the experience. Foundational thinking governs the sequence of work. The intended experience governs the target.

## Redesign from the requirement

When a new requirement challenges the current design, treat it as if it had existed when the system was first designed. Retain constraints that still matter, rather than preserving structure only because it already exists.

1. Read the affected implementation, types, tests, documentation, and examples until the current design and its constraints are clear.
2. Describe the design the requirement naturally calls for. Define the core types and data shapes, then trace how each caller reads or changes them.
3. Compare that target with the current design and identify the smallest coherent migration.
4. Confirm that the target expresses the requirement directly through its types, structures, state ownership, and interfaces, rather than through caller coordination or a special-case layer.

When producing a design, state the chosen foundation, rejected alternatives, and implementation sequence. When implementing, build from that foundation.

## Use the least machinery

Fight for simplicity throughout design and implementation. Writing code is cheap for an agent, which makes over-engineering easy. Account for the maintenance effort a human developer must bear.

The simplest design is the one with the least total complexity that still expresses the required behaviour and constraints. Do not confuse simplicity with fewer lines, fewer files, or less explicit domain modelling. A locally concise change that creates caller coordination, hidden state, or parallel paths makes the system more complex.

- Prefer deletion. When refactoring or improving, look for removals before additions.
- Maintain a flat call hierarchy. A rich interface that hides substantial work is useful. A chain of pass-through calls is not. If answering a question requires tracing through more than three files or layers, flatten it.
- Consolidate decisions. Put one choice behind one source of truth instead of repeating it across callers.
- Make the smallest change that solves the problem. Fewer lines beat elegant boilerplate.
- When a change threads a signal through types, schemas, pipelines, or similar layers, look for a more direct path.
- Remove small pass-throughs, representation leaks, and duplicated choices before they spread.
- Remove in-scope dead weight before adding supporting code. Put foundations that benefit every later phase, such as shared types or necessary test infrastructure, before feature work.

If a human developer would find the code exhausting to maintain, simplify it.

## Minimise reader load

Maintainability is the work a reader must do to understand code. Track two independent costs:

1. **Layers to trace.** Count the indirections between the question and the answer.
2. **State to hold.** Count the hidden or mutable facts the reader must keep in mind.

Collapse layers that do not earn their keep: wrappers with one caller, adapters with no second implementation, and indirection added for a hypothetical future. Adjacent layers should change the abstraction. A layer that repeats the same methods and arguments adds reader load without compression.

Demand interface compression. A broad interface that hides little complexity makes readers learn both the interface and its implementation. Prefer interfaces that hide meaningful decisions.

Shrink state scope. Prefer pure functions over mutation, locals over fields, fields over module state, and module state over globals. Derive values instead of synchronising copies. Name an invariant at the interface so each consumer learns it once.

Identify who owns each state transition. When concurrent actors can change the same state, isolate their writes or define explicit serialisation.

Before adding a layer or mutable state, ask whether it reduces reader load elsewhere by at least as much. A new reader should be able to answer "where does this come from?" and "what can change it?" in under 30 seconds. If not, cut layers or state.

## Model the domain

Encode the real domain in a data structure instead of scattering it across conditionals. Scattered booleans, repeated shape assumptions, and branching across files are accidental complexity. Choosing the structure while writing a feature is cheaper than recovering it in a later refactor.

Match structures to their dominant access paths. Trace how callers read and change the data so the model supports real operations rather than an imagined general case.

Reach for structures such as:

- A state machine instead of scattered booleans, phases, or lifecycle checks.
- A typed model instead of loose parameters or repeated shape assumptions.
- A map, registry, lookup table, or discriminated union instead of branching spread across files.
- A reducer or command and event model instead of ad hoc state mutations.
- A module organised around one body of domain knowledge instead of execution phases such as load, validate, transform, and save.
- A small module whose interface gathers repeated behaviour, ownership, or invariants.
- A queue, cache, index, graph, tree, or normalised collection when the access pattern calls for it.

When none of those structures fits, identify what the code must never allow and how the data is read, then choose a structure that encodes those facts.

Do not force an abstraction. Prefer boring code when the current shape is clear, local, and unlikely to grow. An abstraction must remove branches, duplicated rules, invalid states, or lifecycle risk. A new branch in a growing conditional or a second boolean that must stay in sync signals a missing domain structure. Modules named after execution phases are another signal because they often repeat the same domain rules across steps.

Converge types and data models when the domain is established, but keep repeated code when an abstraction would encode guesses. Prefer explicit coordination inside one coherent abstraction over special cases spread across callers.

## Use the type system as a proof assistant

Use types to eliminate impossible states, mismatched primitives, and unhandled variants at compile time. Prefer defining errors and special cases out of existence over proliferating handlers.

- **Make illegal states unrepresentable.** Model variants as sum types such as discriminated unions, enums with payloads, sealed classes, or algebraic data types. Do not use a bag of optional fields when contradictory combinations can compile. `{ completed: boolean; completedAt?: Date }` permits a completed item without a completion time. Derive completion from one value or model open and completed variants explicitly.
- **Construct types from legal values.** A non-empty list is a head plus a rest. A valid time range is a start plus a duration. Choose a representation that cannot construct the illegal value.
- **Brand semantic primitives.** Identifiers with different meanings should not be interchangeable merely because both use the same primitive representation. Validate once at creation and trust the type downstream.
- **Treat external data as untyped until parsed.** Parse network payloads, files, configuration, environment variables, database rows, and messages into the typed model at their input seam.
- **Do not lie to the type system.** Validate or narrow facts the compiler cannot prove. Treat unsafe casts and coercions as hazards.
- **Match variants exhaustively.** Adding a variant should make every incomplete match fail compilation.
- **Derive from authoritative schemas.** Generate or derive types from protocol, OpenAPI, GraphQL, database, and token definitions instead of maintaining parallel shapes.
- **Strengthen a type only where partiality appears.** A runtime assertion, null check, or impossible-case throw marks a weak type. Do not add precision that buys no safety and reduces reuse.

For TypeScript syntax and examples, apply `$typescript-best-practices`.

Use these checks:

- If a comment must explain which field combinations are valid, split the shape into explicit variants.
- If arguments share a primitive representation but have different meanings, brand them.
- Trace each `any`, cast, assertion, or impossible-case throw back to the input seam or weak type that caused it.
- Adding a variant should make the compiler identify every incomplete match.
- Derive a type when another schema or generated definition already owns its shape.
- Strengthen a type to keep an operation total, not merely to make the type more precise.

## Keep discipline at seams

Place validation, type narrowing, error handling, and framework adaptation at system seams. Trust established typed invariants inside the system. Keep business logic in pure functions and make the shell thin and mechanical.

- At CLI, configuration, network, storage, and external API seams, validate and return useful errors.
- Parse raw input into domain types at the input seam.
- Inside the system, propagate typed data without repeated validation.
- Expose domain concepts across a seam instead of transport, storage, framework, or wire representations.
- Keep general mechanism inside and special policy at the edge.
- Prefer pure transforms for parsing, prompt construction, scoring, and assessment.

Ask whether data is crossing a system seam now. If not, another validation check is probably redundant. Ask whether framework wiring can call a pure function. If it can, extract the decision from the framework shell.
