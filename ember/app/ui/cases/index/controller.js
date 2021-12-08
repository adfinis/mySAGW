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
  @service intl;

  @tracked order = ENV.APP.casesTable.defaultOrder;
  @tracked cases = [];
  @tracked types = [];
  @tracked documentNumber = null;

  orderOptions = ENV.APP.casesTable.orderOptions;

  @calumaQuery({ query: allCases, options: "options" })
  caseQuery;

  get options() {
    return {
      pageSize: 20,
    };
  }

  get showEmpty() {
    return !this.caseQuery.value.length && this.documentNumber === null;
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
                value: this.documentNumber ?? "",
                lookup: "ICONTAINS",
              },
            ],
          },
          { status: "CANCELED", invert: true },
        ],
      });
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
