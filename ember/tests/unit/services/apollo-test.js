import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Service | apollo", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const service = this.owner.lookup("service:apollo");
    assert.ok(service);
  });
});
