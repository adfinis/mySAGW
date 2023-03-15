import { click, render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "mysagw/tests/helpers";

module("Integration | Component | nav-bar", function (hooks) {
  setupRenderingTest(hooks);

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
