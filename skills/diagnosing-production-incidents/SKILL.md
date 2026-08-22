---
name: diagnosing-production-incidents
description: Diagnose urgent live production incidents through authorised reproduction and read-only evidence collection. Invoke explicitly after a production outage or major failure has been classified as an incident. Use diagnosing-bugs for ordinary bugs found in production.
---

# Diagnose production incidents

Use this skill only when the user invokes it explicitly. The invocation means the user has classified the problem as an urgent production incident. Do not invent an organisation-specific severity.

This skill owns the incident workflow. Do not run `$diagnosing-bugs` alongside it. Diagnose the incident, describe urgent mitigation options, and stop before any fix, rollback, deployment, configuration change, restart, scaling action, feature-flag change, or external communication unless the user separately authorises that action.

Keep the default investigation operationally read-only. Querying approved evidence sources, inspecting code and configuration, and creating authorised local temporary diagnostics are allowed. Production instrumentation is a separate change with a separate approval gate.

Redact secrets and sensitive values before showing commands, outputs, or captured artefacts. Query production data in place when possible. Do not copy raw production payloads into the repository or conversation.

## Coordinate parallel investigation

Use parallel subagents when two or more independent branches can reduce elapsed time without duplicating production load. Good branches include ticket analysis, code-path inspection, Sentry, CloudWatch, traces, deployment history, dependency health, and affected-versus-healthy comparisons.

The primary agent owns:

- User communication and approval gates.
- The incident brief and evidence plan.
- Access checks and production reproduction.
- Hypothesis ranking, correlation, and the final diagnosis.

Give every subagent the same incident scope, time window, redaction rules, read-only constraint, and evidence format. Assign one source or falsifiable question to each subagent. Bound concurrency by service limits, query cost, and production load. Treat every delegated finding as a lead until the primary agent checks the underlying evidence.

Use one agent for production reproduction. Never let agents independently repeat production requests. Give one agent sole ownership of local writes and keep all other agents read-only. Continue sequentially when delegation is unavailable or the hand-off would cost more time than it saves.

## Phase 1: Assemble the incident brief

Read all supplied reports, tickets, attachments, screenshots, log excerpts, links, repository documentation, and related source that the current access permits. Use applicable connectors, APIs, or CLIs before asking the user to restate information. Do not update an external source while reading it.

Record:

- Current impact and whether it is worsening.
- Expected and observed behaviour.
- The first and last observation with a timezone.
- Affected and unaffected users, requests, regions, services, and versions.
- Frequency and known reproduction steps.
- Request IDs, trace IDs, error IDs, account IDs, and release versions that can correlate evidence safely.
- Recent deployments, configuration changes, feature flags, infrastructure events, dependency incidents, and attempted mitigations.
- Existing workarounds and actions already taken.

If the report suggests compromise, privacy exposure, data corruption, safety impact, or rapidly increasing damage, pause risky reproduction and instrumentation. Recommend the relevant human incident or security process while continuing only safe evidence collection.

Ask one grouped clarification round for missing information that could change the investigation. Mark other gaps as assumptions and continue. Phase 1 is complete when the incident brief distinguishes known facts, reporter claims, and consequential unknowns.

## Phase 2: Decide whether to reproduce

Ask whether to attempt reproduction locally, in a named remote non-production environment, or in production. State the likely risk and evidence value of each available option. Approval for one environment does not authorise another.

### Local reproduction

Approval to reproduce locally permits temporary local instrumentation, throwaway scripts, runtime overrides, and diagnostic edits.

Before changing tracked files:

1. Record the existing working-tree status and relevant diff.
2. Prefer operating-system temporary files when practical.
3. Tag diagnostic edits with a unique identifier.
4. Give one agent sole ownership of the edits.
5. Ask before proceeding if an edit would overlap existing work or cannot be restored safely.

Remove only the agent's edits when reproduction ends. Do not use broad Git restoration commands. Verify that the original working-tree state remains intact.

### Remote non-production reproduction

Confirm the environment, identity, test data, expected side effects, and stopping condition. Use synthetic data where possible. Do not assume that non-production permits destructive, high-load, or externally visible actions.

### Production reproduction

Prefer passive evidence first. Before a production attempt, obtain approval for the exact action, account or synthetic identity, expected side effects, load, time limit, and stopping condition. A nominally read-only request may still create sessions, warm caches, send analytics, trigger downstream work, or expose customer data.

Do not loop production requests, generate load, impersonate a customer, or write production data unless the user explicitly authorises that exact activity. Stop when the observed effect differs from the approved plan.

Record a declined, unavailable, unsuccessful, or non-reproducing attempt as evidence. Continue to Phase 3 without requiring reproduction.

## Phase 3: Collect and test evidence

Read [Evidence sources](references/evidence-sources.md) at the start of this phase.

Inspect the incident context, repository, deployment configuration, available tools, and agreed environments. Present an evidence plan that names each known service and explains:

- Why it may distinguish the leading possibilities.
- The account, project, environment, region, and time window.
- The connector, API, CLI, browser, or supplied export to use.
- The sensitive-data risk, query cost, and production load.

Ask the user to confirm the plan and provide additions or alternatives. Do not query an unconfirmed production evidence source.

After confirmation, verify access with a benign read. If access fails and an actionable login or permission step exists, give the exact step without asking for credentials. Wait only on the affected branch. Continue other confirmed independent work while the user completes the step, then verify that access again. If direct access cannot be provided, ask for a redacted export or record the evidence gap and continue.

Run a broad first pass that establishes the timeline, scope, telemetry shape, healthy controls, recent changes, and observability coverage. Report a concise non-blocking status update after the first useful evidence pass.

Create three to five ranked, falsifiable hypotheses. For each hypothesis, state the observation that would support it and the observation that would weaken it. Share the list as a non-blocking update, then run targeted queries that distinguish the hypotheses.

Maintain an evidence ledger as [Reporting](references/reporting.md) defines it. Keep reporter claims, direct observations, inferences, and evidence gaps separate. Absence of a log or trace is not evidence of absence until retention, sampling, filtering, and instrumentation health have been checked.

Stop collecting when:

- Decisive evidence distinguishes the cause from realistic alternatives.
- Independent observations make one cause probable and remaining sources are unlikely to change the ranking.
- Further work requires new access, permission, significant cost, or production risk.
- The available evidence cannot narrow the cause further.

### Escalate to temporary instrumentation

Use temporary production instrumentation only after read-only evidence cannot distinguish the remaining hypotheses. Request fresh authorisation that names:

- The hypothesis and the exact code, configuration, or runtime change.
- The environment and deployment action.
- The named safe fields captured and their minimisation or transformation before emission.
- The expected performance, cost, and telemetry-volume effects.
- The expiry or removal condition.
- The check that will prove removal.

Design the probe so sensitive values never enter new telemetry. Never capture secrets, authentication data, payment card data, raw personal data, or complete request and response bodies. Redaction during reporting is not a substitute for minimisation before emission. If no safe probe can test the hypothesis, report that limit instead of instrumenting production.

Approval for a local edit does not authorise deployment. Approval to deploy does not authorise other production changes. Tag the instrumentation uniquely. If safe expiry or removal cannot be guaranteed, do not propose it.

## Phase 4: Report the diagnosis

Read [Reporting](references/reporting.md) before writing the report.

State the most likely cause with its confidence, the evidence that distinguishes it, the affected scope, realistic alternatives, assumptions, and the smallest safe next actions. Describe possible mitigation or rollback options without executing them.

Remove agent-created local diagnostics with targeted, non-recursive operations. Ask before recursively deleting any directory. Restore only the agent's tracked edits and verify the original diff. Production cleanup requires the authorisation that covers that cleanup.

Do not update Jira, publish a document, send a message, apply a fix, or change an external system unless the user separately requests it. State exactly what changed during the investigation. If nothing changed, say so.
