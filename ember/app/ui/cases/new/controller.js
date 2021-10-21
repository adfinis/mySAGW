import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import calumaQuery from "@projectcaluma/ember-core/caluma-query";
import { allForms } from "@projectcaluma/ember-core/caluma-query/queries";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";
import { queryManager } from "ember-apollo-client";
import { restartableTask } from "ember-concurrency";
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

  get forms() {
    // sort forms, so that the ones without permissions are at the bottom
    return this.formQuery.value.sort((firstEl, secondEl) => {
      if (firstEl.isAdvisoryBoardForm || firstEl.isExpertAssociationForm) {
        return -1;
      } else if (
        secondEl.isAdvisoryBoardForm ||
        secondEl.isExpertAssociationForm
      ) {
        return 1;
      }

      return 0;
    });
  }

  reset(_, isExiting) {
    if (isExiting) {
      this.resetQueryParams();
      this.selectedForm = null;
    }
  }

  @restartableTask
  *fetchForms() {
    const organisations = (yield this.store.findAll("identity", {
      reload: true,
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

    yield this.formQuery.fetch({
      filter: [
        { isPublished: true },
        { isArchived: false },
        { orderBy: "NAME_ASC" },
        ...organisationTypeFilter,
      ],
    });
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
      "cases.detail.index",
      decodeId(newCase.startCase.case.id)
    );
  }
}
