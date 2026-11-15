import assert from "node:assert/strict";
import { test } from "node:test";

import { joinUrl } from "./joinUrl.ts";

test("joins a base URL and a path with one slash", () => {
  assert.equal(
    joinUrl("https://api.example.com/", "/accounts/a1"),
    "https://api.example.com/accounts/a1",
  );
});
