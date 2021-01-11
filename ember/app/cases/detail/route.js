import Route from "@ember/routing/route";

export default class CasesDetailRoute extends Route {
  model(params) {
    return params.id;
  }
}
