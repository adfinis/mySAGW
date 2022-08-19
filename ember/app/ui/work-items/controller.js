import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { useCalumaQuery } from "@projectcaluma/ember-core/caluma-query";
import { allWorkItems } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import { restartableTask, timeout } from "ember-concurrency";

import getTasksQuery from "mysagw/gql/queries/get-tasks.graphql";
import { FilteredForms } from "mysagw/utils/filtered-forms";

export default class WorkItemsIndexController extends Controller {
  queryParams = [
    "order",
    "status",
    "role",
    "taskTypes",
    "documentNumber",
    "selectedIdentities",
    "answerSearch",
  ];

  @service session;
  @service store;

  @queryManager apollo;

  // Filters
  @tracked order = { attribute: "CREATED_AT", direction: "DESC" };
  @tracked status = "open";
  @tracked role = "active";
  @tracked taskTypes = [];
  @tracked documentNumber = "";
  @tracked selectedIdentities = [];
  @tracked answerSearch = "";

  workItemsQuery = useCalumaQuery(this, allWorkItems, () => ({
    options: {
      pageSize: 20,
      processNew: this.processNew,
    },
    filter: this.workItemsFilter,
    order: [this.order],
  }));

  filteredForms = FilteredForms.from(this);

  get workItemsFilter() {
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
      {
        assignedUsers: this.selectedIdentities,
      },
    ];

    if (this.status === "closed") {
      filter.push({ status: "COMPLETED" });
    } else {
      filter.push({ status: "READY" });
    }
    if (this.role === "control") {
      filter.push({ controllingGroups: ["sagw"] });
    }
    if (this.filteredForms.value.length) {
      filter.push({
        caseSearchAnswers: [
          {
            forms: this.filteredForms.value.mapBy("node.slug"),
            value: this.answerSearch,
          },
        ],
      });
    }

    return filter;
  }

  @restartableTask
  *getWorkItemIdentities(workItems) {
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
          page: {
            number: 1,
            size: 20,
          },
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
    this.getWorkItemIdentities.perform(workItems);
    return workItems;
  }

  @restartableTask
  *updateFilter(type, eventOrValue) {
    yield timeout(500);
    /*
     * Set filter from type argument, if eventOrValue is a event it is from an input field
     * if its selectedIdentites an array of identities is to be expected
     */
    if (type === "selectedIdentities") {
      this[type] = eventOrValue.filterBy("idpId").mapBy("idpId");
    } else if (eventOrValue.target) {
      this[type] = eventOrValue.target.value;
    } else {
      this[type] = eventOrValue;
    }
  }

  @action
  setOrder(order) {
    this.order = order;
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
          heading: {
            label: "work-items.case",
            sortKey: "CASE__DOCUMENT__FORM__NAME",
          },
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
                heading: {
                  label: "work-items.closedAt",
                  sortKey: "CLOSED_AT",
                },
                modelKey: "closedAt",
                type: "date",
              },
              {
                heading: { label: "work-items.closedBy" },
                modelKey: "closedByUser.fullName",
              },
            ]),
        {
          heading: {
            label: "work-items.distributionPlan",
            sortKey: "verteilplan-nr",
          },
          questionSlug: "verteilplan-nr",
          answerKey: "case.document.answers.edges",
          type: "answer-value",
        },
        {
          heading: { label: "documents.section", sortKey: "sektion" },
          questionSlug: "sektion",
          answerKey: "case.document.answers.edges",
          type: "answer-value",
        },
        {
          heading: {
            label: "documents.society",
            sortKey: "mitgliedinstitution",
          },
          questionSlug: "mitgliedinstitution",
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
}
