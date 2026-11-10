# Fix and verify an authorised change

Read only when the user requested a fix.

## Challenge the cause

Before fixing, ask a contrarian to argue that the cause you settled on is wrong, unless an observation you've already made rules out the alternatives, such as changing only the suspected cause and watching the symptom appear and disappear. Follow the engineering [Cross-provider delegation](../../engineering/references/cross-provider-delegation.md#contrarian) reference, treating each alternative as a part of the judgement. Ask it to name the observation that would tell each alternative apart from your cause, and give it the symptom, the evidence, the alternatives you ruled out, and the affected paths. When the existing evidence can't rule out an alternative, make that observation if it's available and proportionate, or report the alternative as a verification gap. Then fix the cause the evidence supports.

## Add a regression test at the right seam

Write the regression test before the fix only when a seam exercises the real bug pattern as it occurs at the call site. A seam too shallow to reproduce the triggering chain, such as a single-caller test for a bug that needs several callers, gives false confidence. Without one, record the limitation and use the closest useful check under the code-review [Testing](../../code-review/references/testing.md) reference. Watch the test fail before the fix and pass after it, then rerun the original, unminimised reproduction.

## Finish

Before declaring the fix done:

- The original reproduction no longer fails, or the report names the closest check run and the symptom left unexercised.
- All `[DEBUG-...]` instrumentation and throwaway artefacts are removed. Search for the prefix.
- The report, and the commit or pull request description when the task includes one, states the confirmed cause and its evidence.
