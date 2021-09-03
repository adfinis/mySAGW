import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import calumaQuery from "ember-caluma/caluma-query";
import { allWorkItems } from "ember-caluma/caluma-query/queries";
import { restartableTask } from "ember-concurrency";

export default class WorkItemsIndexController extends Controller {
  queryParams = ["order", "responsible", "status", "role"];

  @service session;
  @service store;

  @queryManager apollo;

  @calumaQuery({ query: allWorkItems, options: "options" })
  workItemsQuery;

  // Filters
  @tracked order = "urgent";
  @tracked responsible = "all";
  @tracked status = "open";
  @tracked role = "active";

  get options() {
    return {
      pageSize: 20,
    };
  }

  get tableConfig() {
    return {
      columns: [
        {
          heading: { label: "workItems.task" },
          type: "task-name",
        },
        {
          heading: { label: "workItems.documentNumber" },
          modelKey: "case.document.answers.edges",
          linkTo: "cases.detail.index",
          type: "answer-value",
          questionSlug: "dossier-nr",
        },
        {
          heading: { label: "workItems.case" },
          modelKey: "case.document.form.name",
          linkTo: "cases.detail.index",
        },
        {
          heading: { label: "workItems.caseCreatedBy" },
          modelKey: "case.createdByUser",
          type: "case-created-by",
        },
        ...(this.status === "open"
          ? [
              {
                heading: { label: "workItems.deadline" },
                modelKey: "deadline",
                type: "deadline",
              },
              {
                heading: { label: "workItems.responsible" },
                modelKey: "responsible",
              },
            ]
          : [
              {
                heading: { label: "workItems.closedAt" },
                modelKey: "closedAt",
                type: "date",
              },
              {
                heading: { label: "workItems.closedBy" },
                modelKey: "closedByUser.fullName",
              },
            ]),
      ],
    };
  }

  @restartableTask
  *fetchWorkItems() {
    const filter = [{ hasDeadline: true }];

    if (this.responsible === "own") {
      filter.push({
        assignedUsers: [this.session.data.authenticated.userinfo.sub],
      });
    }

    if (this.status === "closed") {
      filter.push({ status: "COMPLETED" });
    } else {
      filter.push({ status: "READY" });
    }

    if (this.role === "control") {
      filter.push({ controllingGroups: ["sagw"] });
    }

    const order =
      this.order === "urgent"
        ? [{ attribute: "DEADLINE", direction: "ASC" }]
        : [{ attribute: "CREATED_AT", direction: "DESC" }];

    yield this.workItemsQuery.fetch({ filter, order });
    yield this.getIdentities.perform();
  }

  @restartableTask
  *getIdentities() {
    let idpIds = [];

    this.workItemsQuery.value.forEach((workItem) => {
      idpIds = [
        ...idpIds,
        ...workItem.assignedUsers,
        workItem.raw.closedByUser,
        workItem.raw.case.createdByUser,
      ];
    });

    idpIds = idpIds.compact().uniq();

    if (idpIds.length) {
      return yield this.store.query("identity", {
        filter: { idpIds: idpIds.join(",") },
      });
    }
  }

  @action
  updateFilter(type, value) {
    this[type] = value;
    this.fetchWorkItems.perform();
  }
}
