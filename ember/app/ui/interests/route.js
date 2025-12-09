import Route from "@ember/routing/route";
import { service } from "@ember/service";

export default class InterestsRoute extends Route {
  @service can;
  @service router;

  beforeModel() {
    if (this.can.cannot("list interest")) {
      return this.router.transitionTo("notfound");
    }
  }
}
