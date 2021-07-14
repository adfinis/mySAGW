import Route from "@ember/routing/route";

export default class CasesDetailWorkItemsRoute extends Route {
  setupController(controller, model) {
    super.setupController(controller, model);
    controller.fetchWorkItems.perform();
  }
}
