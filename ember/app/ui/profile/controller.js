import Controller from "@ember/controller";
import { filterBy } from "@ember/object/computed";
import { lastValue, restartableTask } from "ember-concurrency-decorators";

export default class ProfileController extends Controller {
  @filterBy("_organisations", "isOrganisation", true) organisations;
  @lastValue("fetchOrganisations") _organisations;
  @restartableTask
  *fetchOrganisations() {
    try {
      const organisations = yield this.store.findAll("identity");

      return organisations;
    } catch (error) {
      console.error(error);

      this.notification.fromError(error);
    }
  }
}
