import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { timeout } from "ember-concurrency";
import { restartableTask, lastValue } from "ember-concurrency-decorators";

export default class IdentitiesIndexController extends Controller {
  @service notification;
  @service store;

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
      this.totalPages = identities.meta.totalPages;
      return identities;
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
    }
  }

  @action onUpdate() {
    this.fetchIdentities.perform();
  }
}
