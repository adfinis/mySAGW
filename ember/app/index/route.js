import Route from "@ember/routing/route";
import { service } from "@ember/service";

export default class IndexRoute extends Route {
  @service can;
  @service notification;
  @service intl;
  @service router;
  @service session;

  afterModel() {
    if (
      !(this.session.identity?.firstName && this.session.identity?.lastName)
    ) {
      this.notification.warning(this.intl.t("profile.noNameSet"));
      return this.router.transitionTo("profile");
    }

    if (this.can.can("list work-item")) {
      return this.router.transitionTo("work-items");
    }

    this.router.transitionTo("cases");
  }
}
