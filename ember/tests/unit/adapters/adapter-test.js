import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Adapter | case access", function (hooks) {
  setupTest(hooks);

  // Replace this with your real tests.
  test("it exists", function (assert) {
    const adapter = this.owner.lookup("adapter:case-access");
    assert.ok(adapter);
  });
});
