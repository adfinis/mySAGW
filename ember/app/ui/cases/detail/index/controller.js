import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency-decorators";
import { saveAs } from "file-saver";

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

  get isNotSubmitted() {
    return this.getNodes.find(
      (workItem) =>
        workItem.task.slug === ENV.APP.caluma.submitTaskSlug &&
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

  @dropTask
  *exportAccounting() {
    const adapter = this.store.adapterFor("identity");

    const uri = `${this.store.adapterFor("identity").buildURL("receipts")}/${
      this.model.id
    }`;
    const init = {
      method: "GET",
      headers: adapter.headers,
    };
    try {
      const response = yield fetch(uri, init);

      if (!response.ok) {
        throw new Error(response.statusText || response.status);
      }

      const blob = yield response.blob();
      const filename = `${this.intl.t("documents.accountingExportFilename", {
        dossierNo:
          this.model.document.answers.edges.firstObject.node.StringAnswerValue,
      })}`;

      saveAs(blob, filename);
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
    }
  }
}
