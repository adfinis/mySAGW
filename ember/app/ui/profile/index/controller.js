import Controller from "@ember/controller";
import { action } from "@ember/object";
import { tracked } from "@glimmer/tracking";
import { lastValue, restartableTask } from "ember-concurrency-decorators";

export default class ProfileIndexController extends Controller {
  queryParams = ["activeTab"];
  @tracked activeTab = 0;

  @lastValue("fetchMemberships") memberships;
  @restartableTask
  *fetchMemberships() {
    try {
      const memberships = yield this.store.query("membership", {
        filter: { identity: this.model.id },
        include: "organisation,role",
      });

      return memberships;
    } catch (error) {
      console.error(error);

      this.notification.fromError(error);
    }
  }

  @action
  setActiveTab(tab) {
    this.activeTab = tab;
  }
}
