import Route from "@ember/routing/route";

export default class CasesDetailIndexRoute extends Route {
  async model() {
    return await this.modelFor("cases.detail");
  }
}
