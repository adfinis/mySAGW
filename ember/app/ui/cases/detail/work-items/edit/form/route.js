import Route from "@ember/routing/route";

export default class CasesDetailWorkItemsEditFormRoute extends Route {
  model() {
    return this.modelFor("cases.detail.work-items.edit");
  }

  setupController(controller, model) {
    super.setupController(controller, model);
    controller.fetchWorkItems.perform(model);
  }
}
