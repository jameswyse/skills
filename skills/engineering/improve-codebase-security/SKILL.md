---
name: improve-codebase-security
description: Review a codebase, subsystem, or diff for evidence-backed security risks in trust boundaries, authentication, authorisation, secret handling, sensitive data, and dependencies. Use only when the user explicitly requests a focused security review or hardening assessment.
---

# Improve codebase security

Find concrete security weaknesses and present the evidence before changing code. Apply
`$engineering` as the baseline.

This is a focused engineering review. It is not a comprehensive scanner, compliance audit,
penetration test, or incident-response process. Recommend Codex Security or a qualified human
security review when the user needs broader automated scanning, dependency intelligence, exploit
validation, or formal assurance.

## Keep the review safe and read-only

The review does not authorise fixes, dependency upgrades, secret rotation, permission changes, or
production configuration changes. Inspect code, configuration, manifests, lockfiles, local history,
and existing read-only tool output.

Do not probe remote services, exploit a weakness, use discovered credentials, or execute untrusted
project or dependency code unless the user separately authorises the exact action and environment.
Never reveal a secret value. Name its variable, provider, or file location and replace the value with
`<REDACTED>`.

If the evidence suggests active compromise or exposed sensitive data, stop risky investigation.
Recommend the relevant human security or incident process and continue only safe evidence collection.

## Establish the security-relevant scope

Review the security-relevant attack surface across the whole repository by default. Inventory the
deployed entry points, identities, trust boundaries, sensitive operations and data, external
services, and dependency manifests. Inspect each relevant path at a useful level and state coverage
gaps.

Use a narrower scope when the user names one:

- For a subsystem, inspect its entry points, callers, data stores, and external dependencies.
- For a diff or recent change, verify the fixed point and include dirty tracked and untracked work.
  Inspect enough surrounding code to determine how the change affects the attack surface.
- For one suspected weakness, trace the complete path from attacker-controlled input or privilege to
  the protected operation or data.

## Build a lightweight threat model

Before ranking findings, identify the protected assets, plausible actors, entry points, trust
boundaries, sensitive operations, and external services in the reviewed scope. Follow misuse paths
supported by the implementation or configuration. Record assumptions and unknowns as coverage gaps.

## Follow evidence through high-risk paths

Use these areas as search directions, not as a checklist or quota:

- **Authentication.** Check how the system establishes identity, creates and expires sessions or
  tokens, recovers accounts, and handles changes in authentication state.
- **Authorisation.** Check server-side enforcement for protected operations, object ownership,
  tenant isolation, privilege changes, and denied paths. Authentication alone is not authorisation.
- **Secrets and sensitive data.** Trace how secrets and sensitive data enter, move through, and leave
  the system. Inspect source code, client bundles, logs, errors, traces, metrics, snapshots, fixtures,
  storage, and transport where they apply.
- **Trust boundaries.** Trace attacker-controlled input through parsing, validation, queries, file or
  URL handling, rendering, deserialisation, and commands to the operation that consumes it.
- **Dependencies.** Inspect manifests, lockfiles, provenance controls, lifecycle scripts, security
  policy, and the relevant transitive graph. Use current advisory data when available. Do not infer a
  vulnerability from age or version number alone.

In a diff review, focus on changed exposure, privileges, checks, defaults, data flows, logging,
configuration, and dependency behaviour. Do not turn a scoped diff review into a repository-wide
audit.

## Require a credible risk path

Include a finding only when the evidence supports all of these points:

1. The attacker-controlled input, identity, privilege, or precondition.
2. The trust boundary or missing, misplaced, or ineffective control.
3. The protected operation or data the path reaches.
4. The concrete impact.
5. The files, symbols, configuration, or tool output that prove the path.

Reopen every cited location and verify the path before reporting it. Exclude generic hardening,
style preferences, controls with no applicable threat, duplicate symptoms, and dependency claims
without current evidence. Treat delegated or automated findings as leads, not proof.

## Report concise findings

Present verified findings first, ordered by concrete impact and reachability. For each finding, give:

- a severity and confidence label without inventing a CVSS score
- the affected files and symbols
- the credible risk path and supporting evidence
- the impact and affected scope
- the smallest coherent remediation
- the focused check and allowed or denied behaviour that would verify the fix

Then state the reviewed revision, requested scope, threat-model summary, coverage, and coverage gaps.
Do not pad the report. If no finding meets the evidence threshold, say that no supported finding was
found within the reviewed coverage.

Do not include secret values, complete exploit payloads, or instructions for attacking a live
system. Use the minimum safe reproduction needed to support the finding.

Selection does not authorise a fix. Make changes only when the user asks for implementation. Apply
`$engineering`, fix the source problem, and verify the protected behaviour when implementation is
authorised.
