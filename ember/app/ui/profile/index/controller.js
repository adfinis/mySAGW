import Controller from "@ember/controller";
import { action } from "@ember/object";
import { tracked } from "@glimmer/tracking";
import { lastValue, restartableTask } from "ember-concurrency";
import QueryParams from "ember-parachute";

const queryParams = new QueryParams({
  // Convert the tab number to a string so its human readable
  activeTab: {
    defaultValue: "identity",
    serialize(value) {
      return value ? "memberships" : "identity";
    },
    deserialize(value) {
      return value === "identity" ? 0 : 1;
    },
  },
});

export default class ProfileIndexController extends Controller.extend(
  queryParams.Mixin
) {
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
