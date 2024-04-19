import { render, click, fillIn } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { authenticateSession } from "ember-simple-auth/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "mysagw/tests/helpers";

module("Integration | Component | identity-phone-numbers", function (hooks) {
  setupRenderingTest(hooks);
  hooks.beforeEach(async function () {
    await authenticateSession({ userinfo: { mysagw_groups: ["sagw"] } });
  });

  test("it renders", async function (assert) {
    this.identity = this.server.create("identity");

    await render(hbs`<IdentityPhoneNumbers @identity={{this.identity}} />`);

    assert
      .dom("h2")
      .includesText("t:components.identity-phone-numbers.title:()");
  });

  // Mirage does not work for relationships
  test.skip("it can add new phone number", async function (assert) {
    this.identity = this.server.create("identity");

    await render(hbs`<IdentityPhoneNumbers @identity={{this.identity}} />`);

    await click("[data-test-phone-add]");

    assert.dom("form").exists();

    await fillIn("input[name=phone]", "+41 31 321 45 67");
    await click("button[type=submit]");

    assert.dom("form").doesNotExist();
  });
});
