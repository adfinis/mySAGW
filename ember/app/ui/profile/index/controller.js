import Controller from "@ember/controller";
import { action } from "@ember/object";
import { filterBy } from "@ember/object/computed";
import { tracked } from "@glimmer/tracking";
import { lastValue, restartableTask } from "ember-concurrency-decorators";

export default class ProfileIndexController extends Controller {
  queryParams = ["activeTab"];
  @tracked activeTab = 0;

  @filterBy("_organisations", "isOrganisation", true) organisations;
  @lastValue("fetchOrganisations") _organisations;
  @restartableTask
  *fetchOrganisations() {
    try {
      const organisations = yield this.store.findAll("identity", {
        adapterOptions: { customEndpoint: "my-orgs" },
      });

      return organisations;
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
