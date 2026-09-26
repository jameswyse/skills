# Code standards

Judge whether a change uses the structures, seams, and types that make its behaviour
straightforward, with the least code and reader effort. Read the sections the scoped diff touches.
Repository rules override these standards.

## Use the least machinery

Writing code is cheap for an agent, which makes over-engineering easy. Weigh the maintenance effort
a human developer must bear.

The simplest design has the least total complexity that still expresses the required behaviour and
constraints. Simplicity does not mean fewer lines, fewer files, or less explicit domain modelling.
A locally concise change that creates caller coordination, hidden state, or parallel paths makes the
system more complex.

- Prefer deletion. Look for removals before additions.
- Prefer the smallest change that solves the problem. Fewer lines beat elegant boilerplate.
- When a change threads a signal through types, schemas, pipelines, or similar layers, look for a
  more direct path.
- Remove in-scope dead weight before adding supporting code.

If a human developer would find the code exhausting to maintain, it needs simplifying.

## Minimise reader load

Maintainability is the work a reader must do to understand code. Track two independent costs:

1. **Layers to trace.** Count the indirections between the question and the answer.
2. **State to hold.** Count the hidden or mutable facts the reader must keep in mind.

Adjacent layers should change the abstraction. A wrapper with one caller, indirection added for a
hypothetical future, or a layer that repeats the same methods and arguments adds reader load without
compression. For module depth, interface compression, and seam placement, use the engineering
[Design](../../engineering/references/design.md) reference.

Shrink state scope. Prefer pure functions over mutation, locals over fields, fields over module
state, and module state over globals. Derive values instead of synchronising copies. Name an
invariant at the interface so each consumer learns it once. A new reader should be able to find
where state comes from and what can change it without tracing unrelated indirection.

## Model the domain

Encode the real domain in a data structure instead of scattering it across conditionals. Scattered
booleans, repeated shape assumptions, and branching across files are accidental complexity. Match
structures to their dominant access paths.

Useful structures include:

- A state machine instead of scattered booleans, phases, or lifecycle checks.
- A typed model instead of loose parameters or repeated shape assumptions.
- A map, registry, lookup table, or discriminated union instead of branching spread across files.
- A reducer or command and event model instead of ad hoc state mutations.
- A module organised around one body of domain knowledge instead of execution phases such as load,
  validate, transform, and save.
- A queue, cache, index, graph, tree, or normalised collection when the access pattern calls for it.

Do not demand an abstraction. Boring code is correct when the current shape is clear, local, and
unlikely to grow. An abstraction must remove branches, duplicated rules, invalid states, or
lifecycle risk. A new branch in a growing conditional or a second boolean that must stay in sync
signals a missing domain structure. Keep repeated code when an abstraction would encode guesses.

## Place responsibilities by what changes them

These responsibilities place a decision. They do not require separate folders, classes, or layers.

- Domain code owns meaning, invariants, calculations, and legal state transitions.
- Application code owns authorisation, policy, coordination, and effect ordering for one operation.
- Adapter code owns framework, protocol, storage, runtime, and third-party translation.
- Entrypoint code owns construction, configuration, and resource wiring.

A simple operation can stay together when splitting it would add pass-through calls or hypothetical
seams. Split mixed code only when the responsibilities change for different reasons or the
separation removes repeated coordination. Apply the repository's established vocabulary when it
names these responsibilities clearly.

## Use the type system as a proof assistant

Types should eliminate impossible states, mismatched primitives, and unhandled variants at compile
time.

- **Make illegal states unrepresentable.** `{ completed: boolean; completedAt?: Date }` permits a
  completed item without a completion time. Derive completion from one value or model open and
  completed variants explicitly. If a comment must explain which field combinations are valid, the
  type should encode them.
- **Construct types from legal values.** A non-empty list is a head plus a rest. A valid time range
  is a start plus a duration.
- **Brand semantic primitives.** Identifiers with different meanings should not be interchangeable
  merely because they share a primitive representation. Validate once at creation.
- **Treat external data as untyped until parsed.** Parse network payloads, files, configuration,
  environment variables, database rows, and messages into the typed model at their input seam.
- **Do not lie to the type system.** Trace each `any`, unsafe cast, assertion, or impossible-case
  throw to the input seam or weak type that caused it, and correct that source.
- **Match variants exhaustively.** Adding a variant should make every incomplete match fail
  compilation.
- **Derive from authoritative schemas.** Generate or derive types from protocol, OpenAPI, GraphQL,
  database, and token definitions instead of maintaining parallel shapes.
- **Strengthen a type only where partiality appears.** Do not demand precision that buys no safety
  and reduces reuse.

For TypeScript syntax and examples, use the "typescript" skill.

## Keep discipline at seams

Validation, type narrowing, error handling, and framework adaptation belong at system seams. Inside
the system, typed data propagates without repeated validation. If data is not crossing a seam, an
added validation check is probably redundant.

- Seams expose domain concepts, not transport, storage, framework, or wire representations.
- Raw records, SDK values, and provider-specific failures stay inside the owning adapter or
  entrypoint.
- General mechanism sits inside and special policy at the edge.
- Business logic stays in pure functions, and the framework shell stays thin. When framework wiring
  could call a pure function, the decision should move out of the shell.

## Failures and diagnostics

An expected failure is part of normal operation, such as invalid input, a missing record, denied
access, a conflict, an unavailable dependency, or a rejected state transition. A defect violates an
internal invariant or reveals a programming error.

- Represent an expected failure in the return type when a caller must branch, retry, report, or
  translate it. Throw or reject for a defect, an impossible state, or framework-required behaviour.
- Treat a configuration error as an expected startup failure, reported safely at the entrypoint.
- Use the repository's established result representation. Otherwise use the smallest discriminated
  union that expresses the caller's decisions. Do not add a result library in an unrelated change.
- Combine low-level failures that lead to the same caller decision, but preserve the context needed
  to diagnose them.
- Use a stable discriminant or error code, a useful message, and structured context that identifies
  the operation and affected domain value.
- Keep failure unions precise near domain and application interfaces. Broaden them only near
  orchestration, logging, and presentation code.

Catch an unclassified third-party exception or rejection inside the adapter that owns the
dependency, and translate it before it crosses that seam. Preserve the original as `cause: unknown`
when supported. At the outer seam, translate application failures into protocol outcomes such as an
HTTP response, CLI exit, queue decision, or startup message. Preserve established logging, tracing,
metrics, and error-reporting hooks.

Secrets, credentials, tokens, and raw sensitive payloads never belong in errors, logs, traces,
metrics, or snapshots. Use safe identifiers, operation names, error codes, and redacted summaries.
Use the repository's redacted-value type when one exists.

## Reliable operations

A state-changing operation must converge to the correct state however many times it runs or wherever
it resumes. Ask what happens if it runs twice and what happens if the previous run crashed halfway.
Convergent startup, content-based cleanup, self-healing locks with liveness checks, and scheduling
that regenerates fresh input for each cycle are useful patterns. If the result depends on leftover
partial state, the operation needs reconciliation.

- Use an ordinary call or a database transaction for work within one process and transactional
  boundary. Use a persistent workflow only when progress or retries must survive process loss or
  redelivery.
- Keep database transactions short. Do not hold one open across a network call.
- Put short technical retries beside the external operation, application retry policy with the
  operation that knows whether another attempt is valid, and crash-resistant retries in the workflow
  that records their progress.
- Every retried mutation needs a concrete idempotency mechanism, such as an idempotency key, a unique
  constraint, a deduplication record, a guarded state transition, or a transactional outbox.

Parse environment variables and configuration at startup or the earliest entry seam, then pass typed
configuration inward. Keep resource creation, use, and cleanup under an explicit owner. Avoid
import-time I/O, connection creation, server startup, and handler registration outside a true
entrypoint. Pass a clock or random source through the nearest useful interface when behaviour
depends on time or randomness.

When concurrent actors might share mutable state, first ask whether they need the same mutable
object. Give independent facts separate owned files, keys, or state directories and merge them at
the read seam. When sharing is a real invariant, enforce serialisation structurally with a lock,
sequential phase, single writer, or compare-and-swap. Two workers writing different fields in one
`state.json` still share mutable state. Instructions to "take turns" are not concurrency control.

## Migrations and legacy paths

When a change introduces a new internal interface, it should migrate the callers and delete the old
path in the same change. Types, tests, documentation, and examples should all express the chosen
design. Tests that only protect the old implementation path should go. A temporary adapter needs a
stated reason and an end point. Keeping both paths is acceptable only when external users require
backward compatibility.

## Security and dependencies

For a change to a security boundary, identify the protected assets, attacker-controlled inputs,
trust boundaries, and credible misuse paths. Authentication and authorisation are separate decisions.
Authorisation belongs at the server-side operation or data boundary that owns the protected action.
Credentials and permissions should have only the scope they need. Look for evidence of allowed and
denied paths, including object or tenant isolation when applicable.

A new dependency needs its maintenance, security, licence, provenance, transitive dependency,
install-time code, and runtime costs justified by the required behaviour. Prefer established
repository tools that already solve the problem.

## Named smells

Smells are evidence to investigate, not automatic refactoring instructions. Confirm the concrete
maintenance or correctness cost in the diff, then report the smallest coherent response. Every
smell finding is a labelled judgement call:

- **Mysterious Name.** A name hides what it does or holds. Rename it. If no honest name exists,
  clarify the design.
- **Duplicated Code.** The same logic shape recurs. Share one owner when the copies express the same
  stable rule and must change together.
- **Feature Envy.** A method reaches into another object's data more than its own. Move the behaviour
  only when the other module owns the knowledge it needs.
- **Data Clumps.** The same fields or parameters travel together. Introduce one type when they form
  a domain concept or share an invariant.
- **Primitive Obsession.** Interchangeable primitives represent distinct domain concepts. Add a
  semantic type when it prevents invalid mixing or centralises validation.
- **Repeated Switches.** The same decision over one domain type recurs. Put the rule in one owner,
  such as a domain model, map, registry, or polymorphic implementation.
- **Ternaryception.** A ternary is nested inside a ternary that is already nested. One level of
  nesting is fine. Beyond that, replace the expression with named branches, a lookup, or a switch.
- **Shotgun Surgery.** One logical change requires scattered edits. Gather what changes together.
- **Divergent Change.** One module changes for unrelated bodies of knowledge. Split it only when the
  result has stronger cohesion and less total reader load.
- **Speculative Generality.** Unused abstraction, parameters, or hooks anticipate unasked needs.
  Delete or inline them.
- **Message Chains.** Callers must understand a long `a.b().c().d()` chain. Move the required
  knowledge to its owner or expose a direct operation when that reduces coupling.
- **Middle Man.** A module mainly delegates. Apply the deletion test. Remove it when its complexity
  disappears, but keep an interface that hides real decisions or coordination.
- **Refused Bequest.** A subtype ignores inherited behaviour or violates the base type's
  expectations. Prefer composition when inheritance does not describe a valid substitution.
- **Parallel Path.** An old and a new way to do the same thing coexist without a compatibility
  requirement. Migrate the remaining callers and delete the old path.
- **Symptom Guard.** A null check, fallback, or catch silences invalid state instead of preventing it
  where it enters. Move the fix to the source.
- **Unnecessary Complexity.** The change adds concepts, state, branches, layers, dependencies, or
  execution paths that its behaviour and constraints do not require. Name the concrete maintenance
  or correctness cost and the smallest coherent alternative. Do not flag essential domain complexity
  or mere line count.

## React Doctor

For a scope that affects React code, apply these instructions to the Standards review in either mode:

- Check for a repository package script or project-local `react-doctor` executable.
- If one is already runnable, use it with the repository's existing configuration. Leave installs
  and upgrades outside the review.
- Return a concise execution summary with the command, version when available, scope or coverage,
  and counts.
- Return only diagnostics relevant to scoped findings or configuration candidates.
- If no runnable command exists, state that.

### Findings and configuration candidates

Include every React Doctor diagnostic that supports an issue in the scoped diff, with its location. Separately report confirmed recurring false positives or repository-accepted patterns. Name the diagnostic, explain why it is non-actionable, and propose the narrowest suppression that keeps actionable instances visible. Configuration candidates are not findings.

Verify each candidate against the diagnostic, code, and current configuration. If necessary, run the narrowest check that resolves uncertainty. Reject unsupported candidates and suppressions that could hide real issues.

After Standards and Spec, list supported candidates under `## React Doctor configuration`. Explain the repeated noise each would remove. Omit the section when there are none. Change configuration only when the user has authorised it; carry forward existing authority and otherwise ask about the concrete proposal.
