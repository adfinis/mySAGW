import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Ability | snippet", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const ability = this.owner.lookup("ability:snippet");
    assert.ok(ability);
  });
});
