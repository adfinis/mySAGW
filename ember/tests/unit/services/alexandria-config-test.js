import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Service | alexandria-config", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const service = this.owner.lookup("service:alexandria-config");
    assert.ok(service);
  });
});
