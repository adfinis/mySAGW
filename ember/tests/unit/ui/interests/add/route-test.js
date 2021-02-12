import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | interests/add", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:interests/add");
    assert.ok(route);
  });
});
