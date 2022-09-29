import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { dropTask } from "ember-concurrency-decorators";
import { saveAs } from "file-saver";

import ENV from "mysagw/config/environment";
export default class CasesDetailDownloadController extends Controller {
  @service notification;
  @service intl;
  @service store;

  get activeDownloads() {
    const downloads = [this.application];
    if (
      this.model.workItems.find(
        (workItem) =>
          workItem.task.slug === ENV.APP.caluma.submitTaskSlug &&
          workItem.status === "COMPLETED"
      )
    ) {
      downloads.push(this.acknowledgement);
    }
    if (
      this.model.workItems.find(
        (workItem) =>
          workItem.task.slug === ENV.APP.caluma.decisionAndCreditTaskSlug &&
          workItem.status === "COMPLETED"
      )
    ) {
      downloads.push(this.creditApproval);
    }
    return downloads;
  }

  @dropTask
  *download(name) {
    const adapter = this.store.adapterFor("identity");

    const uri = `${adapter.buildURL("download")}/${this.model.id}/${name}`;
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
      const filename = `${this.intl.t(`documents.download.${name}`, {
        dossierNo:
          this.model.document.answers.edges.firstObject.node.StringAnswerValue,
      })}`;

      saveAs(blob, filename);
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
    }
  }

  @dropTask
  *application() {
    yield this.download.perform("application");
  }
  @dropTask
  *acknowledgement() {
    yield this.download.perform("acknowledgement");
  }
  @dropTask
  *creditApproval() {
    yield this.download.perform("creditApproval");
  }
}
