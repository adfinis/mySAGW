import { render, click, fillIn } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupRenderingTest } from "ember-qunit";
import { authenticateSession } from "ember-simple-auth/test-support";
import { module, test } from "qunit";

module("Integration | Component | identity-phone-numbers", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);

  hooks.beforeEach(async function () {
    await authenticateSession({ userinfo: { mysagw_groups: ["sagw"] } });
  });

  test("it renders", async function (assert) {
    this.server.create("identity");

    this.identity = { id: "1" };

    await render(hbs`<IdentityPhoneNumbers @identity={{this.identity}} />`);
    assert.ok(this.element);
  });

  test("it can add new addresses", async function (assert) {
    this.server.create("identity");

    this.identity = { id: "1" };

    await render(hbs`<IdentityPhoneNumbers @identity={{this.identity}} />`);
    assert.ok(this.element);

    await click("[data-test-phone-add]");

    assert.dom("form").exists();

    await fillIn("input[name=phone]", "+41 31 321 45 67");
    await click("button[type=submit]");

    assert.dom("form").doesNotExist();
  });
});
