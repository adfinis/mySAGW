import Controller from "@ember/controller";
import { action } from "@ember/object";
import { debounce } from "@ember/runloop";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import calumaQuery from "@projectcaluma/ember-core/caluma-query";
import { allCases } from "@projectcaluma/ember-core/caluma-query/queries";
import { restartableTask } from "ember-concurrency-decorators";

import ENV from "mysagw/config/environment";

export default class CasesIndexController extends Controller {
  queryParams = ["order", "documentNumber"];

  @service store;
  @service notification;

  @tracked order = ENV.APP.casesTable.defaultOrder;
  @tracked cases = [];
  @tracked types = [];
  @tracked documentNumber = "";

  orderOptions = ENV.APP.casesTable.orderOptions;

  @calumaQuery({ query: allCases, options: "options" })
  caseQuery;

  get options() {
    return {
      pageSize: 20,
    };
  }

  get hasFilter() {
    return this.documentNumber;
  }

  @restartableTask
  *fetchCases() {
    try {
      yield this.caseQuery.fetch({
        filter: [
          { workflow: "circulation", invert: true },
          { orderBy: [this.order] },
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
      });

      if (this.caseQuery.value.mapBy("createdByUser").length) {
        yield this.store.query("identity", {
          filter: {
            idpIds: this.caseQuery.value.mapBy("createdByUser").join(","),
          },
        });
      }
    } catch (e) {
      // eslint-disable-next-line no-console
      console.error(e);
      this.notification.danger(this.intl.t("documents.fetchError"));
    }
  }

  @action
  updateOrder(event) {
    this.order = event.target.value;

    this.fetchCases.perform();
  }

  @action
  updateFilter(type, event) {
    this[type] = event.target.value;

    debounce({}, this.fetchCases.perform, 300);
  }
}
