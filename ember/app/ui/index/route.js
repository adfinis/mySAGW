import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class IndexRoute extends Route {
  @service can;

  beforeModel() {
    if (this.can.can("list work-item")) {
      return this.transitionTo("work-items");
    }

    this.transitionTo("cases");
  }
}
