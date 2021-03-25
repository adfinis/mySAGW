import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Controller | identities/edit", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const controller = this.owner.lookup("controller:identities/edit");
    assert.ok(controller);
  });
});
