import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { decodeId } from "ember-caluma/helpers/decode-id";
import { task, lastValue } from "ember-concurrency-decorators";
import QueryParams from "ember-parachute";
import createCaseMutation from "mysagw/gql/mutations/create-case";
import getRootFormsQuery from "mysagw/gql/queries/get-root-forms";
import getWorkflowQuery from "mysagw/gql/queries/get-workflow";

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
      { query: getRootFormsQuery, fetchPolicy: "network-only" },
      "allForms.edges"
    )).map(({ node }) => node);
  }

  @task *createCase() {
    const workflow = (yield this.apollo.query(
      { query: getWorkflowQuery },
      "allWorkflows.edges"
    )).map(({ node }) => node)[0];

    const newCase = yield this.apollo.mutate({
      mutation: createCaseMutation,
      variables: { form: this.selectedForm, workflow: workflow.id },
    });
    this.router.transitionTo(
      "cases.detail.index",
      decodeId(newCase.saveCase.case.id)
    );
  }
}
