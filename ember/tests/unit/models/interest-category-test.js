import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Model | interest category", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const store = this.owner.lookup("service:store");
    const model = store.createRecord("interest-category", {});
    assert.ok(model);
  });
});
