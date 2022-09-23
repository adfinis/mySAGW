import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class WorkItemsIndexRoute extends Route {
  @service router;
  @service can;

  beforeModel() {
    if (this.can.cannot("list work-item")) {
      return this.router.transitionTo("notfound");
    }
  }
}
