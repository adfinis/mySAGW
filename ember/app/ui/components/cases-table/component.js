import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import calumaQuery from "ember-caluma/caluma-query";
import { allCases } from "ember-caluma/caluma-query/queries";
import { restartableTask } from "ember-concurrency-decorators";

import ENV from "mysagw/config/environment";

export default class CasesTableComponent extends Component {
  @service store;

  @tracked cases = [];
  @tracked types = [];

  orderOptions = ENV.APP.casesTable.orderOptions;
  dynamicTableConfig = ENV.APP.dynamicTable;

  @calumaQuery({ query: allCases, options: "options" })
  caseQuery;

  get options() {
    return {
      pageSize: 20,
    };
  }

  @restartableTask
  *fetchCases() {
    try {
      yield this.caseQuery.fetch({
        filter: [
          { workflow: "circulation", invert: true },
          { orderBy: [this.args.order || ENV.APP.casesTable.defaultOrder] },
        ],
      });

      yield this.store.query("identity", {
        filter: {
          idpIds: this.caseQuery.value.mapBy("createdByUser").join(","),
        },
      });
    } catch (e) {
      // eslint-disable-next-line no-console
      console.error(e);
    }
  }

  @action
  fetchMoreCases() {
    this.caseQuery.fetchMore();
  }
}
