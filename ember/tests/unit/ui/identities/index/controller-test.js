import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Controller | identities/index", function (hooks) {
  setupTest(hooks);

  test("it exists", async function (assert) {
    const controller = this.owner.lookup("controller:identities/index");
    assert.ok(controller);

    controller.totalPages = 3;
    assert.strictEqual(controller.pages.length, 3);

    controller.pageNumber = 2;
    await controller.search.perform({ target: { value: "test" } });
    assert.strictEqual(controller.searchTerm, "test");
    assert.strictEqual(controller.pageNumber, 1);
  });
});
