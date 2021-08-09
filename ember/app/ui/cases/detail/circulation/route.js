import Route from "@ember/routing/route";

export default class CasesDetailCirculationRoute extends Route {
  setupController(controller, model) {
    super.setupController(controller, model);
    controller.fetchIdentities.perform();
    controller.fetchWorkItems.perform();
  }
}
