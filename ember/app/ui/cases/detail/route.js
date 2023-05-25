import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";
import calumaQuery from "@projectcaluma/ember-core/caluma-query";
import { allCases } from "@projectcaluma/ember-core/caluma-query/queries";

export default class CasesDetailRoute extends Route {
  @service store;
  @service can;
  @service router;

  @calumaQuery({ query: allCases })
  caseQuery;

  async model({ case_id }) {
    await this.caseQuery.fetch({ filter: [{ id: case_id }] });

    await this.store.query("case-access", {
      filter: { caseIds: this.caseQuery.value.firstObject.id },
      include: "identity",
    });

    return this.caseQuery.value.firstObject;
  }

  afterModel(model) {
    if (this.can.cannot("list case", model)) {
      this.router.transitionTo("cases");
    }
  }

  setupController(controller, model) {
    super.setupController(controller, model);
    controller.fetchWorkItems.perform();
  }
}
