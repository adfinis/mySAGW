import { action } from "@ember/object";
import Component from "@glimmer/component";

export default class CasesTableComponent extends Component {
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
        heading: { label: "documents.distributionPlan" },
        questionSlug: "verteilplan-nr",
        answerKey: "document.answers.edges",
        type: "answer-value",
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

  @action
  fetchMoreCases() {
    this.args.query.fetchMore();
  }
}
