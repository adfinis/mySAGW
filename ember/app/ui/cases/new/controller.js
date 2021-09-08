import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import calumaQuery from "ember-caluma/caluma-query";
import { allForms } from "ember-caluma/caluma-query/queries";
import { decodeId } from "ember-caluma/helpers/decode-id";
import { task } from "ember-concurrency";
import QueryParams from "ember-parachute";

import createCaseMutation from "mysagw/gql/mutations/create-case.graphql";
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

  @calumaQuery({ query: allForms })
  formQuery;

  setup() {
    this.fetchForms.perform();
  }

  reset() {
    this.resetQueryParams();
    this.selectedForm = null;

    this.fetchForms.cancelAll({ reset: true });
    this.createCase.cancelAll({ reset: true });
  }

  @task
  *fetchForms() {
    const organisations = (yield this.store.findAll("identity", {
      adapterOptions: { customEndpoint: "my-orgs" },
    })).filterBy("isAuthorized");

    const organisationTypeFilter = [];
    if (!organisations.isAny("isExpertAssociation")) {
      organisationTypeFilter.push({
        metaHasKey: "expertAssociationForm",
        invert: true,
      });
    }
    if (!organisations.isAny("isAdvisoryBoard")) {
      organisationTypeFilter.push({
        metaHasKey: "advisoryBoardForm",
        invert: true,
      });
    }

    this.formQuery.fetch({
      filter: [
        { isPublished: true },
        { isArchived: false },
        { orderBy: "NAME_ASC" },
        ...organisationTypeFilter,
      ],
    });
  }

  @task
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
      "cases.detail.index",
      decodeId(newCase.startCase.case.id)
    );
  }
}
