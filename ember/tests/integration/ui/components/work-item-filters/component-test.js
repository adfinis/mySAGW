import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupIntl } from "ember-intl/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "mysagw/tests/helpers";

module("Integration | Component | work-item-filters", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);
  setupIntl(hooks);

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
    const form = this.server.create("form");
    this.server.create("question", {
      slug: "mitgliedinstitution",
      label: "mitgliedinstitution",
      formIds: [form.id],
      type: "MULTIPLE_CHOICE",
      hintText: null,
      options: [
        this.server.create("option", {
          slug: "institution-1",
          label: "Institution 1",
        }),
        this.server.create("option", {
          slug: "institution-2",
          label: "Institution 2",
        }),
      ],
    });
    this.server.create("question", {
      slug: "sektion",
      label: "sektion",
      formIds: [form.id],
      type: "MULTIPLE_CHOICE",
      hintText: null,
      options: [
        this.server.create("option", {
          slug: "sektion-1",
          label: "sektion 1",
        }),
        this.server.create("option", {
          slug: "sektion-2",
          label: "sektion 2",
        }),
      ],
    });
    this.server.create("question", {
      slug: "verteilplan-nr",
      label: "verteilplan-nr",
      formIds: [form.id],
      type: "MULTIPLE_CHOICE",
      hintText: null,
      options: [
        this.server.create("option", {
          slug: "verteilplan-nr-1",
          label: "verteilplan-nr 1",
        }),
        this.server.create("option", {
          slug: "verteilplan-nr-2",
          label: "verteilplan-nr 2",
        }),
      ],
    });

    await render(hbs`
      <WorkItemFilters
        @filters={{this.filters}}
        @invertedFilters={{this.invertedFilters}}
      />`);

    assert.dom(this.element).hasAnyText();
  });
});
