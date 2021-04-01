import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Ability | additional-email", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const ability = this.owner.lookup("ability:additional-email");
    assert.ok(ability);
  });
});
