import { render, click, fillIn } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";

module("Integration | Component | identity-emails", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);

  test("it renders", async function (assert) {
    this.server.create("identity");

    this.identity = { id: "1" };

    await render(hbs`<IdentityEmails @identity={{this.identity}} />`);
    assert.ok(this.element);

    assert.dom("[data-test-email-list").exists();
    // The 3 emails are defined in mirage/factories/identity.js
    assert.dom("[data-test-email-item").exists({ count: 3 });
  });

  test("it can add new addresses", async function (assert) {
    this.server.create("identity");

    this.identity = { id: "1" };

    await render(hbs`<IdentityEmails @identity={{this.identity}} />`);
    assert.ok(this.element);

    await click("[data-test-email-add]");

    assert.dom("form").exists();

    await fillIn("input[name=email]", "test@example.com");
    await click("button[type=submit]");

    assert.dom("form").doesNotExist();
  });
});
