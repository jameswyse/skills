# Airteam review labels

A review label tells reviewers where a pull request carries a risk they should check. Reviewers ignore labels that appear on most pull requests, so label the risk, not every area the change touches.

## Scope

Apply review labels only to a pull request whose base repository is a private `airteamaus` repository. Check it once the pull request exists:

1. Take `<owner>/<repo>` from the pull request's URL, then run `gh repo view <owner>/<repo> --json owner,visibility,viewerPermission`.
2. Continue only when `owner.login` is `airteamaus`, `visibility` is `PRIVATE`, and `viewerPermission` is `WRITE`, `MAINTAIN`, or `ADMIN`.

When a check fails or the command errors, skip labels and say which check failed in the report. A pull request from a fork is judged by its base repository, so one from an Airteam fork to an upstream project is out of scope.

## Labels

These baseline labels apply to every Airteam repository. Each entry gives the label's colour and description, then the harm it marks.

- `database` (`5319e7`, "Changes PostgreSQL or Redis"). A mistake could lose, corrupt, or slow down data, or change its shape, such as through a new query client, a transaction or locking change, or a new query on a large table.
- `security` (`b60205`, "Changes authentication, secrets or input validation"). A mistake could let someone see or do something they shouldn't, expose a token or secret, or let untrusted input through. A change that could only stop a legitimate sign-in or connection from working isn't a `security` risk.
- `aws` (`ff9900`, "Affects AWS configuration, images or deployment"). A mistake could break the Docker image, the deployment, or AWS resources and permissions, including objects the service newly writes or deletes, such as files in S3.
- `pricing` (`fbca04`, "Changes prices or how they're calculated"). A mistake could change a price a customer sees or pays, including what happens when price inputs can't be loaded.
- `deploy order` (`0052cc`, "Needs another change released first or alongside it"). Releasing this pull request alone could break or degrade something until another repository's change, infrastructure, a configuration value, or a manual step ships with or before it. A feature that stays off until someone configures it doesn't count, and neither does order within the pull request's own stack, because the stack already merges in order.
- `dependencies` (`0366d6`, "Pull requests that update a dependency file"). Updated dependency versions are the main change, and they don't change runtime behaviour in another label's area, such as an upgrade that only affects development tooling. When an upgrade or replacement changes runtime behaviour in such an area, apply that area's label instead.

### Repository labels

A repository can define review labels for its own risks, such as `multi-tenancy` in a multi-tenant backend. List them with `gh api --paginate repos/<owner>/<repo>/labels --jq '.[] | [.name, .description] | @tsv'`. Outside the baseline, a label is a review label only when its description begins with "Adds", "Affects", "Changes", or "Needs". Its description is its definition. Read it as the harm a mistake in that area could cause, such as breaking a client for an API label. Ignore every other label, such as GitHub's defaults, Dependabot's ecosystem labels like `javascript`, and status labels like `WIP` or `Deploy`.

When the same risk keeps recurring in a repository's pull requests and no label covers it, propose a repository label in the report with a name, colour, and description that begins with one of those words. Create it only after the user approves. When a second repository needs the same label, propose adding it to this baseline instead.

## Choose labels

1. Start with no labels. Most pull requests need one or none. Refactors, renames, tests, and documentation usually need none, however large.
2. Apply a label only when a mistake in this diff could cause the harm the label marks, and a reviewer needs to check for it. Write its reason as one sentence naming the specific change and that harm. A change that touches an area but can't cause that label's harm doesn't count. For example, a new endpoint can't break a client that doesn't call it yet, though it can still carry a `security` risk.
3. Give each risk one label, the most specific that fits. A schema change gets `migration` where the repository has that label, not `database` as well.
4. Label only the risk this pull request carries. When it relies on a change reviewed elsewhere, such as infrastructure from another repository, apply `deploy order` instead of the label for that change.
5. Apply at most three labels. When more seem to apply, recheck each against steps 2 and 3 instead of picking three, because that usually means areas are being labelled. If more than three still apply, keep the three with the most harm and suggest splitting the pull request in the report.

Keep each label's reason for the review step and the report. Don't add a labels section to the body.

These labels from the backend stack this guidance was calibrated on show where the line falls. `api`, `integrations`, and `multi-tenancy` are that repository's own labels, so apply them only where a repository defines them.

| Change                                                                                                     | Labels                             |
| ---------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| Split a 2,000-line data module by concept, leaving the GraphQL schema identical                            | None                               |
| Replace five lodash helpers with native JavaScript                                                         | None                               |
| Upgrade dependencies to fix `pnpm audit` findings                                                          | `dependencies`                     |
| Upgrade the HTTP client that uploads attachments to a partner API                                          | `integrations`                     |
| Replace the clients that sign in to the cache and call a payment provider, keeping their behaviour         | `integrations`                     |
| Replace the PostgreSQL query client, losing automatic retries after deadlocks                              | `database`                         |
| Remove development dependencies from production Docker images                                              | `aws`                              |
| Add developer commands that copy a tenant's CMS content into its database tables                           | `multi-tenancy`                    |
| Add user lookup queries whose identity-provider calls need an IAM permission from an infrastructure change | `security`, `deploy order`         |
| Route content reads through a new data source, changing some responses and quotes                          | `pricing`, `api`                   |
| Add a staff API, off by default, that saves a tenant's content and its files in S3                         | `security`, `aws`, `multi-tenancy` |

## Stacks

Label each layer from its own diff against the layer below, not the stack's combined diff. When a lower layer changes, choose labels again only for layers whose own diff changed.

## Apply labels

1. Create each chosen baseline label the repository lacks, because `gh` rejects unknown labels: `gh label create <name> -R <owner>/<repo> --color <colour> --description <description>`, with exactly the definition above. When the label already exists, use it as it is. Never edit or delete a repository's existing labels, and name each label you created in the report.
2. For a new pull request or stack layer, add the labels once it exists with `gh pr edit <url> --add-label <labels>`.
3. For an existing pull request, choose labels again from its current diff. Immediately before editing, read its current labels with `gh pr view <url> --json labels` and the labels anyone removed from it before:

   ```bash
   gh api --paginate repos/<owner>/<repo>/issues/<number>/events \
     --jq '.[] | select(.event == "unlabeled") | .label.name'
   ```

   Add each chosen label it lacks that wasn't removed before, with the command in step 2. Don't remove labels. In the report, name each review label that no longer seems to apply, with its reason.

For a request to draft without publishing, return the proposed labels and their reasons with the draft.
