import Controller from "@ember/controller";
import { service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import { trackedFunction } from "reactiveweb/function";

import getWorkItem from "mysagw/gql/queries/get-work-item.graphql";

export default class CasesDetailController extends Controller {
  @service session;
  @service caseData;

  @queryManager apollo;

  circulationDecision = trackedFunction(this, async () => {
    return await this.apollo.query(
      {
        query: getWorkItem,
        variables: {
          filter: [
            { task: "circulation-decision" },
            { caseFamily: this.model.id },
          ],
        },
      },
      "allWorkItems",
    );
  });

  get circulationAnswer() {
    return this.circulationDecision.value?.edges[0].node;
  }
}
