import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";

export default class NavbarComponent extends Component {
  @service session;
  @service intl;

  @action
  invalidateSession() {
    this.session.singleLogout();
  }

  @action
  setLocale(locale) {
    this.intl.setLocale(locale)
  }
}
