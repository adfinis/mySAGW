import Route from "@ember/routing/route";
import { service } from "@ember/service";

export default class ProfileIndexRoute extends Route {
  @service session;

  model() {
    return this.session.identity;
  }

  setupController(controller, post) {
    super.setupController(controller, post);

    controller.fetchMemberships.perform();
    controller.memberships = [];
  }
}
