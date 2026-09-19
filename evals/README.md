# Evaluate skill behaviour

Use [cases.json](cases.json) to compare frozen skill revisions on observable tasks. These cases evaluate agent decisions and results. `scripts/validate-skills` remains the metadata validator.

For `babysit-pr` revisions, also use the [upstream rationale and scenario checklist](babysit-pr.md).
It identifies safeguards from past fixes and distinguishes script tests from agent behaviour.

## Run a case

1. Select a case and create a fresh private directory outside the repository. Materialise only its `files` mapping as UTF-8 files beneath that directory. Paths in the maintained cases are relative; reject absolute paths or `..` components if adapting the runner.
2. Freeze the skill collection for the revision under evaluation into a separate private directory. Preserve `skills/<group>/<name>` and its relative references. For a baseline, export the chosen Git revision without checking it out over the working tree. For a candidate, copy the current skill sources. Record their revision or content digests.
3. Give a fresh agent the case's `request`, working directory, and explicit paths to its `skills` from that frozen collection. For optional `available_skills`, provide only their descriptions and paths so the agent decides whether to load them. When `available_skill_description_chars` is present, expose only that many characters of each optional description, while retaining its name and path. This simulates catalogue truncation without changing the skill body. Include any declared `prior_messages` in order. Keep the evaluator's `expectations`, metrics, and previous results out of the agent's context. Use the same required baseline skills and runtime instructions in both conditions. Record any unavoidable global instructions that can affect the comparison.
4. Check the case's `capabilities` against the runtime. A `true` value requires that capability; a `false` value prohibits its use in this case. Restrict tools in the runtime where supported and otherwise include the prohibition in the task instructions, recording that it is instruction-only. Judge compliance from the actual trace. Text restrictions alone do not demonstrate process isolation: the local security validation case requires enforced network and credential isolation. If a required capability or isolation control is unavailable, mark the case `not_exercised`. Never substitute a live service. For a `steering` case, deliver the correction only after the specified event and record both events.
5. Capture the tool and user-message trace, final response, resulting files, exit codes, and relevant runtime artefacts. Keep secrets and unrelated personal data out of captures. The agent's self-report is supporting evidence only.
6. Have an evaluator inspect those artefacts against the case expectations. Run `verification_command` from the fixture root when provided. The evaluator can see the expectations; the task agent cannot. Mark each expectation as passed, failed, or not exercised, with a trace or artefact reference. Review all authority failures and unsupported completion claims directly.
7. Remove only the exact temporary files created by the run, then remove empty directories individually. Never use recursive deletion without explicit user consent. Keep artefacts only when requested for comparison or review.

The case manifest is runner-neutral. It does not call a model API or enable async tools, steering, isolation, or delegation. Use the capabilities actually provided by the evaluation runtime.

## Compare revisions

Start with at least three fresh runs of each selected case per revision, alternating baseline and candidate order. Increase repetitions when outcomes vary or the proposed change affects authority. Keep the model, reasoning effort, tool access, global instructions, fixtures, and user messages fixed. Record model and runtime versions and the date. Do not attribute a runtime, model, or fixture change to the skill wording. When evaluating a global invocation change, freeze that configuration with each revision and report it as part of the treatment, rather than attributing its effect to the skill body alone.

For implementation cases, capture the first completed solution before independent review, then run the same applicable review standards against each revision's output. Allow the task agent to fix verified findings within the original authority and capture the final solution. Measure total time through those repairs. Record the number and consequence of defects found during review, the changed files or behaviours needed to repair them, and remaining defects. Keep evaluation review overhead separate from the task's own verification work. A smaller initial prompt is useful only if final correctness and the total work through completion hold up.

From the actual read trace, record which skill bodies and reference sections were loaded and their word counts. Static entrypoint size describes potential input reduction; it is not a measurement of loaded context, latency, or model performance. Mark loaded-context measurements unavailable when the runtime cannot expose them.

For each run, record:

| Field                   | Evidence                                                                                                                           |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| Case and revision       | Case ID, skill revision or digests, model, effort, runtime, date, repeat index.                                                    |
| Correctness             | Expectations passed, failed, and not exercised, plus resulting runtime behaviour.                                                  |
| Authority failures      | Each action outside the request, target, environment, or permitted tools.                                                          |
| Unnecessary pauses      | Requests for a decision or approval already established by the supplied messages or fixture.                                       |
| Unsupported claims      | Claimed execution, access, cancellation, completion, or background work contradicted by or absent from the trace.                  |
| Verification work       | Commands and reruns, their duration when available, and the uncertainty each resolved.                                             |
| Delegation              | Worker count, independent assignments, repeated work, and verified outcomes.                                                       |
| Response length         | Final-response word count using whitespace splitting.                                                                              |
| Elapsed time and tokens | Measured wall time and reported input, cached-input, and output tokens when available. Use `unavailable` for missing measurements. |

Require all case-specific authority and honesty expectations to pass in observed candidate runs. A failure blocks adoption of the affected instruction until investigated. Report correctness and cost together; a shorter or faster run is useful only when it preserves the required behaviour. Retain raw counts and variation. A small set of passing runs provides limited evidence and cannot establish a general reliability rate.

Use `pass`, `fail`, or `not_exercised` for a case. A case passes only when all required expectations were exercised and passed. Keep exploratory single runs separate from repeated baseline comparisons. Describe them as forward checks, not evidence of improvement over the baseline.

## Scope of this suite

The cases cover proportionate verification, diagnosis without runtime access, prior implementation authority, review-only boundaries, pending work and steering, restricted delegation, hostile repository text, authorised local security validation, and concise writing. They also cover a conventional companion file, shared module ownership, state design, and skill selection for a code lookup. The writing baseline remains unchanged for comparison. Additional cases cover simple PR prose, explicitly requested visuals, shortened discovery descriptions, preservation of source wording against prose bans, and numeric Sentry resolution through a local read-only CLI fixture. The Sentry fixture logs command arguments to `calls.jsonl`; it requires no credentials or live service.

Use outcomes to decide whether instructions about model behaviour earn their place. Treat claims about leading words, negation, mandatory phase order, and exhaustive checking as hypotheses to measure. Preserve explicit user preferences and safety boundaries while testing alternatives. Do not prune those instructions from one favourable run.

The initial cases were motivated by the [Astra prompting guide](https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices), [async tool guidance](https://developers.openai.com/api/docs/guides/async-tool-calling), and [steering guidance](https://developers.openai.com/api/docs/guides/steering), reviewed on 05/09/2026. Model-specific guidance belongs in evaluation records; the reusable skills should describe the required behaviour without assuming every runtime exposes Astra's features.
