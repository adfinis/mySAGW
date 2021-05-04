import Route from "@ember/routing/route";

export default class WorkItemsDetailRoute extends Route {
  model(params) {
    return params.id;
  }

  afterModel() {
    this.transitionTo("work-items.detail.edit");
  }
}
