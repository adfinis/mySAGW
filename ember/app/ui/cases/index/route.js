import Route from "@ember/routing/route";

export default class CasesIndexRoute extends Route {
  setupController(controller, model) {
    super.setupController(controller, model);
    controller.fetchCases.perform();
    controller.fetchIdentities.perform();
  }
}
