import assert from "node:assert/strict";
import { test } from "node:test";

import {
  INVITE_LIFETIME_MS,
  acceptInvite,
  createInviteStore,
  inviteMember,
  revokeInvite,
} from "../src/invites.js";
import { addMember, createTeamStore, roleOf } from "../src/teams.js";

function teamWithAdmin() {
  const teams = createTeamStore();
  addMember(teams, "team-1", "ada@example.com", "admin");
  addMember(teams, "team-1", "bob@example.com", "member");
  return teams;
}

function inviteCy(teams, invites) {
  return inviteMember(teams, invites, {
    teamId: "team-1",
    actor: "ada@example.com",
    email: "cy@example.com",
    now: 0,
  });
}

test("an admin invites a new address", () => {
  const result = inviteCy(teamWithAdmin(), createInviteStore());
  assert.equal(result.ok, true);
  assert.equal(result.invite.email, "cy@example.com");
});

test("a member cannot invite", () => {
  const result = inviteMember(teamWithAdmin(), createInviteStore(), {
    teamId: "team-1",
    actor: "bob@example.com",
    email: "cy@example.com",
    now: 0,
  });
  assert.deepEqual(result, { ok: false, reason: "forbidden" });
});

test("an existing member cannot be invited", () => {
  const result = inviteMember(teamWithAdmin(), createInviteStore(), {
    teamId: "team-1",
    actor: "ada@example.com",
    email: "bob@example.com",
    now: 0,
  });
  assert.deepEqual(result, { ok: false, reason: "already-member" });
});

test("accepting adds the address as a member", () => {
  const teams = teamWithAdmin();
  const invites = createInviteStore();
  const { invite } = inviteCy(teams, invites);
  assert.deepEqual(acceptInvite(teams, invites, { inviteId: invite.id, now: 1000 }), { ok: true });
  assert.equal(roleOf(teams, "team-1", "cy@example.com"), "member");
});

test("an invite stops working after its lifetime", () => {
  const teams = teamWithAdmin();
  const invites = createInviteStore();
  const { invite } = inviteCy(teams, invites);
  assert.throws(() => acceptInvite(teams, invites, { inviteId: invite.id, now: INVITE_LIFETIME_MS + 1 }));
});

test("an admin revokes an invite", () => {
  const teams = teamWithAdmin();
  const invites = createInviteStore();
  const { invite } = inviteCy(teams, invites);
  const result = revokeInvite(teams, invites, { teamId: "team-1", actor: "ada@example.com", inviteId: invite.id });
  assert.deepEqual(result, { ok: true });
});
