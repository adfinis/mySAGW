export default function formatCurrency(value, currency) {
  return new Intl.NumberFormat("de-CH", {
    style: "currency",
    currency,
  })
    .format(value)
    .replace(".00", ".-");
}
