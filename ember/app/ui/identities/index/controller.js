import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { restartableTask, lastValue } from "ember-concurrency-decorators";

export default class IdentitiesIndexController extends Controller {
  @service notification;
  @service store;

  @lastValue("fetchIdentities") identities;

  @restartableTask *fetchIdentities() {
    try {
      return yield this.store.findAll("identity");
    } catch (error) {
      console.error(error);
      this.notification.danger(error.message);
    }
  }

  @action onUpdate() {
    this.fetchIdentities.perform();
  }
}
