import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class WorkItemsIndexRoute extends Route {
  @service can;

  beforeModel() {
    if (this.can.cannot("list work-item")) {
      return this.transitionTo("notfound");
    }
  }

  setupController(controller, model) {
    super.setupController(controller, model);
    controller.fetchTasks.perform();
  }
}
