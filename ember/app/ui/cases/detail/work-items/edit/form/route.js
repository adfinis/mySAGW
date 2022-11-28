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
      this.rawWorkItem = this.apollo.watchQuery(
        {
          query: getWorkItemDetailsQuery,
          variables: {
            filter: [{ id: this.modelFor("cases.detail.work-items.edit") }],
          },
        },
        "allWorkItems.edges"
      );

      return {
        rawWorkItem: this.rawWorkItem,
        workItem: new CustomWorkItemModel((await this.rawWorkItem)[0].node),
      };
    } catch (error) {
      this.notification.danger(this.intl.t("work-items.fetchError"));
    }
  }
}
