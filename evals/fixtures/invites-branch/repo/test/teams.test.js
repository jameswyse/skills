import assert from "node:assert/strict";
import { test } from "node:test";

import { addMember, createTeamStore, roleOf } from "../src/teams.js";

test("a member is stored under their normalised address", () => {
  const teams = createTeamStore();
  addMember(teams, "team-1", " Ada@Example.com ", "admin");
  assert.equal(roleOf(teams, "team-1", "ada@example.com"), "admin");
});

test("a role in one team grants nothing in another", () => {
  const teams = createTeamStore();
  addMember(teams, "team-1", "ada@example.com", "admin");
  assert.equal(roleOf(teams, "team-2", "ada@example.com"), undefined);
});
