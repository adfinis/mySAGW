import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";

export default class CasesDetailWorkItemsEditFormController extends Controller {
  @service router;
  @service notification;
  @service intl;

  get showTaskButton() {
    return this.model.workItem.task.slug === "additional-data-form";
  }

  get taskButtonFilters() {
    return [
      { task: "additional-data" },
      { status: "READY" },
      { case: this.model.workItem.case.id },
    ];
  }

  @action
  async transitionToCaseWorkItems() {
    /*
      Display notification to redo when additional-data has been skipped
      by decision-and-credit but define-amount is being rejected, 
      leading to no open additional-data-form which would place the workflow in a stuck state
    */
    if (
      this.model.workItem.task.slug === "define-amount" &&
      (await this.model.rawWorkItem)[0].node.document.answers.edges.findBy(
        "node.question.slug",
        "define-amount-decision"
      )?.node.StringAnswerValue === "define-amount-decision-reject" &&
      this.model.workItem.case.workItems.edges
        .findBy("node.task.slug", "decision-and-credit")
        .node.document.answers.edges.findBy(
          "node.question.slug",
          "decision-and-credit-decision"
        ).node.StringAnswerValue ===
        "decision-and-credit-decision-define-amount"
    ) {
      this.notification.danger(
        this.intl.t("work-items.rejectDefineAmountNoAdditionData")
      );
    }

    if (this.model.workItem.task.slug === "circulation-decision") {
      return this.router.transitionTo(
        "cases.detail.circulation",
        this.model.workItem.case.id
      );
    }

    this.router.transitionTo(
      "cases.detail.work-items",
      this.model.workItem.case.id
    );
  }
}
