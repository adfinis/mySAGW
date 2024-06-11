import { action } from "@ember/object";
import Component from "@glimmer/component";

export default class CasesTableComponent extends Component {
  get dynamicTableConfig() {
    const columns = [
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
        heading: {
          label: "documents.society",
          sortKey: "mitgliedinstitution",
        },
        questionSlug: "mitgliedinstitution",
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
    ];

    if (this.args.editMode) {
      columns.unshift({
        heading: { label: "documents.bulkEdit.action", hidden: true },
        type: "checkbox",
        selectRow: this.args.selectRow,
        selectAll: this.args.selectAll,
        selected: this.args.selectedCases,
        total: this.args.query.totalCount,
      });
    }

    return { columns };
  }

  @action
  fetchMoreCases() {
    this.args.query.fetchMore();
  }
}
