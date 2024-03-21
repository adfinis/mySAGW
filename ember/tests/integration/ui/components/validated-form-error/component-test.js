import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "mysagw/tests/helpers";

module("Integration | Component | validated-form-error", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    this.errors = ["error1", "error2"];
    await render(hbs`<ValidatedFormError @errors={{this.errors}}/>`);

    assert.dom(this.element).hasText("t:error1:() , t:error2:()");
  });
});
