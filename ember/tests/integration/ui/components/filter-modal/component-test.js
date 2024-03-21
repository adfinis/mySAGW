import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "mysagw/tests/helpers";

module("Integration | Component | filter-modal", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    await render(hbs`
      <FilterModal @setFiltersAmount="3">
        {{t "global.continue"}}
      </FilterModal>
    `);

    assert.dom(this.element).includesText("t:global.continue:()");
    assert.dom("button").includesText("3");
  });
});
