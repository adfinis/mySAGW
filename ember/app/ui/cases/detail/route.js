import Route from "@ember/routing/route";
import { queryManager } from "ember-apollo-client";
import getCaseQuery from "mysagw/gql/queries/get-case.graphql";

export default class CasesDetailRoute extends Route {
  @queryManager apollo;

  async model({ case_id }) {
    const caseRecord = await this.apollo.query(
      {
        query: getCaseQuery,
        variables: { caseId: case_id },
      },
      "allCases.edges"
    );

    return caseRecord.mapBy("node").firstObject;
  }
}
