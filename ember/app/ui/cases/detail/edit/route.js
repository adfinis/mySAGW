import CasesDetailRoute from "mysagw/ui/cases/detail/index/route";

export default class CasesDetailEditRoute extends CasesDetailRoute {
  async model() {
    return await this.modelFor("cases.detail");
  }
}
