import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Ability | membership-role", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const ability = this.owner.lookup("ability:membership-role");
    assert.ok(ability);
  });
});
