import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class ProfileEditRoute extends Route {
  @service store;

  model({ identity }) {
    return this.store.findRecord("identity", identity, {
      adapterOptions: { customEndpoint: "my-orgs" },
    });
  }
}
