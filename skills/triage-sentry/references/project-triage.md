# Project-wide Sentry triage

## Resolve the project

1. Use an explicit `org/project` from the user's request or from the project-level `AGENTS.md` or `CLAUDE.md` that governs the current directory.
2. Otherwise let the CLI auto-detect a candidate, check it with a benign read, and ask the user to confirm it before collecting issues.
3. If auto-detection is missing, ambiguous, or wrong, ask for the Sentry organisation and project. Don't guess from a DSN, repository name, or an unrelated project.

When the target wasn't already known, ask whether to save the confirmed one, without blocking read-only triage. Single-issue triage never offers this. If the user agrees, add or update one entry:

```markdown
## Sentry

- Default project: `org/project`
```

Save it in `AGENTS.md` when the repository root's `CLAUDE.md` imports it, otherwise in the repository-root instruction file the current agent loads. If both files exist without an import and neither owns the entry, ask which should. Never use a user-global file. Preserve the existing instructions and avoid duplicate headings or entries.

## Collect the complete project

The scope is every issue visible to the authenticated user across the project's retained history, including unresolved, resolved, and archived or ignored issues. Fetch a fresh inventory with a time range broad enough to escape the CLI's default 90-day window. Query each status explicitly when the default list omits historical or archived issues, follow pagination to the end of each query, and deduplicate by numeric issue ID. One page, one status, or the requested page limit isn't the project.

For a large project, triage in bounded batches while keeping one compact, deduplicated ledger of report fields, classification, evidence summary, confidence, and proposed action. Discard raw event output. Keep a temporary ledger outside the repository, without sensitive payloads, and remove it after the final report. Batching must not drop issues or split one approval plan into partial reports.

## Project report

Return category sections covering every inventoried issue, an inventory table with one row per issue, and a numbered action plan. Give each issue's short ID and link, impact signals, evidence, likely cause with confidence, and recommended action. For a large project, keep routine notes to one table row and save longer analysis for high-impact or uncertain issues. State the statuses covered and any retention, pagination, or permission gap.
