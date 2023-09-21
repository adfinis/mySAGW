import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";
import { queryManager } from "ember-apollo-client";
import { restartableTask } from "ember-concurrency";
import { trackedFunction } from "ember-resources/util/function";

import createCaseMutation from "mysagw/gql/mutations/create-case.graphql";

export default class CaseNewController extends Controller {
  queryParams = ["selectedForm"];
  @queryManager apollo;

  @service router;
  @service store;
  @service session;
  @service filteredForms;

  @tracked selectedForm = "";

  reset(_, isExiting) {
    if (isExiting) {
      this.resetQueryParams();
      this.selectedForm = null;
    }
  }

  forms = trackedFunction(this, async () => {
    return await this.filteredForms.fetch({
      additionalFilter: { isPublished: true },
    });
  });

  @restartableTask
  *createCase() {
    const newCase = yield this.apollo.mutate({
      mutation: createCaseMutation,
      variables: { form: this.selectedForm, workflow: "document-review" },
    });

    this.router.transitionTo(
      "cases.detail.edit",
      decodeId(newCase.saveCase.case.id)
    );
  }
}
