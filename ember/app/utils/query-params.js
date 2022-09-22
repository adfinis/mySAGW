export function arrayFromString(str) {
  return str.split(",").filter(Boolean);
}

export function stringFromArray(array, key) {
  return array
    .map((obj) => obj[key])
    .filter(Boolean)
    .join(",");
}
