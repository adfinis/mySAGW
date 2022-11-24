import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import { restartableTask, lastValue } from "ember-concurrency";

import CustomWorkItemModel from "mysagw/caluma-query/models/work-item";
import getWorkItemDetailsQuery from "mysagw/gql/queries/get-work-item-details.graphql";
import getWorkItemsQuery from "mysagw/gql/queries/get-work-items.graphql";

export default class CasesDetailWorkItemsEditFormRoute extends Route {
  @queryManager apollo;

  @service notification;
  @service intl;
  @service router;

  get workItemToComplete() {
    return this.workItem.additionalWorkItem
      ? this.additionalWorkItem
      : this.workItem;
  }

  @lastValue("fetchWorkItem") workItem;
  @restartableTask()
  *fetchWorkItem() {
    try {
      const workItem = new CustomWorkItemModel(
        (yield this.rawWorkItem)[0].node
      );

      if (workItem.additionalWorkItem) {
        yield this.fetchAdditonalWorkItem.perform(workItem.additionalWorkItem);
      }

      return workItem;
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("work-items.fetchError"));
    }
  }

  @lastValue("fetchAdditonalWorkItem") additionalWorkItem;
  @restartableTask()
  *fetchAdditonalWorkItem(filter) {
    try {
      const workItem = yield this.apollo.query(
        {
          query: getWorkItemsQuery,
          variables: { filter: [...filter, { case: this.workItem.case.id }] },
        },
        "allWorkItems.edges"
      );

      return new CustomWorkItemModel(workItem[0].node);
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("work-items.fetchError"));
    }
  }

  async model() {
    this.rawWorkItem = this.apollo.watchQuery(
      {
        query: getWorkItemDetailsQuery,
        variables: {
          filter: [{ id: this.modelFor("cases.detail.work-items.edit") }],
        },
      },
      "allWorkItems.edges"
    );

    await this.fetchWorkItem.perform();

    return {
      rawWorkItem: this.rawWorkItem,
      workItem: this.workItem,
      workItemToComplete: this.workItemToComplete,
    };
  }
}
