import { getOwner, setOwner } from "@ember/application";
import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";
import { queryManager } from "ember-apollo-client";

import CustomCaseModel from "mysagw/caluma-query/models/case";
import getCaseQuery from "mysagw/gql/queries/get-case.graphql";

export default class CasesDetailRoute extends Route {
  @service store;
  @service can;
  @service router;

  @queryManager apollo;

  async model({ case_id }) {
    const caseId = decodeId(case_id);

    const [caseEdges] = await Promise.all([
      this.apollo.query(
        {
          query: getCaseQuery,
          variables: { filter: [{ id: caseId }] },
        },
        "allCases.edges"
      ),
      this.store.query("case-access", {
        filter: { caseIds: caseId },
        include: "identity",
      }),
    ]);

    const caseModel = new CustomCaseModel(caseEdges[0].node);
    setOwner(caseModel, getOwner(this));
    return caseModel;
  }

  afterModel(model) {
    // TODO: allow access to case if invited to circulation
    if (this.can.cannot("list case", model)) {
      this.router.transitionTo("cases");
    }
  }

  setupController(controller, model) {
    super.setupController(controller, model);
    controller.fetchWorkItems.perform();
  }
}
