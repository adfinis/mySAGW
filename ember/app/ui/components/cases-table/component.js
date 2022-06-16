import { action } from "@ember/object";
import Component from "@glimmer/component";

export default class CasesTableComponent extends Component {
  dynamicTableConfig = {
    columns: [
      {
        heading: {
          label: "documents.number",
        },
        linkTo: "cases.detail.index",
        firstItem: true,
        questionSlug: "dossier-nr",
        answerKey: "document.answers.edges",
        type: "answer-value",
      },
      {
        heading: {
          label: "documents.type",
          sortKey: "DOCUMENT__FORM__NAME",
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
        heading: {
          label: "documents.distributionPlan",
          sortKey: "verteilplan-nr",
        },
        questionSlug: "verteilplan-nr",
        answerKey: "document.answers.edges",
        type: "answer-value",
      },
      {
        heading: {
          label: "documents.section",
          sortKey: "sektion",
        },
        questionSlug: "sektion",
        answerKey: "document.answers.edges",
        type: "answer-value",
      },
      {
        heading: { label: "documents.society", sortKey: "fachgesellschaft" },
        questionSlug: "fachgesellschaft",
        answerKey: "document.answers.edges",
        type: "answer-value",
      },
      {
        heading: { label: "documents.createdAt", sortKey: "CREATED_AT" },
        modelKey: "createdAt",
        type: "date",
      },
      {
        heading: { label: "documents.modifiedAt", sortKey: "MODIFIED_AT" },
        modelKey: "modifiedAt",
        type: "date",
      },
    ],
  };

  get data() {
    return this.args.dataOverride ?? this.args.query.value;
  }

  @action
  fetchMoreCases() {
    this.args.query.fetchMore();
  }
}
