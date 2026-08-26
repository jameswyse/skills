# Testing review rubric

Use this rubric to judge each test and each important behavioural guarantee. Keep facts and judgements separate. A test smell is a lead to inspect, not an automatic verdict.

## Record one row per test

Give every executable test ID or declared test these fields:

| Field             | Required content                                                                                                                                              |
| ----------------- | -----------------------------------------------------------------------------------------------------------------------------------------------------------   |
| `id`              | Native collector ID when available. Otherwise use `path:line:name`.                                                                                           |
| `location`        | Exact file and line. Name the owning suite for generated or inherited tests.                                                                                  |
| `guarantee`       | The observable behaviour or invariant the test claims to protect.                                                                                             |
| `authority`       | The requirement, domain rule, public interface, schema, bug, or other independent source for that guarantee.                                                  |
| `seam`            | The interface through which a caller, user, process, or external system observes the result.                                                                  |
| `oracle`          | The independently established result or property. State when the expected value comes from the implementation or an unreviewed snapshot.                      |
| `path realism`    | Whether the test exercises the production path, a representative substitute, or a bypass.                                                                     |
| `unique value`    | The failure this test catches that a stronger test does not. Name overlapping tests when the value is shared.                                                 |
| `cost evidence`   | Relevant runtime, retries, flakiness, setup, fixture churn, diagnostic noise, or maintenance coupling. Use `No demonstrated concern` when no evidence exists. |
| `shortcomings`    | Specific smell or missing case. Use `None found` after inspection.                                                                                            |
| `verdict`         | `Keep`, `Improve`, or `Removal candidate`.                                                                                                                    |
| `value tier`      | `Essential`, `High`, `Supporting`, `Low`, or `Negative`.                                                                                                      |
| `rank reason`     | One sentence that explains its position relative to nearby tests.                                                                                             |

Do not infer the guarantee from the test name alone. Read the setup, assertion, called production path, owning code, and any authoritative requirement.

## Stack-rank by value

Produce one ordinal order for the requested scope. Compare tests in this order:

1. Consequence and reach of the protected guarantee. Security, money, irreversible data changes, eligibility, access, and central state transitions usually outrank presentation details.
2. Unique protection. A test that is the only reliable check for an important guarantee outranks overlapping examples.
3. Strength of evidence. Prefer the caller's real seam, an independent oracle, representative inputs, and an outcome that would fail for the real defect.
4. Failure signal. Prefer deterministic tests with local, useful diagnostics over broad failures that hide the cause.
5. Cost. Use observed runtime, flakiness, maintenance coupling, and environment burden only after accounting for the guarantee.

Use source order only to break a remaining tie. Record that tie-break so the ordinal rank does not pretend to have more precision than the evidence.

Use these value tiers:

- `Essential` protects a high-consequence guarantee with no equally strong substitute.
- `High` protects important behaviour through a credible path and adds clear failure detection.
- `Supporting` adds useful boundary, diagnostic, compatibility, or example evidence but is not the primary protection.
- `Low` has little unique protection or weak evidence, but removal is not yet justified.
- `Negative` creates false confidence or demonstrated cost without retaining a useful guarantee. Every `Negative` test is a removal candidate.

A lower-ranked test is not automatically bad. The rank orders expected protection, not code style or author effort.

## Justify removal candidates

List a test as a `Removal candidate` only when both statements are true:

1. The test has no useful guarantee that would become unprotected after removal.
2. The repository shows a concrete cost or false signal.

Supported reasons include:

- a stronger test protects the same guarantee through a more representative seam;
- the test protects a superseded behaviour or implementation path;
- a static type or analyser already provides the whole guarantee, with no distinct runtime behaviour;
- the oracle repeats the implementation and therefore cannot detect a wrong result;
- the assertion proves only that a file, export, call, or mock interaction exists;
- the test is permanently skipped, cannot collect, or cannot reach its claimed assertion;
- demonstrated flakiness, runtime, fixture churn, or diagnostic noise outweighs its non-unique signal.

Name the surviving protection. If an important guarantee would be lost, classify the test as `Improve` even when its current form is poor. If the behaviour is obsolete, cite the production or requirement evidence that makes it obsolete.

## Identify tests that fall short

Use the smell names from `$engineering`'s Testing reference where they fit:

- `Implementation-coupled test`
- `Private mock`
- `Tautological oracle`
- `Frozen configuration`
- `Static-proof test`
- `Timing-dependent test`
- `Edit-proof test`

Also report these concrete weaknesses when present:

- the assertion stops before the important outcome;
- a broad snapshot hides the rule and has no reviewed authority;
- the setup bypasses parsing, authorisation, persistence, rendering, transport, or another production seam that owns the risk;
- only the happy path exists for a state transition, permission, validation rule, or failure path;
- the test replaces the behaviour under test with its mock;
- shared state, order dependence, real time, randomness, or network access makes the result unreliable;
- a broad end-to-end test fails far from the defect and no narrower test identifies the rule;
- parameterised examples repeat one shape while omitting the boundary that defines the rule;
- the test is skipped, retried, quarantined, or conditionally absent without a current reason.

For each `Improve` verdict, state the smallest repair. Prefer a stronger assertion or a better observation seam over adding another test. Recommend replacing a test only when the current shape cannot protect the guarantee durably.

## Map guarantees instead of line coverage

Build the guarantee map independently from the test inventory. Inspect:

- product and domain requirements;
- public entrypoints and interfaces;
- calculations, validation rules, and legal state transitions;
- authentication, authorisation, tenant or object isolation, and sensitive operations;
- schemas, serialisation, persistence, migrations, and idempotence;
- external service, filesystem, queue, clock, randomness, and concurrency seams;
- failure translation, retries, recovery, and cleanup;
- configuration variants and supported platform or browser differences;
- important defects and regressions in repository history when available.

Record each important guarantee with its authority, consequence, observing seam, owning code, protecting test IDs, and one status:

- `Strong`: a deterministic test uses a credible path and an independent oracle.
- `Partial`: a test protects part of the rule, misses a consequential variant, or uses a weak oracle.
- `Indirect`: another test may traverse the path but does not assert this guarantee precisely.
- `None`: no collected test provides evidence for the guarantee.
- `Unknown`: missing documentation, unavailable systems, or incomplete collection prevents a judgement.

Do not convert these statuses into a percentage. Rank gaps by consequence, reach, change likelihood supported by repository evidence, and the feasibility of a durable observation seam.

## Assess the testing stack

Inventory the tools that own these jobs where they exist:

- collection and execution;
- assertions, component rendering, and browser interaction;
- doubles for remote, storage, time, randomness, and other real seams;
- fixtures, factories, generated data, and property tests;
- service integration, protocol compatibility, and end-to-end flows;
- isolation, retries, parallelism, sharding, timing, and reporting;
- CI selection and required checks.

For each tool, state its current job, where it is configured, whether another tool overlaps it, and a `Keep` or `Improve` verdict. A recommendation must solve an observed problem. Prefer using an installed tool's existing capability over adding another dependency. Do not recommend property tests, mutation testing, contract tests, browser tests, or a framework replacement without naming the guarantee or suite cost that makes it worthwhile.
