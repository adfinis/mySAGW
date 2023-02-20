import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { DateTime } from "luxon";
import { module, test } from "qunit";

import { setupRenderingTest } from "mysagw/tests/helpers";

module("Integration | Helper | format-date", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders js date", async function (assert) {
    const date = Date.now();
    this.set("inputValue", date);

    await render(hbs`{{format-date this.inputValue "dd.LL.yy"}}`);

    assert
      .dom(this.element)
      .hasText(DateTime.fromJSDate(date).toFormat("dd.LL.yy"));
  });

  test("it renders iso date", async function (assert) {
    const date = new Date();
    this.set("inputValue", date.toISOString);

    await render(hbs`{{format-date this.inputValue "dd.LL.yy"}}`);

    assert
      .dom(this.element)
      .hasText(DateTime.fromISO(date).toFormat("dd.LL.yy"));
  });

  test("it renders empty", async function (assert) {
    this.set("inputValue", undefined);

    await render(hbs`{{format-date this.inputValue "dd.LL.yy"}}`);

    assert.dom(this.element).hasText("-");
  });
});
