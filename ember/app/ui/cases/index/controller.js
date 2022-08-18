import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { useCalumaQuery } from "@projectcaluma/ember-core/caluma-query";
import { allCases } from "@projectcaluma/ember-core/caluma-query/queries";
import { lastValue, restartableTask, timeout } from "ember-concurrency";

export default class CasesIndexController extends Controller {
  queryParams = ["order", "documentNumber", "selectedIdentities"];

  @service store;
  @service notification;
  @service intl;

  @tracked order = { attribute: "CREATED_AT", direction: "DESC" };
  @tracked types = [];
  @tracked documentNumber = "";
  @tracked identitySearch = "";
  @tracked selectedIdentities = [];

  caseQuery = useCalumaQuery(this, allCases, () => ({
    options: {
      pageSize: 20,
    },
    filter: [
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
    ],
    order: [this.order],
  }));

  get showEmpty() {
    return (
      !this.caseQuery.value.length &&
      this.documentNumber === null &&
      !this.caseQuery.isLoading
    );
  }

  get cases() {
    if (this.selectedIdentities.length) {
      const caseIds = this.caseAccesses?.mapBy("caseId") ?? [];
      return this.caseQuery.value.filter(({ id }) => caseIds.includes(id));
    }

    return this.caseQuery.value;
  }

  get selectedOptions() {
    return this.identities?.filter((i) =>
      this.selectedIdentities.includes(i.idpId)
    );
  }

  @lastValue("fetchIdentities") identities;
  @restartableTask
  *fetchIdentities() {
    yield timeout(400);

    try {
      const identities = yield this.store.query(
        "identity",
        {
          filter: {
            search: this.identitySearch,
            isOrganisation: false,
            has_idp_id: true,
          },
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
        const caseIds = this.caseQuery.value.mapBy("id").join(",");
        const idpIds = this.selectedIdentities.join(",");

        return yield this.store.query("case-access", {
          filter: { caseIds, idpIds },
        });
      }
    } catch (error) {
      console.error(error);
      this.notification.fromError(error);
    }
  }

  @restartableTask
  *updateFilter(type, eventOrValue) {
    yield timeout(2000);

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
