# Code standards

Judge whether a change expresses its behaviour with the least code and reader effort. Read the sections the scoped diff touches. Repository rules override these standards.

## Use the least machinery

Writing code is cheap for an agent, which makes over-engineering easy. Weigh the maintenance a human developer must bear. The simplest design has the least total complexity that still expresses the required behaviour. It doesn't mean fewer lines or files. A locally concise change that creates caller coordination, hidden state, or parallel paths makes the system more complex.

- Look for deletions before additions, and remove in-scope dead weight before adding supporting code.
- When a change threads a signal through several types, schemas, or layers, look for a more direct path.
- Judge reader load by two costs: the layers between a question and its answer, and the hidden or mutable state a reader must hold. Adjacent layers should change the abstraction. Derive values instead of synchronising copies.

## Model the domain

A new branch in a growing conditional, or a second boolean that must stay in sync with the first, signals a missing domain structure, such as a state machine, discriminated union, or lookup table. Don't demand an abstraction otherwise. Boring code is right when it's clear, local, and unlikely to grow, and repeated code is better than an abstraction that encodes guesses. For module depth and seam placement, use the engineering [Design](../../engineering/references/design.md) reference.

## Types and seams

The "typescript" skill holds the type conventions. Trace each `any`, unsafe cast, assertion, or impossible-case throw to the weak type or input seam that caused it, and fix it there. Derive types from protocol, OpenAPI, GraphQL, and database schemas instead of maintaining parallel shapes.

Keep business logic in pure functions and the framework shell thin. For seam placement and what seams expose, use the engineering [Design](../../engineering/references/design.md) reference.

## Failures

Return an expected failure, such as invalid input, a missing record, a conflict, or an unavailable dependency, in the type when the caller must branch on it. Throw for a defect or impossible state. Use the repository's result representation, or the smallest discriminated union, and don't add a result library in an unrelated change. Catch a third-party exception inside the adapter that owns the dependency and translate it there, keeping the original as `cause`.

## Reliable operations

A state-changing operation must converge to the correct state however many times it runs and wherever it resumes. Ask what happens if it runs twice, and if the previous run crashed halfway. Every retried mutation needs a concrete idempotency mechanism, such as an idempotency key, unique constraint, or guarded state transition. Don't hold a database transaction open across a network call.

Parse configuration at startup and pass typed values inward. Avoid import-time I/O and connections outside a true entrypoint.

When concurrent actors share mutable state, first ask whether they need the same object. Give independent facts separate files or keys and merge them where they're read. Two workers writing different fields of one `state.json` still share state, and an instruction to take turns isn't concurrency control. Enforce a real shared invariant with a lock, a single writer, or compare-and-swap.

## Migrations

A change that introduces a new internal interface migrates its callers and deletes the old path in the same change. Keep both paths only when external users need backward compatibility, and give a temporary adapter a stated reason and end point.

## Security

For a change at a security boundary, check authorisation at the server-side operation that owns the protected action, including tenant or object isolation, and look for evidence of both allowed and denied paths.

## Named smells

A smell is a lead. Report it only with the concrete maintenance or correctness cost in the diff and the smallest coherent response. Every smell finding is a labelled judgement call.

- **Code Comment.** The change adds a comment the global no-comments rule forbids, or keeps one in touched code that restates or contradicts the code.
- **Symptom Guard.** A null check, fallback, or catch silences invalid state instead of preventing it where it enters.
- **Parallel Path.** An old and new way to do the same thing coexist without a compatibility requirement.
- **Speculative Generality.** Abstraction, parameters, or hooks for needs nobody asked for.
- **Ternaryception.** A ternary nested inside a ternary that's already nested.
- **Unnecessary Complexity.** Concepts, state, branches, layers, dependencies, or paths the behaviour doesn't require. Don't flag essential domain complexity or line count.

## React Doctor

For a scope that affects React code, run the repository's `react-doctor` script or project-local executable when one is already runnable, with its existing configuration. Don't install or upgrade it during a review. Report the command, version, coverage, and counts, then only the diagnostics that support a scoped finding. If no runnable command exists, say so.

Report confirmed recurring false positives separately as configuration candidates, naming the diagnostic and the narrowest suppression that keeps real instances visible. List them under `## React Doctor configuration` after the three axes. They aren't findings, and configuration changes need the user's authorisation.
