import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";

export default class CasesDetailWorkItemsEditFormController extends Controller {
  @service router;

  @action
  transitionToCaseWorkItems() {
    this.router.transitionTo(
      "cases.detail.work-items",
      this.model.workItem.case.id
    );
  }
}
