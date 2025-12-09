import Route from "@ember/routing/route";
import { service } from "@ember/service";

export default class MembershipRolesAddRoute extends Route {
  @service store;

  model() {
    return this.store.createRecord("membership-role");
  }
}
