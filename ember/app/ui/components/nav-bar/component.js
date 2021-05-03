import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";

export default class NavbarComponent extends Component {
  @service session;
  @service intl;
  @service store;
  @service notification;
  @service intl;

  @tracked searchTerm = "";

  @action
  invalidateSession() {
    this.session.singleLogout();
  }

  @action
  setLocale(locale) {
    this.intl.setLocale(locale);
  }

  @action
  search(event) {
    this.searchTerm = event.target.value;
  }

  @action
  onCopySuccess() {
    this.notification.success(this.intl.t("nav.snippet.copy-success"));
  }

  @action
  onCopyError() {
    this.notification.danger(this.intl.t("nav.snippet.copy-error"));
  }

  get snippets() {
    return this.store.peekAll("snippet").filter((snippet) => {
      return (
        snippet.archived === false &&
        (snippet.title.includes(this.searchTerm) ||
          snippet.body.includes(this.searchTerm))
      );
    });
  }
}
