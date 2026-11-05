> [!NOTE]
> 🤖 {Model} responding on behalf of James

{One or two sentences: the overall assessment and the most important issue, or that the review found nothing worth changing.}

## {Correctness, Spec, or Standards. Include only axes with P0, P1, or P2 findings or questions, in that order.}

### F1 [P1] {The problem in plain words, such as "Orders can be saved with an unlocked price"}

[`{path}:{line}`]({pull request repository URL}/blob/{headRefOid}/{path}#L{start}-L{end})

{What goes wrong: the input or state that triggers it and the wrong result, or the repository rule it breaks with its source.}

{The smallest fix that resolves it, in a sentence or a short `diff` block.}

### Q1 {A Spec question in plain words, such as "Should archived orders be exported?"}

{Quote the requirement, describe what the change does instead, and ask which behaviour the author intends. Link the code when the question maps to it. Questions have no priority.}

{Order findings by priority within each axis, with questions last.}

## Low-priority findings

- F4 [P3] {The problem and its fix in one line}, in [`{path}:{line}`]({link as above}). {Include this section only with P3 findings, which appear nowhere else.}

## Accepted risks

- R1 {The risk and why its fix isn't worth the complexity, in one line}, in [`{path}:{line}`]({link as above}). {Include this section only with accepted risks.}

## Resolved since the last review

- F2 {Earlier finding, and the commit that resolved it. Include this section only on a re-review.}

<details>
<summary>How this review was run</summary>

{The run report from "code-review": its table and outcome line, with priority labels in place of severity words.}

Posted {n} findings ({p0} P0, {p1} P1, {p2} P2, {p3} P3), {q} questions, and {a} accepted risks. Dropped {d} as personal preference or already raised. Rejected {r} candidates.

</details>

{Write to the author directly, as one engineer to another. Use the codebase's terms, skip praise and filler, and leave out anything that needs the review run's context, such as packet paths, axis prompts, or model output.}
