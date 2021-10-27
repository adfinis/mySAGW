import { module, test } from "qunit";

import formatError from "mysagw/utils/format-error";

module("Unit | Utility | format-error", function () {
  test("it handles strings", function (assert) {
    const error = "Error";
    const result = formatError(error);
    assert.strictEqual(result, "Error");
  });

  test("it handles normal errors", function (assert) {
    const error = new Error("Error");
    const result = formatError(error);
    assert.strictEqual(result, "Error");
  });

  test("it handles JSON:API errors", function (assert) {
    const error = {
      errors: [{ detail: "Error 1" }, { detail: "Error 2" }],
    };
    const result = formatError(error);
    assert.strictEqual(result, "Error 1, Error 2");
  });
});
