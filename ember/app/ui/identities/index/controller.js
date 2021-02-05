import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { restartableTask, lastValue } from "ember-concurrency-decorators";

export default class IdentitiesIndexController extends Controller {
  @service store;

  @lastValue("fetchIdentities") identities;

  @restartableTask *fetchIdentities() {
    return yield this.store.findAll("identity");
  }

  @action onUpdate() {
    this.fetchIdentities.perform();
  }
}
