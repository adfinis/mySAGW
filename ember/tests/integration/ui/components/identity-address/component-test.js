import { render, click, fillIn } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "mysagw/tests/helpers";

module("Integration | Component | identity-addresses", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    this.identity = this.server.create("identity");

    await render(hbs`<IdentityAddresses @identity={{this.identity}} />`);

    assert.dom("h2").includesText("t:components.identity-addresses.title:()");
  });

  // Mirage does not work for relationships
  test.skip("it can add new addresses", async function (assert) {
    this.identity = this.server.create("identity");

    await render(hbs`<IdentityAddresses @identity={{this.identity}} />`);

    await click("[data-test-address-add]");

    assert.dom("form").exists();

    await fillIn("input[name=streetAndNumber]", "Musterstrasse. 1");
    await fillIn("input[name=postcode]", "8000");
    await fillIn("input[name=town]", "Zürich");
    await click("button[type=submit]");

    assert.dom("form").doesNotExist();
  });
});
