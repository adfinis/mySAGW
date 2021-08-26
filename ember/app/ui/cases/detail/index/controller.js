import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency-decorators";

import ENV from "mysagw/config/environment";
import cancelCaseMutation from "mysagw/gql/mutations/cancel-case.graphql";
import completeWorkItemMutation from "mysagw/gql/mutations/complete-work-item.graphql";

export default class CasesDetailIndexController extends Controller {
  @service router;
  @service notification;
  @service intl;

  @queryManager apollo;

  get getNodes() {
    return this.model.workItems.edges.mapBy("node");
  }

  get isEditable() {
    return this.getNodes
      .filter((workItem) =>
        ENV.APP.caluma.documentEditableTaskSlugs.includes(workItem.task.slug)
      )
      .isAny("status", "READY");
  }

  get isNotRejected() {
    return this.getNodes.find(
      (workItem) =>
        workItem.task.slug === ENV.APP.caluma.reviseTaskSlug &&
        workItem.status === "READY"
    );
  }

  get readyWorkItems() {
    return this.getNodes.filterBy("status", "READY").length;
  }

  @dropTask
  *closeCase() {
    try {
      yield this.apollo.mutate({
        mutation: cancelCaseMutation,
        variables: { case: this.model.id },
      });

      this.notification.success(this.intl.t("documents.deleteSuccess"));

      this.router.transitionTo("cases.index");
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
    }
  }

  @dropTask
  *submitCase() {
    try {
      yield this.apollo.mutate({
        mutation: completeWorkItemMutation,
        variables: { id: this.model.workItems.edges[0].node.id },
      });

      this.notification.success(this.intl.t("documents.submitSuccess"));

      this.router.transitionTo("cases.index");
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
    }
  }
}
