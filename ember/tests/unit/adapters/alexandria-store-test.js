import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Adapter | alexandria-store", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const adapter = this.owner.lookup("adapter:alexandria-store");
    assert.ok(adapter);
  });
});
