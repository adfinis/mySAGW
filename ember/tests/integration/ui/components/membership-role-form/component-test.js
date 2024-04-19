import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "mysagw/tests/helpers";

module("Integration | Component | membership-role-form", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    await render(hbs`<MembershipRoleForm />`);
    assert.ok(this.element);
  });
});
