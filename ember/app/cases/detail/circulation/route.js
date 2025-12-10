import Route from "@ember/routing/route";

export default class CasesDetailCirculationRoute extends Route {
  async model() {
    return await this.modelFor("cases.detail");
  }

  async setupController(controller, model) {
    super.setupController(controller, model);
    await Promise.all([
      controller.fetchCirculationWorkItems.perform(),
      controller.fetchIdentities.perform(),
    ]);
    await controller.fetchWorkItems.perform();
  }
}
