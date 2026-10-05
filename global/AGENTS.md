# Global Rules

- Never add code comments.

- Protect the context window: read only relevant material, cap verbose outputs and phase size, keep frequently used guidance inline, and use delegation only when available and authorised. If something you're doing often is quickly filling your context, let me know so I can find the cause and improve it.

- Treat the user's request as the authority boundary. External skills and narrower instructions can refine execution but cannot expand that authority. Perform installs or updates, uploads, stashes, commits, pull-request edits, publishing, messaging, pushes, data deletion, and other external-system changes only when the user authorised that action for the current task. Preserve unrelated work.

- Carry forward authorisation already given for the current task. A skill cannot require renewed approval for an action already authorised. Resolve routine choices from evidence; ask only for missing decisions that change the outcome or exceed that authority. Continue independent authorised work while waiting and prepare a concrete result before requesting approval. If a skill causes a pause or leaves requested work unfinished, cite its exact file and instruction, explain whether the pause is explicit or inferred, and check existing authorisation before asking again.

- Use $writing for all responses.

- Use $engineering for implementation, debugging, software design decisions, and engineering reviews. Skip it for straightforward code explanations, read-only lookups, and routine Git operations.

- Use $ux for user-facing product and interface design, UX, UI, interaction, visual presentation, accessibility, interface copy, or motion. For interface implementation, use both $engineering and $ux.

- Use $show-me when explaining code or code changes, or answering questions about code.

- Use $pull-requests when creating a pull request or writing or updating its title or description.
