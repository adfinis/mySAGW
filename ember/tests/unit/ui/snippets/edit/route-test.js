import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | snippets/edit", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:snippets/edit");
    assert.ok(route);
  });
});
