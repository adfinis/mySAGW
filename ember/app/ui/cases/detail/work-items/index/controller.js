import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import calumaQuery from "ember-caluma/caluma-query";
import { allWorkItems } from "ember-caluma/caluma-query/queries";
import { restartableTask } from "ember-concurrency";

export default class CasesDetailWorkItemsController extends Controller {
  @service store;

  @queryManager apollo;

  @calumaQuery({
    query: allWorkItems,
    options: "options",
  })
  readyWorkItemsQuery;

  @calumaQuery({
    query: allWorkItems,
    options: "options",
  })
  completedWorkItemsQuery;

  get options() {
    return {
      pageSize: 20,
    };
  }

  get readyTableConfig() {
    return {
      columns: [
        {
          heading: { label: "workItems.task" },
          type: "task-name",
        },
        {
          heading: { label: "workItems.deadline" },
          modelKey: "deadline",
          type: "deadline",
        },
        {
          heading: { label: "workItems.responsible" },
          modelKey: "responsible",
        },
        {
          heading: { label: "workItems.action" },
          type: "work-item-actions",
        },
      ],
    };
  }
  get completedTableConfig() {
    return {
      columns: [
        {
          heading: { label: "workItems.task" },
          type: "task-name",
        },
        {
          heading: { label: "workItems.closedAt" },
          modelKey: "closedAt",
          type: "date",
        },
        {
          heading: { label: "workItems.closedBy" },
          modelKey: "closedByUser.fullName",
        },
        {
          heading: { label: "workItems.action" },
          type: "work-item-actions",
        },
      ],
    };
  }

  @restartableTask
  *fetchWorkItems() {
    const filter = [{ hasDeadline: true }, { case: this.model.id }];

    yield this.readyWorkItemsQuery.fetch({
      filter: [...filter, { status: "READY" }],
      order: [{ attribute: "DEADLINE", direction: "ASC" }],
    });

    yield this.completedWorkItemsQuery.fetch({
      filter: [...filter, { status: "COMPLETED" }],
      order: [{ attribute: "CLOSED_AT", direction: "DESC" }],
    });

    yield this.getIdentities.perform();
  }

  @restartableTask
  *getIdentities() {
    const idpIds = [
      ...this.readyWorkItemsQuery.value,
      ...this.completedWorkItemsQuery.value,
    ]
      .reduce(
        (idpIds, workItem) => [
          ...idpIds,
          ...workItem.assignedUsers,
          workItem.raw.closedByUser,
          workItem.raw.case.createdByUser,
        ],
        []
      )
      .compact()
      .uniq();

    if (idpIds.length) {
      return yield this.store.query("identity", {
        filter: { idpIds: idpIds.join(",") },
      });
    }
  }
}
