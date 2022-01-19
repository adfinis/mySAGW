import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";
import { queryManager } from "ember-apollo-client";
import { lastValue, restartableTask } from "ember-concurrency";
import QueryParams from "ember-parachute";

import createCaseMutation from "mysagw/gql/mutations/create-case.graphql";
import getFormsQuery from "mysagw/gql/queries/get-form.graphql";
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

  get forms() {
    // sort forms, so that the ones without permissions are at the bottom
    return [
      this.allForms?.expertAssociation,
      this.allForms?.advisoryBoard,
      this.allForms?.bothTypes,
      this.allForms.public,
    ]
      .map((forms) => {
        return forms?.edges ?? [];
      })
      .flat();
  }

  reset(_, isExiting) {
    if (isExiting) {
      this.resetQueryParams();
      this.selectedForm = null;
    }
  }

  @lastValue("fetchForms") allForms;
  @restartableTask
  *fetchForms() {
    const organisations = (yield this.store.findAll("identity", {
      reload: true,
      adapterOptions: { customEndpoint: "my-orgs" },
    })).filterBy("isAuthorized");

    const isExpertAssociation = organisations.isAny("isExpertAssociation");
    const isAdvisoryBoard = organisations.isAny("isAdvisoryBoard");

    const allForms = {
      ...(yield this.apollo.query({
        query: getFormsQuery,
      })),
    };

    if (!isExpertAssociation) {
      delete allForms.expertAssociation;
    }
    if (!isAdvisoryBoard) {
      delete allForms.advisoryBoard;
    }
    if (!isExpertAssociation && !isAdvisoryBoard) {
      delete allForms.bothTypes;
    }

    return allForms;
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
