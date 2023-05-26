import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class IndexRoute extends Route {
  @service can;
  @service store;
  @service notification;
  @service intl;
  @service router;

  model() {
    return this.store.queryRecord("identity", {});
  }

  afterModel(model) {
    if (!(model.firstName && model.lastName)) {
      this.notification.warning(this.intl.t("profile.noNameSet"));
      return this.router.transitionTo("profile");
    }

    if (this.can.can("list work-item")) {
      return this.router.transitionTo("work-items");
    }

    this.router.transitionTo("cases");
  }
}
