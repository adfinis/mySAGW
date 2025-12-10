import Route from "@ember/routing/route";

export default class SnippetsIndexRoute extends Route {
  setupController(controller, post) {
    super.setupController(controller, post);

    controller.fetchSnippets.perform();
  }
}
