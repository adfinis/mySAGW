import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Controller | membership-roles/index", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const controller = this.owner.lookup("controller:membership-roles/index");
    assert.ok(controller);
  });
});
