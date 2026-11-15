# Calibration

The goal is a pull request that bot
reviewers have nothing to say about. Every inline bot comment on a reviewed pull request is a
candidate miss.

## Collect

Run `python3 <skill-dir>/scripts/collect_bot_comments.py --since <YYYY-MM-DD> --output <temporary-json-path>`.
It searches pull requests the user authored and merged since that date and collects top-level inline
comments from bot accounts. It counts pull requests, reported as `counted_pull_requests`, only in
the `bot_commented_repositories` where a bot left an inline comment during that period. Pass
`--author`, `--limit`, or a repeated `--bot` to change the defaults shown by `--help`. Each month's
`comments_per_pull_request` is the candidate rate, which includes noise. The repository filter
approximates which pull requests a bot reviewed, so treat the rates as a trend rather than exact
values. When `limit_reached` is true, narrow `--since` before comparing months.

The script skips review bodies and conversation comments. Bots use those for summaries, approval
verdicts, and status receipts, while their findings arrive inline.

## Classify

Read each comment with enough of the pull request's diff to judge it. Classify it as:

- **Miss.** A real defect or requirement gap the review should have caught.
- **Accepted risk.** Real, but the code-review verification step's weighing would leave it unfixed.
  It isn't a miss.
- **Noise.** Wrong, already handled, or a preference with no concrete cost.

For noise that recurs, recommend tuning that bot, such as repository instructions for Copilot,
instead of changing this review.

## Update the checklist

Group misses into patterns a reviewer can check without the original pull request, then update
[Missed findings](missed-findings.md) and keep it ordered by how often each pattern was missed.
Refine an existing pattern before adding one, and remove a pattern that no longer recurs once the
review catches it. When a miss belongs to an existing axis prompt or standards reference rather than
a checklist pattern, change that source instead.

## Report

Compute the miss rate for each month as classified misses per counted pull request, and add a row
for each month to [Calibration history](calibration-history.md) with the method
`Script: merged PRs, bot-commented repositories`. Report the date range, pull requests
examined, the candidate and miss rates by month and their trend in the history, the patterns added,
changed, or removed, and recommended bot tuning.
