import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import Changeset from "ember-changeset";
import lookupValidator from "ember-changeset-validations";
import { dropTask, restartableTask } from "ember-concurrency-decorators";
import { saveAs } from "file-saver";
import UIkit from "uikit";

import cancelCaseMutation from "mysagw/gql/mutations/cancel-case.graphql";
import CaseValidations from "mysagw/validations/case";

export default class CasesDetailIndexController extends Controller {
  @service router;
  @service notification;
  @service intl;

  @queryManager apollo;

  @tracked newRow;

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
  addRow() {
    this.newRow = new Changeset(
      this.store.createRecord("case", {
        email: undefined,
        caseId: this.model.id,
      }),
      lookupValidator(CaseValidations),
      CaseValidations
    );
  }

  @restartableTask
  *saveRow() {
    if (this.model.invitations.findBy("email", this.newRow.email)) {
      this.notification.danger(
        this.intl.t("documents.invitations.duplicateEmail")
      );
      return;
    }

    if (this.newRow.isValid) {
      yield this.newRow.save();

      this.newRow = null;
      UIkit.modal("#modal-invitation").hide();
    }
  }

  @dropTask
  *deleteRow(invitation) {
    yield this.model.invitations
      .filterBy("email", invitation.email)[0]
      .destroyRecord();
  }

  @dropTask
  *cancelRow() {
    yield this.newRow.destroyRecord();
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
