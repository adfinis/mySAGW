import { click, render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "mysagw/tests/helpers";

module("Integration | Component | dynamic-table/header", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders without ordering", async function (assert) {
    this.config = { classList: ["a", "b"], label: "test" };

    await render(hbs`<DynamicTable::Header @config={{this.config}} />`);

    assert.dom("th").exists();
    assert.dom("th").hasClass("a");
    assert.dom("th").hasClass("b");
    assert.dom("th").hasText("t:test:()");

    assert.dom("button").doesNotExist();
  });

  test("it renders with ordering", async function (assert) {
    this.config = { classList: ["a", "b"], label: "test", sortKey: "test" };
    this.order = "foo";

    await render(
      hbs`<DynamicTable::Header @config={{this.config}} @order={{this.order}} />`,
    );

    assert.dom("th").exists();
    assert.dom("th").hasClass("a");
    assert.dom("th").hasClass("b");

    assert.dom("button").exists();
    assert.dom("th button").hasText("t:test:()");
    assert.dom("th button [uk-icon]").doesNotExist();

    this.set("order", "test");

    assert.dom("th button [uk-icon]").exists();
    assert
      .dom("th button [uk-icon]")
      .hasAttribute("uk-icon", "icon: triangle-up");

    this.set("order", "-test");

    assert.dom("th button [uk-icon]").exists();
    assert
      .dom("th button [uk-icon]")
      .hasAttribute("uk-icon", "icon: triangle-down");
  });

  test("it can update the order", async function (assert) {
    this.config = { classList: ["a", "b"], label: "test", sortKey: "test" };
    this.order = "foo";
    this.setOrder = (value) => {
      assert.step("order");
      this.set("order", value);
    };

    await render(
      hbs`<DynamicTable::Header @config={{this.config}} @order={{this.order}} @setOrder={{this.setOrder}} />`,
    );

    await click("button");

    assert.verifySteps(["order"]);
    assert.strictEqual(this.order, "test");

    await click("button");

    assert.verifySteps(["order"]);
    assert.strictEqual(this.order, "-test");
  });
});
