import Controller from "@ember/controller";
import { inject as service } from "@ember/service";

export default class CasesDetailEditController extends Controller {
  queryParams = ["displayedForm"];
  @service can;

  get disabled() {
    return !this.can.can("edit case", this.model);
  }
}
