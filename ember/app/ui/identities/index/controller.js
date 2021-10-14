import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import {
  timeout,
  restartableTask,
  lastValue,
  dropTask,
} from "ember-concurrency";
import { saveAs } from "file-saver";
import moment from "moment";

export default class IdentitiesIndexController extends Controller {
  @service notification;
  @service store;
  @service intl;

  queryParams = ["pageSize", "pageNumber"];
  @tracked pageSize = 25;
  @tracked pageNumber = 1;
  @tracked totalPages;
  @tracked totalCount = 0;

  get pages() {
    if (!this.totalPages) {
      return null;
    }

    const res = [];

    // insert previous page
    if (this.pageNumber - 1 > 0) {
      res.push({
        number: this.pageNumber - 1,
      });
    }
    if (this.pageNumber - 1 > 2) {
      res.unshift({ dots: true });
    }
    // first page
    if (res.length > 0 && res[0].number !== 1) {
      res.unshift({
        number: 1,
      });
    }

    res.push({
      number: this.pageNumber,
      active: true,
    });

    // insert next page
    if (this.pageNumber + 1 <= this.totalPages) {
      res.push({
        number: this.pageNumber + 1,
      });
    }
    if (this.pageNumber + 1 < this.totalPages - 1 && this.totalPages > 3) {
      res.push({ dots: true });
    }
    // last page
    if (res[res.length - 1].number !== this.totalPages) {
      res.push({
        number: this.totalPages,
      });
    }

    return res;
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
      this.totalCount = identities.meta.pagination.count;
      return identities;
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
    }
  }

  @action onUpdate() {
    this.fetchIdentities.perform();
  }

  @dropTask *exportSearch(endpoint, fileExtension) {
    const adapter = this.store.adapterFor("identity");

    let uri = `${this.store
      .adapterFor("identity")
      .buildURL("identity")}/${endpoint}`;

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
      const filename = `${this.intl.t("identities.index.export.filename", {
        date: moment().format("YYYY-MM-DD"),
      })}.${fileExtension}`;

      saveAs(blob, filename);
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
    }
  }
}
