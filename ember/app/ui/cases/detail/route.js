import Route from "@ember/routing/route";
import { queryManager } from "ember-apollo-client";
import getCaseQuery from "mysagw/gql/queries/get-case.graphql";

export default class CasesDetailRoute extends Route {
  @queryManager apollo;

  async model({ case_id }) {
    const caseEdges = await this.apollo.watchQuery(
      {
        query: getCaseQuery,
        variables: { caseId: case_id },
      },
      "allCases.edges"
    );

    return caseEdges.firstObject.node;
  }

  setupController(controller, model) {
    super.setupController(controller, model);
    controller.fetchWorkItems.perform();
  }
}
