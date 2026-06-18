import Route from "@ember/routing/route";
import { service } from "@ember/service";

export default class ProfileIndexRoute extends Route {
  @service session;
  @service store;

  model() {
    return this.store.queryRecord("identity", {});
  }

  setupController(controller, post) {
    super.setupController(controller, post);

    controller.fetchMemberships.perform();
    controller.memberships = [];
  }
}
