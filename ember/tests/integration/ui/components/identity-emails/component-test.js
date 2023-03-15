import { render, click, fillIn } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "mysagw/tests/helpers";

module("Integration | Component | identity-emails", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    this.identity = this.server.create("identity");

    await render(hbs`<IdentityEmails @identity={{this.identity}} />`);

    assert.dom("h2").includesText("t:components.identity-emails.title:()");
  });

  // Mirage does not work for relationships
  test.skip("it can add new emails", async function (assert) {
    this.identity = this.server.create("identity");

    await render(hbs`<IdentityEmails @identity={{this.identity}} />`);

    await click("[data-test-email-add]");

    assert.dom("form").exists();

    await fillIn("input[name=email]", "test@example.com");
    await click("button[type=submit]");

    assert.dom("form").doesNotExist();
  });
});
