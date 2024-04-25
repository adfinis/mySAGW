import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class SnippetsRoute extends Route {
  @service("router") router;
  @service can;

  beforeModel() {
    if (this.can.cannot("list snippet")) {
      return this.router.transitionTo("notfound");
    }
  }
}
