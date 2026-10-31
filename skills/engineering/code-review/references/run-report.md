# Run report

The run report shows how a review was run: which models reviewed, over how many rounds, and how many
of their findings survived verification. Start a ledger in the first round and keep it through every
later round.

## Keep the ledger

Give each candidate finding an ID from its axis and a number, such as `S1`, `P1`, or `C1`, when it
is first reported. Reuse that ID when another reviewer or a later round reports the same finding, so
the ledger shows every reviewer that found it. Record a finding from your own final pass with the
reviewer "Primary", which gets no table row. For each finding, record its reviewers and its outcome:
its severity when actionable, accepted risk, Spec decision for the user, or rejected. Code-review
step 3 shows each verified finding's ID and reviewers.

Record one entry per reviewer run:

- the provider and model, or "Codex CLI", noting any replacement and its reason;
- the axis it reviewed and the round;
- the IDs of the candidate findings it reported;
- how many of those survived verification as actionable findings or accepted risks. When several
  reviewers report the same finding, count it for each of them.

File findings from a reviewer that covers every axis, such as the Codex CLI or a review bot, under
the axis each belongs to. Record a reviewer that failed or timed out with its reason. Also record the
verifier's confirmed and refuted counts, and how many contrarian objections changed a decision, or
why the contrarian was skipped. When this skill's verification step weighs review-bot comments, such
as in a bot draft review, record each bot's rounds as "Bot 1", "Bot 2", and so on.

## Write the report

Give each reviewer one row per round, with each axis's run as reported and verified counts. Use "-"
for an axis it didn't review. Then give one line of outcomes:

```markdown
| Round | Reviewer            | Standards | Spec  | Correctness |
| ----- | ------------------- | --------- | ----- | ----------- |
| 1     | GPT-6.1-Sol         | 3 / 1     | 2 / 0 | 4 / 3       |
| 1     | Claude Opus 5.5     | -         | 1 / 0 | 4 / 2       |
| 1     | GPT-6.1-Sol (extra) | -         | -     | 3 / 1       |
| 1     | Codex CLI           | 0 / 0     | 0 / 0 | 2 / 1       |
| 2     | GPT-6.1-Sol         | -         | -     | 1 / 0       |
| Bot 1 | Copilot             | 1 / 0     | 0 / 0 | 2 / 1       |

Cells show reported / verified. Verifier GPT-6.1-Sol confirmed 6 and refuted 9. Contrarian Grok 4.7
reversed 1 rejection. Actionable: Standards 1, Spec 0, Correctness 3. Worst: high, unlocked price
saved. Accepted risks 1.
```

Keep the table to these columns. Name failures, timeouts, and replacements in the reviewer cell.
