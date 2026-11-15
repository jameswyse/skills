export function orderTotal(order) {
  return order.lines.reduce((total, line) => total + line.quantity * line.unitPrice, 0);
}
