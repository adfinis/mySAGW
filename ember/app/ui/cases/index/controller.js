import { inject as service } from "@ember/service";
import { useCalumaQuery } from "@projectcaluma/ember-core/caluma-query";
import { allCases } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import { trackedFunction } from "ember-resources/util/function";

import ENV from "mysagw/config/environment";
import casesCountQuery from "mysagw/gql/queries/cases-count.graphql";
import { arrayFromString, serializeOrder } from "mysagw/utils/query-params";
import TableController from "mysagw/utils/table-controller";

export default class CasesIndexController extends TableController {
  @service store;
  @service notification;
  @service intl;
  @service filteredForms;

  @queryManager apollo;

  caseQuery = useCalumaQuery(this, allCases, () => ({
    options: { pageSize: 20 },
    filter: this.caseFilters.value,
    order: [serializeOrder(this.order, "documentAnswer")],
  }));

  showEmpty = trackedFunction(this, async () => {
    return (
      this.apollo.query({ query: casesCountQuery }, "allCases.totalCount") === 0
    );
  });

  caseFilters = trackedFunction(this, async () => {
    // This is necessary to trigger a re-run if identities changed and an answer
    // search is given. If an answer search is given, we await the fetching of
    // the filtered forms which uses `await Promise.resolve()` to avoid an
    // infinite loop. However, all tracked properties used after that await
    // statement won't trigger a re-run if changed.
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

    await Promise.resolve();

    try {
      const accesses = (
        await this.store.query("case-access", {
          filter: { idpIds: idpIds.join(",") },
        })
      ).map((access) => access.get("caseId"));

      // TODO: this needs to be fixed in the backend: empty lists of ids will
      // result in not filtering at all!
      return accesses.length
        ? accesses
        : ["5131f81b-2fca-4b95-9b46-8b9d3997e665"];
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
    }
  }
}
