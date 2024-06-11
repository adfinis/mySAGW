import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { useCalumaQuery } from "@projectcaluma/ember-core/caluma-query";
import { allCases } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import { trackedFunction } from "reactiveweb/function";

import ENV from "mysagw/config/environment";
import casesCountQuery from "mysagw/gql/queries/cases-count.graphql";
import { arrayFromString, serializeOrder } from "mysagw/utils/query-params";
import TableController from "mysagw/utils/table-controller";

export default class CasesIndexController extends TableController {
  @service store;
  @service notification;

  @queryManager apollo;

  @tracked editMode = false;
  @tracked selectedCases = [];
  @tracked refreshList = 0;
  @tracked pageSize = 1;

  caseQuery = useCalumaQuery(this, allCases, () => ({
    options: { pageSize: this.pageSize },
    filter: this.caseFilters.value,
    order: [serializeOrder(this.order, "documentAnswer")],
  }));

  showEmpty = trackedFunction(this, async () => {
    return (
      this.apollo.query({ query: casesCountQuery }, "allCases.totalCount") === 0
    );
  });

  caseFilters = trackedFunction(this, async () => {
    // needed to trigger a re-fetch after editing (e.g. transfer)
    this.refreshList;

    this.selectedCases = [];

    // access to attributes must happen before await, otherwise no reactivity
    const { identities } = this.filters;
    const { identities: invertedIdentites } = this.invertedFilters;

    const filters = [
      { workflow: "circulation", invert: true },
      { status: "CANCELED", invert: true },
    ];

    if (this.filters.documentNumber) {
      filters.push({
        hasAnswer: [
          {
            question: "dossier-nr",
            value: this.filters.documentNumber,
            lookup: "ICONTAINS",
          },
        ],
        invert: Boolean(this.invertedFilters.documentNumber),
      });
    }

    if (this.filters.answerSearch) {
      filters.push({
        searchAnswers: [
          {
            forms: this.forms,
            value: this.filters.answerSearch,
          },
        ],
        invert: Boolean(this.invertedFilters.answerSearch),
      });
    }

    if (this.filters.forms) {
      filters.push({
        documentForms: arrayFromString(this.filters.forms),
        invert: Boolean(this.invertedFilters.forms),
      });
    }

    Object.keys(ENV.APP.caluma.filterableQuestions).forEach((question) => {
      if (!this.filters[question]) {
        return;
      }
      filters.push({
        hasAnswer: [
          {
            question: ENV.APP.caluma.filterableQuestions[question],
            lookup: "IN",
            value: arrayFromString(this.filters[question]),
          },
        ],
        invert: Boolean(this.invertedFilters[question]),
      });
    });

    if (identities) {
      filters.push({
        ids: await this.fetchAccesses(arrayFromString(identities)),
        invert: Boolean(invertedIdentites),
      });
    }

    return filters;
  });

  async fetchAccesses(idpIds) {
    if (!idpIds) {
      return [];
    }

    try {
      const accesses = (
        await this.store.query("case-access", {
          filter: { idpIds: idpIds.join(",") },
        })
      ).map((access) => access.get("caseId"));

      // filtering against an empty list is treated as a no-op, therefore return a dummy value
      return accesses.length
        ? accesses
        : ["00000000-0000-0000-0000-000000000000"];
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
    }
  }

  @action
  selectCase(value) {
    if (this.selectedCases.includes(value.id)) {
      this.selectedCases = this.selectedCases.filter((id) => id !== value.id);
      return;
    }

    this.selectedCases = [...this.selectedCases, value.id];
  }

  @action
  async selectAll() {
    if (this.caseQuery.totalCount === this.selectedCases.length) {
      this.selectedCases = [];
      return;
    }

    // fetch all cases and select them
    let modified = false;
    if (this.caseQuery.hasNextPage) {
      this.pageSize = 0;
      modified = true;
      await this.caseQuery.query._fetchPage.last;
    }


    this.selectedCases = this.caseQuery.value.map((c) => c.id);

    if (modified) {
      this.pageSize = 1;
    }
  }

  get accessToRemove() {
    return arrayFromString(this.filters.identities);
  }

  @action
  afterTransfer() {
    this.editMode = false;
    this.refreshList++;
  }
}
