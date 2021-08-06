import Route from "@ember/routing/route";
import { queryManager } from "ember-apollo-client";
import getCaseQuery from "mysagw/gql/queries/get-case.graphql";

export default class CasesDetailRoute extends Route {
  @queryManager apollo;

  model({ case_id }) {
    return this.apollo
      .query(
        {
          query: getCaseQuery,
          variables: { caseId: case_id },
        },
        "allCases.edges"
      )
      .then(function (value) {
        return value.mapBy("node").firstObject;
      });
  }
}
