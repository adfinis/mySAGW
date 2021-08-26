import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

import ENV from "mysagw/config/environment";

module("Unit | Controller | cases/detail/edit", function (hooks) {
  setupTest(hooks);

  test("it is setup properly", function (assert) {
    ENV.APP.caluma = {};
    ENV.APP.caluma.documentEditableTaskSlugs = ["test"];
    const controller = this.owner.lookup("controller:cases/detail/edit");
    controller.model = {
      workItems: {
        edges: [{ node: { status: "CANCELED", task: { slug: "test" } } }],
      },
    };
    assert.true(controller.disabled);
  });
});
