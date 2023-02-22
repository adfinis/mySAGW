import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { useCalumaQuery } from "@projectcaluma/ember-core/caluma-query";
import { allWorkItems } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import { restartableTask, timeout } from "ember-concurrency";
import { trackedFunction } from "ember-resources/util/function";
import { TrackedObject } from "tracked-built-ins";
import { dedupeTracked } from "tracked-toolbox";

import ENV from "mysagw/config/environment";
import {
  arrayFromString,
  stringFromArray,
  serializeOrder,
} from "mysagw/utils/query-params";

export default class WorkItemsIndexController extends Controller {
  queryParams = [
    "order",
    "status",
    "taskTypes",
    "documentNumber",
    "identities",
    "answerSearch",
    "responsible",
    "filters",
  ];

  @service session;
  @service store;
  @service filteredForms;

  @queryManager apollo;

  // Filters
  _filters = {
    status: "open",
    responsible: "all",
    taskTypes: "",
    documentNumber: "",
    identities: "",
    answerSearch: "",
    forms: "",
    expertAssociations: "",
    distributionPlan: "",
    sections: "",
  };
  @dedupeTracked filters = new TrackedObject(this._filters);
  @dedupeTracked invertedFilters = new TrackedObject(this._filters);
  @dedupeTracked order = "-CREATED_AT";

  workItemsQuery = useCalumaQuery(this, allWorkItems, () => ({
    options: {
      pageSize: 20,
      processNew: this.processNew,
    },
    filter: this.workItemsFilter.value,
    order: [serializeOrder(this.order, "caseDocumentAnswer")],
  }));

  workItemsFilter = trackedFunction(this, async () => {
    const filter = [
      { metaHasKey: "hidden", invert: true },
      { status: this.filters.status === "closed" ? "COMPLETED" : "READY" },
      {
        caseDocumentHasAnswer: [
          {
            question: "dossier-nr",
            value: this.filters.documentNumber,
            lookup: "ICONTAINS",
          },
        ],
      },
    ];

    if (this.filters.taskTypes) {
      filter.push({ tasks: arrayFromString(this.filters.taskTypes) });
    }

    if (this.filters.identities) {
      filter.push({ assignedUsers: arrayFromString(this.filters.identities) });
    }

    if (this.filters.responsible === "own") {
      filter.push({
        assignedUsers: [this.session.data.authenticated.userinfo.sub],
      });
    }

    if (this.filters.answerSearch) {
      filter.push({
        caseSearchAnswers: [
          {
            forms: await this.filteredForms.mainFormSlugs(),
            value: this.filters.answerSearch,
          },
        ],
      });
    }

    if (this.filters.forms) {
      // TODO cant filter for case form
      // filter.push({ caseDocumentForms: arrayFromString(this.filters.forms) });
    }

    Object.keys(ENV.APP.caluma.filterableQuestions).forEach((question) => {
      if (!this.filters[question]) {
        return;
      }
      filter.push({
        caseDocumentHasAnswer: [
          {
            question: ENV.APP.caluma.filterableQuestions[question],
            value: this.filters[question],
          },
        ],
      });
    });

    return filter;
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
    // objects (multiple choice filters), and event or a plain value
    if (Array.isArray(eventOrValue)) {
      this.filters[type] = stringFromArray(
        eventOrValue,
        type === "identities" ? "idpId" : "value"
      );
    } else {
      this.filters[type] = eventOrValue.target?.value ?? eventOrValue;
    }
  }

  @action
  resetFilters() {
    this.filters = new TrackedObject(this._filters);
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
