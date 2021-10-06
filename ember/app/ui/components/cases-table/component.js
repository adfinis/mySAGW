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
  dynamicTableConfig = {
    columns: [
      {
        heading: { label: "documents.number" },
        linkTo: "cases.detail.index",
        firstItem: true,
        questionSlug: "dossier-nr",
        answerKey: "document.answers.edges",
        type: "answer-value",
      },
      {
        heading: {
          label: "documents.type",
        },
        modelKey: "document.form.name",
        linkTo: "cases.detail.index",
      },
      {
        heading: { label: "documents.status" },
        modelKey: "meta.status",
        type: "case-status",
      },
      {
        heading: { label: "documents.createdByUser" },
        modelKey: "createdByUser",
        type: "case-created-by",
      },
      {
        heading: { label: "documents.createdAt" },
        modelKey: "createdAt",
        type: "date",
      },
      {
        heading: { label: "documents.modifiedAt" },
        modelKey: "modifiedAt",
        type: "date",
      },
    ],
  };

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
