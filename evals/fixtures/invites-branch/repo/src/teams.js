import { normaliseEmail } from "./normaliseEmail.js";

export function createTeamStore() {
  return new Map();
}

export function addMember(teams, teamId, email, role) {
  const members = teams.get(teamId) ?? new Map();
  members.set(normaliseEmail(email), role);
  teams.set(teamId, members);
}

export function roleOf(teams, teamId, normalisedEmail) {
  return teams.get(teamId)?.get(normalisedEmail);
}
