import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class IndexRoute extends Route {
  @service can;
  @service store;
  @service notification;
  @service intl;

  model() {
    return this.store.queryRecord("identity", {});
  }

  afterModel(model) {
    if (!(model.firstName || model.lastName)) {
      this.notification.warning(this.intl.t("profile.noNameSet"));
      return this.transitionTo("profile");
    }

    if (this.can.can("list work-item")) {
      return this.transitionTo("work-items");
    }

    this.transitionTo("cases");
  }
}
