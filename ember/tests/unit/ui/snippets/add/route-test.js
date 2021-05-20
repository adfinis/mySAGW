import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | snippets/add", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:snippets/add");
    assert.ok(route);
  });
});
