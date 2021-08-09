import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Ability | form-configuration", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const ability = this.owner.lookup("ability:form-configuration");
    assert.ok(ability);
  });
});
