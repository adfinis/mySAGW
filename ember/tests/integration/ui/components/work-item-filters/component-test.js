import { click, render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import calumaScenario from "mysagw/mirage/scenarios/caluma";
import { setupRenderingTest } from "mysagw/tests/helpers";

module("Integration | Component | work-item-filters", function (hooks) {
  setupRenderingTest(hooks);
  test("it renders", async function (assert) {
    const filters = {
      status: "open",
      responsible: "all",
      taskTypes: "",
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
      <WorkItemFilters
        @filters={{this.filters}}
        @invertedFilters={{this.invertedFilters}}
      />`);

    await click("[data-test-filter-modal-open]");
    assert
      .dom(".uk-modal-title")
      .hasText("t:components.filters.modal.title:()");
  });
});
