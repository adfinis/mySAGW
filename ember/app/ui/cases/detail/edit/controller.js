import Controller from "@ember/controller";
import { inject as service } from "@ember/service";

export default class CasesDetailEditController extends Controller {
  @service can;

  get disabled() {
    return !(
      this.model.hasEditableWorkItem && this.can.can("edit case", this.model)
    );
  }
}
