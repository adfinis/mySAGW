import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import calumaQuery from "@projectcaluma/ember-core/caluma-query";
import { allCases } from "@projectcaluma/ember-core/caluma-query/queries";
import { lastValue, restartableTask, timeout } from "ember-concurrency";

import ENV from "mysagw/config/environment";

export default class CasesIndexController extends Controller {
  queryParams = ["order", "documentNumber", "selectedIdentities"];

  @service store;
  @service notification;
  @service intl;

  @tracked orderAttr = ENV.APP.casesTable.defaultOrder.split("-")[0];
  @tracked orderDirection = ENV.APP.casesTable.defaultOrder.split("-")[1];
  @tracked documentNumber = null;
  @tracked identitySearch = "";
  @tracked selectedIdentities = [];

  orderOptions = ENV.APP.casesTable.orderOptions;

  @calumaQuery({ query: allCases, options: "options" })
  caseQuery;

  get options() {
    return {
      pageSize: 20,
    };
  }

  get showEmpty() {
    return (
      !this.caseQuery.value.length &&
      this.documentNumber === null &&
      !this.fetchCases.isRunning
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

  @restartableTask
  *fetchCases() {
    yield timeout(1000);

    try {
      yield this.caseQuery.fetch({
        filter: [
          { workflow: "circulation", invert: true },
          {
            hasAnswer: [
              {
                question: "dossier-nr",
                value: this.documentNumber ?? "",
                lookup: "ICONTAINS",
              },
            ],
          },
          { status: "CANCELED", invert: true },
        ],
        order: [{ attribute: this.orderAttr, direction: this.orderDirection }],
      });

      yield this.fetchCaseAccesses.perform();
    } catch (e) {
      // eslint-disable-next-line no-console
      console.error(e);
      this.notification.danger(this.intl.t("documents.fetchError"));
    }
  }

  @lastValue("fetchIdentities") identities;
  @restartableTask
  *fetchIdentities() {
    yield timeout(1000);

    try {
      const identities = yield this.store.query(
        "identity",
        {
          filter: {
            search: this.identitySearch,
            isOrganisation: false,
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

  @action
  updateOrder(event) {
    this.orderAttr = event.target.value.split("-")[0];
    this.orderDirection = event.target.value.split("-")[1];

    this.fetchCases.perform();
  }

  @action
  updateFilter(type, eventOrValue) {
    /*
     * Set filter from type argument, if eventOrValue is a event it is from an input field
     * if its selectedIdentites an array is to be expected
     */
    if (eventOrValue.target) {
      this[type] = eventOrValue.target.value;
    } else if (type === "selectedIdentities") {
      this[type] = eventOrValue.filterBy("idpId").mapBy("idpId");
    }

    this.fetchCases.perform();
  }

  @action
  updateIdentitySearch(value) {
    this.identitySearch = value;

    this.fetchIdentities.perform();
  }
}
