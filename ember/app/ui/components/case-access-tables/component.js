import Component from "@glimmer/component";

export default class CaseAccessTablesComponent extends Component {
  get accessTableConfig() {
    return {
      columns: [
        {
          heading: { label: "documents.accesses.table.name" },
          modelKey: "name",
        },
        {
          heading: { label: "documents.accesses.table.action" },
          type: "case-access-actions",
          additionalInfo: this.args.case,
        },
      ],
    };
  }

  get invitationTableConfig() {
    return {
      columns: [
        {
          heading: { label: "documents.accesses.table.email" },
          modelKey: "email",
        },
        {
          heading: { label: "documents.accesses.table.action" },
          type: "case-access-actions",
          additionalInfo: this.args.case,
        },
      ],
    };
  }

  get _accesses() {
    return this.args.case.accesses;
  }

  get accesses() {
    return this._accesses.filterBy("email", null);
  }

  get invitations() {
    return this._accesses.filterBy("email");
  }
}
