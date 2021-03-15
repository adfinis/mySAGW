import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Service | notification", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const service = this.owner.lookup("service:notification");
    assert.ok(service);
  });
});
