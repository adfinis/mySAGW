import Route from "@ember/routing/route";

export default class TableRoute extends Route {
  setupController(controller, model) {
    super.setupController(controller, model);
    controller.fetchForms.perform();
    controller.deserializeFilter();
  }
}
