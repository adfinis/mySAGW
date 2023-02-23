import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupIntl } from "ember-intl/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "mysagw/tests/helpers";

module("Integration | Component | filter-modal", function (hooks) {
  setupRenderingTest(hooks);
  setupIntl(hooks);

  test("it renders", async function (assert) {
    await render(hbs`
      <FilterModal @setFiltersAmount=3>
        template block text
      </FilterModal>
    `);

    assert.dom(this.element).includesText("template block text");
    assert.dom("button").includesText("3");
  });
});
