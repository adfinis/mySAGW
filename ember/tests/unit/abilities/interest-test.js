import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Ability | interest", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const ability = this.owner.lookup("ability:interest");
    assert.ok(ability);
  });
});
