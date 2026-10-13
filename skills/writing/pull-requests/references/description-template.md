{Optional header line: links to the ticket, issue, plan, or related documents. Omit it when there are none.}

## Why the change

{One or two concise sentences, preferably one, explaining the problem this pull request solves and what becomes possible after it ships.}

## Change outline

{Use the smallest combination of the following show-me-style views that explains the implementation. Prefer `diff` blocks for changes to existing shapes and complete blocks for mostly new shapes. Do not include headings for views that are not relevant.}

{...short description...}

```diff|sql|json|etc
{Show changed SQL tables, important columns and relationships, and endpoint request and response contracts.}
```

{...short description...}

```typescript|python|etc
{Show new data structures that are key to the implementation.}
```

{...short description...}

```diff
{Show concise pseudocode for the changed behaviour.}
```

{...short description...}

```diff
{Show a shallow file tree with changed responsibilities.}
```

{...short description...}

```diff
{Show changed React component trees, important hooks or state, and package boundaries.}
```

{...short description...}

```diff|mermaid
{Show changed call trees, call stacks, control flow, or data flow.}
```

{Tell the story in the order that makes it easiest to understand. It may make sense to show files first, or to establish a data structure, SQL table, or API contract first. All views and subheadings are optional. Use only the views that help explain the pull request, and name or order them based on the change rather than a fixed template. Write as one person would write to another. Use `diff` for a focused change to an existing shape. Show the complete target shape in a language-specific or `text` block when it is new, high level, or clearer without diff notation.}

## Notes

- {List 1-3 reviewer-relevant warnings, migrations, constraints, deliberate omissions, or surprising decisions. Use "None." when there are none.}

## Verification

- {List the checks that confirmed the change and their results. Omit checks that did not run and external or private references.}
