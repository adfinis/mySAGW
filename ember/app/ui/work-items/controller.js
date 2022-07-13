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
    "answer",
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
      processNew: this.processNew,
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
        ...(this.status === "open"
          ? [
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
          heading: { label: "work-items.distributionPlan" },
          questionSlug: "verteilplan-nr",
          answerKey: "case.document.answers.edges",
          type: "answer-value",
        },
        {
          heading: { label: "documents.section" },
          questionSlug: "sektion",
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
      { metaHasKey: "hidden", invert: true },
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

    yield this.workItemsQuery.fetch({
      filter,
      order: [{ attribute: "CREATED_AT", direction: "DESC" }],
    });
    yield this.getIdentities.perform(this.workItemsQuery.value);
  }

  @restartableTask
  *getIdentities(workItems) {
    const idpIds = workItems
      .reduce(
        (idpIds, workItem) => [
          ...idpIds,
          ...workItem.assignedUsers,
          workItem.closedByUser,
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

  @restartableTask
  *fetchTasks() {
    return (yield this.apollo.query(
      {
        query: getTasksQuery,
        variables: {
          filter: [{ isArchived: false }],
          order: [{ attribute: "NAME" }],
        },
      },
      "allTasks.edges"
    )).map((task) => {
      return { value: task.node.slug, label: task.node.name };
    });
  }

  @action
  processNew(workItems) {
    this.getIdentities.perform(workItems);
    return workItems;
  }

  @action
  updateFilter(type, eventValue) {
    this[type] = eventValue.target ? eventValue.target.value : eventValue;

    debounce({}, this.fetchWorkItems.perform, 300);
  }
}
