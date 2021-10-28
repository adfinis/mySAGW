import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Route | form/configuration", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const route = this.owner.lookup("route:form/configuration");
    assert.ok(route);
  });
});
