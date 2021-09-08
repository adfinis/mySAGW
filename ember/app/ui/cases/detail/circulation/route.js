import Route from "@ember/routing/route";

export default class CasesDetailCirculationRoute extends Route {
  async model() {
    return await this.modelFor("cases.detail");
  }

  async setupController(controller, model) {
    super.setupController(controller, model);
    await controller.fetchCirculationWorkItems.perform();
    await controller.fetchIdentities.perform();
    await controller.fetchWorkItems.perform();
  }
}
