import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

import ENV from "mysagw/config/environment";

module("Unit | Controller | cases/detail/edit", function (hooks) {
  setupTest(hooks);

  hooks.beforeEach(function () {
    this.owner.register(
      "service:session",
      {
        isAuthenticated: true,
        data: {
          authenticated: {
            userinfo: { email: "lorem@ipsum.co", mysagw_groups: ["sagw"] },
          },
        },
      },
      { instantiate: false }
    );
  });

  test("it is setup properly", function (assert) {
    ENV.APP.caluma = {};
    ENV.APP.caluma.documentEditableTaskSlugs = ["test"];
    const controller = this.owner.lookup("controller:cases/detail/edit");
    controller.model = {
      hasEditableWorkItem: false,
      accesses: [{ email: "test@test.com" }],
    };
    assert.true(controller.disabled);
  });
});
