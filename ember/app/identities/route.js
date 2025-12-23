import Route from "@ember/routing/route";
import { service } from "@ember/service";

export default class IdentitesRoute extends Route {
  @service("router") router;
  @service can;

  beforeModel() {
    if (this.can.cannot("list identity")) {
      return this.router.transitionTo("notfound");
    }
  }
}
