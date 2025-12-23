import Route from "@ember/routing/route";
import { service } from "@ember/service";

export default class IdentitiesEditRoute extends Route {
  @service store;

  model({ identity }) {
    return this.store.findRecord("identity", identity);
  }
}
