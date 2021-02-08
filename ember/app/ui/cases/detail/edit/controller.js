import Controller from "@ember/controller";

export default class CasesDetailEditController extends Controller {
  get disabled() {
    return this.model.status !== "RUNNING";
  }
}
