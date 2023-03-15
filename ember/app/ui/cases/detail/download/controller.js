import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { decamelize } from "@ember/string";
import { dropTask } from "ember-concurrency";

import ENV from "mysagw/config/environment";
import downloadFile from "mysagw/utils/download-file";

export default class CasesDetailDownloadController extends Controller {
  @service notification;
  @service intl;
  @service store;
  @service fetch;

  get activeDownloads() {
    const downloads = [this.application];
    if (
      this.model.workItems.find(
        (workItem) =>
          workItem.task.slug === ENV.APP.caluma.submitTaskSlug &&
          workItem.status === "COMPLETED",
      )
    ) {
      downloads.push(this.acknowledgement);
    }

    const workItem = this.model.workItems.find(
      (workItem) =>
        workItem.task.slug === ENV.APP.caluma.decisionAndCredit.task &&
        workItem.status === "COMPLETED",
    );
    const answer = workItem?.document.answers.edges.find(
      (answer) =>
        answer.node.question.slug === ENV.APP.caluma.decisionAndCredit.question,
    ).node.StringAnswerValue;
    if (
      answer &&
      ENV.APP.caluma.decisionAndCredit.answers.some((choice) =>
        answer.includes(choice),
      )
    ) {
      downloads.push(this.creditApproval);
    }
    return downloads;
  }

  @dropTask
  *download(name) {
    const adapter = this.store.adapterFor("identity");

    const uri = `${adapter.buildURL("download")}/${this.model.id}/${decamelize(
      name,
    )}`;
    const init = {
      method: "GET",
      headers: adapter.headers,
    };
    try {
      yield downloadFile(this.fetch.fetch(uri, init));
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
