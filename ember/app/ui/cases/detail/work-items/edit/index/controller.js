import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import calumaQuery from "ember-caluma/caluma-query";
import { allWorkItems } from "ember-caluma/caluma-query/queries";
import { dropTask, lastValue } from "ember-concurrency-decorators";
import moment from "moment";
import saveWorkItemMutation from "mysagw/gql/mutations/save-work-item.graphql";

export default class CasesDetailWorkItemsEditController extends Controller {
  @queryManager apollo;

  @service store;
  @service notification;
  @service intl;
  @service moment;

  @calumaQuery({ query: allWorkItems, options: "options" })
  workItemsQuery;

  get options() {
    return {
      pageSize: 1,
    };
  }

  @lastValue("fetchWorkItem") workItem;
  @dropTask()
  *fetchWorkItem() {
    try {
      yield this.workItemsQuery.fetch({ filter: [{ id: this.model }] });

      return this.workItemsQuery.value[0];
    } catch (error) {
      this.notification.danger(this.intl.t("workItems.fetchError"));
    }
  }

  @dropTask
  *saveWorkItem(event) {
    event.preventDefault();

    try {
      yield this.apollo.mutate({
        mutation: saveWorkItemMutation,
        variables: {
          input: {
            workItem: this.workItem.id,
            deadline: this.workItem.deadline,
            assignedUsers: this.workItem.assignedUsers,
          },
        },
      });

      this.notification.success(this.intl.t("workItems.saveSuccess"));

      this.transitionToRoute("cases.detail.work-items.index");
    } catch (error) {
      this.notification.danger(this.intl.t("workItems.saveError"));
    }
  }

  @lastValue("fetchIdentities") identities;
  @dropTask
  *fetchIdentities() {
    return yield this.store.query("identity", {
      filter: {
        isOrganisation: false,
        memberships__organisation__organisationName: "sagw",
      },
    });
  }

  @action
  onUpdate() {
    this.fetchWorkItem.perform();
    this.fetchIdentities.perform();
  }

  @action
  setDeadline(value) {
    this.workItem.deadline = moment(value);
  }

  @action
  setAssignedUser(identity) {
    this.workItem.assignedUser = identity.idpId;
  }

  @action
  transistionToCase() {
    this.transitionToRoute("cases");
  }
}
