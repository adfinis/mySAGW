import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import calumaQuery from "@projectcaluma/ember-core/caluma-query";
import { allWorkItems } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
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
          heading: { label: "work-items.task" },
          type: "task-name",
        },
        {
          heading: { label: "work-items.deadline" },
          modelKey: "deadline",
          type: "deadline",
        },
        {
          heading: { label: "work-items.responsible" },
          modelKey: "responsible",
        },
        {
          heading: { label: "work-items.action" },
          type: "work-item-actions",
        },
      ],
    };
  }
  get completedTableConfig() {
    return {
      columns: [
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
          heading: { label: "work-items.closedBy" },
          modelKey: "closedByUser.fullName",
        },
        {
          heading: { label: "work-items.action" },
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
      filter: [...filter, { status: "READY", invert: true }],
      order: [{ attribute: "CLOSED_AT", direction: "DESC" }],
    });

    yield this.getIdentities.perform();
  }

  @restartableTask
  *getIdentities() {
    const idpIds = [
      ...this.readyWorkItemsQuery?.value,
      ...this.completedWorkItemsQuery?.value,
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
