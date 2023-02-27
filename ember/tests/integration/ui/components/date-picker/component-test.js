import { click, fillIn, render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "mysagw/tests/helpers";

module("Integration | Component | date-picker", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    this.onChange = () => {
      assert.step("onChange");
    };

    await render(hbs`<DatePicker @onChange={{this.onChange}}/>`);

    await fillIn('input[type="text"]', "03.04.2020");

    assert.dom('input[type="text"]').hasValue("03.04.2020");

    await click("a");

    assert.dom("input").hasValue("");
    assert.verifySteps(["onChange", "onChange"]);
  });
});
