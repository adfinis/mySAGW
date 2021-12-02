import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Ability | case", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const ability = this.owner.lookup("ability:case");
    assert.ok(ability);
  });
});
