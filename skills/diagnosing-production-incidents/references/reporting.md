# Report a production diagnosis

Write an answer-first technical report for the user. Keep client communication and permanent incident records out of scope unless the user asks for them.

## Maintain the evidence ledger

Record each useful item with:

- **Type.** Reporter claim, direct observation, inference, or evidence gap.
- **Source.** A safe link, issue ID, query ID, trace ID, command, file, or deployment record.
- **Time and scope.** The timezone, environment, region, service, release, and cohort.
- **Finding.** The smallest redacted fact that carries the signal.
- **Implication.** The hypothesis that the finding supports or weakens.
- **Limitation.** Sampling, retention, filtering, missing access, ambiguous correlation, or another reason the finding may mislead.

Do not paste a raw log dump into the report. Include enough evidence for another engineer to verify the conclusion without exposing credentials, personal data, request bodies, or unrelated customer information.

## Assign confidence

Use one of these labels:

- **Confirmed.** Decisive evidence distinguishes the cause from realistic alternatives. A reproduction or intervention can confirm the cause, but one is not mandatory when another decisive observation exists.
- **Probable.** Independent observations support one cause strongly, and the remaining alternatives fit the evidence less well.
- **Possible.** The cause is plausible, but missing or ambiguous evidence prevents a reliable ranking.

Do not upgrade temporal correlation, code reading, one reporter's conclusion, or an absence of telemetry to `confirmed` by itself.

## Use this report structure

### Incident summary

State the current status, user impact, affected scope, and whether the incident is still active.

### Most likely cause

Name the cause and confidence first. Explain the mechanism in plain language. State the evidence that distinguishes it from the alternatives.

### Timeline

List the last known good, first known bad, important changes, reproduction attempts, evidence events, attempted mitigations, and current state. Name the timezone.

### Reproduction

State which environments were attempted, the exact observable result, and any limits. Treat declined, unavailable, or unsuccessful reproduction as a result rather than hiding it.

### Evidence coverage

List the sources checked, the relevant observations, and safe source pointers. Name unavailable sources, failed access, retention gaps, sampling, and broken instrumentation.

### Alternatives

List rejected and remaining hypotheses. State the evidence that weakened each rejected hypothesis and the missing observation that keeps each remaining hypothesis open.

### Assumptions and unknowns

List every assumption that could change the diagnosis. State what evidence would resolve each consequential unknown.

### Suggested next actions

Recommend the smallest safe checks, mitigation options, rollback options, or fix direction. Separate urgent containment from a durable fix. Do not execute an action merely because it appears in this section.

### Changes made

State every local or production change made during diagnosis, including temporary instrumentation and its cleanup status. If the investigation was fully read-only, say that no changes were made.

## Stop at the requested audience

Do not convert the report into client-facing wording, update Jira, publish a document, send a message, or write a postmortem without a separate request. When the user requests another audience, preserve the evidence and confidence while adapting the amount of technical detail.
