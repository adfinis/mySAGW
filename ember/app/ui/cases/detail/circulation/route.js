import Route from "@ember/routing/route";

export default class CasesDetailCirculationRoute extends Route {
  async model() {
    return await this.modelFor("cases.detail");
  }

  setupController(controller, model) {
    super.setupController(controller, model);
    controller.fetchCirculationWorkItems.perform();
    controller.fetchIdentities.perform();
    controller.fetchWorkItems.perform();
  }
}
