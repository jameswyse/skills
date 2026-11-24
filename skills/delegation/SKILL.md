---
name: delegation
description: Use before delegating work to another model or provider through T3's `delegate_task`, and when a skill or instruction asks for an advisor or a contrarian check.
---

# Cross-provider delegation

The caller decides whether the work goes cross-provider. This skill picks the provider, model, and effort.

## Route the work

Read the session's provider and model from `orchestrator_capabilities` (`inheritedProviderInstanceId` and `inheritedModel`), not from your own model name, unless the T3 tools are absent.

| Work                                                                   | Model                                                                                    |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Taste subagents: code, architecture, and UI                            | Opus                                                                                     |
| An advisor on a plan or decision in a complex or large task            | Fable, or Astra from a Fable session                                                     |
| Investigations: non-trivial debugging, computer use, and visual checks | Sol                                                                                      |
| A skill's cross-provider step                                          | Sol from a `claudeAgent` Fable or Opus session, Opus from a `codex` Astra or Sol session |
| First-round code review, Spec axis                                     | Sol, plus Fable from an Opus session or Opus from any other                              |
| First-round code review, Correctness axis                              | Astra, plus Fable from an Opus session or Opus from any other                            |
| First-round Standards review, verifier, and later rounds               | Sol                                                                                      |
| A contrarian check                                                     | Grok, plus Astra from a `claudeAgent` session or Fable from a `codex` session            |

Each model family has one provider and one set of options:

| Model family | Provider      | Options              |
| ------------ | ------------- | -------------------- |
| Fable, Opus  | `claudeAgent` | Effort high          |
| Astra, Sol   | `codex`       | Effort high, Fast on |
| Grok         | `cursor`      | Effort high, Fast on |

- Pick the highest-versioned model of that family from the provider's `models` list, not a remembered ID.
- Set every option in the table explicitly through `target.options`, using the option IDs the catalogue advertises for that model. Effort is `effort` for Claude, `reasoningEffort` for Codex, and `reasoning_effort` for Grok. Fast is `serviceTier: "priority"` for Codex and `fastMode: true` for Grok. Leave out an option the catalogue doesn't list for the model. T3's defaults are unreliable.
- Taste subagents, and an advisor on the session's own provider, run as native subagents. Use `delegate_task` for everything else, and for those two when the native tool can't select the model.
- For a cross-provider step from any other session, keep the caller's same-provider path.

## Delegate

- Call `delegate_task` once per independent piece of work with `mode: "async"`, all in the same step. `mode: "wait"` runs the children in series. Then finish any independent work and end the turn.
- T3 wakes you on each completion. While other tasks from the same step are still running, end that turn without assessing or summarising the reports that have arrived. Weigh them together once every task has completed or failed, which is when the calling skill continues.
- Give each call a distinct `clientRequestId`, stable across retries of that call, and a `role` that matches the work.
- Set `interactionMode` to `default` and `runtimeMode` to `inherit`. Never request a broader runtime mode, even when it would spare the child approval prompts.
- The child gets only the task prompt, in the parent's checkout. Write it to stand alone: the objective, the context and paths, a done condition, and the report you expect as plain text in its final message. For an investigation, ask for what it observed, without fixes.
- For read-only work, say that the child must not modify files, run formatters, create commits, fetch, or change Git state, even when its checkout's instructions say to at the start of a task.
- Put these rules, the no-delegation rule below, and the skills the child must load for its own work in the task prompt itself, before any brief, packet, or manifest path. A child may follow its checkout's start-of-task instructions before it opens a file the prompt points to.
- In every prompt, say that the child must not start agents or subagents, delegate, or apply this routing itself. It loads the same skills, so it would otherwise delegate back.

Treat the child's report as leads under the calling skill's verification rules.

## Fall back

Use the caller's same-provider path, which is a native subagent on the session's provider or your own work when there is none, when the T3 tools are absent, the target provider reports `canRunCrossProviderChildTask: false`, its catalogue lacks the target family, or the delegation fails. Report the provider and model that did the work, or the reason for the fallback. This fallback is a standing instruction from the user, so it isn't the unasked switch that T3 Code's own rules forbid.

## Advisor

Use when the global instructions ask for an advisor. They decide when to ask.

- Send the advisor your brief, routed as above with `role: "review"`, read-only. Give it the goal and constraints, your draft plan or the decision with your leaning, the alternatives you rejected and why, and the relevant paths. Ask for the biggest risks, a simpler approach if one exists, and its recommendation with reasons, and to say your approach holds instead of inventing changes. On a repeat consult, add its earlier advice and what has changed.
- Skip the consult, and report why, when you're a delegated task or subagent, the catalogue lacks the advisor's model, or its call fails. Never substitute another model.

## Contrarian

Use when a calling skill asks a contrarian to argue against a judgement you've made. The calling skill decides which judgements qualify, keeping to those where a wrong call would be costly. Two contrarians answer, Grok and the second model the routing table names. Grok is slow and Cursor usage is limited, so send every qualifying item in one call to each contrarian, both in the same step, never retry a failed call, and skip the check when nothing qualifies.

- Delegate as above with `role: "review"`.
- Keep the brief short. Give it each judgement, your reasoning, and the evidence quoted inline, such as the few lines of code, spec, or output it rests on, with secrets left out. List the most relevant files by absolute path. Ask it to argue from the brief first and open or search files only to test a specific objection.
- Ask for the strongest evidence-based case against each part in at most three sentences, without restating the brief, and for "no real objection" where it finds none.
- Skip one contrarian, and report why, when a Fall back condition applies to it or its call fails. The other's reply still counts.
- Skip the whole check, and report why, when you're a delegated task or subagent, delegation is restricted, or the session already runs on Cursor.
- A contrarian never argues an item it reported itself, such as a reviewer's own rejected finding. Send that item to whichever of Astra and Fable didn't report it and isn't the session's model, or to Grok alone when neither qualifies.
- Never substitute another model for a contrarian that can't run.
