import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { timeout } from "ember-concurrency";
import {
  restartableTask,
  lastValue,
  dropTask,
} from "ember-concurrency-decorators";
import { saveAs } from "file-saver";
import moment from "moment";

export default class IdentitiesIndexController extends Controller {
  @service notification;
  @service store;
  @service intl;

  queryParams = ["pageSize", "pageNumber"];
  @tracked pageSize = 10;
  @tracked pageNumber = 1;
  @tracked totalPages;

  get pages() {
    if (!this.totalPages) {
      return null;
    }

    return Array.from({ length: this.totalPages }).map((_, index) => ({
      number: index + 1,
      active: index + 1 === this.pageNumber,
    }));
  }

  @restartableTask *search(event) {
    yield timeout(1000);
    this.searchTerm = event.target.value;
    this.pageNumber = 1;
  }

  @lastValue("fetchIdentities") identities;

  @restartableTask *fetchIdentities() {
    try {
      const identities = yield this.store.query("identity", {
        "filter[search]": this.searchTerm,
        page: {
          number: this.pageNumber,
          size: this.pageSize,
        },
      });
      this.totalPages = identities.meta.pagination.pages;
      return identities;
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
    }
  }

  @action onUpdate() {
    this.fetchIdentities.perform();
  }

  @dropTask *exportSearch() {
    const adapter = this.store.adapterFor("identity");

    let uri = `${this.store
      .adapterFor("identity")
      .buildURL("identity")}/export`;

    if (this.searchTerm) {
      uri += `?filter[search]=${this.searchTerm}`;
    }

    const init = {
      method: "POST",
      headers: adapter.headers,
    };

    try {
      const response = yield fetch(uri, init);

      if (!response.ok) {
        throw new Error(response.statusText || response.status);
      }

      const blob = yield response.blob();
      const filename = `${this.intl.t("page.identities.index.export.filename", {
        date: moment().format("YYYY-MM-DD"),
      })}.xls`;

      saveAs(blob, filename);
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
    }
  }
}
