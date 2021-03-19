import { action } from "@ember/object";
import { reads } from "@ember/object/computed";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { restartableTask } from "ember-concurrency-decorators";
import ENV from "mysagw/config/environment";
import getCasesQuery from "mysagw/gql/queries/get-cases.graphql";

export default class CasesTableComponent extends Component {
  @queryManager apollo;

  @tracked cases = [];
  @tracked types = [];
  @tracked order;

  @reads("fetchCases.lastSuccessful.value.pageInfo") pageInfo;

  orderOptions = ENV.APP.casesTable.orderOptions;
  dynamicTableConfig = ENV.APP.dynamicTable;

  get noCases() {
    return (
      this.fetchCases.lastSuccessful &&
      !this.fetchCases.isRunning &&
      !this.cases.length
    );
  }

  constructor(...args) {
    super(...args);
    this.order = this.args.order || ENV.APP.casesTable.defaultOrder;
  }

  @action
  setup() {
    this.cases = [];
    this.fetchCases.perform();
  }

  @restartableTask
  *fetchCases(cursor = null) {
    try {
      const raw = yield this.apollo.query(
        {
          query: getCasesQuery,
          variables: {
            cursor,
            orderBy: this.order,
          },

          fetchPolicy: "network-only",
        },
        "allCases"
      );
      const cases = raw.edges.mapBy("node");

      this.cases = [...this.cases, ...cases];

      return {
        cases,
        pageInfo: { ...raw.pageInfo, totalCount: raw.totalCount },
      };
    } catch (e) {
      // eslint-disable-next-line no-console
      console.error(e);
    }
  }
}
