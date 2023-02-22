import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { useCalumaQuery } from "@projectcaluma/ember-core/caluma-query";
import { allCases } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import { restartableTask, timeout } from "ember-concurrency";
import { trackedFunction } from "ember-resources/util/function";
import { TrackedObject } from "tracked-built-ins";
import { dedupeTracked } from "tracked-toolbox";

import ENV from "mysagw/config/environment";
import casesCountQuery from "mysagw/gql/queries/cases-count.graphql";
import {
  arrayFromString,
  stringFromArray,
  serializeOrder,
} from "mysagw/utils/query-params";

export default class CasesIndexController extends Controller {
  queryParams = ["order", "documentNumber", "identities", "answerSearch"];

  @service store;
  @service notification;
  @service intl;
  @service filteredForms;

  @queryManager apollo;

  // Filters
  _filters = {
    documentNumber: "",
    identities: "",
    answerSearch: "",
    forms: "",
    expertAssociations: "",
    distributionPlan: "",
    sections: "",
  };
  @dedupeTracked filters = new TrackedObject(this._filters);
  @dedupeTracked order = "-CREATED_AT";

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
    const { documentNumber, answerSearch, identities, forms } = this.filters;

    const filters = [
      { workflow: "circulation", invert: true },
      { status: "CANCELED", invert: true },
      {
        hasAnswer: [
          {
            question: "dossier-nr",
            value: documentNumber,
            lookup: "ICONTAINS",
          },
        ],
      },
    ];

    if (answerSearch) {
      filters.push({
        searchAnswers: [
          {
            forms: await this.filteredForms.mainFormSlugs(),
            value: answerSearch,
          },
        ],
      });
    }

    if (forms) {
      // TODO cant filter for case form
      // filter.push({ documentForms: arrayFromString(forms) });
    }

    Object.keys(ENV.APP.caluma.filterableQuestions).forEach((question) => {
      if (!this.filters[question]) {
        return;
      }
      filter.push({
        hasAnswer: [
          {
            question: ENV.APP.caluma.filterableQuestions[question],
            value: this.filters[question],
          },
        ],
      });
    });

    if (identities) {
      filters.push({
        ids: await this.fetchAccesses(arrayFromString(identities)),
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
}
