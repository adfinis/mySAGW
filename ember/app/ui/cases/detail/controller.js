import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import { dropTask, lastValue } from "ember-concurrency";
import { trackedFunction } from "ember-resources/util/function";

import getWorkItemChildCaseQuery from "mysagw/gql/queries/get-work-item-child-case.graphql";
import getWorkItemCount from "mysagw/gql/queries/get-work-item-count.graphql";

export default class CasesDetailController extends Controller {
  @service session;

  @queryManager apollo;

  @lastValue("fetchCirculation") circulation;
  @dropTask
  *fetchCirculation() {
    const circulation = yield this.apollo.query(
      {
        query: getWorkItemChildCaseQuery,
        variables: {
          filter: [{ task: "circulation" }, { case: this.model.id }],
        },
      },
      "allWorkItems.edges"
    );

    return circulation.firstObject;
  }

  circulationDecisionCount = trackedFunction(this, async () => {
    return await this.apollo.query(
      {
        query: getWorkItemCount,
        variables: {
          filter: [
            { task: "circulation-decision" },
            { caseFamily: this.model.id },
          ],
        },
      },
      "allWorkItems.totalCount"
    );
  });

  get circulationAnswer() {
    return this.circulation?.node.childCase.workItems.edges.find((workItem) =>
      workItem.node.assignedUsers.includes(
        this.session.data.authenticated.userinfo.sub
      )
    ).node;
  }
}
