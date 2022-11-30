import { getOwner, setOwner } from "@ember/application";
import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";

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

      const WorkItem = getOwner(this).factoryFor(
        `caluma-query-model:work-item`
      ).class;
      const workItem = new WorkItem((await this.rawWorkItem)[0].node);
      setOwner(workItem, getOwner(this));

      return {
        rawWorkItem: this.rawWorkItem,
        workItem,
      };
    } catch (error) {
      this.notification.danger(this.intl.t("work-items.fetchError"));
    }
  }
}
