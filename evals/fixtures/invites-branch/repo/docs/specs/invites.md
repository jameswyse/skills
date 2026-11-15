# Team invites

An admin invites a person to a team by email. The person joins as a member when they accept.

## Requirements

1. Only an admin of a team may invite people to that team or revoke that team's invites. Anyone else gets `forbidden`.
2. Email addresses are trimmed and compared without regard to case everywhere.
3. Inviting an address that already belongs to the team returns `already-member`. Inviting an address with a pending invite to the team returns `already-invited`.
4. A team has at most 5 pending invites. A further invite returns `invite-limit`.
5. An invite lasts 7 days. Accepting it later returns `expired` and leaves the team unchanged.
6. Accepting an invite adds the address to the team as a `member` and removes the invite.
