import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { timeout, restartableTask } from "ember-concurrency";

export default class NavbarComponent extends Component {
  @service session;
  @service intl;
  @service store;
  @service notification;
  @service can;

  @tracked pageSize = 10;
  @tracked pageNumber = 1;
  @tracked searchTerm = "";
  @tracked totalPages;
  @tracked snippets = [];

  @action
  invalidateSession() {
    this.session.singleLogout();
  }

  @action
  setLocale(locale) {
    this.intl.setLocale(locale);
  }

  @action
  onCopySuccess() {
    this.notification.success(
      this.intl.t("components.nav-bar.snippet.copy-success")
    );
  }

  @action
  onCopyError() {
    this.notification.danger(
      this.intl.t("components.nav-bar.snippet.copy-error")
    );
  }

  @action
  loadMoreSnippets() {
    this.pageNumber += 1;
    this.fetchSnippets.perform();
  }

  @restartableTask
  *search(event) {
    yield timeout(1000);
    this.searchTerm = event.target.value;
    this.pageNumber = 1;
    this.snippets = [];
    this.fetchSnippets.perform();
  }

  @restartableTask
  *fetchSnippets() {
    try {
      if (this.can.cannot("list snippet")) {
        return;
      }

      const snippets = yield this.store.query("snippet", {
        filter: { search: this.searchTerm, archived: false },
        page: {
          number: this.pageNumber,
          size: this.pageSize,
        },
      });
      this.totalPages = snippets.meta.pagination?.pages;

      this.snippets = [...this.snippets, ...snippets.toArray()];

      return snippets;
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
    }
  }
}
