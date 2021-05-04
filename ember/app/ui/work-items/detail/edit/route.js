import Route from "@ember/routing/route";

export default class WorkItemsDetailEditRoute extends Route {
  model() {
    return this.modelFor("work-items.detail");
  }
}
