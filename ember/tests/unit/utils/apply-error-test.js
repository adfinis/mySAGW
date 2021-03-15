import Changeset from "ember-changeset";
import applyError from "mysagw/utils/apply-error";
import { module, test } from "qunit";

module("Unit | Utility | apply-error", function () {
  test("it works", function (assert) {
    const changeset = new Changeset({
      name: "Test",
    });
    const error = {
      errors: [
        {
          detail: "This is wrong",
          source: { pointer: "/data/attributes/name" },
        },
      ],
    };

    applyError(changeset, error);
    assert.deepEqual(changeset.errors[0], {
      key: "name",
      value: "Test",
      validation: "This is wrong",
    });
  });
});
