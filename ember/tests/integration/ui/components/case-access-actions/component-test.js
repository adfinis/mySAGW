import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "mysagw/tests/helpers";
module("Integration | Component | case-access-actions", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    await render(hbs`<DynamicTable::CaseAccessActions />`);

    assert.dom(this.element).hasText("");
  });
});
