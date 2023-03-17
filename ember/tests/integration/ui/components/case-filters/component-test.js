import { click, render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupIntl } from "ember-intl/test-support";
import { module, test } from "qunit";

import calumaScenario from "mysagw/mirage/scenarios/caluma";
import { setupRenderingTest } from "mysagw/tests/helpers";

module("Integration | Component | case-filters", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);
  setupIntl(hooks);

  test("it renders", async function (assert) {
    const filters = {
      documentNumber: "",
      identities: "",
      answerSearch: "",
      forms: "",
      expertAssociations: "",
      distributionPlan: "",
      sections: "",
    };
    this.set("filters", filters);
    this.set("invertedFilters", filters);

    calumaScenario(this.server);

    await render(hbs`
      <CaseFilters
        @filters={{this.filters}}
        @invertedFilters={{this.invertedFilters}}
      />
    `);

    await click("[data-test-filter-modal-open]");
    assert
      .dom(".uk-modal-title")
      .hasText("t:components.filters.modal.title:()");
  });
});
