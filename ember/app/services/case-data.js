import { getOwner, setOwner } from "@ember/application";
import Service from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { restartableTask } from "ember-concurrency";

import CustomCaseModel from "mysagw/caluma-query/models/case";
import getCaseQuery from "mysagw/gql/queries/get-case.graphql";
import getWorkItemChildCaseQuery from "mysagw/gql/queries/get-work-item-child-case.graphql";

export default class CaseDataService extends Service {
  @queryManager apollo;

  @tracked case;
  @tracked circulation;

  @restartableTask
  *fetchCase(caseId) {
    const caseEdges = yield this.apollo.query(
      {
        query: getCaseQuery,
        variables: { filter: [{ ids: [caseId] }] },
        fetchPolicy: "network-only",
      },
      "allCases.edges",
    );

    const caseModel = new CustomCaseModel(caseEdges[0].node);
    setOwner(caseModel, getOwner(this));

    this.case = caseModel;
    return caseModel;
  }

  @restartableTask
  *fetchCirculation(caseId) {
    const circulation = yield this.apollo.query(
      {
        query: getWorkItemChildCaseQuery,
        variables: {
          filter: [
            { task: "circulation" },
            { case: caseId },
            { status: "REDO", invert: true },
          ],
        },
        fetchPolicy: "network-only",
      },
      "allWorkItems.edges",
    );

    this.circulation = circulation.firstObject;
    return circulation.firstObject;
  }

  fetch(caseId) {
    return [
      this.fetchCase.perform(caseId),
      this.fetchCirculation.perform(caseId),
    ];
  }
}
