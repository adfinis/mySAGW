import Route from "@ember/routing/route";

export default class CasesDetailWorkItemsEditRoute extends Route {
  model(params) {
    return params.id;
  }
}
