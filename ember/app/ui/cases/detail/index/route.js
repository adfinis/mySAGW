import Route from "@ember/routing/route";
import { queryManager } from "ember-apollo-client";
import getCaseQuery from "mysagw/gql/queries/get-case.graphql";

export default class CasesDetailIndexRoute extends Route {
  @queryManager apollo;

  async model() {
    const model = this.modelFor("cases.detail");
    if (typeof model === "object" && model) {
      return model;
    }

    const caseRecord = await this.apollo.query(
      {
        query: getCaseQuery,
        variables: { caseId: model },
      },
      "allCases.edges"
    );

    return caseRecord.mapBy("node").firstObject;
  }
}
