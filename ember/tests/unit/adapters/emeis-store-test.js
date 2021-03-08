import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Adapter | emeis-store", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const adapter = this.owner.lookup("adapter:emeis-store");
    assert.ok(adapter);
  });
});
