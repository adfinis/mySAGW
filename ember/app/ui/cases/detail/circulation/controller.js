import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import calumaQuery from "ember-caluma/caluma-query";
import { allWorkItems } from "ember-caluma/caluma-query/queries";
import { dropTask, lastValue } from "ember-concurrency";
import moment from "moment";
import createWorkItem from "mysagw/gql/mutations/create-work-item.graphql";

export default class CasesDetailCirculationController extends Controller {
  @queryManager apollo;

  @service store;
  @service notification;
  @service intl;
  @service router;

  @tracked selectedIdentities = [];

  @calumaQuery({ query: allWorkItems })
  workItemsQuery;

  get circulationWorkItem() {
    return this.model.workItems.edges.findBy("node.task.slug", "circulation");
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

  get canFinishCirculation() {
    return this.circulationWorkItem.node.childCase.status === "COMPLETED";
  }

  get circulationActive() {
    return this.circulationWorkItem.node.status === "READY";
  }

  @lastValue("fetchIdentities") _identities;
  @dropTask
  *fetchIdentities() {
    return yield this.store.query("identity", {
      filter: {
        isOrganisation: false,
        memberships__organisation__organisationName: "SAGW",
        hasIdpId: true,
      },
    });
  }

  @dropTask
  *fetchWorkItems() {
    try {
      yield this.workItemsQuery.fetch({
        filter: [
          { task: "circulation-decision" },
          { case: this.circulationWorkItem.node.childCase.id },
        ],
      });
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("workItems.fetchError"));
    }
  }

  @dropTask
  *addToCirculation() {
    for (const identity of this.selectedIdentities) {
      yield this.apollo.mutate({
        mutation: createWorkItem,
        variables: {
          input: {
            case: this.circulationWorkItem.node.childCase.id,
            multipleInstanceTask: "circulation-decision",
            assignedUsers: [identity.idpId],
            deadline: moment().add(5, "d").toISOString(),
          },
        },
      });
    }

    this.selectedIdentities = [];

    yield this.fetchWorkItems.perform();
  }

  @action
  transitionToCaseWorkItems() {
    this.transitionToRoute(
      "cases.detail.work-items",
      this.circulationWorkItem.node.childCase.id
    );
  }
}
