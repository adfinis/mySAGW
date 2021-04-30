import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Controller | snippets/add", function (hooks) {
  setupTest(hooks);

  // TODO: Replace this with your real tests.
  test("it exists", function (assert) {
    const controller = this.owner.lookup("controller:snippets/add");
    assert.ok(controller);
  });
});
