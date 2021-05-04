import Route from "@ember/routing/route";

export default class CasesDetailWorkItemsEditRoute extends Route {
  model() {
    return this.modelFor("cases.detail.work-items.edit");
  }
}
