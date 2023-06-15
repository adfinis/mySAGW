import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";

export default class CasesDetailWorkItemsEditFormController extends Controller {
  @service router;
  @service notification;
  @service intl;
  @service session;
  @service can;
  @service caseData;

  @tracked confirmModal = false;

  get showTaskButton() {
    return this.model.task.slug === "additional-data-form";
  }

  get taskButtonFilters() {
    return [
      { task: "additional-data" },
      { status: "READY" },
      { case: this.model.case.id },
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
      this.model.task.slug === "define-amount" &&
      this.model.raw.document.answers.edges.findBy(
        "node.question.slug",
        "define-amount-decision"
      )?.node.StringAnswerValue === "define-amount-decision-reject" &&
      this.model.case.workItems.edges
        .findBy("node.task.slug", "decision-and-credit")
        .node.document.answers.edges.findBy(
          "node.question.slug",
          "decision-and-credit-decision"
        ).node.StringAnswerValue ===
        "decision-and-credit-decision-define-amount"
    ) {
      this.notification.warning(
        this.intl.t("work-items.rejectDefineAmountNoAdditionData")
      );
    }

    if (this.model.task.slug === "circulation-decision") {
      if (this.can.can("list admin case", this.model.case)) {
        return this.router.transitionTo(
          "cases.detail.circulation",
          this.model.case.id
        );
      }
      return this.router.transitionTo("cases.detail.index", this.model.case.id);
    }

    const fetches = [this.caseData.fetchCase.perform(this.model.case.id)];

    if (this.model.task.slug === "review-document") {
      fetches.push(this.caseData.fetchCirculation.perform(this.model.case.id));
    }

    await Promise.all(fetches);
    this.router.transitionTo("cases.detail.work-items", this.model.case.id);
  }
}
