# Fix and verify an authorised change

Read only when the user requested a fix. Keep work within that authority, including approval already given before diagnosis. Use the code-review [testing reference](../../code-review/references/testing.md) when designing a test or choosing its seam.

## Challenge the cause

Before fixing, ask a contrarian to argue that the cause you settled on is wrong, as the engineering [Cross-provider delegation](../../engineering/references/cross-provider-delegation.md#contrarian) reference describes. Ask it to name the observation that would tell each alternative apart from your cause, and give it the symptom, the evidence, the alternatives you ruled out, and the affected paths. When the existing evidence can't rule out an alternative, make that observation if it's available and proportionate, or report the alternative as a verification gap. Then fix the cause the evidence supports.

## Fix with a practical regression test

Write the regression test **before the fix**, but only if there is a **correct seam** for it.

A correct seam lets the test exercise the **real bug pattern** as it occurs at the call site. The available seam may be too shallow. Examples include a single-caller test for a bug that needs several callers, or a unit test that cannot reproduce the chain that triggered the bug. A regression test at that seam gives false confidence.

If no practical test seam exists, record the limitation and use the closest useful check under the code-review [testing reference](../../code-review/references/testing.md). Distinguish architectural constraints from missing access, tooling, or an expensive test environment. Do not infer an architecture defect merely because no test was added.

If a correct seam exists:

1. Turn the minimised repro into a failing test at that seam.
2. Watch it fail.
3. Apply the fix.
4. Watch it pass.
5. Re-run the original feedback loop against the original (un-minimised) scenario.

## Verify and clean up

Required before declaring the fix done:

- [ ] The original reproduction no longer fails, or the closest available check and the unexercised original symptom are stated explicitly. An inaccessible runtime remains unverified even when source evidence supports the fix.
- [ ] The regression test passes, or the absence of a suitable seam is documented.
- [ ] All `[DEBUG-...]` instrumentation is removed. Search for the prefix.
- [ ] Throwaway artefacts are removed from the temporary directory or kept only at a location the user requested.
- [ ] The confirmed cause and its evidence are stated plainly.
- [ ] The correct hypothesis is stated in the commit or PR description when the task includes writing one.
