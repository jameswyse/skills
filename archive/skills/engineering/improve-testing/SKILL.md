---
name: improve-testing
description: Audit test value, behavioural guarantees, and test tooling when a testing review is explicitly requested.
disable-model-invocation: true
---

# Improve testing

Assess whether the test suite gives useful evidence that the code is correct. Treat line and branch coverage as supporting data only. The main unit of coverage is an important behavioural guarantee.

Use the "engineering" skill. Read the code-review [Testing](../code-review/references/testing.md) reference before judging a test. Read the engineering [Design](../engineering/references/design.md) reference when a test seam or module interface is in question. Repository instructions, testing documentation, and established conventions take precedence.

The review phase is read-only apart from temporary inventory files and the HTML report. Edit tests, dependencies, configuration, or product code only within an implementation request, including authorisation given before the review.

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

Use the "html-report" skill to build and deliver the report. Before writing it, read [HTML-REPORT.md](HTML-REPORT.md) in full. It owns the report's sections, tables, and output location in the temporary directory. Keep generated inventories and working ledgers out of the repository.

The report must include, in this order:

1. A direct summary of the most consequential gap or removal and what to do first.
2. Removal candidates, with the guarantee, missing value, concrete cost, removal reasoning, and the test that retains the useful protection. State directly when there are no supported candidates.
3. Weak and missing behavioural guarantees, with the evidence and consequence for each.
4. Tests that fall short and the smallest repair that would strengthen each one.
5. Testing tools and dependencies that need a change, with the `Keep` tools listed in one line.
6. Exact counts by value tier and verdict, and the complete stack-ranked inventory in a closed disclosure. Give every test a stable ID, source location, guarantee, justification, shortcomings, value tier, ordinal rank, and `Keep`, `Improve`, or `Removal candidate` verdict.
7. Inventory completeness, verification evidence, and remaining review gaps.

Use charts to show exact inventory composition, not codebase health or invented coverage percentages. Keep the complete table searchable and readable without JavaScript. Use exact paths, symbols, test IDs, framework names, commands, and domain terms.

After a review-only request, ask which removal candidates, test repairs, or guarantee gaps the user wants to tackle. Selecting an item for discussion does not authorise changes. If implementation is already authorised, apply the governing authority rules and continue with covered changes. Revalidate the chosen items against the current tree before implementation.
