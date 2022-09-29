import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { dropTask } from "ember-concurrency-decorators";
import { saveAs } from "file-saver";

export default class CasesDetailDownloadController extends Controller {
  @service notification;
  @service intl;
  @service store;

  @dropTask
  *download() {
    const adapter = this.store.adapterFor("identity");

    const uri = `${adapter.buildURL("download")}/${
      this.model.id
    }/acknowledgement`;
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
      const filename = `${this.intl.t(
        "documents.download.creditApprovalFilename",
        {
          dossierNo:
            this.model.document.answers.edges.firstObject.node
              .StringAnswerValue,
        }
      )}`;

      saveAs(blob, filename);
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
    }
  }
}
