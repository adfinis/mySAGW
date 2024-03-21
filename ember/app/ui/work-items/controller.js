import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { useCalumaQuery } from "@projectcaluma/ember-core/caluma-query";
import { allWorkItems } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import { trackedFunction } from "ember-resources/util/function";

import ENV from "mysagw/config/environment";
import { arrayFromString, serializeOrder } from "mysagw/utils/query-params";
import TableController from "mysagw/utils/table-controller";

export default class WorkItemsIndexController extends TableController {
  @service session;
  @service store;
  @service can;

  @queryManager apollo;

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
    ];

    if (this.filters.documentNumber) {
      filter.push({
        caseDocumentHasAnswer: [
          {
            question: "dossier-nr",
            value: this.filters.documentNumber,
            lookup: "ICONTAINS",
          },
        ],
        invert: Boolean(this.invertedFilters.documentNumber),
      });
    }

    if (this.filters.taskTypes) {
      filter.push({
        tasks: arrayFromString(this.filters.taskTypes),
        invert: Boolean(this.invertedFilters.taskTypes),
      });
    }

    if (this.filters.identities) {
      filter.push({
        assignedUsers: arrayFromString(this.filters.identities),
        invert: Boolean(this.invertedFilters.identities),
      });
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
            forms: this.forms,
            value: this.filters.answerSearch,
          },
        ],
        invert: Boolean(this.invertedFilters.answerSearch),
      });
    }

    if (this.filters.forms) {
      filter.push({
        caseDocumentForms: arrayFromString(this.filters.forms),
        invert: Boolean(this.invertedFilters.forms),
      });
    }

    Object.keys(ENV.APP.caluma.filterableQuestions).forEach((question) => {
      if (!this.filters[question]) {
        return;
      }
      filter.push({
        caseDocumentHasAnswer: [
          {
            question: ENV.APP.caluma.filterableQuestions[question],
            lookup: "IN",
            value: arrayFromString(this.filters[question]),
          },
        ],
        invert: Boolean(this.invertedFilters[question]),
      });
    });

    if (this.can.cannot("show all workItem")) {
      filter.push({
        task: "circulation-decision",
      });
    }

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
          .filter(Boolean),
      ),
    ];

    const cachedIdpIds = this.store
      .peekAll("identity")
      .map((identity) => identity.get("idpId"));

    const uncachedIdpIds = idpIds.filter(
      (idpId) => cachedIdpIds.indexOf(idpId) === -1,
    );

    if (uncachedIdpIds.length) {
      await this.store.query(
        "identity",
        { filter: { idpIds: uncachedIdpIds.join(",") } },
        { adapterOptions: { customEndpoint: "public-identities" } },
      );
    }

    return workItems;
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
        ...(this.filters.status === "open"
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
