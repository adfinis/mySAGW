import Route from "@ember/routing/route";
import { service } from "@ember/service";

export default class MembershipRolesEditRoute extends Route {
  @service store;

  model({ role }) {
    return this.store.findRecord("membership-role", role);
  }
}
