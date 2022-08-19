import Route from "@ember/routing/route";

export default class CasesIndexRoute extends Route {
  setupController(controller, model) {
    super.setupController(controller, model);
    controller.fetchCaseAccesses.perform();
    controller.fetchIdentities.perform(true);
  }
}
