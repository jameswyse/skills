# Failures and diagnostics

Make expected outcomes visible to callers that can act on them. Keep defects distinct so unexpected failures remain conspicuous.

## Classify the failure

An expected failure is part of normal operation. Examples include invalid input, a missing record, denied access, a conflict, an unavailable dependency, or a rejected state transition. A defect violates an internal invariant or reveals a programming error.

- Represent an expected failure in the return type when a caller must branch, retry, report, or translate it.
- Throw or reject for a defect, an impossible state, or framework-required behaviour.
- Treat a configuration error as an expected startup failure. Report it safely at the entrypoint and stop startup.
- Follow the repository's established error mechanics when the change does not own a broader migration.

Use the established result representation when the repository has one. Otherwise use the smallest discriminated union that expresses the caller's decisions. Do not add a result library as part of an unrelated change.

Do not expose every low-level failure as a separate public variant. Combine failures that lead to the same caller decision, but preserve the context needed to diagnose them.

## Translate failures at their owning seam

Catch an unclassified third-party exception or promise rejection inside the adapter that owns the dependency. Translate it into an application-understood failure before it crosses the adapter seam. Preserve the original value as `cause: unknown` when the language or error type supports it.

At the outer seam, translate application failures into the protocol's outcomes. Examples include an HTTP response, a CLI exit, a queue decision, a retry decision, or a startup message. Keep domain and application code independent of those representations.

Preserve established logging, tracing, metrics, and error-reporting hooks when translating failures.

## Keep failure interfaces precise

- Use a stable discriminant or error code.
- Include a useful message and structured context that identifies the operation and affected domain value.
- Keep failure unions precise near domain and application interfaces.
- Broaden or group failures only near orchestration, logging, and presentation code.
- Match failure variants exhaustively when the type system supports it.

## Keep diagnostics safe

Never put secrets, credentials, tokens, or raw sensitive payloads in errors, logs, traces, metrics, or snapshots. Pass safe identifiers, operation names, provider names, retry counts, error codes, and redacted summaries instead.

Use the repository's redacted-value type when one exists. Add a shared redacted type only when sensitive values cross enough typed boundaries to justify the mechanism. Unwrap a sensitive value only at the operation that requires its raw representation.
