import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Ability | phone-number", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const ability = this.owner.lookup("ability:phone-number");
    assert.ok(ability);
  });
});
