import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class SnippetsRoute extends Route {
  @service can;

  beforeModel() {
    if (this.can.cannot("list snippet")) {
      return this.transitionTo("notfound");
    }
  }
}
