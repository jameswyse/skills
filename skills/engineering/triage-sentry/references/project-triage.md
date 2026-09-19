# Project-wide Sentry triage

In project-wide mode, treat the target as known only when the user supplied it or the project-level `AGENTS.md` or `CLAUDE.md` records it. Resolve the Sentry target in this order:

1. Use an explicit `org/project` from the user's request or the project-level agent instructions that govern the current directory.
2. Otherwise, let the CLI auto-detect a candidate and check it with a benign read. Ask the user to confirm the candidate before collecting issues.
3. If auto-detection is missing, ambiguous, or wrong, ask the user for the Sentry organisation and project. Do not guess from a DSN, repository name, or an unrelated project.

Whenever a project-wide target was not already known, ask whether to save the confirmed target in the project-level agent instructions. If they agree, add or update one concise entry under a `## Sentry` heading:

```markdown
## Sentry

- Default project: `org/project`
```

If the repository root's `CLAUDE.md` imports `AGENTS.md`, save the entry in `AGENTS.md`. Otherwise, use the repository-root instruction file loaded by the current agent. If both files exist without an import and neither owns the Sentry entry, ask the user which file should own it. Never use a user-global file. Preserve existing instructions and avoid duplicate headings or entries. Asking to save the target does not block read-only triage.

## Collect the complete project

The default triage scope is every issue visible to the authenticated user across the project's retained history, including unresolved, resolved, and archived or ignored issues. State the visible statuses and any Sentry retention or permission limit in the report.

Fetch a fresh inventory with a time range broad enough to avoid the CLI's default 90-day window. Enumerate every issue status through explicit status queries or the API when the default list omits historical or archived issues. Follow pagination to exhaustion for each query, then deduplicate by numeric issue ID. Do not treat one page, one status, or the requested page limit as the complete project.

For a large project-wide inventory, triage in bounded batches while maintaining one compact, deduplicated ledger for the complete project. After each batch, retain only the report fields, classification, evidence summary, confidence, and proposed action. Discard raw event output. If a temporary ledger is needed, keep it outside the repository, exclude sensitive payloads, and remove that exact file after the final report. Batching must not omit issues or turn one project-wide approval plan into unrelated partial reports.

## Project report

Return category sections covering every inventoried issue, an inventory table with one row per issue, and a numbered action plan. Include each issue's short ID and link, impact signals, evidence, likely cause with confidence, and recommended action. For a large project, keep routine notes to one table row and reserve longer analysis for high-impact or uncertain issues. Account for every issue and disclose retention, status, pagination, or permission gaps.
