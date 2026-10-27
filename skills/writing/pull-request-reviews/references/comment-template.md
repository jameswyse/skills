> [!NOTE]
> 🤖 {Model} responding on behalf of James

{One or two sentences: the overall assessment and the most important issue, or that the review found nothing worth changing.}

## {Correctness, Spec, or Standards. Include only axes with posted findings, in that order.}

### {The problem in plain words, such as "Orders can be saved with an unlocked price"}

{High or Medium} severity in [`{path}:{line}`]({pull request repository URL}/blob/{headRefOid}/{path}#L{start}-L{end})

{What goes wrong: the input or state that triggers it and the wrong result, or the repository rule it breaks with its source.}

{The smallest fix that resolves it, in a sentence or a short `diff` block.}

### {A Spec question in plain words, such as "Should archived orders be exported?"}

{Quote the requirement, describe what the change does instead, and ask which behaviour the author intends. Link the code when the question maps to it. Questions have no severity.}

{Order findings by severity within each axis, with questions last.}

## Resolved since the last review

- {Earlier finding, and the commit that resolved it. Include this section only on a re-review.}

<details>
<summary>How this review was run</summary>

{The run report from "code-review": its table and outcome line.}

Posted {h} high and {m} medium findings and {q} questions. Dropped {d} as low severity, personal preference, or already raised. Rejected {r} candidates.

</details>

{Write to the author directly, as one engineer to another. Use the codebase's terms, skip praise and filler, and leave out anything that needs the review run's context, such as packet paths, axis prompts, or model output.}
