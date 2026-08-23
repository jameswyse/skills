# Collect production evidence

Use this reference after the user confirms the evidence plan. Choose the sources that can distinguish the current hypotheses. Do not query every available service by habit.

## Choose the access route

Explicit user choice wins. Otherwise use this order:

1. Use a purpose-built connector or integration when it covers the required operation.
2. Use an authenticated read-only API or CLI when it gives precise, bounded results.
3. Use a browser when the user chose it, authenticated UI access is required, or no suitable connector, API, or CLI exists.
4. Ask for a redacted export when direct access is unavailable.

Search the available and deferred tools before choosing a browser for semantic work. If Chrome is the agreed route and `$chrome:control-chrome` is available, apply it before browser work. Never inspect browser cookies, storage, profiles, passwords, or session stores.

Verify access with a benign identity or metadata request. Confirm the account, project, region, and environment from the returned value rather than an assumption. If login is required, give the user the exact sign-in step and wait. Never ask the user to paste a credential or token.

## Bound every query

Start with the narrowest useful time window around the first and last observations. Preserve the source timezone and normalise correlated times to one named timezone. Widen the window only when the evidence requires it.

Filter by safe identifiers such as a request ID, trace ID, operation name, error code, release, region, or pseudonymous account ID. Quote only the fields and lines that carry the signal. Avoid raw request bodies, authentication headers, session values, and personal data.

Record the query, filters, time range, source pointer, result, and coverage limits. Bound queries that incur cost, consume rate limits, or load a production service. Never "log everything and grep".

## Establish the common baseline

Every incident needs a small common analysis:

- Establish the last known good and first known bad time.
- Compare affected traffic with a healthy control cohort when one exists.
- Correlate the symptom window with deployments, configuration, feature flags, infrastructure events, dependency health, and rollback history.
- Follow identifiers across errors, logs, traces, metrics, queues, and downstream services.
- Check whether sampling, retention, filtering, or instrumentation changed near the incident.
- Separate application failure, dependency failure, observability failure, and client-specific behaviour.

For a production-only failure, record the lack of local reproduction and continue with production evidence. Compare affected and unaffected cohorts, releases, regions, tenants, request shapes, and execution paths. Treat code and configuration as sources of hypotheses, not proof of runtime behaviour.

## Incident reports and tickets

Read the complete supplied report and its accessible comments, attachments, links, and history. Use an applicable Jira or work-management connector before browser UI when one is available. Preserve who observed a symptom and when. Distinguish the reporter's conclusion from the underlying observation.

Read only. Do not comment, change status, assign people, edit fields, or attach evidence unless the user separately requests it.

## Sentry and error monitoring

Search available tools for a Sentry connector first. Use the API or CLI when configured and when it can answer the question more precisely. Use Chrome only when the user explicitly selected Chrome or the connector and API cannot perform the required operation.

Inspect the issue and its events, not only the issue title. Correlate event time, release, environment, transaction, trace, request ID, affected version, tags, breadcrumbs, and safe user or session references. Compare the first seen, last seen, frequency, and affected cohort with the incident report.

Check whether grouping, sampling, filtering, or SDK configuration could hide or merge the relevant failures. Do not treat one grouped issue as the full incident scope.

## AWS and CloudWatch

Confirm the AWS profile, account, region, and role before querying. Use a benign identity check such as `aws sts get-caller-identity` when the AWS CLI is the agreed route. If the session has expired, tell the user to run the exact `aws sso login --profile <profile>` command and wait for completion.

Use bounded CloudWatch Logs Insights, metric, alarm-history, deployment-event, and audit-history queries that fit the approved plan. Start from the incident window and correlation identifiers. Inspect neighbouring errors only when they can identify an upstream or downstream failure.

CloudWatch console access through Chrome is a fallback when the CLI or another integration cannot answer the question. Do not change log levels, retention, alarms, dashboards, infrastructure, tasks, or services during read-only collection.

## OpenTelemetry and distributed traces

OpenTelemetry may export signals rather than store them. Inspect repository or runtime configuration to identify the collector and destination backend before choosing a query route.

Start from a trace ID, request ID, transaction, or failing operation. Follow the trace across service boundaries. Compare span status, duration, attributes, events, retries, and missing spans with a healthy trace. A missing span may indicate sampling, propagation, exporter, or collector failure rather than an absent operation.

Use trace and log correlation to locate the owning service. Do not infer root cause from the slowest or final failing span without checking upstream inputs and downstream responses.

## Logs and metrics

Use structured fields before free-text search. Align log events with request and trace identifiers. Check the first upstream error rather than counting repeated downstream failures.

Use metrics to bound scope and timing. Compare error rate, latency, traffic, saturation, queue depth, retry volume, and dependency health where relevant. Check absolute counts alongside percentages. A rate can move because the denominator changed.

Confirm the telemetry pipeline before concluding that zero events means zero failures. Compare ingestion health, sampling, retention, and filters with a known healthy signal.

## Deployments, configuration, and rollback evidence

Inspect deployment records, release identifiers, source diffs, infrastructure events, configuration audit history, feature flags, dependency changes, and secret or certificate rotation events. Align them with the last known good and first known bad times.

Temporal correlation raises a hypothesis. It does not prove causation. Look for a mechanism and a distinguishing observation. A rollback followed by recovery is strong evidence when the affected scope and timing also match, but executing a rollback is outside this workflow.

## External dependencies and user-visible behaviour

Check an external dependency's official status and the application's observed responses. A green provider status page does not outweigh direct failing responses. A red status page does not prove that the incident shares the same cause.

When visual or interactive evidence matters, inspect the exact production state through the agreed browser. Capture the DOM, console, network, and timestamp needed for the diagnosis. Do not take unrelated screenshots or interact beyond the approved reproduction.
