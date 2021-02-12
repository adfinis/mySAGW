function get(params, key) {
  return params[`filter[${key}]`];
}

export default function parseFilters({ queryParams }, filters) {
  return filters
    .filter((filter) => get(queryParams, filter.source) !== undefined)
    .map((filter) => ({ [filter.target]: get(queryParams, filter.source) }))
    .reduce((query, filter) => Object.assign(query, filter), {});
}
