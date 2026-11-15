import { randomUUID } from "node:crypto";

import { normaliseEmail } from "./normaliseEmail.js";
import { addMember, roleOf } from "./teams.js";

export const INVITE_LIFETIME_MS = 7 * 24 * 60 * 60 * 1000;

export function createInviteStore() {
  return new Map();
}

export function inviteMember(teams, invites, { teamId, actor, email, now }) {
  if (roleOf(teams, teamId, actor) !== "admin") {
    return { ok: false, reason: "forbidden" };
  }
  if (roleOf(teams, teamId, email) !== undefined) {
    return { ok: false, reason: "already-member" };
  }
  const pending = [...invites.values()].filter(
    (invite) => invite.teamId === teamId && invite.email === email,
  );
  if (pending.length > 0) {
    return { ok: false, reason: "already-invited" };
  }
  const invite = { id: randomUUID(), teamId, email: normaliseEmail(email), createdAt: now };
  invites.set(invite.id, invite);
  return { ok: true, invite };
}

export function revokeInvite(teams, invites, { teamId, actor, inviteId }) {
  if (roleOf(teams, teamId, actor) !== "admin") {
    return { ok: false, reason: "forbidden" };
  }
  if (!invites.delete(inviteId)) {
    return { ok: false, reason: "not-found" };
  }
  return { ok: true };
}

export function acceptInvite(teams, invites, { inviteId, now }) {
  const invite = invites.get(inviteId);
  if (!invite) {
    return { ok: false, reason: "not-found" };
  }
  if (now - invite.createdAt > INVITE_LIFETIME_MS) {
    throw new Error("Invite expired");
  }
  addMember(teams, invite.teamId, invite.email, "member");
  invites.delete(inviteId);
  return { ok: true };
}
