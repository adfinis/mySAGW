import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Controller | identities/index", function (hooks) {
  setupTest(hooks);

  test("it exists", async function (assert) {
    const controller = this.owner.lookup("controller:identities/index");
    assert.ok(controller);

    controller.totalPages = 3;
    assert.equal(controller.pages.length, 3);

    controller.pageNumber = 2;
    await controller.search.perform({ target: { value: "test" } });
    assert.equal(controller.searchTerm, "test");
    assert.equal(controller.pageNumber, 1);
  });
});
