import { importOrders } from "./importOrders.js";
import { orderTotal } from "./orderTotal.js";

const currency = new Intl.NumberFormat("en-AU", { style: "currency", currency: "AUD" });

export function formatInvoice(order) {
  return `Order ${order.id}: ${currency.format(orderTotal(order))}`;
}

if (import.meta.main) {
  for (const order of importOrders(process.argv[2])) {
    console.log(formatInvoice(order));
  }
}
