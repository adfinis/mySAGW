import { click, render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupIntl } from "ember-intl/test-support";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";

module("Integration | Component | nav-bar", function (hooks) {
  setupRenderingTest(hooks);
  setupIntl(hooks);

  test("it renders", async function (assert) {
    await render(hbs`<NavBar @text="foo"/>`);

    assert.dom(this.element).includesText("foo");
  });

  test("it switches the locale", async function (assert) {
    await render(hbs`<NavBar />`);

    assert.dom("[data-test-locale]").hasText("en-us");
    await click("[data-test-locale-select='fr']");
    assert.dom("[data-test-locale]").hasText("fr");
  });
});
