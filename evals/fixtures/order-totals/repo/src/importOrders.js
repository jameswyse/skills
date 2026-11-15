import { readFileSync } from "node:fs";

function splitRow(row) {
  const fields = [];
  let field = "";
  let quoted = false;
  for (const character of row) {
    if (character === '"') {
      quoted = !quoted;
    } else if (character === "," && !quoted) {
      fields.push(field);
      field = "";
    } else {
      field += character;
    }
  }
  fields.push(field);
  return fields;
}

export function parseFeed(text) {
  const [, ...rows] = text.trim().split("\n");
  const orders = new Map();
  for (const row of rows) {
    const [orderId, sku, quantity, unitPrice] = splitRow(row);
    const lines = orders.get(orderId) ?? [];
    lines.push({ sku, quantity: Number(quantity), unitPrice: Number(unitPrice) });
    orders.set(orderId, lines);
  }
  return [...orders].map(([id, lines]) => ({ id, lines }));
}

export function importOrders(path) {
  return parseFeed(readFileSync(path, "utf8"));
}
