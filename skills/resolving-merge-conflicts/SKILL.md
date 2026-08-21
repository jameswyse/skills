---
name: resolving-merge-conflicts
description: "Resolve conflicts during an authorised in-progress Git merge or rebase. Use when the user asks to resolve conflicts, or when an authorised merge or rebase encounters them. Do not use for read-only conflict inspection or merge planning."
---

1. **See the current state** of the merge or rebase. Check Git history, the conflicting files, and the existing staged, unstaged, and untracked changes. Preserve unrelated work.

2. **Find the primary sources** for each conflict. Understand deeply why each change was made, and what the original intent was. Read the commit messages, check the PRs, check original issues/tickets.

3. **Resolve each hunk.** Preserve both intents where possible. Where they are incompatible, pick the intent that matches the merge's stated goal and note the trade-off. Do not invent new behaviour. Do not abort or restart the operation unless the user asks.

4. Discover the project's **automated checks** and run them, typically typecheck, then tests, then format. Fix anything the merge broke.

5. **Finish the authorised operation.** Stage only the resolved conflict paths. Preserve unrelated staged, unstaged, and untracked changes. Continue the active merge or rebase with its native command only when completion is within the authorised scope. Do not create a separate commit merely to record the resolution.
