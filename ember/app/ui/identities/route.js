import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class IdentitesRoute extends Route {
  @service can;

  beforeModel() {
    if (this.can.cannot("list identity")) {
      return this.transitionTo("notfound");
    }
  }
}
