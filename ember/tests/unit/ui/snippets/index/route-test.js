import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | snippets/index", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:snippets/index");
    assert.ok(route);
  });
});
