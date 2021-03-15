export default function formatError(error) {
  if (error.payload) {
    error = error.payload;
  }

  // Handle non-JSON:API errors.
  // Can be an Error object or simple string.
  if (!error.errors) {
    return error.message || error;
  }

  return error.errors.map(({ detail }) => detail).join(", ");
}
