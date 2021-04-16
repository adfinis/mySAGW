import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Adapter | identity", function (hooks) {
  setupTest(hooks);

  // Replace this with your real tests.
  test("it exists", function (assert) {
    const adapter = this.owner.lookup("adapter:identity");
    assert.ok(adapter);
  });
});
