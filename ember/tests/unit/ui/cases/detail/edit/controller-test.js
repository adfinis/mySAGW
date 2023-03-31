import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Controller | cases/detail/edit", function (hooks) {
  setupTest(hooks);

  hooks.beforeEach(function () {
    this.controller = this.owner.lookup("controller:cases/detail/edit");
    this.controller.model = {
      hasEditableWorkItem: false,
      accesses: [{ email: "test@test.com" }],
    };
  });

  test("no access", function (assert) {
    this.owner.register(
      "service:session",
      {
        isAuthenticated: true,
        data: {
          authenticated: {
            userinfo: { email: "lorem@ipsum.co", mysagw_groups: [] },
          },
        },
      },
      { instantiate: false }
    );

    assert.true(this.controller.disabled);
  });

  test("admin access", function (assert) {
    this.owner.register(
      "service:session",
      {
        isAuthenticated: true,
        data: {
          authenticated: {
            userinfo: { email: "lorem@ipsum.co", mysagw_groups: ["admin"] },
          },
        },
      },
      { instantiate: false }
    );

    assert.false(this.controller.disabled);
  });

  test("user access", function (assert) {
    this.owner.register(
      "service:session",
      {
        isAuthenticated: true,
        data: {
          authenticated: {
            userinfo: { email: "lorem@ipsum.co", mysagw_groups: [] },
          },
        },
      },
      { instantiate: false }
    );
    this.controller.model = {
      hasEditableWorkItem: true,
      accesses: [{ email: "lorem@ipsum.co" }],
    };

    assert.true(this.controller.disabled);
  });
});
