import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import calumaQuery from "ember-caluma/caluma-query";
import { allWorkItems } from "ember-caluma/caluma-query/queries";
import { restartableTask, lastValue } from "ember-concurrency";

export default class CasesDetailWorkItemsEditFormController extends Controller {
  @queryManager apollo;

  @service store;
  @service notification;
  @service intl;
  @service moment;
  @service session;

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
      this.notification.danger(this.intl.t("workItems.fetchError"));
    }
  }

  @action
  transitionToCase() {
    this.transitionToRoute("cases");
  }
}
