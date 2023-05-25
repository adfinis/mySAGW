import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import { dropTask, lastValue } from "ember-concurrency";

import getWorkItemChildCaseQuery from "mysagw/gql/queries/get-work-item-child-case.graphql";

export default class CasesDetailController extends Controller {
  @service session;

  @queryManager apollo;

  @lastValue("fetchWorkItems") circulation;
  @dropTask
  *fetchWorkItems() {
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

  get circulationAnswer() {
    return this.circulation?.node.childCase.workItems.edges.find((workItem) =>
      workItem.node.assignedUsers.includes(
        this.session.data.authenticated.userinfo.sub
      )
    ).node;
  }
}
