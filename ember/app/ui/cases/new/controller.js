import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";
import { queryManager } from "ember-apollo-client";
import { restartableTask } from "ember-concurrency";
import QueryParams from "ember-parachute";

import createCaseMutation from "mysagw/gql/mutations/create-case.graphql";
import getWorkflowQuery from "mysagw/gql/queries/get-workflow.graphql";
import { FilteredForms } from "mysagw/utils/filtered-forms";

const queryParams = new QueryParams({
  selectedForm: {
    defaultValue: "",
    replace: true,
  },
});

export default class CaseNewController extends Controller.extend(
  queryParams.Mixin
) {
  @queryManager apollo;

  @service router;
  @service store;
  @service session;

  @tracked selectedForm;

  filteredForms = FilteredForms.from(this);

  reset(_, isExiting) {
    if (isExiting) {
      this.resetQueryParams();
      this.selectedForm = null;
    }
  }

  @restartableTask
  *createCase() {
    const workflow = (yield this.apollo.query(
      {
        query: getWorkflowQuery,
        variables: {
          filter: [
            {
              slug: "document-review",
            },
          ],
        },
      },
      "allWorkflows.edges"
    )).firstObject.node;

    const newCase = yield this.apollo.mutate({
      mutation: createCaseMutation,
      variables: { form: this.selectedForm, workflow: workflow.id },
    });

    this.router.transitionTo(
      "cases.detail.edit",
      decodeId(newCase.saveCase.case.id)
    );
  }
}
