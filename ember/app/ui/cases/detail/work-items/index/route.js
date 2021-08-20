import Route from "@ember/routing/route";

export default class CasesDetailWorkItemsRoute extends Route {
  setupController(controller, model) {
    super.setupController(controller, model);

    // The rule is broken when using controllerFor
    // https://github.com/ember-cli/eslint-plugin-ember/issues/1108
    // eslint-disable-next-line ember/no-controller-access-in-routes
    this.controllerFor("cases.detail").fetchWorkItems.perform();
    controller.fetchWorkItems.perform();
  }
}
