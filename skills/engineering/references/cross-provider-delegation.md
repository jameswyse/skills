# Cross-provider delegation

The caller decides whether the work goes cross-provider. This reference picks the provider, model, and effort.

## Route the work

Read the session's provider and model from `orchestrator_capabilities` (`inheritedProviderInstanceId` and `inheritedModel`), not from your own model name, unless the T3 tools are absent.

| Work                                                                     | Provider                                    | Model                                                                       | Effort        |
| ------------------------------------------------------------------------ | ------------------------------------------- | --------------------------------------------------------------------------- | ------------- |
| Taste subagents: code, architecture, and UI                              | Same provider, native subagent              | Newest Opus                                                                 | High          |
| Advisors on a plan or decision in a complex or large task                | Same provider, native subagent, and `codex` | Newest Fable, and newest listed Astra                                       | High          |
| Investigations: non-trivial debugging, computer use, and visual checks   | `codex`                                     | Newest listed Sol                                                           | High          |
| A skill's cross-provider step from a `claudeAgent` Fable or Opus session | `codex`                                     | Newest listed Sol                                                           | High          |
| A skill's cross-provider step from a `codex` Astra or Sol session        | `claudeAgent`                               | Newest listed Opus                                                          | High          |
| First-round code review, Spec axis                                       | `codex` and `claudeAgent`                   | Newest listed Sol, plus Fable from an Opus session or Opus from any other   | High          |
| First-round code review, Correctness axis                                | `codex` and `claudeAgent`                   | Newest listed Astra, plus Fable from an Opus session or Opus from any other | High          |
| First-round Standards review, verifier, and later rounds                 | `codex`                                     | Newest listed Sol                                                           | High          |
| A contrarian check                                                       | `cursor`                                    | Newest listed Grok                                                          | High, Fast on |

- Pick the highest-versioned model of that family from the provider's `models` list, not a remembered ID.
- Set the effort explicitly through `target.options`, using the option ID the catalogue advertises for that model, such as `reasoningEffort` for Codex or `effort` for Claude. T3's default effort is unreliable.
- When a native subagent tool can't select the model, use `delegate_task` on the same provider.
- For a cross-provider step from any other session model, keep the caller's same-provider path.

## Delegate

- Call `delegate_task` once per independent piece of work with `mode: "async"`, all in the same step. `mode: "wait"` runs the children in series. Then finish any independent work and end the turn. Each completion arrives as a notification, and the calling skill continues once every task has completed or failed.
- Give each call a distinct `clientRequestId`, stable across retries of that call, and a `role` that matches the work.
- Set `interactionMode` to `default` and `runtimeMode` to `inherit`. Never request a broader runtime mode, even when it would spare the child approval prompts.
- The child gets only the task prompt, in the parent's checkout. Write it to stand alone: the objective, the context and paths, a done condition, and the report you expect as plain text in its final message. For an investigation, ask for what it observed, without fixes.
- For read-only work, say that the child must not modify files, run formatters, create commits, fetch, or change Git state, even when its checkout's instructions say to at the start of a task.
- Put these rules, the no-delegation rule below, and the skills the child must load for its own work in the task prompt itself, before any brief, packet, or manifest path. A child may follow its checkout's start-of-task instructions before it opens a file the prompt points to.
- In every prompt, say that the child must not start agents or subagents, delegate, or apply this routing itself. It loads the same skills, so it would otherwise delegate back.

Treat the child's report as leads under the calling skill's verification rules.

## Fall back

Use the caller's same-provider path, which is a native subagent on the session's provider or your own work when there is none, when the T3 tools are absent, the target provider reports `canRunCrossProviderChildTask: false`, its catalogue lacks the target family, or the delegation fails. Report the provider and model that did the work, or the reason for the fallback. This fallback is a standing instruction from the user, so it isn't the unasked switch that T3 Code's own rules forbid.

## Advisors

Use when the global instructions ask for advisors. They decide when to ask.

- Send Fable and Astra the same brief in the same step, delegating as above with `role: "review"`, read-only. Give them the goal and constraints, your draft plan or the decision with your leaning, the alternatives you rejected and why, and the relevant paths. Ask each for the biggest risks, a simpler approach if one exists, and its recommendation with reasons, and to say your approach holds instead of inventing changes. On a repeat consult, add each advisor's earlier advice and what has changed.
- Skip both, and report why, when you're a delegated task or subagent. Skip one, and report why, when the catalogue lacks its model or its call fails. Never substitute another model.

## Contrarian

Use when a calling skill asks a contrarian to argue against a judgement you've made. The calling skill decides which judgements qualify, keeping to those where a wrong call would be costly. Grok is slow and Cursor usage is limited, so send every qualifying item in one call, never retry a failed call, and skip the check when nothing qualifies.

- Delegate as above with `role: "review"`, and set both the effort and Fast through `target.options`.
- Keep the brief short. Give it each judgement, your reasoning, and the evidence quoted inline, such as the few lines of code, spec, or output it rests on, with secrets left out. List the most relevant files by absolute path. Ask it to argue from the brief first and open or search files only to test a specific objection.
- Ask for the strongest evidence-based case against each part in at most three sentences, without restating the brief, and for "no real objection" where it finds none.
- Skip the check, and report why, when you're a delegated task or subagent, delegation is restricted, the session already runs on Cursor, or a Fall back condition applies. Never substitute another model, because the check needs a family that took no part in the judgement.
