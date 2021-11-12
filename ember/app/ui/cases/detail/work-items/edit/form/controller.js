import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import calumaQuery from "@projectcaluma/ember-core/caluma-query";
import { allWorkItems } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import { restartableTask, lastValue } from "ember-concurrency";

export default class CasesDetailWorkItemsEditFormController extends Controller {
  @queryManager apollo;

  @service notification;
  @service intl;
  @service router;

  @calumaQuery({ query: allWorkItems })
  workItemQuery;

  @calumaQuery({ query: allWorkItems })
  additionalWorkItemQuery;

  get completeWorkItem() {
    return this.workItem.additionalWorkItem
      ? this.additionalWorkItem
      : this.model;
  }

  @lastValue("fetchWorkItem") workItem;
  @restartableTask()
  *fetchWorkItem(model) {
    try {
      yield this.workItemQuery.fetch({ filter: [{ id: model }] });

      if (this.workItemQuery.value[0].additionalWorkItem) {
        this.fetchAdditonalWorkItem.perform(
          this.workItemQuery.value[0].additionalWorkItem
        );
      }

      return this.workItemQuery.value[0];
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("work-items.fetchError"));
    }
  }

  @lastValue("fetchAdditonalWorkItem") additionalWorkItem;
  @restartableTask()
  *fetchAdditonalWorkItem(filter) {
    try {
      yield this.additionalWorkItemQuery.fetch({
        filter: [...filter, { case: this.workItemQuery.value[0].raw.case.id }],
      });

      return this.additionalWorkItemQuery.value[0].id;
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("work-items.fetchError"));
    }
  }

  @action
  transitionToCaseWorkItems() {
    this.router.transitionTo("cases.detail.work-items", this.workItem.case.id);
  }
}
