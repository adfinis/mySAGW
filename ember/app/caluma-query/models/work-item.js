import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import WorkItemModel from "@projectcaluma/ember-core/caluma-query/models/work-item";
import { queryManager } from "ember-apollo-client";

import ENV from "mysagw/config/environment";
import saveWorkItemMutation from "mysagw/gql/mutations/save-work-item.graphql";

export default class CustomWorkItemModel extends WorkItemModel {
  @queryManager apollo;

  @service store;
  @service router;
  @service intl;
  @service notification;
  @service session;

  @tracked meta = this.raw.meta;
  @tracked assignedUsers = this.raw.assignedUsers;

  get assignedUser() {
    return this.store
      .peekAll("identity")
      .find((identity) => this.assignedUsers.includes(identity.idpId));
  }
  set assignedUser(idpId) {
    this.assignedUsers = [idpId];
  }

  get closedByUser() {
    return this.store
      .peekAll("identity")
      .findBy("idpId", this.raw.closedByUser);
  }

  get createdByUser() {
    return this.store
      .peekAll("identity")
      .findBy("idpId", this.raw.closedByUser);
  }

  get isAssignedToCurrentUser() {
    return this.assignedUsers.includes(
      this.session.data.authenticated.userinfo.sub,
    );
  }

  get isReady() {
    return this.raw.status === "READY";
  }

  get isCompleted() {
    return this.raw.status === "COMPLETED";
  }

  get canEdit() {
    if (this.raw.task.slug === "circulation-decision") {
      return this.isReady && this.isAssignedToCurrentUser;
    }
    return this.isReady;
  }

  get canComplete() {
    if (this.raw.task.slug === "circulation-decision") {
      return this.isReady && this.isAssignedToCurrentUser;
    } else if (["advance-credits"].includes(this.raw.task.slug)) {
      return false;
    }
    return this.isReady;
  }

  get canSkip() {
    return (
      this.isReady &&
      ENV.APP.caluma.skippableTaskSlugs.includes(this.raw.task.slug)
    );
  }

  get responsible() {
    return this.assignedUser?.fullName ?? "-";
  }

  get case() {
    return this.raw.case.parentWorkItem?.case ?? this.raw.case;
  }

  get statusName() {
    return this.intl.t(`work-items.statuses.${this.raw.status}`);
  }

  async assignToMe() {
    return await this.assignToUser(
      this.session.data.authenticated.userinfo.sub,
    );
  }

  async assignToUser(user) {
    try {
      this.assignedUser = user;

      if (this.task.slug === "circulation-decision") {
        this.meta = {
          ...this.meta,
          assigneeName: this.assignedUser.fullName,
          assigneeEmail: this.assignedUser.email,
        };
      }

      await this.apollo.mutate({
        mutation: saveWorkItemMutation,
        variables: {
          input: {
            workItem: this.id,
            assignedUsers: this.assignedUsers,
            meta: JSON.stringify(this.meta),
          },
        },
      });

      return true;
    } catch (error) {
      this.notification.danger(this.intl.t("work-items.saveError"));
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
    description
    document {
      id
      form {
        slug
      }
      answers(filter: [{questions: ["circulation-decision", "circulation-comment", "circulation-antrag-betrag"]}]) {
        edges {
          node {
            id
            question {
              slug
              meta
              ... on ChoiceQuestion {
                options {
                  edges {
                    node {
                      slug
                      label
                    }
                  }
                }
              }
            }
            ... on StringAnswer {
              StringAnswerValue: value
            }
            ... on FloatAnswer {
              FloatAnswerValue: value
            }
          }
        }
      }
    }
    case {
      id
      meta
      createdByUser
      parentWorkItem {
        id
        status
        task {
          slug
        }
        case {
          id
          document {
            id
            form {
              slug
              name
            }
            answers(filter: [{questions: ["dossier-nr", "sektion", "verteilplan-nr", "mitgliedinstitution"]}]) {
              edges {
                node {
                  id
                  question {
                    slug
                    ... on ChoiceQuestion {
                      options {
                        edges {
                          node {
                            slug
                            label
                          }
                        }
                      }
                    }
                  }
                  ... on StringAnswer {
                    StringAnswerValue: value
                  }
                  ... on IntegerAnswer {
                    IntegerAnswerValue: value
                  }
                }
              }
            }
          }
        }
        childCase {
          id
          status
        }
      }
      document {
        id
        form {
          slug
          name
        }
        answers(filter: [{questions: ["dossier-nr", "sektion", "verteilplan-nr", "mitgliedinstitution"]}]) {
          edges {
            node {
              id
              question {
                slug
                ... on ChoiceQuestion {
                  options {
                    edges {
                      node {
                        slug
                        label
                      }
                    }
                  }
                }
              }
              ... on StringAnswer {
                StringAnswerValue: value
              }
              ... on IntegerAnswer {
                IntegerAnswerValue: value
              }
            }
          }
        }
      }
    }
    childCase {
      id
      status
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
