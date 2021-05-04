import Route from "@ember/routing/route";

export default class WorkItemsIndexRoute extends Route {
  setupController(controller, model) {
    super.setupController(controller, model);
    controller.fetchWorkItems.perform();
  }
}
