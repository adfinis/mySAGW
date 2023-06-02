import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class ProtectedRoute extends Route {
  @service session;
  @service store;

  beforeModel(transition) {
    this.session.requireAuthentication(transition, "login");
  }

  model() {
    return Promise.all([
      this.store.query(
        "membership",
        {
          include: "organisation",
        },
        { adapterOptions: { customEndpoint: "my-memberships" } }
      ),
      this.store.queryRecord("identity", {}),
    ]);
  }
}
