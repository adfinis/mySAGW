import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";

export default class InterestsEditRoute extends Route {
  @service store;

  model({ category }) {
    return this.store.findRecord("interest-category", category, {
      include: "interests",
    });
  }
}
