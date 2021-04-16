import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Ability | form-builder", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const ability = this.owner.lookup("ability:form-builder");
    assert.ok(ability);
  });
});
