import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { useCalumaQuery } from "@projectcaluma/ember-core/caluma-query";
import { allWorkItems } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import { restartableTask, timeout } from "ember-concurrency";
import { trackedFunction } from "ember-resources/util/function";
import { dedupeTracked } from "tracked-toolbox";

import getTasksQuery from "mysagw/gql/queries/get-tasks.graphql";
import {
  arrayFromString,
  stringFromArray,
  serializeOrder,
} from "mysagw/utils/query-params";

export default class WorkItemsIndexController extends Controller {
  queryParams = [
    "order",
    "status",
    "role",
    "taskTypes",
    "documentNumber",
    "identities",
    "answerSearch",
    "responsible",
  ];

  @service session;
  @service store;
  @service filteredForms;

  @queryManager apollo;

  // Filters
  @dedupeTracked order = "-CREATED_AT";
  @dedupeTracked status = "open";
  @dedupeTracked role = "active";
  @dedupeTracked taskTypes = "";
  @dedupeTracked documentNumber = "";
  @dedupeTracked identities = "";
  @dedupeTracked answerSearch = "";
  @dedupeTracked responsible = "all";

  workItemsQuery = useCalumaQuery(this, allWorkItems, () => ({
    options: {
      pageSize: 20,
      processNew: this.processNew,
    },
    filter: this.workItemsFilter.value,
    order: [serializeOrder(this.order, "caseDocumentAnswer")],
  }));

  get selectedTaskTypes() {
    const taskTypes = arrayFromString(this.taskTypes);

    return (
      this.allTaskTypes.value?.filter((taskType) =>
        taskTypes.includes(taskType.value)
      ) ?? []
    );
  }

  get selectedIdentities() {
    return arrayFromString(this.identities);
  }

  workItemsFilter = trackedFunction(this, async () => {
    const filter = [
      { metaHasKey: "hidden", invert: true },
      { status: this.status === "closed" ? "COMPLETED" : "READY" },
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

    if (this.taskTypes) {
      filter.push({ tasks: arrayFromString(this.taskTypes) });
    }

    if (this.identities) {
      filter.push({ assignedUsers: arrayFromString(this.identities) });
    }

    if (this.responsible === "own") {
      filter.push({
        assignedUsers: [this.session.data.authenticated.userinfo.sub],
      });
    }

    if (this.answerSearch) {
      filter.push({
        caseSearchAnswers: [
          {
            forms: await this.filteredForms.mainFormSlugs(),
            value: this.answerSearch,
          },
        ],
      });
    }

    return filter;
  });

  allTaskTypes = trackedFunction(this, async () => {
    const response = await this.apollo.query(
      {
        query: getTasksQuery,
        variables: {
          filter: [{ isArchived: false }],
          order: [{ attribute: "NAME" }],
        },
      },
      "allTasks.edges"
    );

    return response.map((edge) => ({
      value: edge.node.slug,
      label: edge.node.name,
    }));
  });

  @action
  async processNew(workItems) {
    const idpIds = [
      ...new Set(
        workItems
          .flatMap((workItem) => [
            ...workItem.assignedUsers,
            workItem.closedByUser,
          ])
          .filter(Boolean)
      ),
    ];

    const cachedIdpIds = this.store
      .peekAll("identity")
      .map((identity) => identity.get("idpId"));

    const uncachedIdpIds = idpIds.filter(
      (idpId) => cachedIdpIds.indexOf(idpId) === -1
    );

    if (uncachedIdpIds.length) {
      await this.store.query(
        "identity",
        { filter: { idpIds: uncachedIdpIds.join(",") } },
        { adapterOptions: { customEndpoint: "public-identities" } }
      );
    }

    return workItems;
  }

  @restartableTask
  *updateFilter(type, eventOrValue) {
    if (["documentNumber", "answerSearch"].includes(type)) {
      // debounce only input filters by 500ms to prevent too many requests when
      // typing into a search field
      yield timeout(500);
    }

    // Update the filter with the passed value. This can either be an array of
    // objects (task types or identities), and event or a plain value
    if (type === "identities") {
      this[type] = stringFromArray(eventOrValue, "idpId");
    } else if (type === "taskTypes") {
      this[type] = stringFromArray(eventOrValue, "value");
    } else {
      this[type] = eventOrValue.target?.value ?? eventOrValue;
    }
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
