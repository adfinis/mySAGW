import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import calumaQuery from "@projectcaluma/ember-core/caluma-query";
import { allWorkItems } from "@projectcaluma/ember-core/caluma-query/queries";
import { restartableTask } from "ember-concurrency";

import ENV from "mysagw/config/environment";

export default class CasesDetailWorkItemsController extends Controller {
  @service store;
  @service can;

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
          heading: { label: "work-items.responsible" },
          modelKey: "responsible",
        },
        {
          heading: { label: "work-items.distributionPlan" },
          questionSlug: "verteilplan-nr",
          answerKey: "case.document.answers.edges",
          type: "answer-value",
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
    const filter = [
      { metaHasKey: "hidden", invert: true },
      { case: this.model.id },
    ];

    if (this.can.cannot("show all work-item")) {
      filter.push({ tasks: ENV.APP.caluma.documentEditableTaskSlugs });
    }

    yield Promise.all([
      this.readyWorkItemsQuery.fetch({
        filter: [...filter, { status: "READY" }],
        order: [{ attribute: "CREATED_AT", direction: "DESC" }],
      }),
      this.completedWorkItemsQuery.fetch({
        filter: [
          ...filter,
          { status: "READY", invert: true },
          { status: "REDO", invert: true },
        ],
        order: [{ attribute: "CLOSED_AT", direction: "DESC" }],
      }),
    ]);

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
      return yield this.store.query(
        "identity",
        {
          filter: { idpIds: idpIds.join(",") },
        },
        { adapterOptions: { customEndpoint: "public-identities" } }
      );
    }
  }
}
