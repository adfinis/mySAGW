import Route from "@ember/routing/route";
import { service } from "@ember/service";

export default class MembershipRolesRoute extends Route {
  @service("router") router;
  @service can;

  beforeModel() {
    if (this.can.cannot("list membership-role")) {
      return this.router.transitionTo("notfound");
    }
  }
}
