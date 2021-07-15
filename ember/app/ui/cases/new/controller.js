import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { decodeId } from "ember-caluma/helpers/decode-id";
import { task, lastValue } from "ember-concurrency";
import QueryParams from "ember-parachute";
import createCaseMutation from "mysagw/gql/mutations/create-case.graphql";
import getRootFormsQuery from "mysagw/gql/queries/get-root-forms.graphql";
import getWorkflowQuery from "mysagw/gql/queries/get-workflow.graphql";

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

  setup() {
    this.fetchForms.perform();
  }

  reset() {
    this.resetQueryParams();
    this.selectedForm = null;

    this.fetchForms.cancelAll({ reset: true });
    this.createCase.cancelAll({ reset: true });
  }

  @lastValue("fetchForms") forms;
  @task *fetchForms() {
    return (yield this.apollo.query(
      {
        query: getRootFormsQuery,
        fetchPolicy: "network-only",
        variables: { isPublished: true, isArchived: false },
      },
      "allForms.edges"
    )).mapBy("node");
  }

  @task *createCase() {
    const workflow = (yield this.apollo.query(
      { query: getWorkflowQuery },
      "allWorkflows.edges"
    )).mapBy("node").firstObject;

    const newCase = yield this.apollo.mutate({
      mutation: createCaseMutation,
      variables: { form: this.selectedForm, workflow: workflow.id },
    });

    this.router.transitionTo(
      "cases.detail.index",
      decodeId(newCase.startCase.case.id)
    );
  }
}
