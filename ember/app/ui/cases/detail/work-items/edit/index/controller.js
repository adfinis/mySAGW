import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import calumaQuery from "ember-caluma/caluma-query";
import { allWorkItems } from "ember-caluma/caluma-query/queries";
import { dropTask } from "ember-concurrency-decorators";
import moment from "moment";
import completeWorkItem from "mysagw/gql/mutations/complete-work-item.graphql";
import saveWorkItem from "mysagw/gql/mutations/save-work-item.graphql";

export default class CasesDetailWorkItemsEditController extends Controller {
  @queryManager apollo;

  @service store;
  @service notification;
  @service intl;
  @service moment;

  @tracked workItem;

  @calumaQuery({ query: allWorkItems, options: "options" })
  workItemsQuery;

  get options() {
    return {
      pageSize: 1,
    };
  }

  @dropTask()
  *fetchWorkItems() {
    try {
      yield this.workItemsQuery.fetch({ filter: [{ id: this.model }] });

      this.workItem = this.workItemsQuery.value[0];
    } catch (error) {
      this.notification.danger(this.intl.t("workItems.fetchError"));
    }
  }

  @dropTask
  *finishWorkItem(event) {
    event.preventDefault();

    try {
      yield this.apollo.mutate({
        mutation: saveWorkItem,
        variables: {
          input: {
            workItem: this.workItem.id,
            meta: JSON.stringify(this.workItem.meta),
          },
        },
      });

      yield this.apollo.mutate({
        mutation: completeWorkItem,
        variables: { id: this.workItem.id },
      });

      this.notification.success(this.intl.t("workItems.finishSuccess"));

      this.transitionToRoute("cases.detail.work-items.index");
    } catch (error) {
      this.notification.danger(this.intl.t("workItems.saveError"));
    }
  }

  @dropTask
  *saveManualWorkItem(event) {
    event.preventDefault();

    try {
      yield this.apollo.mutate({
        mutation: saveWorkItem,
        variables: {
          input: {
            workItem: this.workItem.id,
            description: this.workItem.description,
            deadline: this.workItem.deadline,
            meta: JSON.stringify(this.workItem?.meta),
          },
        },
      });

      this.notification.success(this.intl.t("workItems.saveSuccess"));

      this.transitionToRoute("cases.detail.work-items.index");
    } catch (error) {
      this.notification.danger(this.intl.t("workItems.saveError"));
    }
  }

  @action
  setDeadline(value) {
    this.workItem.deadline = moment(value);
  }
}
