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

  @calumaQuery({ query: allWorkItems })
  workItemsQuery;

  @lastValue("fetchWorkItems") workItem;
  @restartableTask()
  *fetchWorkItems(model) {
    try {
      yield this.workItemsQuery.fetch({ filter: [{ id: model }] });

      return this.workItemsQuery.value[0];
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("work-items.fetchError"));
    }
  }

  @action
  transitionToCaseWorkItems() {
    this.transitionToRoute("cases.detail.work-items", this.workItem.case.id);
  }
}
