import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import Changeset from "ember-changeset";
import lookupValidator from "ember-changeset-validations";
import { dropTask, restartableTask } from "ember-concurrency-decorators";
import { saveAs } from "file-saver";

import cancelCaseMutation from "mysagw/gql/mutations/cancel-case.graphql";
import CaseValidations from "mysagw/validations/case";

export default class CasesDetailIndexController extends Controller {
  @service router;
  @service notification;
  @service intl;

  @queryManager apollo;

  @tracked newRow;
  @tracked modalVisible;

  get readyWorkItems() {
    return this.model.workItems.filterBy("status", "READY").length;
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

  @action
  transtionToCases() {
    this.router.transtionTo("cases");
  }

  @action
  addAccessRow() {
    this.newRow = new Changeset(
      this.store.createRecord("case-access", {
        email: undefined,
        caseId: this.model.id,
      }),
      lookupValidator(CaseValidations),
      CaseValidations
    );

    this.modalVisible = true;
  }

  @restartableTask
  *saveAccessRow() {
    if (this.model.accesses.findBy("email", this.newRow.email)) {
      this.notification.danger(
        this.intl.t("documents.accesses.duplicateEmail")
      );
      return;
    }

    if (this.newRow.isValid) {
      const email = this.newRow.email;

      this.newRow.save();

      yield this.store.query(
        "identity",
        { filter: { email } },
        { adapterOptions: { customEndpoint: "public-identities" } }
      );

      this.newRow = null;
      this.modalVisible = false;
    }
  }

  @dropTask
  *deleteAccessRow(access) {
    yield this.model.accesses.findBy("email", access.email).destroyRecord();

    if (this.can.cannot("list case", this.model)) {
      this.router.transitionTo("cases");
    }
  }

  @dropTask
  *cancelAccessRow() {
    yield this.newRow.destroyRecord();
    this.modalVisible = false;
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
