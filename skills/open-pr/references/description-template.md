{Optional header line: links to the ticket, issue, plan, or related documents. Omit it when there are none.}

## Why the change

{One or two concise sentences, preferably one, explaining the problem this pull request solves and what becomes possible after it ships. Lead with the problem as the user saw it, not a list of what changed. Good: "Saved orders could show a different price from checkout, because the price was looked up again on save. Orders now keep the price the customer saw." Bad: "Moved the price lookup from `saveOrder` into `checkout`, added `lockedPrice`, and updated three callers."}

## Change outline

{Use the smallest combination of the following views that explains the implementation: blocks for shapes in the code and bullets for behaviour. Do not include headings for views that are not relevant.}

{...short description...}

```diff|sql|json|etc
{Show changed SQL tables, important columns and relationships, and endpoint request and response shapes.}
```

{...short description...}

```typescript|python|etc
{Show new data structures that are key to the implementation.}
```

{...short description...}

```diff|text
{Show concise pseudocode for changed logic with branches or ordering.}
```

- {Show behaviour that reads as a sentence, one bullet per behaviour, led by the area it affects, with identifiers in backticks.}

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

{Tell the story in the order that makes it easiest to understand. It may make sense to show files first, or to establish a data structure, SQL table, or API endpoint first. All views and subheadings are optional. Use only the views that help explain the pull request, and name or order them based on the change rather than a fixed template. Write as one person would write to another.}

## Notes

- {List 1-3 reviewer-relevant warnings, migrations, constraints, deliberate omissions, or surprising decisions. Use "None." when there are none.}

## Verification

- {List the checks that confirmed the change and their results. Omit checks that did not run and external or private references.}

<details>
<summary>How this change was reviewed</summary>

{The run report from "code-review": its table and outcome line. Omit this block when "code-review" did not run.}

</details>

> [!NOTE]
> 🤖 {Each model that worked on the change and its role, including reviewers, such as "Claude Opus 5.5 (implementation), GPT-6.1-Sol (code review)".}
