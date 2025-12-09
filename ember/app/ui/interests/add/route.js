import Route from "@ember/routing/route";
import { service } from "@ember/service";

export default class InterestsAddRoute extends Route {
  @service store;

  model() {
    return this.store.createRecord("interest-category");
  }
}
