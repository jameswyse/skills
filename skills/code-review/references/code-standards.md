# Code standards

Judge whether a change expresses its behaviour with the least code and reader effort. Read the sections the scoped diff touches. Repository rules override these standards.

## Use the least machinery

Code is cheap for an agent to write and costly for a person to maintain. The simplest design has the least total complexity that still expresses the behaviour, which isn't the fewest lines or files. A locally concise change that creates caller coordination, hidden state, or parallel paths makes the system more complex.

- Look for deletions before additions, and remove in-scope dead weight before adding supporting code.
- When a change threads a signal through several types, schemas, or layers, look for a more direct path.
- Judge reader load by the layers between a question and its answer, and the hidden or mutable state a reader must hold. Adjacent layers should change the abstraction. Derive values instead of synchronising copies.
- A new branch in a growing conditional, or a second boolean that must stay in sync with the first, signals a missing state machine, discriminated union, or lookup table. Otherwise don't demand an abstraction. Repeated code beats one that encodes guesses.

## Types, failures, and seams

- Trace each `any`, unsafe cast, assertion, or impossible-case throw to the weak type or input seam that caused it, and fix it there. The "typescript" skill holds the type conventions.
- Derive types from protocol, OpenAPI, GraphQL, and database schemas instead of maintaining parallel shapes.
- Return an expected failure, such as invalid input, a missing record, a conflict, or an unavailable dependency, in the type when the caller must branch on it, using the repository's result representation or the smallest discriminated union, without adding a result library in an unrelated change. Throw for a defect or impossible state.
- Catch a third-party exception inside the adapter that owns the dependency and translate it there, keeping the original as `cause`.
- Check an HTTP response's status before decoding its body as the success type, and read each body once.
- Keep business logic in pure functions and the framework shell thin. For module depth and seam placement, use the engineering [Design](../../engineering/references/design.md) reference.

## Reliable operations

- A state-changing operation must converge however many times it runs and wherever it resumes. Every retried mutation needs a concrete idempotency mechanism, such as an idempotency key, unique constraint, or guarded state transition.
- Don't hold a database transaction open across a network call.
- A write that depends on an earlier read of the same record needs a conditional update, upsert, row lock, or unique constraint, because another writer can change the record between the read and the write.
- Bound every retry by attempts, elapsed time, or a timeout, and retry only failures that a later attempt can fix. Bound concurrency when the number of items comes from input or stored data, such as files, rows, or accounts.
- Create a cache once, when its owner is built, not inside a function that runs on every call. Use the platform's cache before hand-building one from a map, timestamps, and timers.
- Parse configuration at startup and pass typed values inward, with no import-time I/O outside a true entrypoint.
- When concurrent actors share mutable state, first ask whether they need the same object. Give independent facts separate files or keys and merge them where they're read. Two workers writing different fields of one `state.json` still share state, and an instruction to take turns isn't concurrency control. Enforce a real shared invariant with a lock, a single writer, or compare-and-swap.
- A change that introduces a new internal interface migrates its callers and deletes the old path in the same change. Keep both only for external backward compatibility, and give a temporary adapter a stated reason and end point.
- At a security boundary, check authorisation at the server-side operation that owns the protected action, including tenant or object isolation, with evidence of both allowed and denied paths.

## Named smells

Every smell finding is a labelled judgement call. Report one only with its concrete cost in the diff and the smallest coherent response.

- **Code Comment.** The change adds a comment the global no-comments rule forbids, or keeps one in touched code that restates or contradicts the code. For another author's change, report only a comment that contradicts the code, unless the repository's rules or conventions forbid comments.
- **Symptom Guard.** A null check, fallback, or catch silences invalid state instead of preventing it where it enters.
- **Mysterious Name.** A function or value name, such as `handle`, `process`, or `getData`, doesn't say what it does, what it returns, or which effects it has, so readers must open it to find out.
- **Parallel Path.** An old and new way to do the same thing coexist without a compatibility requirement.
- **Speculative Generality.** Abstraction, parameters, or hooks for needs nobody asked for.
- **Ternaryception.** A ternary nested inside a ternary that's already nested.
- **Unnecessary Complexity.** Concepts, state, branches, layers, dependencies, or paths the behaviour doesn't require. Don't flag essential domain complexity or line count.

## React Doctor

For a scope that affects React code, run the repository's `react-doctor` script or project-local executable when one is already runnable, with its existing configuration. Don't install or upgrade it during a review. Report the command, version, coverage, and counts, then only the diagnostics that support a scoped finding. If no runnable command exists, say so.

Report confirmed recurring false positives separately under `## React Doctor configuration` after the three axes, naming the diagnostic and the narrowest suppression that keeps real instances visible. They aren't findings, and configuration changes need the user's authorisation.
