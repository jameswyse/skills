import assert from "node:assert/strict";
import { test } from "node:test";

import { orderTotal } from "../src/orderTotal.js";

test("sums quantity times unit price across lines", () => {
  const order = {
    id: "1",
    lines: [
      { sku: "A", quantity: 2, unitPrice: 1.5 },
      { sku: "B", quantity: 1, unitPrice: 4 },
    ],
  };
  assert.equal(orderTotal(order), 7);
});

test("an order with no lines totals zero", () => {
  assert.equal(orderTotal({ id: "2", lines: [] }), 0);
});
