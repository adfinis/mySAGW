import ENV from "mysagw/config/environment";

export function arrayFromString(str) {
  return str.split(",").filter(Boolean);
}

export function stringFromArray(array, key) {
  return array
    .map((obj) => obj[key])
    .filter(Boolean)
    .join(",");
}

export function serializeOrder(orderString, orderAttribute) {
  const key = orderString.replace(/^-/, "");
  const attribute = ENV.APP.caluma.orderTypeKeys.attribute.includes(key)
    ? "attribute"
    : orderAttribute;

  return {
    [attribute]: key,
    direction: /^-/.test(orderString) ? "DESC" : "ASC",
  };
}
