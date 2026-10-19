# Reproduction techniques

Use when building or minimising a reproduction, or for intermittent behaviour. The [entrypoint](../SKILL.md)'s authority and fallback rules still apply.

- Keep throwaway scripts, fixtures, and captures in the operating system's temporary directory unless the user authorised adding them to the repository. For diagnosis-only work, prefer an existing test or a command that needs no repository changes.
- Choose the cheapest loop that drives the actual bug path, such as a failing test at the seam that reaches the bug, an HTTP or CLI script, a headless browser script, a replayed captured trace, a harness for `git bisect run`, or the same input run through two versions or configurations.
- When a person must act, guide them with the [human-assisted loop template](../scripts/hitl-loop.template.sh) and use their captured output as the next input.
- Assert the user's exact symptom, not a nearby failure or a run that merely doesn't crash. Capture the error message, wrong output, or timing so verification can show the fix addresses it.
- For intermittent failures, record the conditions, attempt count, and failure rate. Stop adding attempts when more are unlikely to distinguish causes.
- Once the loop fails, cut inputs, callers, configuration, and steps one at a time, rerunning after each cut. Stop when further reduction won't change the diagnosis, and keep the original scenario for final verification.

When no reproduction is practical, request only evidence that would change the diagnosis, such as access to an affected environment, a redacted capture, or permission to add temporary production instrumentation. Continue independent investigation while waiting.
