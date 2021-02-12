import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Controller | interests/index", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const controller = this.owner.lookup("controller:interests/index");
    assert.ok(controller);
  });
});
