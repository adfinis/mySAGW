import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { useCalumaQuery } from "@projectcaluma/ember-core/caluma-query";
import { allCases } from "@projectcaluma/ember-core/caluma-query/queries";
import { lastValue, restartableTask, timeout } from "ember-concurrency";

import { FilteredForms } from "mysagw/utils/filtered-forms";
export default class CasesIndexController extends Controller {
  queryParams = [
    "order",
    "documentNumber",
    "selectedIdentities",
    "answerSearch",
  ];

  @service store;
  @service notification;
  @service intl;

  @tracked order = { attribute: "CREATED_AT", direction: "DESC" };
  @tracked types = [];
  @tracked documentNumber = "";
  @tracked identitySearch = "";
  @tracked selectedIdentities = [];
  @tracked answerSearch = "";

  caseQuery = useCalumaQuery(this, allCases, () => ({
    options: {
      pageSize: 20,
    },
    filter: this.caseFilters,
    order: [this.order],
  }));

  filteredForms = FilteredForms.from(this);

  get showEmpty() {
    return (
      !this.caseQuery.value.length &&
      this.documentNumber === null &&
      !this.caseQuery.isLoading
    );
  }

  get selectedOptions() {
    return this.identities?.filter((i) =>
      this.selectedIdentities.includes(i.idpId)
    );
  }

  get caseFilters() {
    const filters = [
      { workflow: "circulation", invert: true },
      {
        hasAnswer: [
          {
            question: "dossier-nr",
            value: this.documentNumber,
            lookup: "ICONTAINS",
          },
        ],
      },
      { status: "CANCELED", invert: true },
      { ids: this.caseAccesses?.mapBy("caseId") ?? [] },
    ];

    if (this.filteredForms.value.length) {
      filters.push({
        searchAnswers: [
          {
            forms: this.filteredForms.value.mapBy("node.slug"),
            value: this.answerSearch,
          },
        ],
      });
    }

    return filters;
  }

  @lastValue("fetchIdentities") identities;
  @restartableTask
  *fetchIdentities(initial = false) {
    yield timeout(500);

    try {
      const filter = {
        search: this.identitySearch,
        isOrganisation: false,
        has_idp_id: true,
      };

      if (initial && this.selectedIdentities.length) {
        filter.idpIds = this.selectedIdentities.join(",");
      }

      const identities = yield this.store.query(
        "identity",
        {
          filter,
          page: {
            number: 1,
            size: 20,
          },
        },
        { adapterOptions: { customEndpoint: "public-identities" } }
      );

      return identities;
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
    }
  }

  @lastValue("fetchCaseAccesses") caseAccesses;
  @restartableTask
  *fetchCaseAccesses() {
    try {
      if (this.selectedIdentities.length) {
        return yield this.store.query("case-access", {
          filter: { idpIds: this.selectedIdentities.join(",") },
        });
      }
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
    }
  }

  @restartableTask
  *updateFilter(type, eventOrValue) {
    yield timeout(500);
    /*
     * Set filter from type argument, if eventOrValue is a event it is from an input field
     * if its selectedIdentites an array is to be expected
     */
    if (type === "selectedIdentities") {
      this[type] = eventOrValue.filterBy("idpId").mapBy("idpId");
    } else {
      this[type] = eventOrValue.target.value;
    }

    this.fetchCaseAccesses.perform();
  }

  @action
  updateIdentitySearch(value) {
    this.identitySearch = value;

    this.fetchIdentities.perform();
  }

  @action
  setOrder(order) {
    this.order = order;
  }
}
