import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "mysagw/tests/helpers";

module("Integration | Component | work-item-filters", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    // Set any properties with this.set('myProperty', 'value');
    // Handle any actions with this.set('myAction', function(val) { ... });

    await render(hbs`<WorkItemFilters />`);

    assert.dom(this.element).hasText("");

    // Template block usage:
    await render(hbs`
      <WorkItemFilters>
        template block text
      </WorkItemFilters>
    `);

    assert.dom(this.element).hasText("template block text");
  });
});
