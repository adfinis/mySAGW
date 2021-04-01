import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Ability | interest-category", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const ability = this.owner.lookup("ability:interest-category");
    assert.ok(ability);
  });
});
