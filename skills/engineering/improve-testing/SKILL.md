---
name: improve-testing
description: Audit a whole repository or user-selected area by inventorying every test, ranking each test by the guarantee it protects, finding weak and removable tests, mapping important unprotected behaviour, assessing test tooling, and producing a visual HTML report. Use only when the user explicitly requests a testing audit or test-suite improvement review.
---

# Improve testing

Assess whether the test suite gives useful evidence that the code is correct. Treat line and branch coverage as supporting data only. The main unit of coverage is an important behavioural guarantee.

Apply `$engineering`. Read its [Testing](../engineering/references/testing.md) reference before judging a test. Read [Deep modules](../engineering/references/deep-modules.md) when a test seam or module interface is in question. Repository instructions, testing documentation, and established conventions take precedence.

This workflow is a read-only review apart from temporary inventory files and the HTML report. Do not edit tests, dependencies, configuration, or product code unless the user later asks for implementation.

## Establish the review boundary

Review the whole repository by default. If the user names an area, review that area and the callers, shared code, entrypoints, and integration seams needed to assess its guarantees.

Read the relevant repository instructions, architecture and domain documentation, testing guides, local skills, manifests, lockfiles, test configuration, scripts, and CI workflows. Apply a repository-local or available framework skill when its trigger matches the code under review. Do not install a tool or change the active toolchain for the audit.

Record the revision, working-tree state, requested scope, major areas, and exclusions. Derive areas from the repository's own packages, applications, domains, and entrypoints. Do not let recent Git history or the dirty tree narrow an unqualified whole-repository review.

## Build a complete inventory

Read [REVIEW-RUBRIC.md](REVIEW-RUBRIC.md) in full before building the assessment ledger.

Run `python3 <skill-dir>/scripts/collect_test_inventory.py <repository-root> --output <temporary-json-path>` to collect a static inventory. Repeat `--scope <path>` for a focused review. Read [the helper source](scripts/collect_test_inventory.py) only when adapting or diagnosing it.

Use the repository's native test collector or list mode when it is available through an existing local dependency and can run safely. Compare its executable test IDs with the static inventory. Inspect configuration, setup, fixtures, factories, mocks, snapshots, test data, and custom runners that affect collection.

The helper finds common declarations but cannot expand every macro, parameterised test, generated suite, inherited case, or custom DSL. Resolve its `dynamic_declarations`, `files_without_declared_cases`, and `read_warnings`. Treat the native collector as the authority for executable IDs. If no collector can list cases, inspect every test file and state the remaining collection limitation.

Keep a temporary assessment ledger using the row fields in [REVIEW-RUBRIC.md](REVIEW-RUBRIC.md). Account for every collected test ID as assessed, excluded with a reason, or unresolved. A generated fuzz input is not a durable test ID. Assess its property and generator as one test definition. For a parameterised declaration, list each stable runtime ID when the collector exposes it. Otherwise record the declaration, its parameter boundary, and the number of known cases.

For a large repository, work in non-overlapping batches so the inventory, test source, and owning production area stay in context together. When delegation is available and authorised, give each focused agent:

- one bounded set of test IDs and owning source paths;
- this skill's testing rubric;
- only the repository documentation and instructions that govern that area; and
- the ledger row schema, with no suggested verdicts.

Require each agent to account for every assigned ID. The coordinating agent reconciles duplicates and gaps, checks the returned evidence, and reopens every removal candidate and high-consequence guarantee gap before reporting it.

## Assess the test portfolio

For every test, explain the guarantee it claims to protect, the seam and oracle it uses, its unique value, its shortcomings, and the evidence for its verdict. Stack-rank all tests within the requested scope. Use ordinal ranks and qualitative value tiers. Do not invent a numeric quality score.

Derive guarantees independently from the tests. Trace product and domain requirements, public interfaces, state transitions, schemas, permission rules, calculations, failure handling, persistence, external seams, and important bug history. Map each important guarantee to `Strong`, `Partial`, `Indirect`, `None`, or `Unknown` protection. `None` and high-consequence `Partial` entries are the meaningful coverage gaps.

Assess the testing libraries and dependencies already in use. Identify each runner, assertion library, environment, browser tool, fixture or mocking tool, property-test tool, reporting tool, and overlapping framework. Recommend a dependency, replacement, or configuration change only when it closes a named guarantee gap, removes demonstrated duplication, improves determinism or diagnostics, or cuts measured suite cost. Confirm version-specific claims against current official documentation when access permits. Do not recommend churn because a tool is old or unfamiliar.

Run proportionate existing test commands when they are safe and useful. Capture collection failures, skipped tests, retries, timing, flakiness evidence, and CI differences. Do not run an expensive full suite only to create a health score. State any command, runtime path, browser, external service, or environment that was not exercised.

## Produce the HTML report

Before writing the report, read [HTML-REPORT.md](HTML-REPORT.md) in full. Use its scaffold and visual rules.

Write one static file to `<tmpdir>/testing-review-<timestamp>.html`. Resolve the temporary directory from `$TMPDIR`, then `/tmp` on Unix or `%TEMP%` on Windows. Keep generated inventories and working ledgers out of the repository.

The report must include:

1. The repository state, review boundary, inventory completeness, and verification evidence.
2. The testing-library and dependency assessment, including a direct `Keep` or evidence-backed improvement verdict.
3. Exact counts and accessible charts for the test-value tiers and verdicts.
4. The behavioural guarantee map, with the evidence and consequence for each weak or missing guarantee.
5. A prominent table of removal candidates. Include the guarantee, overlap or absence of value, concrete cost, removal reasoning, and the test that retains the useful protection. State directly when there are no supported candidates.
6. Tests that fall short and the smallest repair that would strengthen each one.
7. The complete stack-ranked test inventory. Give every test a stable ID, source location, guarantee, justification, shortcomings, value tier, ordinal rank, and `Keep`, `Improve`, or `Removal candidate` verdict.
8. Collection limitations and remaining review gaps.

Use charts to show exact inventory composition, not codebase health or invented coverage percentages. Keep the complete table searchable and readable without JavaScript. Use exact paths, symbols, test IDs, framework names, commands, and domain terms.

Inspect the rendered report at a desktop width and at `320px`. Confirm that the full inventory remains accessible, tables scroll without widening the page, charts include text values, filters have labels, colours are not the only status cue, and the page has no horizontal overflow. Fix the report before opening it with `open`, `xdg-open`, or `start`. Tell the user the absolute path.

End by asking which removal candidates, test repairs, or guarantee gaps the user wants to tackle. Selection does not authorise changes. Revalidate the chosen item against the current tree before implementing an explicitly requested change.
