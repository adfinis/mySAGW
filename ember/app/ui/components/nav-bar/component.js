import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";

export default class NavbarComponent extends Component {
  @service session;

  @action
  invalidateSession() {
    this.session.singleLogout();
  }
}
