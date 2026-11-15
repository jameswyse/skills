# Visual evidence

Use when a pull request changes an interface, to show reviewers what changed before they open the diff.

## Capture

Use the browser tool available in the session, such as agent-browser or the T3 Code preview tools, and follow its own instructions. Without one, use screenshots the user supplied, or state in the description that no visual evidence is attached.

- Capture before from the base branch or production, and after from the branch or its preview deployment. A new screen needs only an after capture.
- Use the same viewport, data, and state for each pair, and the same scoped region for a component. GitHub centres a shorter image in a table cell, so make each pair the same height.
- Add a mobile pair when the change affects small screens.
- Save captures to a new temporary directory, never the repository. Keep tokens, signed URLs, personal data, and browser state out of them.

## Write the block

Put the evidence near the top of the description, after the opening context and before implementation detail. Write images as a table with local paths relative to the body file:

```markdown
| Before                                          | After                                         |
| ----------------------------------------------- | --------------------------------------------- |
| ![Before: settings page](./settings-before.png) | ![After: settings page](./settings-after.png) |
```

Label a mobile row or extra states in the alt text. Put each video in a paragraph of its own, with a blank line before and after, as `![Checkout flow](./checkout.mp4)`. GitHub renders it as a player only there.

## Publish

Write the body file in the same temporary directory as the captures. For an existing pull request, start it from the current description, `gh pr view <number> --json body --jq .body`, and change only the evidence block. Then attach each capture as you publish:

```bash
gh pr edit <number> --body-file <tmpdir>/body.md \
  --attach <tmpdir>/settings-before.png --attach <tmpdir>/settings-after.png
```

`gh pr create` takes the same `--attach` flags. GitHub uploads each file and rewrites its local reference to the hosted asset.

Before publishing, check every capture, including any the user supplied, for secrets and private details. Then read the body back with `gh pr view <number> --json body` and confirm no local paths remain. When an upload fails, `gh` still updates the pull request with the files that succeeded and exits non-zero, so rerun the whole command with every `--attach` flag.
