import { click, render, settled, waitFor } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupIntl } from "ember-intl/test-support";
import { module, test } from "qunit";

import ENV from "mysagw/config/environment";
import { setupRenderingTest } from "mysagw/tests/helpers";

module("Integration | Component | submit-button", function (hooks) {
  setupRenderingTest(hooks);
  setupIntl(hooks);
  setupMirage(hooks);

  hooks.beforeEach(function () {
    this.set("field", {
      document: this.server.create("document", {
        case: this.server.create("case", {
          workItems: [
            this.server.create("workItem", {
              task: this.server.create("task", {
                slug: ENV.APP.caluma.submitTaskSlug,
              }),
              status: "READY",
            }),
          ],
        }),
      }),
    });
  });

  test("it renders", async function (assert) {
    await render(hbs`<SubmitButton @field={{this.field}}/>`);
    await waitFor("[data-test-submit-confirm-open]");
    await settled();

    assert
      .dom("[data-test-submit-confirm-open]")
      .hasText("t:components.submit-button.title:()");
    assert.dom("[data-test-submit-confirm-open]").isNotDisabled();
  });

  test("it shows confirmation", async function (assert) {
    await render(hbs`<SubmitButton @field={{this.field}}/>`);
    await waitFor("[data-test-submit-confirm-open]");
    await waitFor(":not([data-test-submit-confirm-open]:disabled)");
    await settled();

    await click("[data-test-submit-confirm-open]");

    assert.dom("p").hasText("t:components.submit-button.confirmation:()");
    assert.dom("[data-test-submit]").isNotDisabled();

    await click("[data-test-submit]");
  });
});
