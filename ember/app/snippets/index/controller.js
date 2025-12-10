import Controller from "@ember/controller";
import { action } from "@ember/object";
import { service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { timeout, restartableTask, lastValue } from "ember-concurrency";

export default class SnippetsIndexController extends Controller {
  @service notification;
  @service store;

  queryParams = ["pageSize", "pageNumber", { searchTerm: "search" }];
  @tracked pageSize = 20;
  @tracked pageNumber = 1;
  @tracked searchTerm = "";
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

  @restartableTask
  *search(event) {
    yield timeout(1000);
    this.searchTerm = event.target.value;
    this.pageNumber = 1;
    this.fetchSnippets.perform();
  }

  @lastValue("fetchSnippets") snippets;
  @restartableTask
  *fetchSnippets() {
    try {
      const snippets = yield this.store.query("snippet", {
        "filter[search]": this.searchTerm,
        page: {
          number: this.pageNumber,
          size: this.pageSize,
        },
      });
      this.totalPages = snippets.meta?.pagination?.pages;
      return snippets;
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
    }
  }

  @action
  setPageNumber(number) {
    this.pageNumber = number;
    this.fetchSnippets.perform();
  }
}
