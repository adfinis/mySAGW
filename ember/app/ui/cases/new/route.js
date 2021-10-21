import Route from "@ember/routing/route";

export default class CasesNewRoute extends Route {
  async setupController(controller, model) {
    super.setupController(controller, model);
    await controller.fetchForms.perform();
  }
}
