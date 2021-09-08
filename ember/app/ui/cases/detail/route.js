import Route from "@ember/routing/route";
import calumaQuery from "ember-caluma/caluma-query";
import { allCases } from "ember-caluma/caluma-query/queries";

export default class CasesDetailRoute extends Route {
  @calumaQuery({ query: allCases })
  caseQuery;

  async model({ case_id }) {
    await this.caseQuery.fetch({ filter: [{ id: case_id }] });

    return this.caseQuery.value.firstObject;
  }

  setupController(controller, model) {
    super.setupController(controller, model);
    controller.fetchWorkItems.perform();
  }
}
