# Fix and verify an authorised change

## Challenge the cause

Before fixing, ask a contrarian to argue that the cause you settled on is wrong, as the Contrarian section of "delegation" describes. Skip this only when an observation you've already made rules out the alternatives, such as changing only the suspected cause and watching the symptom appear and disappear. Treat each alternative as a part of the judgement. Give it the symptom, the evidence, the alternatives you ruled out, and the affected paths, and ask for the observation that would tell each alternative apart from your cause. When the evidence can't rule out an alternative, make that observation if it's available and proportionate, or report the alternative as a verification gap. Then fix the cause the evidence supports, following the "engineering" skill's source-fix rules.

## Add a regression test at the right seam

Write the regression test before the fix only when a seam exercises the real bug pattern as it occurs at the call site. A seam too shallow to reproduce the triggering chain, such as a single-caller test for a bug that needs several callers, gives false confidence. Without one, record the limitation and use the closest useful check under the code-review [Testing](../../code-review/references/testing.md) reference. Watch the test fail before the fix and pass after it, then rerun the original, unminimised reproduction.

## Finish

- The original reproduction no longer fails, or the report names the closest check run and the symptom left unexercised.
- No `[DEBUG-...]` instrumentation or throwaway artefact remains. Search for the prefix.
- The report, and the commit or pull request description when the task includes one, states the confirmed cause and its evidence.
