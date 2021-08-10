import Route from "@ember/routing/route";

export default class CasesDetailWorkItemsRoute extends Route {
  setupController(controller, model) {
    super.setupController(controller, model);

    this.controllerFor("cases.detail").fetchWorkItems.perform();
    controller.fetchWorkItems.perform();
  }
}
