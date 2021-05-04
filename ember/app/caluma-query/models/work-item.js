import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import WorkItemModel from "ember-caluma/caluma-query/models/work-item";
import saveWorkItemMutation from "mysagw/gql/mutations/save-work-item.graphql";

export default class CustomWorkItemModel extends WorkItemModel {
  @queryManager apollo;

  @service store;
  @service router;
  @service intl;
  @service notification;

  @tracked meta = this.raw.meta;
  @tracked notViewed = this.raw.meta["not-viewed"];
  @tracked assignedUsers = this.raw.assignedUsers;

  get assignedUser() {
    return this.store
      .peekAll("identity")
      .find((identity) => this.assignedUsers.includes(identity.id));
  }
  set assignedUser(identity) {
    this.assignedUsers = [identity.id];
  }

  get closedByUser() {
    return this.raw.closedByUser;
  }

  get createdByUser() {
    return this.raw.createdByUser;
  }

  get isReady() {
    return this.raw.status === "READY";
  }

  get isCompleted() {
    return this.raw.status === "COMPLETED";
  }

  get canEdit() {
    return this.isReady;
  }

  get canComplete() {
    return this.isReady;
  }

  get responsible() {
    return this.assignedUser;
  }

  get case() {
    return this.raw.case.parentWorkItem?.case || this.raw.case;
  }

  async toggleRead() {
    try {
      this.notViewed = !this.notViewed;

      await this.apollo.mutate({
        mutation: saveWorkItemMutation,
        variables: {
          input: {
            workItem: this.id,
            meta: JSON.stringify({
              ...this.raw.meta,
              "not-viewed": this.notViewed,
            }),
          },
        },
      });

      return true;
    } catch (error) {
      this.notification.danger(this.intl.t("workItems.saveError"));
    }
  }

  async assignToMe() {
    return await this.assignToUser(/* TODO current user*/);
  }

  async assignToUser(user) {
    try {
      this.assignedUser = user;

      await this.apollo.mutate({
        mutation: saveWorkItemMutation,
        variables: {
          input: {
            workItem: this.id,
            assignedUsers: this.assignedUsers,
          },
        },
      });

      return true;
    } catch (error) {
      this.notification.danger(this.intl.t("workItems.saveError"));
    }
  }

  static fragment = `{
    createdAt
    createdByUser
    createdByGroup
    closedAt
    closedByUser
    closedByGroup
    status
    meta
    addressedGroups
    controllingGroups
    assignedUsers
    name
    deadline
    description
    document {
      id
      form {
        slug
      }
    }
    case {
      id
      meta
      document {
        id
        form {
          slug
          name
        }
      }
    }
    task {
      slug
      name
      description
      meta
      __typename
    }
  }`;
}
