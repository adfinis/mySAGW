import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { useCalumaQuery } from "@projectcaluma/ember-core/caluma-query";
import { allCases } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import { restartableTask, timeout } from "ember-concurrency";
import { trackedFunction } from "ember-resources/util/function";
import { dedupeTracked } from "tracked-toolbox";

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

  @dedupeTracked order = "-CREATED_AT";
  @dedupeTracked documentNumber = "";
  @dedupeTracked identities = "";
  @dedupeTracked answerSearch = "";

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

  get selectedIdentities() {
    return arrayFromString(this.identities);
  }

  caseFilters = trackedFunction(this, async () => {
    // This is necessary to trigger a re-run if identities changed and an answer
    // search is given. If an answer search is given, we await the fetching of
    // the filtered forms which uses `await Promise.resolve()` to avoid an
    // infinite loop. However, all tracked properties used after that await
    // statement won't trigger a re-run if changed.
    const { documentNumber, answerSearch, identities } = this;

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
    /*
     * Set filter from type argument, if eventOrValue is a event it is from an input field
     * if its identities an array is to be expected
     */
    if (type === "identities") {
      this[type] = stringFromArray(eventOrValue, "idpId");
    } else {
      yield timeout(500);
      this[type] = eventOrValue.target.value;
    }
  }
}
