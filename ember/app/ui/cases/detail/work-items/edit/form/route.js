import { getOwner, setOwner } from "@ember/application";
import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";

import CustomWorkItemModel from "mysagw/caluma-query/models/work-item";
import getWorkItemDetailsQuery from "mysagw/gql/queries/get-work-item-details.graphql";

export default class CasesDetailWorkItemsEditFormRoute extends Route {
  @queryManager apollo;
  @service notification;
  @service intl;

  async model() {
    try {
      const rawWorkItem = await this.apollo.watchQuery(
        {
          query: getWorkItemDetailsQuery,
          variables: {
            filter: [{ id: this.modelFor("cases.detail.work-items.edit") }],
          },
        },
        "allWorkItems.edges"
      );

      const workItem = new CustomWorkItemModel(rawWorkItem[0].node);
      setOwner(workItem, getOwner(this));

      return workItem;
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("work-items.fetchError"));
    }
  }
}
