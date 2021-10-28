import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class MembershipRolesRoute extends Route {
  @service can;

  beforeModel() {
    if (this.can.cannot("list membership-role")) {
      return this.transitionTo("notfound");
    }
  }
}
