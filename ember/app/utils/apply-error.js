export default function applyError(changeset, error) {
  error?.errors
    .filter(
      ({ source: { pointer } }) =>
        pointer.startsWith("/data/attributes") &&
        !pointer.endsWith("non-field-errors")
    )
    .map(({ detail, source: { pointer } }) => ({
      field: pointer.substr(pointer.lastIndexOf("/") + 1),
      message: detail,
    }))
    .forEach(({ field, message }) => changeset.addError(field, message));
}
