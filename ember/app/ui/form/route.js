import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class FormRoute extends Route {
  @service("router") router;
  @service can;

  beforeModel() {
    if (this.can.cannot("list form-builder")) {
      return this.router.transitionTo("notfound");
    }
  }
}
