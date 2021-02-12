import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | interests/edit", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:interests/edit");
    assert.ok(route);
  });
});
