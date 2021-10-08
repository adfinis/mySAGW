import Controller from "@ember/controller";
import { action } from "@ember/object";
import { debounce } from "@ember/runloop";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import calumaQuery from "@projectcaluma/ember-core/caluma-query";
import { allWorkItems } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import { restartableTask } from "ember-concurrency";

import getTasksQuery from "mysagw/gql/queries/get-tasks.graphql";

export default class WorkItemsIndexController extends Controller {
  queryParams = [
    "order",
    "responsible",
    "status",
    "role",
    "taskTypes",
    "documentNumber",
  ];

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
  @tracked taskTypes = [];
  @tracked documentNumber = "";

  get options() {
    return {
      pageSize: 20,
    };
  }

  get tableConfig() {
    return {
      columns: [
        {
          heading: { label: "work-items.task" },
          type: "task-name",
        },
        {
          heading: { label: "work-items.documentNumber" },
          linkTo: "cases.detail.index",
          linkToModelField: "case.id",
          questionSlug: "dossier-nr",
          answerKey: "case.document.answers.edges",
          type: "answer-value",
        },
        {
          heading: { label: "work-items.case" },
          modelKey: "case.document.form.name",
          linkTo: "cases.detail.index",
          linkToModelField: "case.id",
        },
        {
          heading: { label: "work-items.caseCreatedBy" },
          modelKey: "case.createdByUser",
          type: "case-created-by",
        },
        ...(this.status === "open"
          ? [
              {
                heading: { label: "work-items.deadline" },
                modelKey: "deadline",
                type: "deadline",
              },
              {
                heading: { label: "work-items.responsible" },
                modelKey: "responsible",
              },
            ]
          : [
              {
                heading: { label: "work-items.closedAt" },
                modelKey: "closedAt",
                type: "date",
              },
              {
                heading: { label: "work-items.closedBy" },
                modelKey: "closedByUser.fullName",
              },
            ]),
        {
          heading: { label: "documents.section" },
          questionSlug: "section",
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

  @restartableTask
  *fetchWorkItems() {
    const filter = [
      { hasDeadline: true },
      { tasks: this.taskTypes.mapBy("value") },
      {
        caseDocumentHasAnswer: [
          {
            question: "dossier-nr",
            value: this.documentNumber,
            lookup: "ICONTAINS",
          },
        ],
      },
    ];

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
    const idpIds = this.workItemsQuery.value
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

  @restartableTask
  *fetchTasks() {
    return (yield this.apollo.query(
      {
        query: getTasksQuery,
        variables: {
          filter: [{ isArchived: false }, { orderBy: ["NAME_ASC"] }],
        },
      },
      "allTasks.edges"
    )).map((task) => {
      return { value: task.node.slug, label: task.node.name };
    });
  }

  @action
  updateFilter(type, eventValue) {
    this[type] = eventValue.target ? eventValue.target.value : eventValue;

    debounce({}, this.fetchWorkItems.perform, 300);
  }
}
