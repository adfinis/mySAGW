import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Controller | cases/detail/edit", function (hooks) {
  setupTest(hooks);

  test("it is setup properly", function (assert) {
    const controller = this.owner.lookup("controller:cases/detail/edit");
    controller.model = { status: "CANCELED" };
    assert.true(controller.disabled);
  });
});
