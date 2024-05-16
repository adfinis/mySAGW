import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import calumaQuery from "@projectcaluma/ember-core/caluma-query";
import { allWorkItems } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import { dropTask, lastValue, restartableTask } from "ember-concurrency";

import ENV from "mysagw/config/environment";
import completeWorkItem from "mysagw/gql/mutations/complete-work-item.graphql";

export default class CasesDetailCirculationController extends Controller {
  @queryManager apollo;

  @service store;
  @service notification;
  @service intl;
  @service router;

  @tracked selectedIdentities = [];

  @calumaQuery({ query: allWorkItems })
  workItemsQuery;

  @calumaQuery({ query: allWorkItems })
  circulationWorkItemsQuery;

  get tableConfig() {
    return {
      columns: [
        {
          heading: { label: "work-items.responsible" },
          modelKey: "responsible",
        },
        {
          heading: { label: "work-items.status" },
          modelKey: "status",
        },
        {
          heading: { label: "work-items.task" },
          type: "task-name",
        },
        {
          heading: { label: "work-items.closedAt" },
          modelKey: "closedAt",
          type: "date",
        },
        {
          heading: { label: "work-items.circulationDecision" },
          questionSlug: "circulation-decision",
          answerKey: "document.answers.edges",
          type: "answer-value",
        },
        {
          heading: { label: "work-items.circulationComment" },
          questionSlug: "circulation-comment",
          answerKey: "document.answers.edges",
          type: "answer-value",
        },
        {
          heading: { label: "work-items.circulationAmount" },
          questionSlug: "circulation-antrag-betrag",
          answerKey: "document.answers.edges",
          type: "answer-value",
        },
        {
          heading: { label: "work-items.actions.title", hidden: true },
          type: "work-item-actions",
        },
      ],
    };
  }

  get circulationWorkItem() {
    return (
      this.circulationWorkItemsQuery.value.findBy("task.slug", "circulation") ??
      this.model.workItems.findBy("task.slug", "circulation")
    );
  }

  get finishCirculationWorkItem() {
    return this.circulationWorkItemsQuery.value.findBy(
      "task.slug",
      "finish-circulation",
    );
  }

  get inviteToCirculationWorkItem() {
    return this.circulationWorkItemsQuery.value.find((workItem) => {
      return workItem.task.slug === "invite-to-circulation" && workItem.isReady;
    });
  }

  get canFinishCirculation() {
    if (!this.workItemsQuery.value.length) {
      return false;
    }

    return this.workItemsQuery.value.every(
      (workItem) => workItem.raw.status === "COMPLETED",
    );
  }

  get circulationActive() {
    return (
      (this.circulationWorkItem?.raw?.status ??
        this.circulationWorkItem?.status) === "READY"
    );
  }

  get identities() {
    const assignedUsers = this.workItemsQuery.value
      .filter((workItem) => workItem.isReady)
      .map((workItem) => workItem.raw.assignedUsers)
      .flat();

    return this._identities?.filter((identity) => {
      return !assignedUsers.includes(identity.idpId);
    });
  }

  @lastValue("fetchIdentities") _identities;
  @dropTask
  *fetchIdentities() {
    return yield this.store.query("identity", {
      filter: {
        isOrganisation: false,
        member_of_organisations: ENV.APP.circulationOrganisations.toString(),
        hasIdpId: true,
      },
    });
  }

  @dropTask
  *fetchWorkItems() {
    try {
      if (!this.circulationWorkItem) {
        return;
      }

      yield this.workItemsQuery.fetch({
        filter: [
          { task: "circulation-decision" },
          { case: this.circulationWorkItem.childCase.id },
        ],
      });
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("work-items.fetchError"));
    }
  }

  @restartableTask
  *fetchCirculationWorkItems() {
    yield this.circulationWorkItemsQuery.fetch({
      filter: [
        {
          tasks: ["circulation", "invite-to-circulation", "finish-circulation"],
        },
        { caseFamily: this.model.id },
        { status: "REDO", invert: true },
      ],
      order: [{ attribute: "CREATED_AT", direction: "DESC" }],
    });
  }

  @dropTask
  *addToCirculation() {
    yield this.apollo.mutate({
      mutation: completeWorkItem,
      variables: {
        id: this.inviteToCirculationWorkItem.id,
        context: JSON.stringify({
          assign_users: this.selectedIdentities.map((identity) => {
            return {
              idpId: identity.idpId,
              name: identity.fullName,
              email: identity.email,
            };
          }),
        }),
      },
    });

    this.selectedIdentities = [];

    yield Promise.all([
      this.fetchWorkItems.perform(),
      this.fetchCirculationWorkItems.perform(),
    ]);
  }

  @action
  transitionToCaseWorkItems() {
    this.router.transitionTo("cases.detail.work-items", this.model.id);
  }
}
