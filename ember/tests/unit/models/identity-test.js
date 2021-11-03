import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Model | identity", function (hooks) {
  setupTest(hooks);

  test("it exists", function (assert) {
    const store = this.owner.lookup("service:store");
    const model = store.createRecord("identity", {
      firstName: "John",
      lastName: "Doe",
    });
    assert.ok(model);
    assert.strictEqual(model.fullName, "Doe John");
  });
});
