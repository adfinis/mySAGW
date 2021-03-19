import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | membership-roles/add", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:membership-roles/add");
    assert.ok(route);
  });
});
