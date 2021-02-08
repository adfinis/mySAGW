import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import { task } from "ember-concurrency-decorators";
import cancelCaseMutation from "mysagw/gql/mutations/cancel-case";

export default class CasesDetailIndexController extends Controller {
  @service router;
  @queryManager apollo;

  @task *closeCase() {
    yield this.apollo.mutate({
      mutation: cancelCaseMutation,
      variables: { case: this.model.id },
    });
    this.router.transitionTo("cases.index");
  }
}
