import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Model | membership role", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const store = this.owner.lookup("service:store");
    const model = store.createRecord("membership-role", {});
    assert.ok(model);
  });
});
